#!/usr/bin/env python3
"""loop-con-modelo.py - el mismo loop, pero ahora un modelo real lee la señal
y decide la próxima acción. Esto es, literalmente, lo que hace un coding agent."""
import json, subprocess, sys, urllib.request

MODEL = "gpt-oss:120b-cloud"
CMD = ["node", "/tmp/m1-practica/test-malo.mjs"]
MAX = 3

def correr():
    r = subprocess.run(CMD, capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr).strip()

def pensar(vuelta, rc, salida):
    prompt = f"""Sos un agente de coding. Tenés un test que debe pasar.

Vuelta {vuelta}/{MAX}.
Último resultado -> exit {rc}
Salida:
{salida[-600:]}

El archivo es /tmp/m1-practica/test-malo.mjs

Respondé SOLO con una de estas dos opciones, sin explicar:
  ACCION: esperar   (si ya está verde)
  ACCION: arreglar  (si hay que corregir el test o el código)
"""
    req = urllib.request.Request(
        "http://127.0.0.1:11434/api/generate",
        data=json.dumps({"model": MODEL, "prompt": prompt, "stream": False}).encode(),
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)["response"].strip()

for i in range(1, MAX+1):
    print(f"── vuelta {i} ─────────────")
    rc, out = correr()
    print(f"   actuo: exit {rc}")
    print(f"   señal: {out.splitlines()[-1][:90] if out else '(vacío)'}")
    if rc == 0:
        print("   VERDE -> loop termina solo"); sys.exit(0)
    decision = pensar(i, rc, out)
    print(f"   modelo decide: {decision}")
