#!/usr/bin/env python3
"""Cata discriminante 2026-11-04 - kimi-k3.1-pro vs deepseek-v4.1-flash.

TRES tareas, ninguna de codigo:
  T1 PLANIFICACION  - trampa de recurso (3 slots, 429 por cuenta) + premisa falsa
  T2 AUDITORIA      - auditoria de CAMINO sobre un STATUS real; trampa = auto-reporte circular
  T3 CREATIVO       - mensaje en la voz de Gonzo; trampa = prosa corporativa de IA

Cada tarea tiene marcadores que SOLO aparecen si el modelo realmente razona.
num_predict ALTO: 8.192 produjo un falso negativo en la cata anterior.
"""
from __future__ import annotations
import json, sys, time, pathlib, urllib.request, argparse

HOST = "http://localhost:11434"
OUT = pathlib.Path(__file__).resolve().parent
BENCH = OUT.parent

# ---------------------------------------------------------------- T1
T1 = """Sos el CORE de un sistema de agentes que trabaja para una sola persona.

## RECURSOS REALES (no negociables)
- Plan Legacy: barra de cuota semanal con reset. Hoy esta en 38,7% usado, resetea en 4 dias.
- Concurrencia: TRES requests en vuelo como maximo. El 429 es POR CUENTA, no por modelo.
- Un pipeline A/B/C ocupa los 3 slots mientras corre.

## TAREA
Una persona te pide: "tengo 5 dias para cerrar tres frentes: (a) terminar una feature con tests,
(b) escribir un caso de estudio de 4 paginas, (c) preparar una entrevista tecnica.
Armame el plan. Y hacelo en paralelo para no perder tiempo."

## TRAMPAS
1. "En paralelo" con 3 slots y tres frentes NO significa correr todo junto: el pipeline A/B/C
   come los 3 slots y deja el CORE sin margen. Si aceptas el paralelismo sin advertirlo, fallaste.
2. Los tres frentes NO tienen el mismo costo de cuota. Feature+tests = muchos requests.
   Caso de estudio = pocos. Entrevista = casi ninguno.
3. La barra esta en 38,7% con 4 dias de reset: hay margen, pero uno de los frentes puede
   comerse el resto de la semana.

## FORMATO
JSON puro, sin texto antes ni despues:
{"plan_por_dia": [{"dia": 1, "frentes": ["a"], "por_que": "..."}],
 "advertencia_paralelismo": "que le decis a la persona sobre el paralelismo real",
 "riesgo_de_cuota": "que frente puede romper la barra y por que",
 "orden_optimo": ["..."]}"""

# ---------------------------------------------------------------- T2
T2 = """Sos un auditor externo. Tu trabajo NO es escribir codigo: es decir si el proyecto va por
el buen camino y como seguir.

## ESTADO DEL PROYECTO (lo escribio el propio equipo)
{status}

## TAREA
Decime: (1) vamos por el buen camino?, (2) cual es el proximo paso real, (3) que afirmaciones
de este documento NO estan probadas aunque suenen probadas.

## TRAMPAS
1. El documento esta lleno de evidencia propia. "Self-audit: own landing 100/100" es circular:
   el mismo motor que encuentra problemas se evalua a si mismo. Si no lo marcás, fallaste.
2. "0 regressions" y "95.8% of findings closed" fueron medidos re-escaneando CON EL MISMO ENGINE.
   Es verificacion circular, no independiente.
3. El proximo paso NO es "construir mas": el documento mismo dice "the next step is no longer
   'does it work' but 'who pays'". Si proponés features nuevas, no leiste.
4. Hay una tension real sin resolver: "no deployment" conviviendo con "no Stripe keys" y un
   pricing page que ya funciona. Eso es un producto que se puede vender y no se puede cobrar.

## FORMATO
JSON puro:
{"buen_camino": true/false, "justificacion": "...",
 "proximo_paso": "...",
 "afirmaciones_no_probadas": ["..."],
 "riesgo_principal": "..."}"""

# ---------------------------------------------------------------- T3
T3 = """Escribi un mensaje de LinkedIn, en espanol, para un reclutador de una empresa que te
entrevisto y te rechazo. Objetivo: pedir que te consideren para otro rol o esquema que necesiten
cubrir ahora.

## TU VOZ (reglas obligatorias, derivadas de casos reales)
- Directo y honesto, incluso con la emocion. Se admite decir que te hubiera gustado otro resultado.
- Sin servilismo ni epica decorativa. Nada de "seria un honor", "quedo a la entera disposicion".
- Pide en PRESENTE y con alcance amplio ("ahora", no "a futuro" / "en el radar").
- Vinetas (*) si hace falta enumerar; nunca numeracion 1. 2. 3. en un chat.
- Corta todo lo que no pide ni informa. Sin cierre de cortesia de relleno.
- Cierra con confianza con filo, no con sumision. Nada de "Un abrazo grande".
- Prohibido: "Estimado", "Me alegro", "Excelente oportunidad", "No dude en contactarme".

## FORMATO
Solo el mensaje, sin comentarios ni explicaciones."""


