#!/usr/bin/env python3
"""
bench_compare.py - U4 de performance-benchmark: comparar dos corridas y decidir.

El problema que resuelve: la skill pide una linea base, un resultado tras el
cambio, el delta y un veredicto contra un umbral. Sin ejecutable, el veredicto
queda en prosa y aparece el "cambio 12 %" sin direccion, que no dice si mejoro ni
si alcanza.

Que hace:
  1. Lee dos archivos de corrida (JSON): baseline y candidate.
  2. Compara la metrica declarada, calcula el delta absoluto y porcentual.
  3. Decide contra el umbral y la direccion (menor es mejor / mayor es mejor).
  4. Escribe `bench/report.md` con antes, despues, delta y veredicto.

Formato de una corrida (JSON). Minimo: la metrica y su valor.

    {"metric": "p95", "value": 210, "unit": "ms", "runs": 5, "env": "m1 pro, node 22"}

Exit codes:
  0  el cambio cumple el objetivo
  1  el cambio no lo cumple (empeoro, o no alcanzo el umbral)
  2  no se pudo medir (archivo ilegible, metrica distinta, sin valor, sin umbral)

Un 2 nunca es verde: dos corridas que miden cosas distintas no se comparan.

Cero dependencias. Solo stdlib.

Uso:
    bench_compare.py --baseline base.json --candidate cand.json --threshold 200 --lower-is-better
    bench_compare.py ... --json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Lectura y validacion. Pura.
# ---------------------------------------------------------------------------


def load_run(path: Path) -> tuple[dict | None, str]:
    """Devuelve (run, error). error != "" significa exit 2."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        return None, f"no se pudo leer {path}: {exc}"
    except json.JSONDecodeError as exc:
        return None, f"JSON invalido en {path}: {exc}"

    if not isinstance(data, dict):
        return None, f"{path} no es un objeto JSON"
    if "value" not in data:
        return None, f"{path} no declara 'value'"
    value = data["value"]
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None, f"{path}: 'value' no es un numero ({value!r})"
    if not data.get("metric"):
        return None, f"{path} no declara 'metric'"
    return data, ""


def same_metric(baseline: dict, candidate: dict) -> tuple[bool, str]:
    """Dos corridas solo se comparan si miden la misma metrica."""
    if baseline["metric"] != candidate["metric"]:
        return False, (f"metricas distintas: baseline '{baseline['metric']}' vs "
                       f"candidate '{candidate['metric']}'")
    b_unit = baseline.get("unit")
    c_unit = candidate.get("unit")
    if b_unit and c_unit and b_unit != c_unit:
        return False, f"unidades distintas: {b_unit} vs {c_unit}"
    return True, ""


# ---------------------------------------------------------------------------
# Comparacion. Pura: recibe numeros, devuelve el veredicto.
# ---------------------------------------------------------------------------


def compare(before: float, after: float, threshold: float, lower_is_better: bool) -> dict:
    """Calcula delta y veredicto contra el umbral.

    Dos preguntas distintas, y las dos importan:
      - El resultado cumple el umbral? (210 ms con objetivo 200 ms: no)
      - El cambio movio la aguja en la direccion correcta?
    Un cambio puede mejorar y aun no alcanzar el objetivo. Decir solo "mejoro"
    oculta que sigue fuera de contrato.
    """
    delta = after - before
    pct = (delta / before * 100.0) if before else None

    improved = (delta < 0) if lower_is_better else (delta > 0)
    if delta == 0:
        direction = "sin-cambio"
    else:
        direction = "mejora" if improved else "empeora"

    meets = (after <= threshold) if lower_is_better else (after >= threshold)

    if not meets:
        verdict = "no-cumple"
    elif direction == "empeora":
        verdict = "cumple-con-regresion"
    else:
        verdict = "cumple"

    return {
        "before": before,
        "after": after,
        "delta": delta,
        "delta_pct": round(pct, 2) if pct is not None else None,
        "threshold": threshold,
        "lower_is_better": lower_is_better,
        "direction": direction,
        "meets_threshold": meets,
        "verdict": verdict,
    }


