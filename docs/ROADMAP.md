# ROADMAP - Sistema de trabajo con IA

> Hoja de ruta de **decisiones y estado por capa**, no lista de features ni segundo backlog. Cada item define qué es, por qué importa, el criterio de éxito, y la señal de que está listo. La prioridad no es "lo más importante", es **lo que desbloquea más camino por unidad de esfuerzo** en el contexto actual (sesiones por proyecto, búsqueda laboral activa, una sola máquina).

**Última revisión: 2026-10-06** (verificada contra fuentes reales: git, GitHub, filesystem, `memory/memory.db`, runtime `openclaw`). Reconstruido desde cero: la versión anterior (revisión 09-14) arrastraba hipótesis ya refutadas y un estado de búsqueda laboral falso. El histórico queda en git.

**Qué NO es este documento:**
- No define el "para qué" de largo plazo: eso es `docs/NORTH.md`.
- No es la lista de tareas: eso es `memory/memory.db` (tabla `todos`, espejo `memory/todos.md`). Si un item de acá se vuelve tarea concreta y fechada, vive en la DB, no acá.
- No es el análisis del ecosistema externo (plugins/repos candidatos): eso es `docs/ecosystem/DECISIONS.md`.

**Cómo se mantiene:** con `docs/checklists/roadmap-review-checklist.md`. La revisión se hace **contra fuentes reales** (git, GitHub, filesystem, logs, DB, runtime), nunca contra lo que creíamos recordar. Un item solo pasa a 🟢 con su señal de listo verificada.

## Cómo leer este documento

- **Capas**: el sistema vive en 5 planos superpuestos (fundaciones, pipeline, portfolio, ecosistema, crecimiento). Cada capa tiene su propio tipo de optimización.
- **Prioridad**: P0 = desbloquea todo lo demás. P1 = alto valor, bajo riesgo. P2 = ganancia marginal, no urgente.
- **Estado**: 🔴 no iniciado / 🟡 en curso o con deuda activa / 🟢 estable / ⚫ deprecado o retirado.
- **Señal de listo**: el criterio objetivo que confirma que el item está resuelto, no "se siente mejor".
- **Regla de estado**: un item solo pasa a 🟢 con evidencia de la señal de listo. El estado se revisa, no se arrastra.

---

## La ruta (secuencia fijada, 2026-10-06)

Una sola ruta, no cuatro mapas que se contradicen. Esto ordena **qué va primero**, y gobierna la prioridad consolidada de abajo.

| Tramo | Foco | Criterio de salida |
|---|---|---|
| **T1 - ahora → dic 2026** | **OnWheels** (obra finita) + **design system** (se aprende dentro de la obra) + **CPACC** (examen, fecha dura 9-dic) | OnWheels entregado a Esteban; examen CPACC rendido |
| **T2 - ene → mar 2027** | OnWheels como **caso de estudio** + **reactivar la búsqueda laboral** | 1 proceso laboral nuevo avanzando (no de una oferta inexistente) |
| **T3 - Q1 2027** | **UNA** apuesta comercial: `soporteml` (ya factura) o `kanam-fixer` (más defendible) - no las dos | Primer pago real, o descarte fundado |
| **D - continuo** | El sistema como **soporte** (`kanam-os`, memoria, pipeline) - solo si sirve a T1/T2/T3 | No compite; habilita los tramos |

**La tensión que esta secuencia resuelve:** los tramos que *facturan* (empleo, producto) estaban fríos mientras los que no facturan (construir, sistema) consumían el tiempo. T1 arranca por la obra terminable y la credencial; el retorno comercial va en T3, no ahora.

**Regla de la ruta:** no se abre un frente nuevo (ni un noveno proyecto, ni un segundo producto comercial) hasta cerrar el tramo en curso. Lo que no entra, se anota en `memory/inbox.md`.

---

## Capa 0 - Fundaciones (sostiene todo)