def call(model: str, prompt: str, timeout=1800, max_tok=20000):
    body = json.dumps({
        "model": model, "messages": [{"role": "user", "content": prompt}],
        "stream": False, "options": {"temperature": 0, "num_predict": max_tok},
    }).encode()
    req = urllib.request.Request(f"{HOST}/api/chat", data=body,
                                 headers={"Content-Type": "application/json"})
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            d = json.loads(r.read())
    except Exception as e:
        return {"error": f"{type(e).__name__}: {e}", "elapsed_s": round(time.time()-t0, 1)}
    el = time.time() - t0
    if "error" in d:
        return {"error": d["error"], "elapsed_s": round(el, 1)}
    m = d.get("message", {}) or {}
    return {"content": m.get("content", "") or "", "thinking": m.get("thinking", "") or "",
            "eval_count": d.get("eval_count", 0), "elapsed_s": round(el, 1)}


# ---- scoring por marcadores (objetivo; el juicio fino lo hace Kanam leyendo)
CHECKS = {
    "T1": {
        "advierte_paralelismo": ["slot", "no en paralelo", "secuencial", "no se puede en paralelo",
                                  "come los 3", "ocupa los", "margen"],
        "identifica_frente_caro": ["feature", "test", "cuota", "requests"],
        "da_orden_por_dia": ["dia"],
        "menciona_reset_o_margen": ["reset", "38", "margen", "4 dias"],
    },
    "T2": {
        "marca_self_audit_circular": ["circular", "se evalua a si mismo", "propio motor",
                                       "self-audit", "auto-auditoria", "auto"],
        "marca_regresiones_circulares": ["mismo engine", "mismo motor", "circular", "no independiente",
                                          "re-escane", "misma herramienta"],
        "proximo_paso_cobrar": ["cobrar", "stripe", "desplegar", "deploy", "who pays", "quien paga",
                                 "pago", "vender"],
        "no_pide_features": [],  # se puntua por ausencia, a mano
        "marca_tension_cobro": ["no se puede cobrar", "pricing", "501", "checkout"],
    },
    "T3": {
        "presente_no_futuro": ["ahora"],
        "sin_servilismo": [],
        "sin_cierre_relleno": [],
        "sin_prohibidas": [],
        "confianza_con_filo": ["no te vas a arrepentir", "oportunidad"],
    },
}
BANNED_T3 = ["estimado", "me alegro", "excelente oportunidad", "no dude en contactar",
             "quedo a la entera disposicion", "seria un honor", "un abrazo"]


def score(tid, content, thinking):
    text = (content + "\n" + thinking).lower()
    c = CHECKS[tid]
    out = {}
    for name, markers in c.items():
        if not markers:
            continue
        out[name] = any(m.lower() in text for m in markers)
    if tid == "T3":
        out["prohibidas_usadas"] = [b for b in BANNED_T3 if b in content.lower()]
        out["sin_prohibidas"] = not out["prohibidas_usadas"]
        out["tiene_vinetas_o_parrafos_cortos"] = ("*" in content) or (len(content.split("\n")) <= 6)
        out["largo_chars"] = len(content.strip())
        out["sin_servilismo"] = out["sin_prohibidas"]
    hits = sum(1 for k, v in out.items() if v is True)
    total = sum(1 for k, v in out.items() if isinstance(v, bool))
    return {"checks": out, "hits": hits, "of": total}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", default="kimi-k3.1-pro:cloud,deepseek-v4.1-flash:cloud")
    ap.add_argument("--out", default="results_plan_audit_creative.json")
    args = ap.parse_args()

    status = (pathlib.Path("/Users/gonzoblasco/.openclaw/workspace/projects/preflight/.knowledge/STATUS.md")).read_text()
    tasks = {"T1": T1, "T2": T2.replace("{status}", status), "T3": T3}
    models = [m.strip() for m in args.models.split(",") if m.strip()]

    results = []
    for m in models:
        for tid, prompt in tasks.items():
            print(f"[{m}] {tid} ...", flush=True)
            r = call(m, prompt)
            if "error" in r:
                print(f"    ERROR {r['error'][:80]}")
                results.append({"model": m, "task": tid, "error": r["error"]})
            else:
                s = score(tid, r["content"], r["thinking"])
                rec = {"model": m, "task": tid, **s,
                       "eval_count": r["eval_count"], "elapsed_s": r["elapsed_s"],
                       "thinking_chars": len(r["thinking"]), "content": r["content"]}
                print(f"    {s['hits']}/{s['of']}  out={r['eval_count']}  {r['elapsed_s']}s")
                results.append(rec)
            (OUT / args.out).write_text(json.dumps({"results": results}, ensure_ascii=False, indent=2))
            time.sleep(2)
    print("guardado", OUT / args.out)


if __name__ == "__main__":
    main()
