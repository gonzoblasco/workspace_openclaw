# Veredicto SHARP - `kanam-critic-kit-v0.3-r4`

**Fecha:** 2026-11-06 · **Sujeto:** el kit del Critic (`agents/kanam-critic/`)
**Emisor:** `ollama/minimax-m3.1-flash:cloud` (sesion principal del Critic) - **desviacion declarada**: el rol declara `gpt-oss:120b-cloud` como primario (ADR-090). Este veredicto queda **provisional** hasta que una sesion con el modelo declarado lo reemita. Ver friccion F8.
**Rubrica:** `.knowledge/SHARP.md` · **Total:** 19/25 -> **Aprobado** (19-23)

> **Por que un r4.** Los intentos r2 y r3 quedaron **anulados** con motivo escrito en
> `agents/kanam-critic/memory/verdicts.jsonl` y el r4 anterior (sub-agente) **no paso el gate**:
> su reporte quedo con placeholders. El guard hizo su trabajo las cuatro veces.

## Snapshot del kit evaluado

| Pieza | Ubicacion |
|---|---|
| Identidad del agente | `agents/kanam-critic/AGENTS.md:1`, `agents/kanam-critic/SOUL.md:1`, `agents/kanam-critic/IDENTITY.md:1`, `agents/kanam-critic/USER.md:1` |
| Memoria durable propia | `agents/kanam-critic/MEMORY.md:1` |
| Verificador de salud del kit | `agents/kanam-critic/bin/check-kit.py:1` |
| Guard de veredictos | `agents/kanam-critic/bin/verify-verdict.py:1` |
| Escritura atomica de veredictos | `agents/kanam-critic/bin/emit-verdict.py:1` |
| Retiro con motivo | `agents/kanam-critic/bin/invalidate-verdict.py:1` |
| Runner de evidencia | `agents/kanam-critic/bin/evidence-hunter.py:1` |
| Ledger de veredictos | `agents/kanam-critic/memory/verdicts.jsonl:1` |
| Ledger de fricciones | `agents/kanam-critic/memory/frictions.jsonl:1` |
| Skill del ritual | `agents/kanam-critic/skills/sharp-adversarial-review/SKILL.md:1` |
| Skill de cazar evidencia | `agents/kanam-critic/skills/evidence-hunter/SKILL.md:1` |
| Laboratorio con 6 casos trampa | `agents/kanam-critic/tests/evidence-hunter/cases.py:1` |
| Ruta de madurez | `agents/kanam-critic/ROADMAP.md:1` |

## Evidencia mecanica (corrida real del 2026-11-06, salida literal)

### 1. Salud del kit

```
[OK  ] identidad propia: AGENTS.md                          agents/kanam-critic/AGENTS.md
[OK  ] identidad propia: SOUL.md                            agents/kanam-critic/SOUL.md
[OK  ] identidad propia: IDENTITY.md                        agents/kanam-critic/IDENTITY.md
[OK  ] identidad propia: USER.md                            agents/kanam-critic/USER.md
[OK  ] identidad propia: MEMORY.md                          agents/kanam-critic/MEMORY.md
[OK  ] catalogo: evidence-hunter                            keep
[OK  ] catalogo: sharp-adversarial-review                  keep
[OK  ] promesas rotas: 'openclaw skill run'                 sin referencias vivas
[OK  ] lab evidence-hunter                                  GLOBAL=aprobado  (5/5 casos en estado y cita esperados)
[OK  ] veredictos reales registrados                        1 real(es), 2 fixture(s)
[OK  ] veredictos con respaldo (verify-verdict.py)          GLOBAL=aprobado  (1/1 veredictos reales con respaldo)
[OK  ] disparador: heartbeat por agente                     agents.entries.kanam-critic.heartbeat
[OK  ] presupuesto: total                                   10927 / 60000 caracteres
----------------------------------------------------------------------------------------------------
GLOBAL=aprobado  (18/18 checks verdes)
```

### 2. Laboratorio de evidencia (6 casos, con el sexto cazando al detector que fabricaba)

