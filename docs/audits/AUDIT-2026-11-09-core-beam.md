# AUDIT-2026-11-09 - Kanam CORE (`main`), ventana `beam:cloud`

<!-- project: github.com/gonzoblasco/workspace_openclaw -->

Auditoría de los tres días en que el agente `main` corrió con `beam:cloud`
(2026-11-07 17:07 a 2026-11-09 23:00), con el mismo método que se usó para los
roles: **correr lo que cada artefacto afirma, no leer el mensaje del commit.**

Fecha: 2026-11-09.

## Veredicto

**No se introdujeron errores de fondo.** Los artefactos de gobierno están
consistentes y todos los gates pasan. Dos defectos reales, ambos de forma y
ambos en el mismo archivo — las reglas con las que yo mismo opero — y un tercer
hallazgo que es deuda previa, no de la ventana.

Los dos defectos están corregidos en el commit que acompaña a este informe.

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

## 6. Lo que se verificó del trabajo sustantivo

- **Retención del CHANGELOG** (`22eb901319`, -147 líneas): las entradas del
  2026-10-23 aparecen **7 veces** en `docs/archive/CHANGELOG-archive.md` y **0**
  en el CHANGELOG vivo. Se archivaron, no se perdieron.
- **Gate de overlap promovido a bloqueante** (`04dc33c08a`): el flag
  `--own-only` excluye `-bundled`, `-extra` y `-custodian`, y hoy el comando
  completo sale en 0. El pre-commit no está bloqueando trabajo legítimo.
- **Skill router** (`22eb901319`): 10/10 casos en el top-3, verificado corriendo
  el test, no leyendo el commit.
- **CVs de la ventana** (Feltsense, Mercado Libre): los 14 CVs del workspace
  siguen coincidiendo con `career-facts.md`.

## 7. Nota de método

El dato que ordena todo esto no es el commit: es la columna `model` de la tabla
de sesiones. Sin ella no había forma de saber *qué* sesiones corrieron con
`beam`; con ella, la ventana se acota a 9 sesiones y 4 commits, y el resto se
descarta sin leerlo.

```bash
openclaw sessions list --json | jq -r '.sessions[] | select(.agentId=="main") | [.updatedAt,.model,.totalTokens] | @tsv'
```