### 0.1 Integridad del bootstrap 🟢 P0
- **Qué**: los archivos que OpenClaw inyecta en **cada arranque** de sesión (`AGENTS.md`, `MEMORY.md`, `USER.md`, `SOUL.md`, `IDENTITY.md`) tienen un cap de inyección. Lo que lo supera **se trunca en silencio**: el agente arranca sin esas reglas y no lo sabe.
- **Corrección histórica (2026-10-06)**: el item anterior ("Estabilidad de la infraestructura (gateway)") partía de *"el gateway se reinicia solo bajo sesiones largas"*. El re-diagnóstico del 14/09 (leído contra los dumps y el código fuente) ya había mostrado que **no hay reinicios espontáneos**: los 19 registrados eran `source=cli`/`handoff`, es decir intencionales. El problema real nunca fue el reinicio; fue el truncado del bootstrap. La versión vieja mantuvo la hipótesis refutada durante tres semanas.
- **Estado verificado 2026-10-06** (caracteres como los mide el runtime, unidades UTF-16 - no `wc -c`, que sobreestima en español por los acentos):

  | Archivo | Tamaño | Cap | Estado |
  |---|---|---|---|
  | `AGENTS.md` | 18.798 | 20.000 | 🟢 +1.202 |
  | `MEMORY.md` | 13.705 | 20.000 | 🟢 +6.295 |
  | `USER.md` | 3.600 | 4.000 (fijo, no configurable) | 🟢 +400 |
  | `SOUL.md` | 2.915 | 20.000 | 🟢 |
  | `IDENTITY.md` | 3.243 | 20.000 | 🟢 |
  | TOTAL | 42.261 | 60.000 | 🟢 |

- **Caps (fuente: código instalado `dist/bootstrap-*.mjs`, OpenClaw 2026.9.8)**: `DEFAULT_BOOTSTRAP_MAX_CHARS=2e4`, `USER_BOOTSTRAP_MAX_CHARS=4e3` (fijo), `DEFAULT_BOOTSTRAP_TOTAL_MAX_CHARS=6e4`. No hay override en `openclaw.json` (verificado).
- **Enforcement (2026-10-06)**: `scripts/check-bootstrap-budget.py` mide los 5 archivos y falla si alguno supera su cap o el total. Cableado al pre-commit (sin condición) y al CI. Antes de esto el item era un falso verde: la regla estaba escrita y **nada la verificaba** (ningún check cubría el tamaño de los archivos inyectados).
- **Por qué importa**: es la deuda más cara y la más invisible: se paga en cada arranque. `USER.md` ya se había resuelto el 14/09 (10.008 -> 3.986) y **regresó** a 4.582; una regla sin guarda se viola sola.
- **Criterio de éxito**: los tres archivos por debajo de su cap.
- **Señal de listo**: `python3 scripts/check-bootstrap-budget.py` sale 0 (y el pre-commit no frena).
- **Acciones**:
  - [x] Bajar `AGENTS.md` a <20.000 (el detalle ampliado va a `docs/AGENTS-DETALLE.md`).
  - [x] Bajar `MEMORY.md` a <20.000 (el detalle por proyecto va bajo `memory/` -que `memory_search` sí indexa-, no dentro del propio `MEMORY.md`).
  - [x] Bajar `USER.md` a <=4.000 (detalle a `memory/user-profile.md`; el entorno a `docs/SETUP.md`).
  - [x] Guard que verifique el cap (`scripts/check-bootstrap-budget.py`, pre-commit + CI).
- **Regla operativa (no es checkbox)**: un archivo de bootstrap no es documentación libre, es **contexto que se inyecta en cada turno**. Su detalle vive en `docs/` o `memory/`, nunca en el propio archivo. Al agregar a `AGENTS.md`/`MEMORY.md`, la regla es: ¿esto tiene que estar en cada arranque? Si no, va a un doc referenciado.

### 0.2 Higiene del workspace 🟢 P1
- **Qué**: `git status` del workspace limpio y explicable; sin cruft, sin punteros desincronizados, sin archivos de sesión trackeados por error.
- **Por qué**: un workspace que se entiende de una mirada reduce fricción al arrancar cada sesión.
- **Señal de listo**: `git status --short` no muestra nada inesperado al abrir una sesión.
- **Estado verificado 2026-10-06**: `git status` muestra solo `M memory/memory.db` y `M memory/todos.md` (cambios de sesión esperados). `projects/` es el espacio común del workspace (ADR-098). `a11y-fixer` figura `isArchived: true` en GitHub.
- **Acciones**:
  - [x] Proyectos de vuelta en `<workspace>/projects/` (ADR-098, 2026-10-08; supersede ADR-075). El workspace no los trackea (`.gitignore` `/projects/`), pero son alcanzables por todos los agentes.
  - [x] `a11y-fixer` archivado en GitHub (`gh repo view --json isArchived` -> true).
  - [x] Regla de guion (em dash) cerrada (ADR-082).
  - [ ] **`.knowledge/` sin respaldo en proyectos que no lo trackean** (id en `todos`): algunos proyectos propios excluyen su `.knowledge/` del repo individual (via `.git/info/exclude`), asi que esa memoria vive solo en disco. El respaldo es trackearla EN el repo del proyecto. *(Correccion 2026-10-13: `projects/` es una carpeta plana 100% ignorada, cada proyecto es su propio repo; NO hay repo agregado. La nota previa que decia que "`projects/.git` apunta a `workspace_openclaw`" era FALSA - `projects/` nunca tuvo `.git` propio; `git -C projects` resuelve al `.git` del workspace.)*
  - [ ] Decidir destino de `kanam-skills` público (desactualizado; ver `docs/NORTH.md`).
