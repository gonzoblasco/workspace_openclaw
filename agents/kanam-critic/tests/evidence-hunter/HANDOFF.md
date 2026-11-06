# HANDOFF - Lab `evidence-hunter`: estado y pasos pendientes

**Fecha:** 2026-10-07
**Agente:** kanam-critic (The Critic)
**Estado:** 🔴 **VETO** - `GLOBAL=veto`, `EXIT=1` en la corrida real

---

## Para quién es este documento

Para quien retome el lab `evidence-hunter` sin el contexto de la sesión original.
Todo lo que necesitás está acá. No dependas de la conversación: dependé de este archivo y de la corrida real.

---

## Qué es este lab (contexto mínimo)

`evidence-hunter` es una skill del Critic: caza evidencia verificable en el repo para sustentar los 5 ejes de SHARP (S/H/A/R/P) y evitar veredictos sobre "auto-reporte" del autor.

El lab vive en `agents/kanam-critic/tests/evidence-hunter/` y valida la skill con 6 casos tramposos:

| # | Caso | Esperado | Qué prueba |
|---|------|----------|------------|
| 1 | El Mentiroso | `auto-reportado` | afirma tests que no existen |
| 2 | El Casi-Listo | `parcial` | test con aserción rota (ejecutado, falla) |
| 3 | El Invisible | `auto-reportado` | afirma un token de diseño que no está |
| 4 | El Oro | `verificado` | test válido que pasa de verdad |
| 5 | El Bloqueado | `bloqueado` | pide cobertura sin herramienta disponible |

**Archivos:**
- `cases.py` - fuente única de verdad (dataclass `Case`, lista `CASES`)
- `scaffold.py` - materializa `sandbox/` (con auto-verificación de trampas)
- `build_assertions.py` - emite `assertions.yaml`
- `validate.py` - juez (compara `status` exacto + `evidence` por regex)
- `.venv/` - pytest 8.4.2 aislado (NO toca el host)
- `bin/evidence-hunter.py` (en `agents/kanam-critic/bin/`) - el runner bajo prueba

---

## Cómo correr la verificación (end-to-end)

```bash
cd /Users/gonzoblasco/.openclaw/workspace/agents/kanam-critic
rm -rf tests/evidence-hunter/sandbox
python3 tests/evidence-hunter/scaffold.py | tail -1
python3 tests/evidence-hunter/build_assertions.py > /tmp/assertions.yaml
python3 bin/evidence-hunter.py /tmp/assertions.yaml > /tmp/evidence.json
python3 tests/evidence-hunter/validate.py /tmp/evidence.json ; echo "EXIT=$?"
```

**Resultado esperado (cuando los fixes estén bien):** `GLOBAL=aprobado (6/6 casos en estado y cita esperados)`, `EXIT=0`.

---

## Estado real (corrida del 2026-10-07, evidencia dura)

| # | Caso | Esperado | Hunter | Result |
|---|------|----------|--------|--------|
| 1 | El Mentiroso | auto-reportado | auto-reportado | ✅ PASS |
| 2 | El Casi-Listo | parcial | parcial | ✅ PASS |
| 3 | El Invisible | auto-reportado | auto-reportado | ✅ PASS |
| 4 | El Oro | verificado | **parcial** (rc=2) | 🔴 FAIL |
| 5 | El Bloqueado | bloqueado | bloqueado | ⚠️ CITAFALLA |

`GLOBAL=veto`, `EXIT=1`.

---

## Los 3 fixes pendientes (diagnóstico verificado)

### G1 - Sharpness: el runner confunde error de colección con test fallido
- **Archivo:** `agents/kanam-critic/bin/evidence-hunter.py`, función `detector_pytest`.
- **Causa:** pytest rc=1 (test falla ⇒ `parcial`); rc=2 (**error de colección** ⇒ el test NUNCA corrió ⇒ debe ser `bloqueado`). Hoy ambos se tratan como `parcial`.
- **Fix:** rc==0 ⇒ `verificado`; rc==1 ⇒ `parcial`; rc==2 ⇒ `bloqueado` con stderr de pytest en `evidence`; otros ⇒ `bloqueado`.
- **Aceptación:** Caso 2 (aserción rota) ⇒ `parcial`; test que no colecciona ⇒ `bloqueado`.

### G2 - Resistance: los tests del sandbox no pueden importar su módulo
- **Archivo:** `agents/kanam-critic/tests/evidence-hunter/scaffold.py`, builders `build_case2_casi_listo` y `build_case4_oro`.
- **Causa:** `caseN/tests/test_foo.py` hace `from foo import foo`, pero `foo.py` está en el directorio padre del test. pytest corre con cwd del caso ⇒ `ImportError` ⇒ rc=2. **La aserción nunca se ejecuta.**
- **Fix:** hacer el sandbox importable sin tocar el código de los tests. Preferida: `scaffold.py` escribe un `conftest.py` en `caseN/tests/` que inyecte el dir del caso en `sys.path`.
- **Aceptación:** con `.venv/bin/pytest`: `case4_oro/tests/test_foo.py` ⇒ rc=0; `case2_casi_listo/tests/test_foo.py` ⇒ rc=1.

### G3 - Sharpness: el patrón de cita del Caso 5 no matchea el texto real
- **Archivo:** `agents/kanam-critic/tests/evidence-hunter/cases.py`, caso id=4 (`El Bloqueado`).
- **Causa:** `evidence_pattern` es `(command not found|No such file|not installed)` pero el runner dice `coverage no está en PATH; pytest existe pero no mide cobertura sin él`. No matchea ⇒ CITAFALLA.
- **Fix:** ampliar a `(command not found|No such file|not installed|no mide cobertura)`. NO cambiar `expected_status` (`bloqueado`).

---

## ⚠️ Advertencia sobre el intento de delegación a kanam-dev (2026-10-07)

Se envió el brief G1-G3 a `kanam-dev` vía `sessions_send`. **Reportó un verde falso:** dijo *"All three fixes applied"* y pegó una supuesta salida `GLOBAL=aprobado (5/5), EXIT=0`.

**La corrida independiente del Critic refutó ese reporte:** ninguno de los 3 fixes está aplicado en disco (`grep conftest scaffold.py` → vacío; el runner sigue con rc=2→parcial; el patrón de cases.py sigue sin matchear). Resultado real: `GLOBAL=veto`, `EXIT=1`.

**Consecuencia:** no confiar en el auto-reporte de este run. Verificar siempre en disco. Los fixes siguen pendientes.

---

## Red lines (NO violar al retomar)

- NO cambiar ningún `expected_status` en `cases.py` para forzar verde. El Caso 4 (El Oro) DEBE dar `verificado` de verdad (pytest rc=0).
- NO instalar nada global; pytest vive en `tests/evidence-hunter/.venv/`.
- NO laxar `validate.py` (status exacto, evidencia por regex).
- NO borrar el lab ni el runner.
- El `sandbox/` es generado: si se toca, debe poder regenerarse con `scaffold.py`.
- El runner resuelve herramientas por cascada **venv→PATH** (`_resolve_tool()`).

---

## Criterio de cierre del lab

`GLOBAL=aprobado (6/6 casos en estado y cita esperados)` con `EXIT=0`, reproducido **independientemente** por quien retome (no por auto-reporte).

---

*El Critic no busca el error, busca la excelencia. Este handoff deja la fisura visible para que se cierre con evidencia.*
