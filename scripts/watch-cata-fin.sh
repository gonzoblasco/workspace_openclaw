#!/usr/bin/env bash
# Avisa cuando la tanda de la cata TERMINA, y con que resultado.
#
# Por que existe: el driver corre en background y su salida va a un log, asi
# que sin esto el owner se queda sin enterarse hasta que alguien mire. El
# watcher mira el ESTADO (results.json / artefactos), no el log: el log se
# bufferiza y no sirve para seguir el avance.
#
# Dispara UNA vez por tanda: el sello se guarda en /tmp/cata-harnesses/CATA-DONE
# y el trigger lo borra al arrancar una tanda nueva.
set -uo pipefail

OUT="/tmp/cata-harnesses"
SEALLO="$OUT/CATA-DONE"

# 1. La tanda sigue corriendo?
if pgrep -f "run-cloud-3.sh|run-sweep-9.sh|run-all.sh|run-local-1task.sh|chain-local.sh" > /dev/null 2>&1; then
  echo '{"fire": false, "reason": "la tanda sigue en curso"}'
  exit 0
fi
if pgrep -f "runner\.py" > /dev/null 2>&1; then
  echo '{"fire": false, "reason": "hay una corrida en curso"}'
  exit 0
fi

# 2. Ya se aviso de esta tanda?
if [ -f "$SEALLO" ]; then
  echo '{"fire": false, "reason": "ya se aviso de esta tanda"}'
  exit 0
fi

# 3. Hubo cata en esta maquina?
if [ ! -d "$OUT" ]; then
  echo '{"fire": false, "reason": "no hay cata en esta maquina"}'
  exit 0
fi

# 4. Tanda terminada: se arma el resumen y se sella.
python3 - <<'PY'
import json, pathlib, subprocess, sys

ROOT = pathlib.Path("/tmp/cata-harnesses")
MODELOS = [
    ("deepseek-v4.1-flash:cloud", "deepseek-v4.1-flash__cloud"),
    ("gpt-oss:120b-cloud", "gpt-oss_120b-cloud"),
    ("nemotron-3-super:cloud", "nemotron-3-super_cloud"),
    ("minimax-m3.1-flash:cloud", "minimax-m3.1-flash_cloud"),
    ("gemma4:cloud", "gemma4_cloud"),
    ("glm-5.3-flash:cloud", "glm-5.3-flash_cloud"),
    ("nova-2b:latest", "hf.co_ModernoTech_nova-2b_latest"),
    ("ornith-1.5:9b", "ornith-1.5_9b"),
    ("gemma4:12b-mlx", "gemma4_12b-mlx"),
    ("qwen3.5:9b-mlx", "qwen3.5_9b-mlx"),
]
TAREAS = ("T1", "T2", "T3")
HAR = ("claude", "opencode", "openhands")

lineas = []
hechas = 0
for model, slug in MODELOS:
    d = ROOT / slug
    art = d / "artefactos"
    n = 0
    if art.exists():
        for t in TAREAS:
            for h in HAR:
                p = art / t / f"{h}.md"
                if p.exists() and p.stat().st_size > 0:
                    n += 1
    hechas += n
    sp = tt = 0
    sp_path = d / "suite.json"
    if sp_path.exists():
        try:
            for s in json.loads(sp_path.read_text()):
                sp += s.get("asserts_passed") or 0
                tt += s.get("asserts_total") or 0
        except json.JSONDecodeError:
            pass
    a = f"{sp}/{tt}" if tt else "-"
    lineas.append(f"  {model:<34} {n}/9  asserts {a}")

msg = (
    "La tanda de la cata de harnesses TERMINO.\n\n"
    + "\n".join(lineas)
    + f"\n\n  TOTAL: {hechas}/90 celdas con entregable"
    + "\n\n  Detalle y analisis: python3 "
    + str(ROOT / "status.py")
    + " y el informe en docs/evaluacion/cata-harnesses-3-modelos-2026-10-28.md"
)
# Sellar: esta tanda ya se aviso.
(ROOT / "CATA-DONE").write_text(msg)
print(json.dumps({"fire": True, "message": msg}))
PY