- **Restricción cerrada (no es acción)**: `soporteml` y sus versiones no se tocan en barridos - decisión de ADR-001 de `portfolio-strategy` y del ADR-0001 del proyecto `soporteml`.

### 0.3 Consolidación de memoria 🟢 P1
- **Qué**: `memory/memory.db` es la fuente de verdad (tablas `daily_notes`, `todos`, `inbox`, `contributions`); los `.md` son vistas regenerables. El daily se escribe por `session-end.sh`/`scripts/memory-end-session.py`, no a mano.
- **Por qué**: la memoria es el sistema de continuidad; si se llena de ruido o se desincroniza de la DB, deja de ser útil.
- **Señal de listo**: al retomar, el daily del día anterior responde "dónde estábamos" sin re-descubrir; `.md` y DB coinciden.
- **Estado**: flujo DB-first operativo. Reconcile `.md`->DB antes del export (commit `d9e964e`).
- **Acciones**:
  - [ ] Dedupe de `contributions` (filas duplicadas por repo+pr; números "pelados" sin `#`) - id en `todos`.
  - [ ] Sanear `CHANGELOG.md` (sección mezclada en el cierre del 30/09) - id en `todos`.

---

## Capa 1 - Pipeline de ejecución (cómo trabajamos)

### 1.1 Pipeline A/B 🟢 P1
- **Qué**: A escribe (`gpt-oss:120b-cloud`), B revisa/corrige (`deepseek-v4.1-flash:cloud`), pre-filtro `gemma4:cloud` (triage). El CORE redacta los prompts y **verifica el repo**, pero su verificación **no reemplaza** al revisor B.
- **Por qué**: es la arquitectura de calidad del sistema; sin enforcement se degrada a "un agente que dice que revisó".
- **Criterio de éxito**: el gate `scripts/check-pipeline-enforcement.py` pasa; el pipeline se usa por defecto, no por recordatorio.
- **Señal de listo**: 5+ sesiones con A/B aplicado y verificado sin excepción manual.
- **Base**: ADR-077 (A/B asimétrico), ADR-088 (enforcement), ADR-089 (pre-filtro).
- **Acciones**:
  - [ ] Registrar duración por tarea (inicio/fin) en `pipeline-track.sh`.
  - [ ] Contar cuántas veces B introduce bugs al "corregir" (el cross-review no es infalible, 2026-08-21).

### 1.2 Ruteo y política de modelos 🟢 P1
- **Qué**: un modelo por rol, con fallback y nivel de pensamiento. Decisión viva en **ADR-090** (2026-10-06).
- **Por qué**: el modelo correcto por tarea ahorra tiempo y presupuesto; el incorrecto lo quema (ver el caso del "thinking alto universal" que vaciaba el output).
- **Asignación vigente (ADR-090, aplicada y verificada en runtime)**:

  | Rol | Modelo | Fallback | Thinking |
  |---|---|---|---|
  | main | `deepseek-v4.1-flash:cloud` | `glm-5.3-flash:cloud` | off |
  | mind | `deepseek-v4.1-flash:cloud` | `gemma4:cloud` | off |
  | dev | `gpt-oss:120b-cloud` | `deepseek-v4.1-flash:cloud` | off |
  | ops | `gpt-oss:120b-cloud` | `deepseek-v4.1-flash:cloud` | off |
  | studio | `gemma4:cloud` | `glm4:9b` local | off |
  | critic | `gpt-oss:120b-cloud` | `nemotron-3-super:cloud` | low |
  | auditor | `deepseek-v4.1-flash:cloud` | `gemma4:cloud` | low |
  | planner | `gpt-oss:120b-cloud` | `glm-5.3-flash:cloud` | low |

  `kimi-k3:cloud` queda reservado al review previo al deploy.