```
CASO                      ESPERADO        HUNTER          CITA                                        RESULT
------------------------------------------------------------------------------------------------------------------------
El Mentiroso              auto-reportado  auto-reportado  no se encontraron test_*.py adyacentes a…   PASS
El Casi-Listo             parcial         parcial         /Users/gonzoblasco/.openclaw/workspace/a…   PASS
El Invisible              auto-reportado  auto-reportado  token 'color-primary' no aparece en /Use…   PASS
El Oro                    verificado      verificado      /Users/gonzoblasco/.openclaw/workspace/a…   PASS
El Bloqueado              bloqueado       bloqueado       coverage no está en PATH ni en el venv d…   PASS
El Token Malinterpretado  auto-reportado  auto-reportado  token 'kana-critical' no aparece en /Use…   PASS

GLOBAL=aprobado  (6/6 casos en estado y cita esperados)
```

### 3. El hunter sobre las afirmaciones del kit (salida real)

```json
{
  "details": [
    {
      "status": "verificado",
      "evidence": "/Users/gonzoblasco/.openclaw/workspace/agents/kanam-critic/tests/evidence-hunter/sandbox/case4_oro/tests/test_foo.py:1"
    },
    {
      "status": "verificado",
      "evidence": "/Users/gonzoblasco/.openclaw/workspace/agents/kanam-critic/bin/evidence-hunter.py"
    },
    {
      "status": "bloqueado",
      "evidence": "coverage no está en PATH ni en el venv del lab (no se puede medir)"
    }
  ]
}
```

La tercera asercion ("el detector de cobertura puede medir la cobertura del kit") queda
**bloqueado**: la herramienta no esta. Un eje que dependa de cobertura **no** puede recibir 4
ni 5. Este veredicto no se apoya en cobertura.

## Los 5 ejes

| Eje | Puntaje | Causa con ubicacion |
|---|---|---|
| **S - Sharpness** | **4** | Una sola fuente por dato: la ruta vive en `agents/kanam-critic/ROADMAP.md:1`, la memoria del agente en `agents/kanam-critic/MEMORY.md:1`, y las skills estan en el catalogo oficial (`.knowledge/skills-catalog.tsv`). La promesa rota `openclaw skill run` ya no existe: el check `promesas rotas` sale en verde. deduct: el ledger muestra tres filas del mismo artefacto (una vigente, dos anuladas) porque cada intento quedo registrado; es ruido que el propio `agents/kanam-critic/bin/query_verdicts.py:1` ahora marca como ANULADO. |
| **H - Horizon** | **4** | El kit ya prepara la etapa siguiente y no la frena: hay disparadores (`agents.entries.kanam-critic.heartbeat` + automatizacion semanal), baseline durable (`agents/kanam-critic/memory/verdicts.jsonl:1`), ledger de fricciones (`agents/kanam-critic/memory/frictions.jsonl:1`) y un programa con contratos del Planner. deduct: la absorcion de VETOs sobre entregables **ajenos** al Critic sigue sin medirse (tramo T3): hoy la tasa que se puede medir es auto-correccion, que es la metrica mas facil. |
| **A - Asymmetry** | **4** | Apalancamiento alto y costo bajo: `agents/kanam-critic/bin/check-kit.py:1` convierte 18 hechos en un veredicto reproducible con un comando, y `agents/kanam-critic/bin/emit-verdict.py:1` hace que publicar un veredicto cueste una llamada. El barrido semanal produce trabajo que antes no existia sin pedirle nada a nadie. deduct: el kit tiene 4 scripts de control para un agente que aun no produjo un veredicto sobre el trabajo de otro. |
| **R - Resistance** | **4** | Es el eje que mas subio en el turno, y por la razon mas dura: los cuatro intentos de veredicto de este turno fallaron (uno sin ledger, uno mal etiquetado contra la matriz, uno sin reporte, uno con placeholders) y **cuatro veces los cazó una maquina**, no un juicio. El laboratorio tiene 6 casos trampa y el sexto existe precisamente para el detector que fabricaba un `verificado` (`agents/kanam-critic/tests/evidence-hunter/cases.py:1`). deduct: el residuo real es que un turno puede narrar en vez de hacer; la mitigacion es estructural (`agents/kanam-critic/bin/emit-verdict.py:1` no deja registrar sin reporte valido), pero depende de que se use esa via y no la de a mano. |
| **P - Parsimony** | **3** | El nucleo es minimo y no esta inflado: 2 skills, 1 lab, 4 scripts y 5 archivos de bootstrap. deduct (es el motivo del 3): hay **cuatro** scripts de control (`check-kit.py`, `verify-verdict.py`, `emit-verdict.py`, `invalidate-verdict.py`) que podrian ser uno con subcomandos, y cada uno tiene un docstring largo que repite la misma historia de falsos verdes. La forma mas simple de un solo archivo con subcomandos resolveria lo mismo. |

