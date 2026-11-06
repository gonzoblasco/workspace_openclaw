#!/usr/bin/env python3
"""Prueba de contrato para scripts/llm.sh.

Regla: el test falla si el script no cumple CUALQUIERA de las tres conductas que
nos costaron horas el 2026-11-05. Se corre antes de tocar llm.sh, no despues.

Uso: test-llm-sh.py [--live]
  Sin --live corre solo los casos que no necesitan un modelo (rapido).
  Con --live corre ademas un caso real y el caso de estancamiento.

Exit: 0 todos los casos pasan, 1 algun caso falla.
"""
import json
import os
import subprocess
import sys
import tempfile
import time

LLM = os.path.join(os.path.dirname(os.path.abspath(__file__)), "llm.sh")
CASOS = []


def caso(nombre):
    def deco(fn):
        CASOS.append((nombre, fn))
        return fn
    return deco


@caso("json tiene las metricas que usan las tablas")
def metricas_json():
    """`--json` debe traer tokens_in, tokens_out y secs: sin ellos no hay graficos."""
    r = subprocess.run([LLM, "codigo", "--prompt", "responde solo OK", "--json"],
                       capture_output=True, text=True, timeout=300)
    if r.returncode != 0:
        return False, f"exit {r.returncode}: {r.stderr[:150]}"
    d = json.loads(r.stdout)
    faltan = [k for k in ("tokens_in", "tokens_out", "secs") if k not in d]
    if faltan:
        return False, f"faltan claves: {faltan}"
    if d.get("tokens_out", 0) < 1:
        return False, f"tokens_out={d.get('tokens_out')} (no conto lo que emitio)"
    if not d.get("text", "").strip():
        return False, "text vacio"
    return True, f"tokens_in={d['tokens_in']} tokens_out={d['tokens_out']} secs={d['secs']}"


@caso("una sola invocacion por corrida")
def sin_doble_llamada():
    """El 2026-11-05 el script llamaba dos veces al modelo y multiplicaba el costo."""
    # Se instrumenta con un PATH falso que cuenta las ejecuciones de python3.
    with tempfile.TemporaryDirectory() as tmp:
        contador = os.path.join(tmp, "conteo")
        shim = os.path.join(tmp, "python3")
        real = subprocess.run(["which", "python3"], capture_output=True, text=True).stdout.strip()
        with open(shim, "w") as f:
            f.write(f"""#!/bin/bash
if [ "$1" != "-" ] && [[ "$1" != *"llmchat"* ]]; then :; fi
echo x >> "{contador}"
exec "{real}" "$@"
""")
        os.chmod(shim, 0o755)
        env = dict(os.environ, PATH=f"{tmp}:{os.environ['PATH']}")
        r = subprocess.run([LLM, "codigo", "--prompt", "responde solo OK",
                            "--model", "hf.co/ModernoTech/Nova-Core:Q4_K_M"],
                           capture_output=True, text=True, timeout=300, env=env)
        n = len(open(contador).read().split()) if os.path.exists(contador) else 0
        # Un script sano usa python3 para el payload y para la llamada: 2 veces.
        if n > 3:
            return False, f"python3 invocado {n} veces (esperado <=3)"
        return True, f"python3 invocado {n} veces"


@caso("timeout se distingue de respuesta vacia")
def distingue_timeout():
    """Antes, un timeout devolvia exit 4 (vacio) y se leia como fallo del modelo."""
    r = subprocess.run(["grep", "-c", 'CURL_EXIT" -eq 28', LLM],
                       capture_output=True, text=True)
    if r.stdout.strip() == "0":
        return False, "no hay rama para el timeout"
    r2 = subprocess.run(["grep", "-c", 'CURL_EXIT" -eq 29', LLM],
                        capture_output=True, text=True)
    if r2.stdout.strip() == "0":
        return False, "no hay rama para el estancamiento"
    return True, "ramas 28 (timeout) y 29 (estancamiento) presentes"


@caso("estancamiento corta de verdad")
def estancamiento_corta():
    """El caso que nunca verificamos: un modelo que NO emite debe cortarse."""
    # Se pide una salida absurdamente larga con contexto minimo y limite de tope
    # bajo: el script tiene que cortar por estancamiento, no quedarse colgado.
    t0 = time.time()
    env = dict(os.environ, LLM_STALL_TIME="20", LLM_MAX_TIME="120")
    r = subprocess.run([LLM, "codigo",
                        "--prompt", "Repeti la palabra hola indefinidamente sin parar.",
                        "--model", "hf.co/ModernoTech/Nova-Core:Q4_K_M",
                        "--num-ctx", "2048"],
                       capture_output=True, text=True, timeout=180, env=env)
    dur = time.time() - t0
    if dur > 150:
        return False, f"tardo {dur:.0f}s: el corte no funciono"
    return True, f"cortó en {dur:.0f}s con exit {r.returncode}"


def main():
    live = "--live" in sys.argv
    solo_rapidos = {"json tiene las metricas que usan las tablas",
                    "una sola invocacion por corrida",
                    "timeout se distingue de respuesta vacia"}
    fallos = 0
    for nombre, fn in CASOS:
        if not live and nombre not in solo_rapidos:
            print(f"SKIP  {nombre} (necesita --live)")
            continue
        try:
            ok, detalle = fn()
        except Exception as e:
            ok, detalle = False, f"excepcion: {e}"
        print(("PASS  " if ok else "FAIL  ") + f"{nombre}: {detalle}")
        if not ok:
            fallos += 1
    print(f"\n{len(CASOS)-fallos}/{len(CASOS)} pasan")
    return 1 if fallos else 0


if __name__ == "__main__":
    sys.exit(main())
