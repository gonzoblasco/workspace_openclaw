# AUDIT-2026-11-09 - Kanam CORE (`main`), ventana `beam:cloud`

<!-- project: github.com/gonzoblasco/workspace_openclaw -->

Auditoría de los tres días en que el agente `main` corrió con `beam:cloud`
(2026-11-07 17:07 a 2026-11-09 23:00), con el mismo método que se usó para los
roles: **correr lo que cada artefacto afirma, no leer el mensaje del commit.**

Fecha: 2026-11-09.

## Veredicto

**No se introdujeron errores de fondo.** Los artefactos de gobierno están
consistentes, y cada artefacto que `beam` produjo hace exactamente lo que su
documentación afirma cuando se lo ejecuta (§6). Tres defectos reales, ninguno de
contenido: dos de forma en `AGENTS.md` (§3 y §4) y una lección que enseña un flag
inexistente (§7). Un cuarto hallazgo es deuda previa, no de la ventana (§5).

Los tres defectos están corregidos en el commit que acompaña a este informe.

## 1. Alcance: qué corrió en `main` durante la ventana

23 sesiones de `main` activas en el período. De ellas, **9 con `beam:cloud`**:

| Cuándo | Modelo | Tokens |
|---|---|---|
| 11-07 17:07 | beam:cloud | 33.570 |
| 11-07 19:36 | beam:cloud | 24.335 |
| 11-07 19:38 | beam:cloud | 464.406 |
| 11-07 20:11 | beam:cloud | 103.903 |
| 11-08 00:44 | beam:cloud | 168.691 |
| 11-08 00:55 | beam:cloud | 146.024 |
| 11-08 09:44 | beam:cloud | 76.886 |
| 11-08 09:45 | beam:cloud | 507.200 |
| 11-08 13:02 | beam:cloud | 186.543 |

**1.711.558 tokens** en 9 sesiones. El resto de la ventana (11-06 y desde el
11-09 03:00) corrió con `deepseek-v4.1-flash:cloud`.

Producción concreta de esas sesiones, en cuatro commits:

```
22eb901319  chore(router): close skill-router-improvement (8/8 passes auditor gate)
04dc33c08a  fix(gate): overlap scan own-only; promoted to blocking for internal skills
87f8a68381  docs(memory): classify skill-overlap pairs (13 internal)
0f6febebec  kanam-auditor: cerrar Flujo A/B/C parcial, memoria y arsenal
```

## 2. Gates corridos

| Gate | Resultado |
|---|---|
| `check-bootstrap-budget.py` | OK · 48.558/60.000 |
| `check-agent-skill-boundary.py` | OK · 9 skills de rol en su lugar, 0 duplicados |
| `check-adr-integrity.py` | OK · 68 ADRs indexados, sin refs rotas |
| `check-adr-supersede.py` | OK · grafo consistente |
| `check-pipeline-enforcement.py` | OK |
| `check-single-source.py` | OK · ningún dato repetido |
| `check-refs.py` | OK · 180 rutas citadas existen |
| `check-learnings-integrity.py` | OK · 272 learnings |
| `check-prompts.py` | OK |
| `check-content-dirs.py` | OK · 10 directorios |
| `check-cv-facts.py` | OK · **14 CVs** coinciden con `career-facts.md` |
| `check-roadmaps.py` | OK · 7/7 roles |
| `check-foreign-knowledge.py` | OK |
| `check-design-tokens.py` | OK |
| `check-a11y-trigger.py` | OK |
| `test-skill-router.py` | **10/10** top-3 |
| `check-skill-overlap.py --staged --own-only --blocking` | exit 0 · 0 pares ≥ 0.87 |
| `check-handoff-merge.py` | exit 1 · **deuda previa**, ver §5 |

## 3. Defecto 1: typo en la regla de frontera de roles (corregido)

`AGENTS.md` línea 76, sección "Frontera de roles":

```
Antes de escribir: *¿gobnar o implementar?*
```

Lo introdujo `64edac4def` (2026-11-08 22:41, sesión con `beam`). Sobrevivió hasta
hoy. **Por qué importa:** `AGENTS.md` es el archivo que reciben *todos* los
subagentes; un typo ahí no rompe nada, pero es la primera cosa que lee un modelo
del rol que tiene que decidir si escribe código o no.

Corregido a "¿gobernar o implementar?".

## 4. Defecto 2: el presupuesto de bootstrap quedó a 5 caracteres del límite (corregido después)

La misma edición agregó una sección entera (`Conocimiento: el CORE llama a MIND`)
**sin medir el cap**:

| Commit | `AGENTS.md` |
|---|---|
| `058f1bfd6e` (2026-11-06) | 17.924 chars |
| `64edac4def` (2026-11-08, beam) | **19.995 / 20.000** |
| `9c5f51df07` (2026-11-09, planner) | 19.834 |

Quedó a **cinco caracteres** del límite: la palabra siguiente rompía el gate.
Lo destrabó el Planner al día siguiente, en un commit cuyo título dice
"restore bootstrap margin" — es decir, el problema existió y se arregló, pero no
por el CORE que lo causó.

El comportamiento correcto es correr `check-bootstrap-budget.py` **antes** de
escribir la sección, no después.