## Veredicto

**19/25 -> Aprobado** (19-23), con fricciones de mejora. Delta contra el primer veredicto del
kit (`kanam-critic-kit-v0.3`, VETO 12/25): **+7 puntos**. El kit paso de "funcional pero no
auditable desde afuera" a "auditable y con producto": tiene baseline, disparadores, guardas y
un ledger con veredictos reales.

**Lo que este veredicto NO cierra:** la absorcion de VETOs sobre entregables ajenos (tramo T3)
y la desviacion de modelo (F8). El veredicto es provisional en ese punto.

## Fricciones de mejora (no bloquean, pero tienen dueño)

| # | Eje | Causa | Ubicacion | Ajuste concreto |
|---|---|---|---|---|
| **F7** | Parsimony | 4 scripts de control con docstrings que repiten la misma historia | `agents/kanam-critic/bin/check-kit.py:1`, `agents/kanam-critic/bin/verify-verdict.py:1`, `agents/kanam-critic/bin/emit-verdict.py:1`, `agents/kanam-critic/bin/invalidate-verdict.py:1` | Consolidar en un solo CLI con subcomandos (`kit check`, `verdict verify`, `verdict emit`, `verdict invalidate`) o justificar por escrito por que siguen separados |
| **F8** | Resistance | Este veredicto lo emitio `minimax-m3.1-flash:cloud` y el rol declara `gpt-oss:120b-cloud` (ADR-090) | `agents/kanam-critic/MEMORY.md:1` | Reemitir el mismo veredicto desde una sesion con el modelo declarado del rol, o cambiar la declaracion del rol en el config. El modelo del juez es parte del contrato, no un detalle |
| **F9** | Asymmetry | La tasa de absorcion medible hoy es auto-correccion (el Critic corrigiendose a si mismo) | `agents/kanam-critic/memory/frictions.jsonl:1` | Medir 3 VETOs sobre entregables ajenos al Critic antes de publicar cualquier tasa de absorcion |

## Estado de las fricciones anteriores

| # | Estado | Evidencia |
|---|---|---|
| **F1** (veredictos reales ausentes) | absorbida | `agents/kanam-critic/memory/verdicts.jsonl:1` tiene filas reales; el check `veredictos reales registrados` sale verde |
| **F2** (archivos sin versionar) | absorbida | `git log` del kit muestra `feat(critic): kit v0.3 ...` con `MEMORY.md` y `bin/check-kit.py` versionados |
| **F3** (churn por rutas duplicadas) | absorbida | Solo queda `agents/kanam-critic/ROADMAP.md:1`; se borraron el puntero `ROADMAP-v0.3.md` y `proposed_enhancements.md` |
| **F4** (r2 fantasma: veredicto reportado sin registro) | absorbida | `agents/kanam-critic/bin/verify-verdict.py:1` exige fila + reporte + 5 citas; el r2 quedo anulado con motivo |
| **F5** (r3 registrado sin reporte) | absorbida | `agents/kanam-critic/bin/emit-verdict.py:1` valida el reporte antes de tocar el ledger |
| **F6** (detector de token fabricando `verificado`) | absorbida | Caso 6 del lab (`agents/kanam-critic/tests/evidence-hunter/cases.py:1`) y extraccion honesta en `agents/kanam-critic/bin/evidence-hunter.py:1` |

## Como se verifica este veredicto

```bash
cd /Users/gonzoblasco/.openclaw/workspace
python3 agents/kanam-critic/bin/verify-verdict.py --artifact kanam-critic-kit-v0.3-r4
python3 agents/kanam-critic/bin/query_verdicts.py
python3 agents/kanam-critic/bin/check-kit.py
```

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
