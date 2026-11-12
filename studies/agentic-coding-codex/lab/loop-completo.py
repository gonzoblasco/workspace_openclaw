#!/usr/bin/env python3
"""loop-completo.py - las TRES tools que necesita un agente:
leer, ejecutar, escribir. Si falta escribir, el loop gira en vacío."""
import json, subprocess, sys, urllib.request

MODEL = "deepseek-v4.1-flash:cloud"
TESTS = "/tmp/m1-practica/test-malo.mjs"
CODIGO = "/tmp/m1-practica/caja.mjs"
MAX = 4

def leer():  return open(CODIGO).read()
def escribir(t): open(CODIGO, "w").write(t)
def correr():
    r = subprocess.run(["node", TESTS], capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr).strip()

def senal_real(out):
    """La línea del AssertionError, no el cierre del stack."""
    for l in out.splitlines():
        if "AssertionError" in l or "actual" in l or "expected" in l:
            return l.strip()
    return out.splitlines()[-1] if out else ""

def pensar(rc, out, cod):
    prompt = f"""Sos un coding agent. Hay un test que falla.

CÓDIGO ACTUAL (caja.mjs):
```js
{cod}
```

TEST QUE FALLA (test-malo.mjs) — la señal:
{senal_real(out)}

El test exige {1512.5} pero el código da 1250. Hay que aplicar IVA 21%.

Devolvé SOLO el código completo y corregido de caja.mjs, sin explicación y sin backticks."""
    req = urllib.request.Request("http://127.0.0.1:11434/api/generate",
        data=json.dumps({"model": MODEL, "prompt": prompt, "stream": False}).encode(),
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.load(r)["response"].strip()

for i in range(1, MAX+1):
    print(f"── vuelta {i} ─────────────")
    rc, out = correr()
    print(f"   ejecutar -> exit {rc}")
    if rc == 0:
        print("   ✅ VERDE: el loop cerró solo"); sys.exit(0)
    print(f"   señal    -> {senal_real(out)[:80]}")
    print(f"   escribir -> pidiendo el fix al modelo...")
    cod = leer()
    nuevo = pensar(rc, out, cod)
    nuevo = nuevo.replace("```js","").replace("```","").strip()
    if nuevo and "total" in nuevo:
        escribir(nuevo + "\n")
        print(f"   escribir -> archivo actualizado ({len(nuevo)} chars)")
    else:
        print("   ⚠️ respuesta inservible, no escribo"); 
print("── no cerró en", MAX, "vueltas ──"); sys.exit(1)