## 5. Hallazgo 3: deuda previa, no de la ventana

`check-handoff-merge.py` sale con exit 1 sobre 14 decisiones de baja cobertura
en el ledger. Una sola es de la ventana auditada:

```
cov=0.12  Adaptador real-browser.mjs se corrigio para usar Playwright de
          projects/kanam-fixer en vez de a11y-fixer archivado
```

Las otras trece (LEGAL, HEBRUS, REA, CV de Feltsense, etc.) son de días
anteriores. Es backlog de triage, no un error introducido por `beam`.

## 6. Verificación de contenido, artefacto por artefacto

Método: ejecutar cada artefacto y compararlo con lo que su documentación afirma. Leer el
commit no cuenta como verificación.

| Artefacto (commit) | Qué afirma | Qué se corrió | Resultado |
|---|---|---|---|
| `design-system-enforcer` (0f6febebec) | 7 tests de detección + excluir archivos propios | `npm test` | **7/7 pass** |
| Enforcer, ruta de bloqueo | bloquea ante gradiente/color/radio/padding/hex | CSS sembrado con las 4 faltas | **4 BLOCKS, 2 WARNINGS, exit 1** |
| Enforcer, `--apply` | reemplazo 1:1 solo con mapeo único | `.btn { color:#3b82f6 }` → apply | reemplaza por `var(--k-interactive-primary)`, correcto |
| Enforcer, dry-run | "dry-run deja el archivo intacto" | `--fix` sin `--apply` | archivo intacto, **exit 0** — correcto. El flag `--dry-run` **no existe** (§7) |
| `pixel-baseline` (0f6febebec) | guarda/lista baselines | `--help`, `--list` | responde; `--save/--dir/--name/--list` existen |
| `surface-score` (0f6febebec) | score del último report | ejecución real | **100/100 (A)**, coincide con L-010 |
| `enforcer.config.yaml` (0f6febebec) | whitelist de 10 hex del template | enforcer sobre directorio real | corre, exit 0, cada color con su motivo |
| `capability-index` (22eb901319) | procedimiento de 5 pasos con comandos | pasos 1 y 3 tal cual | `openclaw skills list --agent main --json` OK; `skill-router.py -n 3 "revisar un PR de OSS"` → **pr-review-response 0.73** |
| `capability-index` §4 | 4 convenciones de ruta | `test -e` sobre el catálogo | `skills/capability-index/SKILL.md` resuelve |
| Router 10/10 (22eb901319) | 10 casos en top-3 | `test-skill-router.py` | **10/10** |
| "13 pares" (87f8a68381) | scan own-only, 13 pares sobre 0.87 | `check-skill-overlap.py --own-only --threshold 0.87` | **13 pares exactos** |
| Gate de overlap bloqueante (04dc33c08a) | no bloquea trabajo legítimo | `--staged --own-only --blocking` | **exit 0** |
| Programa skill-router (22eb901319) | 8 pasos, todos cerrados | lectura del JSON | 8/8 `completed`, `closed_at` 2026-11-07 |
| Retención CHANGELOG (22eb901319) | 14 días vivos, resto archivado | grep 2026-10-23 en ambos archivos | **7 en el archivo, 0 en el vivo** |
| CV Feltsense (11-08) | perfil agentic, sin inventar stack | cruce de 24 tecnologías contra `career-facts.md` | GCP/LLM/OpenAI aparecen **solo** en "Not claimed (not in my stack)" |
| CV Mercado Libre (11-08) | gaps honestos en Go/Python/Redis | cruce de 23 tecnologías | Python y Redis figuran como **gap declarado**, no como claim |

**Ningún artefacto produjo un resultado distinto de lo que su documentación afirma.**

## 7. Defecto 3: una lección que enseña un flag inexistente (corregido)

`agents/kanam-auditor/LEARNINGS.md` L-008, escrito por `beam` el 2026-11-07:

```
Evidencia: CLI smoke: dry-run deja el archivo intacto
Efecto: B.3 (--fix determinístico 1:1, --dry-run primero)
```

**El flag `--dry-run` no existe.** El CLI real ofrece `--fix` (dry-run por
defecto) y `--apply`. Correr `--fix --dry-run` devuelve
`error: unknown option '--dry-run'`.

**La sustancia era cierta** —`--fix` solo deja el archivo intacto, verificado—
pero la lección manda al próximo lector a escribir un comando que falla. Es el
modo de falla que importa: no un hecho falso, una instrucción que no se puede
ejecutar.

Corregido a `--fix` sin `--apply` en las dos líneas.

## 8. Nota de método

El dato que ordena todo esto no es el commit: es la columna `model` de la tabla
de sesiones. Sin ella no había forma de saber *qué* sesiones corrieron con
`beam`; con ella, la ventana se acota a 9 sesiones y 4 commits, y el resto se
descarta sin leerlo.

```bash
openclaw sessions list --json | jq -r '.sessions[] | select(.agentId=="main") | [.updatedAt,.model,.totalTokens] | @tsv'
```

Y el segundo control es el que más rinde: **extraer los flags que la
documentación nueva introduce y contrastarlos con `--help`**. De 30 flags
distintos usados en los cuatro commits, uno solo no existía.