- **Nota de método (2026-10-06)**: la cata que decidió esto tenía un defecto de harness (runner por CLI que mezclaba thinking con el entregable, inflando un "leakage" que era artefacto del CLI, no de producción). El ADR-090 lo declara explícitamente. Para futuras catas: usar la API, no el CLI.
- **Criterio de éxito**: el router elige el modelo correcto sin intervención manual en tareas estándar.
- **Señal de listo**: 0 casos de "este modelo no sirvió para esto" en una semana de tareas rutinarias.
- **Acciones**:
  - [ ] **Test de contexto largo** (el único experimento que confirma o refuta la intuición de que nemotron "pierde el hilo"): meter un dato clave a 10k/50k/200k/300k y ver dónde cada modelo lo pierde.
  - [ ] Telemetría de fallos por modelo (cuándo rotar).

### 1.3 Stack opinado como sistema 🟡 P1
- **Qué**: OpenSpec, Biome, ADRs, HANDOFF, CHANGELOG. Está decidido.
- **Por qué**: el valor está en la consistencia, no en la elección.
- **Criterio de éxito**: se aplica siempre, no cuando lo recordamos.
- **Señal de listo**: pre-commit hooks (lint -> test -> build) presentes en los proyectos activos; ADRs para decisiones nuevas.
- **Estado**: auditoría 14/09 = **0 de 21** proyectos con hook. Re-verificar contra `projects/*`.
- **Acciones**:
  - [ ] Instalar pre-commit hooks en los proyectos activos. Regla: prioridad sobre features.

---

## Capa 2 - Portfolio (qué construimos)