def verdict_exit(verdict: dict) -> int:
    """0 solo si cumple. Una regresion que aun cumple sale 1.

    Por que: si el umbral es 200 y la version pasa de 120 a 190, cumple pero
    perdio 58 %. Aprobarlo silenciosamente es como se acumula una regresion que
    dos releases despues rompe el contrato.
    """
    if verdict["verdict"] == "no-cumple":
        return 1
    if verdict["verdict"] == "cumple-con-regresion":
        return 1
    return 0


# ---------------------------------------------------------------------------
# CLI.
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="bench_compare.py",
        description="Compara dos corridas y decide contra el umbral declarado.",
    )
    ap.add_argument("--baseline", required=True, help="corrida antes del cambio")
    ap.add_argument("--candidate", required=True, help="corrida despues del cambio")
    ap.add_argument("--threshold", type=float, required=True, help="objetivo declarado")
    ap.add_argument("--lower-is-better", action="store_true",
                    help="latencia, memoria, tiempo: el numero mas bajo gana")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--out", default="bench", help="directorio del informe")
    args = ap.parse_args(argv)

    base_path = Path(args.baseline)
    cand_path = Path(args.candidate)

    baseline, err = load_run(base_path)
    if err:
        print(f"[INFRA] {err}", file=sys.stderr)
        return 2
    candidate, err = load_run(cand_path)
    if err:
        print(f"[INFRA] {err}", file=sys.stderr)
        return 2

    ok, why = same_metric(baseline, candidate)
    if not ok:
        print(f"[INFRA] {why}", file=sys.stderr)
        return 2

    verdict = compare(
        float(baseline["value"]),
        float(candidate["value"]),
        args.threshold,
        args.lower_is_better,
    )

    # La varianza se declara: una sola corrida puede ser ruido.
    runs = [baseline.get("runs"), candidate.get("runs")]
    low_confidence = any(isinstance(r, int) and r < 3 for r in runs if r is not None)

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    report = out_dir / "report.md"
    unit = candidate.get("unit") or baseline.get("unit") or ""
    metric = candidate["metric"]

    lines = [
        f"# Benchmark: {metric}",
        "",
        f"Antes: {verdict['before']} {unit} | Despues: {verdict['after']} {unit} "
        f"| Delta: {verdict['delta']:+g} {unit}"
        + (f" ({verdict['delta_pct']:+g} %)" if verdict["delta_pct"] is not None else ""),
        "",
        f"Objetivo: {'<=' if args.lower_is_better else '>='} {args.threshold} {unit}",
        f"Direccion esperada: {'menor es mejor' if args.lower_is_better else 'mayor es mejor'}",
        f"Veredicto: **{verdict['verdict']}**",
        "",
        f"Entorno baseline: {baseline.get('env', 'no declarado')}",
        f"Entorno candidate: {candidate.get('env', 'no declarado')}",
        f"Corridas: baseline={baseline.get('runs', 'no declarado')}, "
        f"candidate={candidate.get('runs', 'no declarado')}",
    ]
    if low_confidence:
        lines += ["", "**Advertencia:** menos de 3 corridas declaradas. El delta puede ser ruido."]
    if baseline.get("env") and candidate.get("env") and baseline["env"] != candidate["env"]:
        lines += ["", "**Advertencia:** los entornos declarados difieren; la comparacion no es estricta."]
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")

    if args.json:
        print(json.dumps({**verdict, "metric": metric, "unit": unit,
                          "low_confidence": low_confidence}, ensure_ascii=False, indent=2))
    else:
        delta_pct = f" ({verdict['delta_pct']:+g} %)" if verdict["delta_pct"] is not None else ""
        print(f"{metric}: {verdict['before']} -> {verdict['after']} {unit} "
              f"delta {verdict['delta']:+g}{delta_pct}")
        print(f"objetivo {'<=' if args.lower_is_better else '>='} {args.threshold} {unit}"
              f" -> {verdict['verdict']}")
        if low_confidence:
            print("[AVISO] menos de 3 corridas: el delta puede ser ruido")
        print(f"informe: {report}")

    return verdict_exit(verdict)


if __name__ == "__main__":
    sys.exit(main())