### 2.1 Estrategia de proyectos 🟢 P0
- **Qué**: qué 2-3 proyectos sostienen el pitch "fullstack con IA como infraestructura" + el nicho a11y.
- **Por qué**: sin esto, el pipeline optimiza lo equivocado. Dispersión = portfolio que no cuenta una historia.
- **Fuentes vivas**: `projects/portfolio-strategy/ADR-001` (pilares + anclas), `memory/notes/portfolio-curation.md` (curaduría de presencia, 2026-09-21).
- **CORRECCIÓN (2026-10-06)**: el item decía que `kanam-fixer` tenía **"alcance SIN DEFINIR"**. **Era falso.** El alcance se definió el 2026-09-14/15 (BRIEF + ROADMAP del proyecto, dirección confirmada por Gonzo) y el ciclo `0.0.1` **cerró con evidencia** el 2026-09-15. Lo confirma ADR-001 §6 ("los 4 pendientes cerrados... ancla candidata formalizada con alcance ya definido"). El ROADMAP arrastró el estado pre-definición durante tres semanas: otro falso pendiente, como el Tablero y el design system.
- **Estado verificado 2026-10-06** (contra `projects/kanam-fixer` + GitHub + npm):
  - **Ancla vigente**: `kanam-fixer` (sucede a `a11y-fixer`, archivado 2026-09-14). **Alcance DEFINIDO**: asercion sobre el **anuncio del lector de pantalla** (no sobre atributos del DOM), la misma asercion en dos planos (virtual en CI, real en local). **Greenfield** (no hereda el engine de `a11y-fixer`).
  - **Ciclo `0.0.1` CERRADO** (2026-09-15); `0.0.2` abierto (MCP companion server, commit `f1f60fa`). Repo **público** `gonzoblasco/kanam-fixer` (isArchived=false), paquete npm **`kanam-fixer@0.0.2`** publicado. Último commit `262c004` (2026-09-17). Último push al repo 2026-09-26.
  - **Limitación declarada (S3)**: el plano real (VoiceOver) no es verificable en esta máquina hasta que Guidepup soporte Darwin 27 ([issue #149](https://github.com/guidepup/guidepup/issues/149)). El valor del proyecto se invirtió hacia el **plano real como único juez** de la clase timing/viewport.
  - **Apuestas de producto vivas** (absorbidas de `APUESTAS.md`, retirado el 2026-10-06):
    - **`soporteml`** (producto, privado): v4 cerrado (ADR-0002 del proyecto `soporteml`); sigue por la version funcional de Lovable, con cobro por Stripe ya operativo. Primer proyecto con billing real.
    - **`kanam-fixer`** (producto): diferenciador defendible (auditoría sobre lo que el lector de pantalla *anuncia*, no sobre atributos del DOM como axe-core).
  - **Showcase (curaduría 09-21)**: `kanam-fixer`, `ai-developer-stack`, `kanam-skills`.
- **Criterio de éxito**: una lista corta de proyectos "estrella" con su rol en el pitch, sin contradicciones entre ADR-001 y este roadmap.
- **Señal de listo**: el pilar *Accesibilidad* tiene ancla formal. **✅ Cumplida** (ADR-001 §6: ancla formalizada en `kanam-fixer`). La validación de *impacto* del ancla sigue siendo el criterio de NORTH H1 (usuarios que no sean Gonzo), no la definición de alcance.
- **Acciones**:
  - [x] **Definir el alcance de `kanam-fixer`** - HECHO 2026-09-14/15 (BRIEF + ROADMAP, dirección confirmada por Gonzo).
  - [x] Reconciliar la lista de proyectos de `MEMORY.md` con `projects/` real - MEDIDA 2026-10-06. Drift real hallado y corregido en `MEMORY.md`: (a) la lista no incluía repos vivos en GitHub (`kanam-minesweeper`, `kanam-sudoku`, `match3`, `system-health-check`, `catalogo-de-venta-de-coches`); (b) `kanam-insight` existe como repo (GitHub, no archivado) aunque el proyecto está descontinuado - la memoria lo decía "no existe como proyecto", que es correcto sobre su rol, no sobre el repo.

### 2.2 Cadena OSS -> LinkedIn 🟡 P1
- **Qué**: cada merge de a11y/agentic -> post. El patrón está definido (2026-08-25); falta la cadencia real.
- **Por qué**: ligado directo al objetivo laboral (nicho a11y/agentic).
- **Estado verificado 2026-10-06** (fuente: DB `contributions`): **18 PRs abiertos, 8 mergeados, 22 cerrados sin merge, 15 colaboraciones no-código, 22 repos**. Posts en `docs/linkedin/`.
- **Criterio de éxito**: cada merge de a11y/agentic genera un post en `docs/linkedin/` dentro de la semana.
- **Señal de listo**: 3+ posts publicados con el patrón didáctico, no solo drafts.
- **Acciones**:
  - [ ] Sostener la cadencia: 1 post por merge de a11y/agentic dentro de la semana.
  - [ ] Flip `draft` -> publicado documentado en el archivo de cada post.

### 2.3 Búsqueda laboral 🔴 P0
- **Qué**: procesos abiertos y su estado. **Fuente de verdad única**: `docs/entrevistas/job-search-tracker.md`.
- **Por qué**: es el objetivo activo del Horizonte 0 (`docs/NORTH.md`); situación económica urgente.
- **CORRECCIÓN MAYOR (2026-10-06)**: la versión anterior de este ROADMAP afirmaba *"EIT/HTC/Disney - OFERTA ACEPTADA (11/09), USD 4.000/mes, arranque 01/10"*. **Era falso.** El tracker (actualizado al **2026-09-24**) dice: **EIT nunca tuvo oferta firme** (el rate lo aceptó el reclutador, el cliente jamás hizo call; era un bench req amplio). **No hay procesos abiertos: todos cerrados.** El estado 🟢 del item anterior era un falso verde de tres semanas.
- **Criterio de éxito**: al menos un proceso avanza a oferta/onboarding.
- **Señal de listo**: onboarding efectivo de un proceso nuevo (no de una oferta inexistente).
- **Estado al 2026-09-24** (todos cerrados): EIT/HTC, Wigou, OpenSistemas, Ritz-Carlton, Kake, Koin, Aliancers, Ciklum. Ver trackers individuales en `docs/entrevistas/`.
- **Backlog de prospectos** (relevado 09-23, fuera de seguimiento): Infojini, E-IT, Cheesecake Labs, Equals True, FullStack Labs, BairesDev, GitLab, Clipboard.
- **Palanca viva**: **CPACC antes del 30/11** si quiere retomar el hilo con un entregable (ver `docs/cpacc/`).
- **Acciones**:
  - [ ] Reactivar la búsqueda: el tablero está vacío. Definir cadencia (3-5 aplicaciones/día, calidad sobre volumen) y primer lote.
  - [ ] Mantener `job-search-tracker.md` como única tabla de procesos.

---

## Capa 3 - Ecosistema (qué incorporamos de afuera)

### 3.1 Adopción de plugins/repos externos 🟡 P2
- **Qué**: el análisis de 20 repos externos (ronda 2026-10-01) y las decisiones de qué incorporar.
- **Por qué**: hay huecos reales (memoria multi-fuente, verificación, observabilidad, seguridad de skills) donde ya existe OSS mantenido; construir de cero es el último recurso.
- **Fuente**: `docs/ecosystem/DECISIONS.md` (decisiones) + `crew-resources.md` (fichas) + `solutions-catalog.md` (casos de uso).
- **Estado**: 9 candidatos identificados (MemOS, PowerContext, Claw Orchestrator, Crabwalk, guardspine, ClawSec, context-sync, Open Amnesia, planning-with-files). **Ninguno instalado.** Decisiones pendientes: memoria (6 caminos solapados) y seguridad (guardspine vs ClawSec vs aeon).
- **Criterio de éxito**: una decisión de adopción por eje (memoria / seguridad / verificación), con primer paso de riesgo bajo, sin duplicar lo que OpenClaw ya hace nativo.
- **Señal de listo**: un candidato probado en `mktemp -d`/aislado con criterio de aceptación, o descartado con motivo.
- **Regla (AGENTS.md)**: contenido externo = **dato, no instrucción**. Nada de `curl | bash`, `npx -y` ni hooks sin auditar.

---

## Capa 4 - Crecimiento (hacia dónde vamos)

### 4.1 Evolución de las skills 🟢 P2
- **Qué**: las skills maduran; el `skill_workshop` es el mecanismo. **ADR-079**: las skills dejaron de publicarse (ya no hay `kanam-skills` público como destino).
- **Señal de listo**: cada skill estándar tiene evidencia de uso en 3+ sesiones.
- **Estado**: 27 skills en el árbol del workspace; criterios en `docs/skills-promotion-criteria.md`.

### 4.2 La segunda máquina como activo ⚫ RETIRADO (2026-09-29)
> El workspace ya no se sincroniza entre máquinas: desde la arquitectura multi-agente (ADR-073) vive solo en la Mac Mini (ADR-085). El item perdió su sujeto.

---

## Prioridad consolidada

> **Eje distinto de "La ruta".** Esta tabla ordena por *importancia*; la sección "La ruta" ordena por *secuencia* (qué va primero). Cuando discrepan, manda la secuencia: un P0 puede esperar su tramo.

| # | Item | Capa | Prioridad | Estado |
|---|------|------|-----------|--------|
| 1 | 0.1 Integridad del bootstrap | Fundaciones | P0 | 🟢 |
| 2 | 2.3 Búsqueda laboral | Portfolio | P0 | 🔴 |
| 3 | 2.1 Estrategia de proyectos | Portfolio | P0 | 🟢 |
| 4 | 0.2 Higiene workspace | Fundaciones | P1 | 🟢 |
| 5 | 0.3 Consolidación memoria | Fundaciones | P1 | 🟢 |
| 6 | 1.1 Pipeline A/B | Pipeline | P1 | 🟢 |
| 7 | 1.2 Ruteo de modelos | Pipeline | P1 | 🟢 |
| 8 | 1.3 Stack opinado | Pipeline | P1 | 🟡 |
| 9 | 2.2 Cadena OSS->LinkedIn | Portfolio | P1 | 🟡 |
| 10 | 3.1 Adopción ecosistema | Ecosistema | P2 | 🟡 |
| 11 | 4.1 Evolución skills | Crecimiento | P2 | 🟢 |
| 12 | 4.2 Segunda máquina | Crecimiento | P2 | ⚫ retirado |

---

## Notas de creación y mantenimiento

- Creado 2026-08-28 a partir de la sesión de refactor de Moderno AI Cleaner Pro.
- Revisado 2026-09-14: contraste item por item contra fuentes reales.
- **Reconstruido desde cero 2026-10-06**: la revisión del 09-14 durmió tres semanas arrastrando (a) una hipótesis de inestabilidad de gateway ya refutada y (b) un estado de búsqueda laboral falso (oferta aceptada que nunca existió). Ambos corregidos contra las fuentes. Se agregó la capa *Ecosistema* (análisis de 20 repos, 2026-10-01) que la versión previa no tenía.
- Este documento es vivo: se revisa cuando un item cambia de estado o se toma una decisión de prioridad. **Regla: la revisión se hace contra fuentes reales, no contra lo que creíamos recordar.**
