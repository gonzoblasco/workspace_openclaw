# CHANGELOG.md

Registro de cambios estructurales del workspace. Contiene las entradas de los **últimos 30 días** (corte: 2026-09-06). Lo anterior está archivado en [`./docs/archive/CHANGELOG-archive.md`](./docs/archive/CHANGELOG-archive.md). No incluye actividad diaria (ver `memory/`).

> **Política de rotación:** la mantiene `scripts/changelog-rotate.py` (pre-commit `--check` + cierre de sesión). Al superar la ventana, el bloque viejo se mueve al archivo. Reconstruir el activo desde cero cuando arrastre hipótesis refutadas.

---

## [2026-10-07] - El Critic deja de ser un rol sin skills: nace `sharp-adversarial-review`

### Added
- **`agents/kanam-critic/skills/sharp-adversarial-review/SKILL.md`:** primera skill del rol Critic. El ritual de presión adversarial con la rúbrica SHARP: cómo puntuar los 5 ejes (Sharpness, Horizon, Asymmetry, Resistance, Parsimony) con evidencia citable, el mapa de veredicto (VETO en `<= 18`, Aprobado, ORO en `>= 24`) y el entregable del VETO (puntos de fricción obligatorios). Presta de `skills/verification-gates` la guarda de verde falso y de `skills/trust-vocabulary-report` el contrato de evidencia; marca el deslinde sustancia vs forma con el Auditor.
- **`agents/kanam-critic/skills/`:** el árbol de rol del Critic no existia. Su `workspaceDir` solo tenia AGENTS/IDENTITY/SOUL/USER, asi que el agente veia **cero** skills y su job semanal de revision corria sobre un directorio vacio.

### Changed
- **`SKILLS-INDEX.md`:** sumada la fila `agents/kanam-critic/skills/` (1) y la seccion 3.6; total de activas 78 -> 79.

### Notes
- **El job `skill-collection-review:kanam-critic` corria en error** (`Ls failed`): revisa el Skill Workshop del agente (`agent/workshop-skills/`), que estaba vacio. Con el arbol de rol ya en pie, el agente tiene material propio; el job queda sin bloqueo de arbol.

---

## [2026-10-06] - kanam-fixer: el alcance estaba definido; el ROADMAP mentia desde hacia 3 semanas

### Fixed
- **`docs/ROADMAP.md` §2.1 decia que `kanam-fixer` tenia "alcance SIN DEFINIR". Era FALSO.** El alcance se definio el 2026-09-14/15 (BRIEF + ROADMAP del proyecto, direccion confirmada por Gonzo) y el ciclo `0.0.1` cerro con evidencia ese mismo dia. Lo confirma `portfolio-strategy/ADR-001` §6. Otro falso pendiente (como el Tablero y el design system: gobernanza dormida acumulando estados viejos). Corregido: ancla formalizada, alcance definido, ciclo 0.0.1 cerrado / 0.0.2 abierto, npm `kanam-fixer@0.0.2`, repo publico. §2.1 pasa a 🟢.
- **`docs/NORTH.md`** (decision abierta #1): mismo falso pendiente corregido. Lo que sigue abierto no es la *definicion* del alcance sino la *validacion de impacto* del ancla (criterio H1).
- **`MEMORY.md`** (reconciliacion pedida por §2.1, medida contra `gh repo list`): sumados repos propios vivos que faltaban (`catalogo-de-venta-de-coches`, `create-stack`, `kanam-minesweeper`, `kanam-sudoku`, `match3`, `system-health-check`); aclarado que `kanam-forge` es fork (no propio) y que `kanam-insight` existe como repo (privado) aunque el proyecto esta descontinuado.

### Changed
- **`portfolio-strategy/.knowledge/ADR-001-portfolio-strategy.md`** (fuera del workspace): nueva seccion 8 que **verifica** el estado contra fuentes reales y cierra formalmente el pendiente de definicion de la seccion 6. El pilar Accesibilidad tiene ancla formal.

---

## [2026-10-06] - Integridad del bootstrap deja de ser un falso verde (ROADMAP 0.1)

### Added
- **`scripts/check-bootstrap-budget.py`:** guard del cap de inyeccion del runtime. Los archivos que OpenClaw inyecta en cada arranque (AGENTS/MEMORY/USER/SOUL/IDENTITY) se truncan EN SILENCIO al superar su cap. Mide en caracteres como el runtime (unidades UTF-16, no bytes: `wc -c` sobreestima en espanol por los acentos y da un margen falso). Caps verificados contra el codigo instalado (`dist/bootstrap-*.mjs`): 20.000 por archivo, 4.000 fijo para USER.md, 60.000 total. Modo reporte + bloqueante.
- **`tests/python/test_check_bootstrap_budget.py`:** 10 casos (mide UTF-16 como el runtime, cap propio de USER.md, borde exacto, la CLASE y el total, contrato de salida del script real).

### Changed
- **Pre-commit (sin condicion) + CI (`skills-ci.yml`):** el check corre siempre. Los archivos de bootstrap no cambian por un pathspec predecible; un trigger por diff dejaria pasar el crecimiento que ocurre en cualquier otra edicion.
- **`USER.md` (3.933 -> 3.600 chars, margen 67 -> 400):** el contenido de ENTORNO (canal remoto Telegram, gateway 24/7) se movio a `docs/SETUP.md`. Un archivo de bootstrap es contexto de cada turno; el entorno no lo es.
- **`MEMORY.md` (13.893 -> 13.705):** quitadas las referencias a harness (Claude Code, terminal harnesses, jsdom/headless); la leccion de fondo se conserva. Pedido de Gonzo para aflojar margen.
- **`docs/SETUP.md` seccion Red / remoto:** corregida la linea stale (decia Tailscale+PWA como canal; Telegram lo reemplazo el 2026-09-07) y absorbidos los dos bullets de entorno.

---

## [2026-10-06] - El design system gana su tema oscuro; kanam-os migra (ADR-096)

### Added
- **`design/tokens/themes/dark.tokens.json`:** tema oscuro del sistema base (el `kanam.css` base ES el claro). Paleta tomada del tema oscuro de kanam-os (probada), recalculada al piso WCAG. 11 pares verificados (text.primary 12.83:1, danger 7.50:1, brand 4.85:1).
- **`tests/python/test_check_design_tokens.py`:** caso del tema oscuro (existe + cumple).

### Changed
- **`design/tokens/build-tokens.py` + `scripts/check-design-tokens.py`:** `dark` sumado al REGISTRY y al guard. El build genera 7 hojas (antes 5).
- **`design/README.md`:** tabla de temas con `dark` + nota modo vs marca (el claro no necesita archivo: `kanam.css` = `:root`).

### Delegado
- **kanam-os migra a consumir `design/tokens/` (DEV, pipeline A/B).** Contrato en ADR-096: consume kanam.css + dark.css, sync en build (anti-drift), preserva el toggle server-side. Verificación del CORE sobre el repo real al cerrar.

### Fixed
- **Regresión detectada en la verificación:** `--k-brand-primary` del dark (`#4ea870`) daba 3.73-4.28:1 como texto sobre card/elevated (kanam-os lo usa así). Corregido a `#6ee7a0` (7-8:1). El guard medía brand solo sobre `surface.base` - **hueco cerrado**: ahora también sobre `card`/`elevated`.
- **kanam-os:** la migración de A aliasaba tokens inventados (`--k-bg`, `--k-text`...); B la corrigió a los tokens reales + cargó los CSS + hookeó el sync a npm. Verificado por el CORE: build verde, ambos temas, 200, color-contrast limpio salvo `aria-pressed` (preexistente) y opacity en `/learnings` (preexistente).

---

### Added
- **ADR-095** (`docs/adr/ADR-095-reevaluacion-decisiones-diseno.md`): re-evaluación pedida por Gonzo ("lo que ya está hecho de decisiones de diseño deben ser revaluadas").
- **`scripts/check-design-tokens.py`:** mide el contraste WCAG de los tokens de cada tema contra el piso por rol (texto 4.5:1, componente 3:1; los bordes decorativos no se exigen). Modo reporte + `--check` bloqueante. Cableado al pre-commit (cambios en `design/`) y al CI.
- **`tests/python/test_check_design_tokens.py`:** 8 casos (matemática WCAG, el guard puede fallar, bordes decorativos no son falso positivo, el sistema real pasa).

### Fixed
- **10 pares de tokens bajo el piso WCAG** en los 3 temas, corregidos preservando la identidad (un paso más oscuro del mismo tono, con primitivas existentes): el teal de marca como texto (3.74 -> 5.25), el ámbar de warning (3.45-3.64 -> 4.96-5.23), los `muted` de Plaza/Terrario (3.33-3.94 -> 5.23-5.69), el `info` de Terrario (4.32 -> 6.33).
- **Matrices `$contrast`:** los números de Plaza/Terrario eran a mano y nunca medidos (decían "danger 4.9", el real era 4.70). Reemplazados por valores medidos; el sistema base ahora **declara la suya** (antes no existía).

### Changed
- **`design/README.md`, `ADR-047`, `DECISIONS.md` §2.8, `docs/NORTH.md`:** corregidas las afirmaciones falsas. El design system **ya existe** (`design/`, ADR-047 desde 2026-09-14) - el "paso 0" era un falso pendiente; la precondición del auditor de diseño ya se cumple. Lo que queda es **adopción** (kanam-os usa un tema paralelo) + práctica (`studies/design/`).
- **Pre-commit + CI:** el cambio en `design/` regenera el `dist/` y corre el guard de contraste.

---

## [2026-10-06] - Reconciliación: una sola ruta (APUESTAS + MAPA retirados, kanam-insight descontinuado)

### Removed
- **`docs/APUESTAS.md` y `docs/MAPA-PROXIMOS-PASOS.md` eliminados.** Cuatro documentos decían "qué sigue" y se contradecían (NORTH/ROADMAP/APUESTAS/MAPA, fechas 10-06/10-06/09-24/09-14). Quedan dos con roles distintos: `NORTH` (el para qué) y `ROADMAP` (el cómo y en qué orden). El MAPA estaba stale (hablaba de kanam-lab/kanam-studio como eje; NORTH ya los sacó). El contenido de producto de APUESTAS pasó a `ROADMAP.md` §2.1.
- **`kanam-insight` descontinuado y fuera del roadmap.** No existe como proyecto (no está en `~/projects/`) y Gonzo confirmó que no recuerda haberlo querido. Fuera de NORTH, ROADMAP §2.1, MEMORY.md y el registro del proyecto.

### Added
- **`docs/ROADMAP.md` - "La ruta" (secuencia fijada).** Tramos T1 (OnWheels + design system + CPACC), T2 (caso de estudio + reactivar búsqueda laboral), T3 (UNA apuesta comercial), D (sistema como soporte). Resuelve la tensión: los tramos que facturan estaban fríos mientras los que no facturan consumían el tiempo.

### Changed
- **`docs/ROADMAP.md`:** §2.1 absorbe las apuestas de producto vivas (soporteml, kanam-fixer); la prioridad consolidada aclara que ordena por *importancia* y "La ruta" por *secuencia*.
- **`docs/NORTH.md`, `docs/LANGCHAIN_STRATEGY.md`, `docs/adr/ADR-063`, `docs/adr/ADR-091`, `docs/adr/ADR-085`, `README.md`, `MEMORY.md`:** reapuntados para no citar los docs retirados. ADR-063 queda como registro histórico de la decisión de stack de kanam-insight (estado del sujeto: DESCONTINUADO).

## [2026-10-06] - Etapa 4 de Kanam OS: accesibilidad medida, tests/node cableados, Tablero cerrado

### Added
- **ADR-094** (`docs/adr/ADR-094-etapa-4-a11y-scan-tests-node-tablero.md`): cierra/reubica los tres componentes de la Etapa 4.
- **`scripts/a11y-scan.mjs`:** mide accesibilidad real de una página viva con axe-core (OSS) + playwright-core, sin `axe-devtools` pago. Exit 2 si la infra (playwright/axe) no está: un gate que no puede correr no es un verde. El juicio (`classify`) es puro y testeable. **Primera corrida:** encontró `aria-allowed-attr` `critical` (`aria-pressed` sobre `<a href>`) en `kanam-os` `/todos`, `/fichas`, `/learnings` - bug real de accesibilidad.
- **`tests/node/run.sh`:** runner de los tests Node del workspace (antes `tests/node/` no corría en ningún lado).
- **`tests/node/a11y-scan.test.js`:** 8 casos del clasificador (umbral, impacto desconocido = peor caso, umbral inválido lanza).

### Changed
- **`tests/node/` cableado** al pre-commit (junto a bats y pytest) y al CI (nuevo step "Node functional tests").
- **`docs/ecosystem/DECISIONS.md` §2.5:** el Tablero se cierra - la superficie visual del backlog **es** `kanam-os /todos` (modelo **pull**, fuente de verdad `memory.db`). Falso pendiente de 6 días.
- **`docs/ecosystem/DECISIONS.md` §2.8:** la pata de **medición** a11y ya existe (`a11y-scan`).
- **`docs/NORTH.md`:** Etapa 4 - a11y medida, Tablero cerrado, especialistas diferidos a propósito (el esqueleto Crew+SHARP ya está; los 13 roles del Academic System son dispersión).

---

### Added
- **ADR-093** (`docs/adr/ADR-093-plan-de-sesion-persistente.md`): el plan de sesión como objeto persistente del sistema. Cierra el hueco declarado en `docs/NORTH.md` (la Etapa 2 tenía cinco gates que nadie invocaba).
- **`scripts/session_plan.py close`:** marca el plan `completed` y lo archiva en `.knowledge/archive/session_plan_<id>.json`. Defensivo e idempotente (sale 0 siempre: el cierre corre bajo `set -e`).
- **`tests/python/test_session_plan.py`:** 5 casos (path portable/sobrescribible, init, close+archivo, idempotencia, exit code del CLI).

### Changed
- **`scripts/session_plan.py` portable:** el path, antes clavado a `/Users/gonzoblasco/...`, ahora se deriva del script y es sobrescribible con `SESSION_PLAN_PATH`. El plan se muda de la raíz (`.session_plan.json`) a `.knowledge/session_plan.json`.
- **`session-start.sh`:** hook de arranque. Si hay un plan activo, lo presenta antes de scorear/buscar memoria ("retomando: estábamos en el paso X"). Elimina la amnesia de sesión que el `AGENTS.md` del planner ya prohibía y nada garantizaba.
- **`session-end.sh`:** hook de cierre. Cierra y archiva el plan.
- **`session-start.sh` (path obsoleto):** el HANDOFF se resolvía en `projects/$PROJECT/.knowledge/` - estructura **pre-ADR-075**, muerta desde 2026-09-26. Se alinea con `scripts/session-handoff.py` (workspace -> `.knowledge/` propio; proyecto -> `~/projects/<slug>/.knowledge/`).

### Docs
- **`docs/session-planning-hooks.md`:** estado `PARCIAL` -> `ADOPTADO`.
- **`docs/NORTH.md`:** Etapa 2 actualizada (2 de 5 gates cableados; los 3 restantes sin cablear a propósito, con motivo).

---

### Changed
- **`EVOLUTION.md` eliminado; su contenido vive en `docs/NORTH.md`.** El blueprint de madurez de Kanam OS (etapas + metodología) pasó a la nueva sección "El camino de madurez del sistema". Había tres documentos diciendo "hacia dónde va Kanam" (`NORTH`, `EVOLUTION`, capa 4 del `ROADMAP`): ahora hay uno. Refs de agentes reapuntadas: `agents/kanam-critic/AGENTS.md` y `agents/kanam-planner/AGENTS.md` (leían `EVOLUTION.md`); entity `.knowledge/entities/projects/kanam_os.md` actualizado.
- **Los 5 specs de Kanam OS Etapa 2 documentan su estado real.** No eran huérfanos: son las specs de implementaciones vivas que nadie cableó.
  - `docs/security-scan-spec.md` -> **ADOPTADO**: cableado al pre-commit.
  - `docs/skill-evals-spec.md`, `docs/skill-lifecycle-tracker.md`, `docs/regression-control-spec.md` -> **EXPERIMENTO NO ADOPTADO** (implementación existe, nada la invoca).
  - `docs/session-planning-hooks.md` -> **PARCIAL** (el `AGENTS.md` del planner la referencia; no hay hook automático).

### Added
- **`scripts/security-scan.py --staged`:** modo gate que escanea **solo el código ejecutable staged bajo un árbol de skills** (`skills/`, `agents/<rol>/skills/`). El modo original sobre `scripts/` daba falsos positivos sobre código propio (se marca a sí mismo por citar `/etc/passwd` como patrón, los triggers `.js` por usar `exec(`, `test-skills.sh` por navegar `./../..`); `--staged` los evita por scope.
- **Pre-commit (hook + template):** corre `security-scan.py --staged` ante cambios de `skills/` o `agents/` - el caso real de "skill de afuera".

### Fixed
- **`scripts/regression_gate.py` no compilaba:** un bloque ` ``` ` de markdown al EOF, una flecha rota en un f-string y un path absoluto `/Users/...`. Reparado.
- **`scripts/lifecycle_tracker.py`:** path absoluto `/Users/...` hardcodeado. Ahora deriva del propio script.

### Removed
- **`EVOLUTION.md`** (contenido absorbido en `docs/NORTH.md`).

## [2026-10-06] - Dream Diary en rotación mensual (DREAMS)

### Added
- **`scripts/dreams-rotate.py`:** mantiene `DREAMS.md` en el mes en curso; los meses anteriores se archivan por mes en `memory/archive/dreaming/DREAMS-YYYY-MM.md`. Idempotente, solo toca el contenido entre los marcadores del diary del plugin (deja el bloque `Deep Sleep` intacto), una entrada sin fecha no se archiva. `--check`, `--dry-run`, `--today`, `--root` (tests).
- **`tests/bash/dreams-rotate.bats`:** 7 casos (drift, rota, marcadores intactos, idempotencia, `--check` limpio, `--dry-run`, fecha inválida).

### Changed
- **`skills/session-lifecycle/scripts/session-end.sh`:** rota DREAMS en cada cierre, junto con el CHANGELOG. Sin gate en pre-commit porque `DREAMS.md` está gitignored (estado local del plugin).

## [2026-10-06] - CHANGELOG con ventana de 30 días y rotación automatizada (ADR-092)

### Added
- **`scripts/changelog-rotate.py`:** mantiene `CHANGELOG.md` en una ventana activa de ~30 días; lo viejo se archiva en `docs/archive/CHANGELOG-archive.md`. Idempotente, ordena por fecha descendente, regenera los headers. `--check` (exit 1 si hay drift), `--dry-run`, `--days N`, `--today` (tests).
- **`tests/python/test_changelog_rotate.py`:** 8 casos (split, ventana, idempotencia, acumulación sin duplicados, orden, exit codes de `--check`, `--dry-run` no escribe, fecha inválida).

### Changed
- **`.git/hooks/pre-commit` + `scripts/pre-commit.template`:** nuevo check (solo si `CHANGELOG.md` está staged) que corre `changelog-rotate.py --check` y falla si el activo está desfasado.
- **`skills/session-lifecycle/scripts/session-end.sh`:** rota el CHANGELOG en cada cierre de sesión, para que la ventana nunca quede vieja.
- **`docs/archive/CHANGELOG-pre-2026-09.md` → `docs/archive/CHANGELOG-archive.md`:** el archivo pasa a ser rodante único (lo mantiene el script), no un snapshot con nombre de fecha.
- **`memory/2026-10-06.md`:** la entrada de gobernanza de esta sesión (análisis + reconciliación de AGENTS.md/AGENTS-DETALLE.md/SETUP.md), que había quedado sin commitear.

### Fixed
- **`docs/archive/` agregado a `SKIP_DIRS` de `check-refs.py` y a `MD_EXEMPT` del hook:** la historia congelada cita rutas de la época (un ADR luego renombrado) y conserva guiones largos; no se reescribe (política de ADR-084/ADR-082, igual que `docs/records/`).
- **`mindstudio_proposal.md` eliminado:** propuesta de vendor sin refs en markdown trackeado ni valor durable (Gonzo, 2026-10-06).

### Removed
- **`proposal.md`** (duplicado byte-idéntico de `mindstudio_proposal.md`) y **`mindstudio_proposal.md`**.

## [2026-10-06] - Refactor de gobernanza: AGENTS.md, AGENTS-DETALLE.md y SETUP.md reconciliados

### Fixed
- **Contradicción `.knowledge/` resuelta.** `docs/AGENTS-DETALLE.md` decía que el workspace `trackea projects/**/.knowledge/` (modelo pre-ADR-075) mientras `AGENTS.md` decía lo contrario. Se reescribió la sección "Triple Git" completa al modelo ADR-075: proyectos en `~/projects/`, workspace sin `projects/` ni `.knowledge/`, agregado vía `aggregate-sync.sh`. Anotada la deuda de `init-project.sh` (todavía resuelve `PROJECTS_DIR=workspace/projects`).
- **`HEARTBEAT.md` fantasma.** `AGENTS.md` mandaba "editar `HEARTBEAT.md`"; ese archivo no existe (git log: `182635ee2b`, 2026-10-04). Reemplazado por el estado real: checklist silencioso vía `automations`, mapa en `docs/gateway-operations.md`.
- **Referencia a API legacy.** `cron(action: wake, ...)` → `automations(action: "wake", ...)` (la sintaxis vigente).
- **`nomic-embed-text` 768 dims → 1024 dims.** `docs/SETUP.md` decía que la búsqueda semántica usa embeddings de 768 dims; los scripts usan `qwen3-embedding:0.6b` (1024 dims). El `768` de los scripts es `n_context`/truncado, no la dimensionalidad.
- **`scripts/session-start.sh` roto en `SETUP.md`** → `skills/session-lifecycle/scripts/session-start.sh`.

### Changed
- **Bloques de modelo duplicados colapsados.** `AGENTS.md` tenía DOS bloques MANAGED con el mismo contenido (`model-triple` y `model-operativo`). Se eliminó `model-triple` de `AGENTS.md`; queda un único bloque (`model-operativo`). `managed-blocks.py`: entrada `model-triple` de `AGENTS.md` removida del REGISTRY. `docs/SETUP.md` conserva su `model-triple` (mide los modelos primario/auxiliar/alternativo, ejes distintos).
- **`AGENTS.md`: "Modelos y razonamiento" fuera de `Git & Commits`.** Esa sección y "Skills Mirror & Públicas" colgaban de `Git & Commits` sin ser git. Modelos pasó a `## 3. Ingeniería`; el bloque de skills públicas (archivado 2026-09-28) se comprimió a un párrafo con puntero al detalle.
- **Política de modelos unificada.** `AGENTS.md` ahora cita **ADR-090** como fuente de modelo+thinking y explicita que supersede ADR-053 y las secciones de modelo/thinking de ADR-040. `docs/SETUP.md` y `docs/AGENTS-DETALLE.md` marcaron ADR-040 como histórico y apuntan a ADR-090.
- **Red Lines y "External vs Internal" en español.** El propio archivo declara que el workspace privado va en español; eran las últimas líneas en inglés.
- **`type(#issue)` sin issue definido.** Se aclaró: sin ticket, `type: description`.
- **Formato `type(#issue)`:** documentado el caso sin issue asociado.
- **Fechas de cierre** de `AGENTS.md` y `docs/SETUP.md` actualizadas al 2026-10-06.

### Added
- **`AGENTS.md`: margen recuperado.** Bajó de 19.542 a ~18.955 chars (límite bootstrap 20K): el colapso de bloques y la compresión de la receta de skills devolvieron holgura.

### Fixed (seed)
- **`managed-blocks.py` DEFAULTS.** `thinking_default: high` → `off` (ADR-090) y `model_by_agent` alineado al ADR-090 (antes tenía la distribución pre-cata de 2026-10-05: `planner minimax-m3`, `dev/ops glm-5.3-flash`). Es semilla: la DB ya estaba correcta; faltaba el fallback.
- **`tests/python/test_managed_blocks.py`** actualizado al nuevo default (`thinking_default == "off"`).

### Verified
- `managed-blocks.py apply` idempotente (4 bloques "al dia"); `pytest` no corre en esta máquina (no instalado), bats sí.
- Gates del pre-commit en verde: `check-refs` (489 rutas), `check-adr-integrity` (91 ADRs), `check-pipeline-enforcement` (pacto A/B consistente), `check-agent-skill-boundary`, `check-content-dirs`.
- `AGENTS.md`: bloques MANAGED restantes = `model-operativo` y `pipeline-ab`.

## [2026-10-06] - Cierre de sesion con HANDOFF del proyecto + plantilla del informe

### Added
- **`scripts/session-handoff.py`:** genera/actualiza el `HANDOFF.md` del proyecto en curso (o del workspace) al cerrar sesion. Destino: `~/projects/<slug>/.knowledge/HANDOFF.md` (ADR-075); para el sistema, `<workspace>/.knowledge/HANDOFF.md`. Deriva el HANDOFF del informe de cierre (resumen + estado + proximos pasos + decisiones + archivos tocados). Normaliza guiones largos.
- **`memory/_templates/session-close.md`:** plantilla del informe detallado de cierre de sesion (el formato de `memory/YYYY-MM-DD.md` que Gonzo pidio registrar).

### Changed
- **`skills/session-lifecycle/scripts/session-end.sh`:** reescrito. Acepta `--status`, `--next-steps`, `--decisions`; el HANDOFF lo genera `session-handoff.py` en el destino correcto (el bloque viejo apuntaba a `projects/<slug>/.knowledge` y quedo obsoleto con ADR-075). Ahora el cierre deja **dos entregables**: informe en `memory/` + HANDOFF del proyecto.
- **`skills/session-lifecycle/SKILL.md`** y **`AGENTS.md`:** documentado el doble entregable y que **"guardar sesion" y "cerrar sesion" son el mismo disparador**.
- **`memory/README.md`:** plantilla `session-close.md` registrada.

### Verified
- `session-end.sh` probado end-to-end: genera HANDOFF del workspace y escribe el informe en la DB.

## [2026-10-06] - Pagos: Stripe como proveedor unico reconocido (ADR-042 superseded de nuevo)

### Changed
- **`docs/adr/ADR-042`:** reescrito y **renombrado** a `ADR-042-stripe-pagos.md` (el slug ya no dice `mercado-pago`). **Stripe es el proveedor de pagos unico reconocido del ecosistema**, sea o no un proyecto sobre Lovable. Mercado Pago queda **fuera como intencion** (no se borra su existencia ni el trabajo previo; deja de figurar como opcion prevista). No se reconocen otros proveedores. Supersede la version intermedia de la misma fecha ("eleccion por proyecto") y la original ("Mercado Pago obligatorio").
- **`docs/adr/README.md`:** fila 042 actualizada al titulo nuevo + slug nuevo.
- **`MEMORY.md`, `AGENTS.md`:** regla de pagos simplificada a "Stripe es el proveedor unico".
- **`docs/adr/ADR-091`:** punto 3 de la decision alineado (Stripe deja de ser "excepcion"; es el proveedor reconocido).
- **`docs/APUESTAS.md`:** nota de SoporteML ajustada.
- **DB (`memory/memory.db`, tabla `learnings`):** leccion durable agregada.

### Verified
- `check-adr-integrity.py` (91 ADRs), `check-refs.py`: OK. `git mv` conserva la historia del archivo.

## [2026-10-06] - SoporteML v4 cerrado; el producto sigue por la version funcional de Lovable con cobro por Stripe

### Added
- **`docs/adr/ADR-091-soporteml-v4-cierre-stripe.md`:** cierra SoporteML v4 (supera el greenfield de ADR-068) y registra que el producto sigue por la version funcional de Lovable (v1), ahora con **cobro por Stripe** habilitado en Argentina. Decision de alcance cerrada: **la version se queda en Lovable** (no migra a stack propio); sin pendientes abiertos. Indice `docs/adr/README.md` actualizado.

### Changed
- **`docs/adr/ADR-042`:** reescrito. Deja de ser "Mercado Pago obligatorio, Stripe por excepcion": ahora **el proveedor se elige por proyecto y se justifica**. Lovable -> Stripe (unica integracion de la plataforma); fuera de Lovable, Mercado Pago es opcion fuerte (no unica) y Stripe tambien es valido. La regla deja de limitar Stripe.
- **`docs/adr/ADR-091`:** la clausula de pagos pasa de "excepcion" a "opcion natural del entorno (Lovable)".
- **`docs/adr/ADR-042` (previo, misma fecha):** titulo/estado ajustados; nota de que Argentina ya opera con Stripe.
- **`MEMORY.md`:** entrada de SoporteML reescrita (v4 cerrado; sigue por Lovable v1 con Stripe); regla de pagos actualizada (eleccion por proyecto).
- **`AGENTS.md`:** regla de pagos ajustada (eleccion por proyecto; Lovable -> Stripe).
- **`docs/APUESTAS.md`:** apuesta 2 pasa de `soporteml-v4` a `soporteml` (version funcional de Lovable) con Stripe operativo.
- **`docs/NORTH.md`**, **`docs/ROADMAP.md`**, **`memory/user-profile.md`:** referencias a `soporteml-v4` actualizadas al estado nuevo.
- **DB (`memory/memory.db`, tabla `learnings`):** leccion durable agregada (categoria `proyectos`).

### Verified
- `check-adr-integrity.py` (91 ADRs), `check-refs.py`: OK.
- El cambio a Stripe ya asomaba en superficies de CV (2026-10-01) sin haberse propagado a las fuentes durables; este ADR cierra ese hueco.

## [2026-10-06] - Bootstrap bajo cap: ROADMAP y NORTH reconstruidos, AGENTS/MEMORY/USER trimados

### Fixed
- **Bootstrap truncado (regresión):** `AGENTS.md` (20.656), `MEMORY.md` (24.017) y `USER.md` (4.582) estaban **sobre su cap de inyección** (20.000 / 20.000 / 4.000 fijo) y se descartaba contenido en silencio en cada arranque. Ahora: `AGENTS.md` 19.041, `MEMORY.md` 14.062, `USER.md` 3.976. `SOUL.md` e `IDENTITY.md` ya estaban OK.
- **`USER.md`:** corregido doble guion (`--`) que debía ser lista; compactado sin perder reglas.

### Changed
- **`docs/ROADMAP.md`:** reconstruido desde cero contra fuentes reales. Se quitó la hipótesis ya refutada de "inestabilidad del gateway" (no hay reinicios espontáneos; el problema real era el truncado del bootstrap) y el falso verde de búsqueda laboral ("oferta aceptada" que nunca existió). Se agregó la capa *Ecosistema* (análisis de 20 repos, 2026-10-01) y el item 0.1 *Integridad del bootstrap*.
- **`docs/NORTH.md`:** reconstruido. Ubicaciones de proyectos corregidas a `~/projects/` (ADR-075), Horizonte 0 rearmado sobre el estado real (sin procesos abiertos), constelación actualizada (`kanam-onwheels`, `kanam-spec`, `ollama-visor`, etc.) y orden de apuestas de `docs/APUESTAS.md`.
- **`MEMORY.md`:** destilado. Historial de decisiones de modelo/engine movido a `memory/model-history.md`; entradas de proyecto comprimidas a lo vigente con puntero a `~/projects/<slug>/.knowledge/`; agregado `kanam-onwheels`; corregida la regla de modelos (hoy ADR-090, no ADR-053).
- **`AGENTS.md`:** comprimidas las secciones de Frontera de roles, Feedback en PRs y sandbox sin perder reglas; bloque de razonamiento actualizado a ADR-090.

### Added
- **`memory/model-history.md`:** archivo del historial de decisiones de motor/modelo (2026-08 a 2026-09), movido fuera de `MEMORY.md` para bajar el bootstrap.

### Verified
- `wc -c` de los 5 archivos de bootstrap: los tres grandes dentro de cap.
- `managed-blocks.py check`: sin drift. `check-refs.py` (147 rutas), `check-content-dirs.py` (10), `check-adr-integrity.py` (90 ADRs): OK.

## [2026-10-06] - Cata persistida y "thinking leakage" re-diagnosticado como artefacto del CLI

### Changed
- **`sandbox/model-cata-2026-10-06/`:** la cata de modelos (6 modelos × 6 roles × 4 escenarios, 144 corridas + 4 evaluaciones cross) se copió de `/tmp` (efímero) al workspace. `sandbox/` está gitignored: sobrevive reboot sin inflar el repo.
- **`docs/adr/ADR-090-pensamiento-nivel-configuracion.md`:** corregida la narrativa del "thinking leakage". No era defecto del harness de producción sino **artefacto del runner de la cata** (`ollama run`, que imprime el thinking a stdout mezclado con la respuesta).

### Added
- **`sandbox/model-cata-2026-10-06/run-one-api.py`:** runner de cata corregido. Llama a `POST /api/chat` y guarda el entregable en `raw_output` y el razonamiento en `thinking_output`, en campos separados. Reemplaza el `run-one.sh`/`run-one-safe.py` basados en CLI.
- **`sandbox/model-cata-2026-10-06/verify-no-leakage.py`:** sonda que verifica la separación thinking/content.

### Verified
- **Sonda `verify-no-leakage.py`:** 6 modelos × {think off, think high} → **0 fugas**. El campo `thinking` de la API llega poblado y separado del `content`; con `think:false` el thinking viene vacío.
- **Claude Code headless** (`claude -p --model deepseek-v4.1-flash:cloud`): output limpio, sin fuga. Es el motor estándar del pipeline A/B (ADR-049) y ya separaba el razonamiento.
- **Conclusión:** no había bug de producción que arreglar. Lo útil era persistir la evidencia y corregir la narrativa. El fix real para futuras catas es usar la API, no el CLI.

---

## [2026-10-06] - ADR-090 corregido: decisión de modelos por rol vs estado real del runtime

### Changed
- **`docs/adr/ADR-090-pensamiento-nivel-configuracion.md`:** reescrito. El documento estaba desactualizado y contenía una **ref cruzada rota** (citaba `ADR-210`, que no existe) que dejaba el corpus ADR desreconciliado (`check-adr-integrity.py` fallaba). Ahora:
  - Registra la decisión de thinking por agente y la asignación de modelos por rol surgida de la cata 2026-10-06.
  - Separa explícitamente **decisión** de **estado de implementación**: el runtime (`openclaw.json`) no coincide con la decisión en 6 de 8 agentes.
  - Reemplaza context windows estimados por contextos **medidos** con `ollama show` (gpt-oss 128k, deepseek 1M, nemotron 256k, gemma4 256k, minimax 500k, glm-5.3 1M).
  - Documenta los límites reales: cata con defecto de harness, n=1 por celda, evaluadores con sesgo estructural, re-verificación post-fix sin completar.
- **`docs/adr/README.md`:** título del índice alineado al nuevo alcance del ADR.
- **`ADR-090-*.md.backup`:** a la papelera (redundante con git).

### Notes
- **Por qué:** el ADR afirmaba cambios de modelo que nunca se aplicaron al runtime; un ADR que miente es peor que no tenerlo (regla de corpus ADR + README).
- **Verificación:** `check-adr-integrity.py` → `OK: 90 ADRs, todos indexados, sin duplicados ni refs rotas`.

### Changed (corrección 2026-10-06, decisión de Gonzo)
- **Decisión de modelos corregida:** `main` y `kanam-mind` NO van a nemotron-3-super ("se pierde y quiere resolver en lugar de conversar" en asientos de orquestación/diálogo); quedan en `deepseek-v4.1-flash:cloud`. El resto de la asignación por rol se mantiene.
- **Thinking corregido:** los tres de juicio (`kanam-critic`, `kanam-auditor`, `kanam-planner`) bajan de `high` a `low`; los cinco de ejecución (`main`, `kanam-dev`, `kanam-mind`, `kanam-ops`, `kanam-studio`) pasan a `off` explícito. Default global `off`.
- **Runtime aplicado y verificado:** los 8 agentes en `~/.openclaw/openclaw.json` coinciden con la decisión (model.primary, fallbacks, thinkingDefault), vía el tool `openclaw`, sin editar el JSON a mano.
- **Bloques gestionados regenerados:** corregido el uso de `managed-blocks.py` (el bloque de AGENTS.md lee `model_by_agent`, no `model.triple`); `AGENTS.md` y `docs/SETUP.md` alineados con el runtime.
- **ADR-090:** decisión y estado de implementación actualizados; se documenta que cambiar el modelo de `main` desde una sesión que corre sobre `main` bloquea el tool (`prepared model runtime plugin generation was superseded`) y se resuelve con restart.

---

### Changed
- **`agents/kanam-dev/scripts/validate-spec.sh`:** deja de ser un validador propio y **delega** en el validador compartido de la skill (`~/.agents/skills/spec-driven-development/scripts/validate-spec.sh`). Pasa a recibir el directorio de specs como argumento (default `./specs`) y a ejecutar el compartido vía `exec`. Fallback explícito con `exit 2` si el compartido no existe.

### Notes
- **Por qué:** la versión propia chequeaba **forma, no sustancia** (daba `exit 0` sobre una spec con el Brief vacío, sin Status y con placeholders de plantilla sin completar). Dos validadores con criterios distintos es peor que uno malo: el mismo archivo pasa en uno y falla en el otro, y no se sabe a cuál creer.
- **Verificación:** el script delega y corre (`bash agents/kanam-dev/scripts/validate-spec.sh <dir>`); el original queda recuperable en `git HEAD` y su copia `.bak-share-20261005` es redundante con git (se retira).
- **Origen:** cambio de una sesión previa del día quedó sin commitear en el árbol (mtime 12:24); se documenta el rationale y se registra acá.
- Sin commit: el Core verifica primero (ADR-078).

---

## [2026-10-05] - Skill nueva `design-direction`: dirección de arte antes de escribir código

### Added
- **`agents/kanam-dev/skills/design-direction/`** (kanam-dev 34 → 35): cubre el hueco entre decidir qué construir (spec, `openspec-pattern`) y cómo implementarlo (`frontend-ui-engineering`). Cuatro bloques:
  - Las 4 preguntas antes de codear (propósito, tono, restricciones, diferenciación). Regla: la clave es la **intencionalidad**, no la intensidad - un minimalismo refinado y un maximalista bold son igualmente válidos si son decisiones.
  - La distinción de contexto: **herramienta funcional** (dashboard, form, tabla densa: la neutralidad ES la decisión, fuentes de sistema/Inter correctas) vs **pieza memorable** (landing, portfolio, marca: la neutralidad es pereza, pareja display/body). Primero preguntar qué es, después elegir tipografía.
  - El orden de las 4 fases de pensamiento: layout → tema → animación → código, enlazado a `incremental-implementation` (el cómo) y `frontend-ui-engineering` (la ejecución).
  - La regla de intencionalidad: "la ausencia de look malo no es un look bueno" - evitar el look IA no alcanza, hay que comprometerse con una dirección.
  - Anclaje al stack real: tokens semánticos (`--primary`, `--muted`, `--border`), Lucide para iconografía (nunca emojis), CSS Modules como vía de estilado, loop cerrado con `a11y-at-validation`.
- Origen: `docs/specs/design-direction-spec.md` (análisis de 3 skills externas de diseño traidas por Gonzo). Nada se importó ni instaló: el criterio se reescribió para este workspace y su stack.

### Changed
- **`frontend-ui-engineering/SKILL.md`:** 1 sola línea de contexto al inicio de "Design Thinking Before Code": asume dirección existente y deriva UI sin dirección a `design-direction`. Nada más cambió en esa skill.
- **`SKILLS-INDEX.md`:** fila nueva en §3.2 y conteo de kanam-dev 34 → 35 (línea 24).

### Notes
- **Grupo Build, no Define:** no es definición de requerimientos (eso es Define); su output alimenta directamente a `frontend-ui-engineering` dentro del mismo ciclo, así que la fila va inmediatamente antes de esa skill.
- **Verificación real:** `check-agent-skill-boundary.py` OK, `check-refs.py` OK (145 rutas), `test-skills.sh` completo OK (80 SKILL.md: frontmatter, em dash, refs, links), `check_em_dash.py` OK sobre los 4 archivos, y grep del stack de las skills externas: 1 línea única (rechazo explícito de Tailwind/Shadcn/Radix, con la excepción del spec §6.3: rechazo, no adopción; 0 líneas de Flowbite/cdn/unpkg).
- Sin commit: el Core verifica primero (ADR-078).
- **Heredado, fuera de alcance:** la fila "Total activas" (78) ya traía una inconsistencia antes de este cambio (la suma de los encabezados daba 79): re-medir con `openclaw skills list` en la próxima pasada completa. Los follow-ups del spec §9 quedan abiertos: ADR de Radix/shadcn, WCAG 2.1 vs 2.2, regla transform/opacity.

---

## [2026-10-05] - Rediseño de modelos: distribución por agente (2026-10-05)

### Changed
- **`openclaw.json`:** limpieza completa de modelos - defaults (primary `ollama/glm-5.3-flash:cloud`, utilityModel y `defaults.models` solo glm) + 8 agentes con primary/fallbacks explícitos:
  - main glm-5.3-flash:cloud · dev deepseek-v4.1-flash:cloud · auditor nemotron-3-super:cloud · critic gpt-oss:120b-cloud · planner minimax-m3:cloud · mind deepseek-v4.1-flash:cloud · ops glm-5.3-flash:cloud · studio gemma4:cloud.
  - Fallbacks: glm-5.3-flash universal; ops/studio caen a glm4:9b local.
  - Eliminados ~27 fallbacks huérfanos del agente `main` (locales inexistentes, rutas hf.co/...) - causa del "configured (not in catalog)".

### Changed (docs)
- **`AGENTS.md`:** sección de modelos operativos + bloque managed `model-triple` actualizados a la distribución por agente (supersede ADR-053).
- **`docs/adr/ADR-053`:** sección "Actualización 2026-10-05" que registra el supersede sin borrar el histórico.
- **Pipeline A/B (sin cambios, verificado):** ADR-077 + skill `agent-orchestration-pipeline` ya definían la pareja asimétrica vigente (A `gpt-oss:120b-cloud` escribe / B `deepseek-v4.1-flash:cloud` 1M revisa).

### Notes
- Backup pre-cambio: `~/.openclaw/openclaw.json.bak-20261005-models`.
- Probe de fallbacks studio: `glm4:9b` aprobado (7.9s local); DavidAU GLM-4.7 mod descartado (29GB, 62% CPU, hangs).
- Rev. 01:22 - canje deepseek/glm: main/defaults pasan a `deepseek-v4.1-flash:cloud` (chat común, 6.5s vs 19.8s; glm consume muchos más recursos); dev y ops toman `glm-5.3-flash:cloud`. Fallbacks: deepseek para dev/ops/auditor, glm para main/planner. AGENTS.md y ADR-053 alineados.
- **Cata por rol (ADR-087):** 7 roles x 2 modelos + probe especifico de auditor. La distribucion queda **validada** (4 roles con ganador claro, 3 empates). `nemotron-3-ultra` descartado para auditor (550B, mismo contexto 256k, mas lento y perdio en calidad vs super). utilityModel fijado en `gemma4:cloud` (el mas liviano: 0.5s / 12 tokens en la cata; tareas cortas como titulos, narracion y recaps); defaults.models alineado; drift re-baselineado.
- Evidencia de latencia previa (cata 2026-09-28): deepseek 6.5s · gemma4 1.9s · glm-5.3-flash 19.8s.

---

## [2026-10-01] - Ecosistema OpenClaw: ronda de análisis de 29 repos + criterios de filtrado

### Added
- **`docs/ecosystem/`** (carpeta nueva, 3 capas):
  - **`DECISIONS.md`** - consolidado ejecutivo. Candidatos reales, solapamientos a resolver, patrones a adoptar sin instalar, descartes con razón, y movimiento recomendado.
  - **`crew-resources.md`** - ficha de detalle de los 29 repos analizados (en dos tandas).
  - **`solutions-catalog.md`** - catálogo de casos de uso por problema.
- **Regla dura: cripto/Web3 = fuera** (registrada en `USER.md` y en `crew-resources.md`).

### Changed
- **`USER.md`:** nueva preferencia de fondo - 🚫 cripto/Web3 no se hace (blockchain, tokens, wallets, DeFi, NFT, chains, mercados on-chain).

### Notes
- **Método:** cada repo se lee en dos capas - *implementación* (¿lo instalamos?) y *diseño* (¿qué aprendemos?). Descartar el repo no descarta la lección.
- **Hallazgo principal (1ra tanda):** el core de OpenClaw está más completo de lo que pensábamos. Dos repos (MCP adapter y MCP server) resultaron **redundantes**: el core ya expone y consume MCP nativo (`openclaw mcp add` / `openclaw mcp serve`). Regla nueva: **verificar qué hace el core antes de sumar tooling externo.**
- **Hallazgo transversal (1ra tanda):** tres candidatos distintos (Claw Orchestrator, MemoV, ClawSec) resuelven el mismo problema de fondo - trazar, verificar y proteger lo que hizo el agente. Es el hueco real del setup.
- **2da tanda (9 repos):** context-sync (MCP, memoria de codebase), Open Amnesia (memoria desde trazas crudas, local-first), planning-with-files (planificación persistente). Descartados: Supermemory (cloud - el descarte más claro), y cinco dashboards de tercero que compiten con el Control UI (vibeclaw, Studio, ClawDeck, Autensa, mission-control rdsthomas).
- **Hallazgo transversal (2da tanda):** el ecosistema **no tiene formato canónico de memoria** - cinco bases SQLite paralelas contadas en dos tandas, cada herramienta la suya. **El que defina un formato interoperable gana**; conviene adoptar el **formato** antes que la herramienta.
- **Patrón repetido (2da tanda), ya del ecosistema y no anécdota:** memoria por **hooks de turno** (4 repos), comando **`doctor`** (4 repos), **ledger/checkpoint de agente** (3 repos).
- **Aporte más transferible de la 2da tanda:** `determinism-before-LLM` (Open Amnesia) - normalizar, filtrar y deduplicar **antes** de cualquier paso de LLM. *"Data consistency beats prompt cleverness."*
- **Hallazgo que nos toca directo:** una **sesión compartida entre tareas degrada al agente hasta atascarlo** (bug documentado de Autensa v2.5.0). Confirma nuestra sesión-por-tarea. Y nuestro backlog vive en `memory.db` y **no es visible** (deuda real, §2.5 de DECISIONS).
- **Profundización (2026-10-01, tarde):** se abrieron los **5 conjuntos que habían quedado solo como directorio** en la primera parte (deuda reconocida: se catalogó el repo, no el ítem). Hallazgos:
  - **`design-audit`** (jdrhyne) - rol auditor de diseño; sus 8 reglas destilan el criterio que no teníamos. **Precondición: el design system (no lo tenemos).**
  - **`knowledge-graph`** (jdrhyne) - memoria **sin base de datos nueva** (2 archivos de texto, cero infraestructura, reconoce `memory/YYYY-MM-DD.md` y `MEMORY.md`). **Redefine la decisión de §2.1: quizá no haya que elegir motor, sino agregar esta capa.**
  - **Suite `aeon`** (Bankr) - **el hueco más grande de las dos rondas:** ciclo de vida de skills (auditar/evaluar/reparar/evolucionar). Tenemos `skill_workshop` para crear, nada más.
  - **Cluster de diseño** (VoltAgent) - `anti-slop-design` (previene la estética genérica) + `kj-ui-ux-pro-max` (**genera los tokens que `design-audit` necesita**). `axe-devtools` descartado por costo.
  - **Academic Multi-Agent System** (13 roles) - el patrón Factory ya construido; el **`critic`** (rúbrica SHARP) es el rol de gusto adversarial que nos falta.
- **`DECISIONS.md` ampliado:** nuevas secciones §2.6 (ciclo de vida de skills - hueco propio), §2.7 (los dos roles ausentes), §2.8 (pipeline de diseño con orden). Movimiento recomendado reordenado: **el design system pasó a ser el paso 0**.
- **Regla de oro de la profundización:** *lo que falta no es una herramienta más, son tres roles y un sistema de tokens.*
- **Pendiente abierto:** decidir el eje de memoria (`DECISIONS.md` §2.1) - ahora con **seis** candidatos, no cuatro. Es lo que desbloquea el resto.

### Fixed
- **`DECISIONS.md` §2.4 (error propio corregido):** `clawdeck` estaba listado como alternativa de **observabilidad** a Crabwalk, cuando es un **Kanban** (no un monitor). Se movió a §2.5 ("el backlog como objeto visible").

---

## [2026-09-30] - ADR-086: el embudo de entrada conversacional (Módulo 1 de OpenClaw Use Cases)

### Added
- **`docs/adr/ADR-086-embudo-de-entrada-conversacional.md`:** marco de referencia para el comportamiento del agente frente a canales externos. Fija cinco patrones secuenciales - triaje determinista antes de razonar (L1), especialización por Persona (L2), borradores con rationale en vez de envío directo (L3), escalación como entrega de mando y no como alerta (L4), y límites de contexto con filtro determinista previo al semántico (L5).
- **3 learnings nuevos en `memory.db`:** el marco de los 5 patrones (`pipeline-agentes`), la equivalencia del TTL de la L5 con el heartbeat y los scripts de sesión (`pipeline-agentes`), y el método de estudio por módulo con cierre en Laboratorio de Activos (`metodologia`). Exportados a `docs/learnings/`.
- **`studies/openclaw-use-cases/`:** registro del curso (índice de progreso + L01-L05), en español.

### Notes
- **El ADR nombra una práctica que ya existía:** L2 = los agentes `kanam-dev/ops/mind/studio` y la frontera de roles (ADR-083); L4 = el handoff al humano; L5 = heartbeat + registros de sesión (ADR-084). El aporte no es infraestructura nueva sino el marco que explica por qué esas piezas están separadas.
- **Regla accionable:** el filtro por identidad es determinista y va ANTES de cualquier búsqueda semántica. El orden inverso es una fuga de datos.
- **Fuera de alcance:** el agente no tiene acceso a las cuentas personales de Gonzo (Gmail, iCloud). El ADR describe seguridad para cuando esos conectores existan, no los habilita.
- **Método acordado con Gonzo:** el estudio se procesa por módulo, y la skill del propio Laboratorio de Activos se escribirá al final, después de practicarlo al menos una vez.

---



### Added
- **Supabase conectado y migrado:** proyecto `lpvtjipxzxpxygeobixn.supabase.co` (Postgres 17.6) con **7 migraciones aplicadas y verificadas**: 17 tablas, **0 sin RLS**, 36 policies, extension `vector`, y las 3 funciones publicas. Las migraciones quedan registradas en `supabase_migrations.schema_migrations`, asi que un `supabase db push` futuro no las repite.
- **`scripts/db-apply.mjs`:** dry-run real (aplica dentro de una transaccion y hace ROLLBACK) y `--apply`. El dry-run prueba que las migraciones corren limpias contra el proyecto real **sin dejar rastro** antes de aplicarlas.
- **`scripts/check-env.mjs`:** reporta que variables faltan o estan mal formadas **sin imprimir nunca un valor**, y marca riesgo si un secreto lleva prefijo `NEXT_PUBLIC_`.
- **Guarda del seed (ADR-069):** `supabase/seed/dev.sql` es data de PRUEBA y ahora **se niega a correr** sin un opt-in explicito (`onwheels.allow_seed=yes`). Verificado en ambos sentidos. El seed no se aplico a Supabase: los datos de prueba no comparten base con un proyecto real.
- **Check 14** en `tests/sql/invariants.sql`: guarda de regresion para la fuga de policies. El suite paso de 13 a **14/14 checks**.

### Fixed
- **FUGA DE SEGURIDAD en el catalogo compartido, encontrada verificando contra el proyecto real (no por un test que fallara).** Las policies eran `to authenticated using (state <> 'discarded')` sobre `spec` y `using (true)` sobre `model`: **cualquier usuario autenticado podia leer las specs scrapeadas SIN aprobar y los modelos en borrador**. Contradecia `docs/data-model.md` seccion 9 y dejaba sin sustento la invariante I9 (el corazon del producto: nada se publica sin aprobacion humana).
  - **Demostrado antes de arreglar:** como usuario autenticado cualquiera, 1 spec propuesta y 1 modelo en borrador visibles.
  - **Despues del arreglo:** 0 y 0, con las 23 specs aprobadas y los 5 modelos publicados todavia legibles.
  - La concesionaria **si** necesita ver el modelo que esta enriqueciendo, asi que la policy de `model` ahora permite publicado **o** el borrador alcanzado por su propio `enrichment_run` (el esquema ya tenia el dato para responderlo).
- **Un artefacto de redaccion en `.env.development.local`:** la herramienta de escritura redacto la contrasena y dejo un `***` literal, lo que tumbo el catalogo de desarrollo. Detectado probando la pagina en vivo. Corregido.

### Notes
- **Totales verificados:** 111 tests, lint, typecheck y build en verde; `verify-schema.sh` 14/14.
- **La base de Supabase esta vacia a proposito.** Vacia no es roto: el catalogo en modo produccion muestra el estado vacio honesto, sin error.
- **Leccion del hallazgo:** los tests cubrian lo que se habia pensado probar. La fuga vivia en una policy que nadie habia probado nunca. Verificar el esquema real encontro lo que el suite no buscaba.
- **IPv6:** el host directo de la base tiene solo registro AAAA. Funciona desde esta maquina; el Session Pooler queda como alternativa documentada.

---


### Changed
- **El proyecto `retail-vehiculos` pasa a llamarse `Kanam OnWheels`.** Nombre definido por Gonzo; es **temporal**: el sitio publico tomara el nombre del cliente. Slug `kanam-onwheels`, ruta `~/projects/kanam-onwheels/`. Registrado en **`ADR-0009`** del proyecto. El nombre del producto no se filtra a la marca visible del concesionario.
- **`MEMORY.md`:** la entrada del proyecto refleja las cuatro etapas cerradas mas el estado real del desarrollo, el stack decidido y los bloqueos.

### Added
- **Repo privado `github.com/gonzoblasco/kanam-onwheels`** creado y pusheado (57 archivos, `main` sincronizado). Auditoria previa al push: **cero secretos** en el arbol remoto (`.env.local` ignorado por `.gitignore`, `.knowledge/` excluido por `.git/info/exclude`). Es el repo que Supabase pide para el setup.
- **Investigacion del MCP de Supabase** (paquete oficial `@supabase/mcp-server-supabase`, endpoint `https://mcp.supabase.com/mcp` con OAuth): recomendado para administrar tablas, config y consultas, **con `read_only=true` y `project_ref`** fijado en la URL para acotar el alcance. Los secretos se cargan por el prompt enmascarado, nunca en el chat.
- **Camino de migraciones definido:** `supabase link --project-ref` + `supabase db push --dry-run` (revision) + `supabase db push` (aplicacion). El CLI `supabase` 2.118 ya existe via `npx`; no hace falta el MCP para las migraciones y es menos superficie de riesgo.
- **Desarrollo de Fase 1 iniciado, con evidencia en cada pieza:**
  - **Esquema de base:** 6 migraciones (tenancy, catalogo compartido, stock, ingesta, conocimiento/chat/publico, y la unificacion del estado de ficha). **13/13 checks de invariantes en verde contra un Postgres real desde cero** (`scripts/verify-schema.sh`, contenedor descartable).
  - **Base de desarrollo persistente:** `scripts/dev-db.sh` (Docker + volumen, puerto 55433) con seed realista en `supabase/seed/dev.sql`.
  - **Nucleo de enriquecimiento:** normalizacion de unidades (kW→hp metrico, cm→mm, lb→kg, y los separadores decimales es/en), registro de extractores por dominio (Pierer, BRP, Segway, generico) y orquestador con **errores tipados** (nunca lista vacia como exito).
  - **Catalogo publico:** server-rendered (indexable, con Open Graph por unidad), filtros que viven en la URL, es-AR, estados vacios honestos y 404.
- **`scripts/visual-check.mjs`:** validacion visual con Playwright sobre el servidor de desarrollo (el navegador del gateway bloquea localhost por politica SSRF). 12 capturas, dos viewports.

### Fixed
- **Dos fuentes de verdad para el estado de la ficha tecnica.** La ficha de unidad calculaba "parcial/completa" con un umbral propio del componente, mientras el catalogo lo derivaba en SQL. Encontrado por **revision visual**. Se extrajo `model_spec_state()`: **la base es la unica definicion**.
- **Un bug real de unidades, encontrado por los tests:** el normalizador devolvia la unidad de origen en vez de la canonica (`96 cm` no llegaba a `960 mm`), lo que habria roto el filtro por cilindrada en silencio.

### Notes
- **Totales verificados:** 111 tests (6 archivos), typecheck, lint y build en verde.
- **Bloqueos reales declarados:** el panel necesita Supabase Auth; el chat necesita proveedor de embeddings y clave de modelo. Ninguno esta contratado, asi que esas dos piezas no se reportan como terminadas.
- Los ADRs del proyecto viven en `docs/adr/` del repo del proyecto, no en el workspace (ADR-067).

---

## [2026-09-29] - ADR-083: el CORE orquesta y no escribe codigo (la regla pasa a estar verificada)

### Added
- **`scripts/check-agent-skill-boundary.py` + suite (6 tests):** verifica la frontera entre el arbol del CORE y los arboles de rol. Caza tres cosas: una skill del ciclo de desarrollo en `skills/`, una skill en dos arboles, y el ciclo SDD incompleto en su rol. Probado **en negativo** (sembrada `skills/hermes-builder/SKILL.md`, el hook aborta con exit 1) y **en positivo**. Corre en el pre-commit.
- **Regla en `AGENTS.md`:** "Frontera de roles: CORE no escribe codigo". Va al bootstrap porque es el unico archivo que el CORE lee siempre - antes vivia solo en `SKILLS-INDEX.md` y en ADR-073/074, que son documentacion y no contexto.

### Changed
- **El ciclo SDD (9 skills `hermes-*`) se movio de `skills/` a `agents/kanam-dev/skills/`.** Estaba en el arbol del CORE, asi que el CORE veia el playbook de ingenieria - `hermes-builder` dice "implementation. Writes the change's code" - y lo ejecuto durante una sesion entera de `kanam-onwheels`. **La separacion de arboles ES el enforcement: lo que un agente ve, un agente lo ejecuta.** El CORE conserva `sdd-agent-loop`, el orquestador.
- **Totales del indice re-medidos:** Core 36 -> 27, kanam-dev 25 -> 34. El total sigue en 78 (fueron movimientos, no altas ni bajas).
- **`SKILLS-INDEX.md` §2.4:** la verificacion pasa de `dispatch-validation.sh` (voluntario, sin test, nunca invocado) al check automatico.

### Fixed
- **El check nuevo nacio con el fallo que persigue:** su primera conexion usaba el disparador de `skills/|scripts/`, que **no matchea** `agents/<rol>/skills/` - justo donde se viola la frontera. Sembrar la violacion y ver que el hook salia 0 lo destapo. La conexion es parte del enforcement, no un detalle de instalacion.

### Notes
- **Contexto:** el 2026-09-29 el CORE escribio migraciones SQL, el cliente de datos, el panel completo y un e2e de Playwright de `kanam-onwheels`. Gonzo pregunto por que no se usaba `kanam-dev`. La regla existia en tres lugares y nada la verificaba. Detalle en ADR-083.
- **Pendiente declarado:** la identidad git no distingue agentes (todos commitean como `gonzoblasco`), asi que el enforcement es previo (que ve cada agente), no forense. OpenClaw soporta `agents.entries.*.tools.github.gitAuthor`.
- **Ruteo por etapa:** el dueño natural de una etapa no siempre es DEV - discovery y research son de MIND. El discovery de `kanam-onwheels` lo hizo el CORE solo; MIND debia haber sido convocado.

---

## [2026-09-29] - retail-vehiculos: diseno cerrado (arquitectura, modelo de datos, dominio y 8 ADRs)

### Added
- **Etapa de diseno del proyecto `retail-vehiculos` cerrada.** Cuatro artefactos en `~/projects/retail-vehiculos/docs/`:
  - **`architecture.md`** (377 lineas): 8 decisiones, cada una con alternativa descartada y consecuencias; evaluacion de las 5 señales del disparador DDD; 16 invariantes de dominio, cada una con el test que falla al violarla; 6 fronteras de capacidad; 4 contratos de API; 9 riesgos con mitigacion; y tabla de trazabilidad specs ↔ diseno.
  - **`data-model.md`** (449 lineas): contrato del esquema. Dos mitades declaradas (catalogo compartido sin `company_id` vs operacion del local con `company_id`), las 3 transiciones que no se pueden expresar como constraint de fila, la superficie publica de solo 3 funciones, y la verificacion automatica de RLS.
  - **`CONTEXT.md`** (166 lineas): glosario autoritativo. 13 terminos con definicion afirmativa y sinonimos rechazados bajo `_Evitar_`, mas las fronteras entre capacidades.
  - **`adr/` con 8 ADRs** + indice: cada uno con las 5 secciones, tabla de alternativas descartadas y reversibilidad.

### Changed
- **`retail-vehiculos` cambio de stack respecto del discovery.** El frontend candidato era React + Vite (heredado de `soporteml`); el diseno lo reemplaza por **Next.js App Router** con motivo concreto: el catalogo publico tiene que ser **indexable** y una SPA entrega HTML vacio. El precedente no aplicaba porque `soporteml` es un panel privado detras de login. Registrado en `ADR-0001` (supersede `ADR-011` y `ADR-020` para este proyecto).
- **Specs reconciliadas con el diseno** (4 cambios, para que no queden dos verdades): SPEC-004 (edita su unidad, al catalogo compartido propone), SPEC-003 (`raw_value` ademas del normalizado), SPEC-002 (rate limit por sesion e IP), SPEC-005 (`company_id` denormalizado en el chunk).
- **`DISCOVERY.md` y `BRIEF.md` actualizados** en la seccion de stack y estado; `.knowledge/STATUS.md` y `HANDOFF.md` reflejan el cierre de la etapa.
- **`MEMORY.md`:** la entrada del proyecto pasa de "discovery cerrado" a las cuatro etapas cerradas, con el stack decidido y las decisiones centrales.

### Notes
- **Sin repo git todavia.** Los 8 ADRs viven en `docs/adr/` del proyecto, no en `docs/adr/` del workspace (ADR-067). El repo se inicializa al arrancar desarrollo.
- **Cero decisiones abiertas** para quien construya: lo que queda son detalles de implementacion.
- **Pieza genuinamente nueva del sistema:** el motor de scraping multi-marca (6 marcas, al menos 3 estructuras de sitio). Todo lo demas reutiliza patrones de `soporteml`.
- **Riesgo que sigue abierto:** que el sitio no se use. Es lo que le paso a las dos generaciones anteriores de sitio de concesionaria (`sportcars`, `pro-motors-docs`), construidas y borradas sin operacion.

---

## [2026-09-29] - retail-vehiculos: discovery, specs y knowledge de un proyecto nuevo

### Added
- **Proyecto `retail-vehiculos` en `~/projects/retail-vehiculos/`.** Sitio de un concesionario oficial multi-marca (KTM, Husqvarna, Can-Am, Sea-Doo, Ski-Doo, Segway) con catalogo publico, chatbot IA con RAG y alta de unidades con enriquecimiento desde la URL de la ficha oficial. Vive fuera del worktree (ADR-075); el workspace solo registra el puntero en `MEMORY.md`.
- **`.knowledge/` del proyecto** (no versionado por el workspace, es memoria del proyecto): `DISCOVERY.md` (problema, usuarios, 12 capacidades candidatas, prior art verificado, riesgos), `KNOWLEDGE.md` (negocio, dominio, decisiones, reutilizacion), `BRIEF.md`, `STATUS.md`, `HANDOFF.md`, y `specs/` con `SPEC-001..006` + `README.md`.
- **Seis specs con criterios verificables.** Cada una con `Acceptance Criteria`, `Edge Cases & Error Handling` y `Verification Plan` (las tres secciones que valida el checker de `kanam-spec`): catalogo publico, chatbot RAG, enriquecimiento desde URL, revision y aprobacion humana, base de conocimiento del local, y multi-tenancy con RLS.

### Notes
- **Prior art relevado con evidencia:** `sportcars` y `pro-motors-docs` fueron borrados el 2026-08-17; `motothrill` nunca existio como proyecto. No hay codigo de concesionaria que reutilizar, pero si un motor: `soporteml` v1 aporta RAG (`kb-search`), indexado (`kb-process-article`), multi-tenant con RLS y el patron de enriquecimiento (`enrich-product`, 352 lineas).
- **La pieza genuinamente nueva es el scraping multi-marca**, no el catalogo ni el chat.
- **Sin repo git todavia.** El proyecto se inicializa en la etapa de desarrollo; el ADR de stack corresponde a ese momento y va en el repo del proyecto, no en `docs/adr/` del workspace (ADR-067).
- **Discovery cerrado con 7 decisiones** tomadas por Gonzo (alcance multi-marca, multi-tenant, origen del dato, destino sin billing, autos fuera de Fase 1, Fase 1 = motos, origen del stock actual).
- **Pendiente tecnico detectado:** `kanam-spec-v2/server/index.mjs` no existe como archivo y `kanam-spec-nextgen` no esta en disco, asi que el flujo de specs por API (`spec-draft-creation`, `spec-discovery-creation`) no puede correr. Las specs se escribieron a mano con `docs/checklists/spec-template.md`.

---

## [2026-09-29] - SKILLS-INDEX.md reescrito de cero: índice canónico, no changelog

### Changed
- **`SKILLS-INDEX.md` reescrito.** El archivo acumulaba nueve bloques `Actualización <fecha>` que se contradecían entre sí y mezclaban tres cosas distintas: inventario, historial de mantenimiento y notas de consolidación. Los totales declarados en esos bloques (82, 81, 65, 63) nunca salieron del CLI y no reflejaban el set real. La estructura nueva es fija: (1) qué es el índice y cómo se cuenta, (2) metodología (dos árboles, dónde va una skill nueva, ciclo de vida, Core define vs delega, contrato del archivo), (3) inventario de las 78 skills activas por árbol y por fase, (4) retiradas, (5) herramientas de verificación.
- **Regla explícita: este archivo no lleva su propio changelog.** El historial de mantenimiento vive en `CHANGELOG.md` y en git; el índice es inventario. Era la causa de la repetición: cada cambio agregaba un bloque en vez de reemplazar.

### Fixed
- **Totales corregidos y medidos:** 78 activas (36 en `skills/` + 42 en `agents/*/skills/`: kanam-dev 25, kanam-mind 7, kanam-ops 4, kanam-studio 7), más 1 placeholder (`study-tracker`, `user-invocable: false`). Verificado contra el árbol en disco y contra `openclaw skills list --agent <id> --json` (filtro `source == "openclaw-workspace"`), que coincide: 36 + 25 + 7 + 4 + 7.
- **Los cinco árboles quedan completos:** antes faltaban filas de `skills/` en el índice (`compaction-domain-aware`, `complexity-driven-pipeline`, `engineering-governance`, `find-skills`, `self-improving-agent`, `superpowers`), mientras había secciones propias para skills de rol. Ahora cada árbol tiene su tabla y las 78 rutas resuelven.

### Notes
- **Verificado end-to-end:** `check-refs.py` default OK (144 rutas, +2 respecto de las 142 previas), `test-skills.sh` en verde, `check-adr-integrity.py` OK, y un diff de conjuntos entre los links del índice y las rutas reales: la única diferencia es `study-tracker`, que es el placeholder documentado a propósito.
- **Guiones normalizados.** El borrador tenía en dash (U+2013) como separador; se reemplazaron por guion común porque el hook del pre-commit sigue activo (ADR-082 retira la obligación de estilo, no el mecanismo).

---

## [2026-09-29] - ADR-085: una sola maquina - el workspace deja de sincronizarse entre equipos

### Changed
- **La documentacion dejo de describir un mundo que ya no existe.** El workspace se presentaba como "compartido entre Mac Mini y MacBook Air, sincronizado por git" en `README.md`, `AGENTS.md`, `USER.md`, `MEMORY.md`, `docs/SETUP.md`, `docs/gateway-operations.md`, `.knowledge/BRIEF.md` y `docs/LANGCHAIN_STRATEGY.md`. Con la arquitectura multi-agente (ADR-073) el modo de trabajo cambio: el sistema orquesta agentes en **una sola maquina**. Corregido en todas las superficies.
- **`memory.db` sigue en git, con otro fundamento.** El motivo original era que la memoria viajara entre equipos (ADR-050/054). Con una sola maquina ese motivo desaparece; la DB se queda como **respaldo versionado**. El umbral de higiene de git (bloat) sigue vigente; los conflictos de merge entre equipos, no. Notas de estado agregadas a ADR-050 y ADR-054 (el texto historico se conserva).
- **Regla "merge, nunca reset" conservada, sin su porque original.** Nacio para no descartar commits de la otra maquina. Sigue siendo buena practica al resolver conflictos de historial; se retiro la justificacion "de la otra maquina" en `MEMORY.md` y `memory/user-profile.md`.
- **Registros fechados con nota, no reescritos.** `docs/learnings/infraestructura.md` y `docs/learnings/metodologia.md` conservan su texto y suman una nota de que el escenario cambio.

### Removed
- **`docs/machine-switch-protocol.md` eliminado.** Su unico sujeto era el cambio de maquina. Sus fragmentos vivos (datos locales irrecoverables, gitlinks, `pull --rebase`) ya viven en `AGENTS.md` y `docs/AGENTS-DETALLE.md`; el resto no tenia referente. Retirado tambien el item de roadmap "3.2 La segunda maquina como activo".

### Notes
- **Hallazgo de registro:** la decision sobre la Air no estaba escrita en ningun lado (se busco en los dailies del 27/28/29 y en la memoria). Este ADR es el registro que faltaba. Una decision que solo se dice en una conversacion no viaja a la documentacion, y el sistema sigue describiendo un mundo vencido.
- **El gate atrapo al propio ADR:** `check-refs.py --all` marco que ADR-085 citaba el archivo que acababa de retirar. Corregido. La guarda funciono sobre su propio autor.
- Verificado: `check-adr-integrity` 85 ADRs, `check-refs --all` 441 rutas, `test-skills` verde.

---

## [2026-09-29] - ADR-084: registros de sesion consolidados y el segundo arbol de skills cubierto

### Changed
- **`docs/conversations/` + `docs/history/` -> `docs/records/` (ADR-084).** Eran dos casas para el mismo genero, sin criterio que las separara. Los dos archivos de `conversations/` eran **dos redacciones del mismo evento** (sesion kanam-lab del 2026-09-16). Consolidados en `docs/records/2026-09-16-kanam-lab-ui.md` y `docs/records/2026-09-21-kanam-lab-profile.md`. Convencion de nombre: `YYYY-MM-DD-<tema>.md`.
- **`SKIP_DIRS` de `scripts/check-refs.py` deja de nombrar un fantasma.** La lista era `("docs/archives/", "docs/history/", "docs/conversations/")`; `docs/archives/` **ya no existia** desde el rename del 09-28. Ahora es `("docs/records/",)`, un solo directorio que si existe. El criterio de ADR-056 no cambio: la historia no se chequea, solo su lista.
- **El registro del 09-16 declara su propia desactualizacion.** Describe la eliminacion de dos tabs de `kanam-lab`, y el proyecto los **volvio a tener** (commit `4587022`, 2026-09-29). El texto queda intacto con una nota arriba en vez de mentir por omision.

### Fixed
- **`test-skills.sh` solo escaneaba `skills/` (36), no `agents/*/skills/` (42).** Las 42 skills de agente no tenian **ningun** check: ni sintaxis, ni frontmatter, ni guion, ni scripts referenciados, ni links. La misma clase de falso verde que el de `SKILLS-INDEX.md` (Nivel 2): un check que reporta "36 ok" mientras la mitad del arbol no se mira. Ahora escanea los dos arboles via `SKILL_ROOTS`: 79 SKILL.md, 21 scripts bash, 9 python.
- **7 links cross-skill rotos destapados por la cobertura nueva.** 4 eran referencias reales con la ruta mal puesta (`knowledge-management` -> `engineering-governance`/`tech-docs`, `background-execution` -> `planning-and-task-breakdown`/`session-lifecycle`): corregidas a la ruta real. 3 eran **ejemplos de una plantilla** (`spec-driven-development`, la skill del formato de spec: rutas de un proyecto destino como `REQ-001` o `tests/registration.test.ts`), declarados en `ALLOWLIST_LINK` con la misma justificacion que ya usaba `ALLOWLIST_REF`.
- **`scripts/ui-measure.mjs` -> `agents/kanam-dev/skills/cross-engine-css-measurement/scripts/`.** Era un huerfano en `scripts/`: nacio como one-shot de `kanam-story-bible` y no lo citaba nadie (solo su propio comentario de uso). Un instrumento de medicion pertenece a la skill de medicion.

### Notes
- **Auto-consistencia:** mover `ui-measure.mjs` a una skill de agente **exigio** extender `test-skills.sh`; si no, la propia adicion quedaba sin verificar. El hallazgo lateral y el cambio principal se sostienen uno al otro.
- Verificado: `check-refs` 144 rutas (default) / 434 (`--all`), `check-adr-integrity` 84 ADRs, `test-skills` verde, pytest verde, bats 55/55.

---

## [2026-09-29] - README.md: el router de entrada del workspace

### Added
- **`README.md` en la raiz.** El repo tenia cinco puertas de entrada (`AGENTS.md` = conducta, `docs/SETUP.md` = entorno, `memory/README.md` = memoria, `SKILLS-INDEX.md` = skills, `CONTRIBUTING.md` = OSS) y ninguna decia "que es esto y a donde ir". El README cubre esa capa: puntos de entrada, mapa de nivel 1 (incluidas las carpetas invisibles), contexto de bootstrap y sus caps, contrato del worktree, flujo de trabajo, maquinas y mantenimiento. **Rol explicito de router, no de copia:** solo enlaza; si repite contenido, se desincroniza (precedente: `AGENTS.md` -> `docs/SETUP.md`, mirror `.github/skills/`).
- **`README.md` sumado a `DEFAULTS` de `scripts/check-refs.py`.** Sin eso quedaba fuera del escaneo default, replicando el falso verde que tenia `SKILLS-INDEX.md` antes del fix de Nivel 2: un doc de entrada que nadie escanea se rompe en silencio. Corrida default: 142 rutas (antes 129).

### Tests
- `tests/python/test_check_refs.py`: nuevo `test_readme_is_scanned` que fija el contrato. Suite python completa en verde.

### Notes
- **Verificado end-to-end, no solo por el test:** se agrego a proposito un link roto a `README.md`, el checker default fallo nombrando `README.md:92 -> ./docs/no-existe-jamas-xyz.md`, y al restaurar volvio a OK. Un test que fija una constante no prueba que el archivo se escanee; esto si.

---

## [2026-09-29] - Auditoria Nivel 2: 62 links rotos y el falso verde que los tapaba

### Fixed
- **`check-refs.py` no escaneaba links a directorios.** `is_link_skippable` descartaba todo link terminado en `/` con el criterio "link a directorio, no a archivo". Pero un link a un directorio promete que ese directorio existe: el skip tapaba **42 links rotos** solo en `SKILLS-INDEX.md` (apuntaban a `skills/<slug>/`, que ya no existe: las skills viven en `agents/<rol>/skills/`). Un check que reportaba "291 rutas OK" mientras 42 links rotos pasaban por debajo. Corregido: los links a directorio se verifican.
- **`SKILLS-INDEX.md` no estaba en `DEFAULTS`.** El checker nunca lo escaneaba en su corrida default. Agregado. Ahora la corrida default revisa 369 rutas (antes 291).
- **`SKILLS-INDEX.md`: 42 links corregidos** a la ruta real (`agents/<rol>/skills/<slug>/`), y el total actualizado: decia 65 skills (dato del 2026-09-22); son **78 activas** (36 en `skills/` + 42 en `agents/*/skills/`, excluido el placeholder `study-tracker`).
- **`agents/kanam-ops/scripts/aggregate-sync.sh`:** copia stale (2026-09-08) apuntaba a `${WORKSPACE_DIR}/projects`, ruta que ADR-075 elimino. Sincronizada con la version del workspace (`${HOME}/projects`).

### Tests
- `tests/python/test_check_refs.py`: el test que fijaba la conducta vieja (`test_directory_link_is_skipped`) se reemplazo por `test_directory_link_is_checked` + `test_reports_a_broken_directory_link` + `test_skills_index_is_scanned`. 21/21 en verde.

### Notes
- **La lección de siempre:** una guarda que dice tener respaldo sin tenerlo es peor que no tener guarda, porque induce a confiar. El skip de links a directorio era el punto ciego; los 42 links rotos llevaban ahi desde que las skills se movieron a `agents/`.

---

## [2026-09-29] - La regla del guion comun deja de ser obligatoria (ADR-082)

### Changed
- **Se retira la regla del guion comun** (`-` siempre, nunca em/en dash) como regla obligatoria del workspace, por decision explicita de Gonzo: *"ya tenemos una evolucion y una robustez para tener identidad propia, dejemos de perder tiempo y recursos revisando los guiones"*. Formalizado en ADR-082.
- **Archivos de instruccion limpiados:** `USER.md`, `MEMORY.md`, `AGENTS.md`, `CONTRIBUTING.md` (seccion "Em dash check obligatorio" completa) y los archivos `AGENTS.md`/`USER.md` de los cuatro agentes (`kanam-mind`, `kanam-dev`, `kanam-ops`, `kanam-studio`). Tambien el eco en `skills/github/SKILL.md`, `skills/github/references/conventional-commits.md`, `agents/kanam-studio/skills/content-serializer/SKILL.md`, `docs/SETUP.md`, `docs/voz-gonzo.md` y `studies/narrative-engineering/metodo.md`.
- **ADR-071** (hyphen enforcement) pasa a `status: superseded por ADR-082`.

### Notes
- **El aparato mecanico NO se desarma.** El hook del pre-commit, `scripts/check_em_dash.py`, `scripts/hyphen_enforcer.sh` y `scripts/test-skills.sh` se conservan tal como estan: siguen corriendo y no molestan. Desarmarlos es una tarea aparte.
- **Sin barrido retroactivo.** Los proyectos actuales y los textos ya publicados no se tocan: la regla se retira hacia adelante.
- **Trade-off aceptado:** sin la regla declarada, un em dash puede volver a colarse en textos nuevos. Es el precio de dejar de gastar recursos en el cosmético.

---

## [2026-09-29] - `docs/stories/` como casa de las historias + la novela Quienes Quedan

### Added
- **`docs/stories/quienes_quedan/`:** la novela (WORLD, CHARACTERS, PLOT, STYLE, README, `manuscript/` con 3 capitulos, `.knowledge/`), importada desde `~/projects/quienes_quedan/`.

### Changed
- **`docs/stories/el_descenso/historia_descenso.md`:** `historia_descenso.md` movida a una carpeta por historia.
- **La novela deja de ser un proyecto de codigo:** tenia repo git propio en `~/projects` (privado en GitHub), pero es literatura, no herramienta. ADR-075 rige para proyectos de codigo; el contenido narrativo vive con el workspace. Se retiro la carpeta local (`~/projects/quienes_quedan` -> Trash; backup en `/tmp/quienes-quedan-backup-20260929-163652`). El workspace sigue privado, asi que la novela no se expone.
- **Excepcion documentada al guion comun en el pre-commit:** el manuscrito usa la raya (U+2014) como raya de dialogo (decision de Gonzo 2026-09-24 en `STYLE.md`, *"solo en este proyecto, no corregir"*). El hook (y `scripts/pre-commit.template`) exceptua `docs/stories/quienes_quedan/` del chequeo y del enforcer, para no convertir el manuscrito. El CI no chequea guiones largos (verificado: solo `skills-ci.yml`, sin `check_em_dash`).

### Notes
- **Pendiente de decision de Gonzo:** el repo privado `github.com/gonzoblasco/quienes_quedan` quedo sin uso (contenido ya en el workspace). No se toco: borrarlo o archivarlo es una accion hacia afuera.

## [2026-09-29] - `memory/` reorganizado en carpetas predecibles + fix del hook de renames

### Added
- **`memory/README.md`:** mapa de la estructura y del **contrato del tooling** (que DEBE quedar en la raiz y por que).

### Changed
- **Retencion en `memory/`: la raiz guarda solo la ultima semana.** Los dailies con fecha anterior a hoy-7 se mueven a `archive/dailies/` (26 dailies + el set `09-18-cpacc-*`). El contenido sigue en la DB (`daily_notes`, fuente de verdad); el `.md` archivado es la copia legible. `user-interests.md` tambien pasa a `notes/` (nadie lo referenciaba).
- **Colision de nombre resuelta en `2026-08-10`:** la raiz tenia un fragmento suelto (1 KB, check-in de swift-testing) con el mismo nombre que el daily archivo completo (23 KB). El rico queda intacto; el fragmento se preserva como `archive/dailies/2026-08-10-swift-testing-check.md` (era contenido duplicado de check-ins ya presentes en 7 dailies archivados, y sin fila en la DB).
- **`memory/README.md`:** documenta la regla de retencion (raiz = ultima semana) y el chequeo de colision antes de archivar.
- **`memory/` deja de ser una carpeta plana:** 509 archivos -> estructura por tipo. Nuevas carpetas `handoffs/`, `notes/`, `_templates/`; `archive/` partido en `archive/dailies/` (consolidados) y `archive/sessions/` (logs con hora); `archives/` (duplicado semantico) absorbido.
- **Raiz de `memory/` solo con lo que el tooling resuelve ahi:** `memory.db`, el daily vigente (`YYYY-MM-DD.md`), las vistas generadas (`todos.md`, `inbox.md`) y `user-profile.md` (referenciado por el bootstrap). El resto se movio: 5 notas -> `notes/`, 8 handoffs -> `handoffs/`, el template -> `_templates/`.
- **`.gitignore`:** el glob de session logs se vuelve a anclar a la raiz (un `*` no cruza `/`, asi `archive/sessions/` sigue versionado) y cubre el sufijo de desempate `-N` (antes `memory/2026-08-29-2345-2.md` estaba trackeado por error).
- **Refs actualizadas:** skill `knowledge-management` (archivado a `archive/dailies|sessions`), `docs/SETUP.md`, `MEMORY.md` (handoff de soporteml).

### Fixed
- **El pre-commit trataba un rename puro (`R100`) como contenido nuevo:** el filtro `--diff-filter=ACMR` incluia `R`, asi que un movimiento byte-identico pasaba por el chequeo de guion largo y heredaba los em dash historicos del archivo (200 de 445 en esta reorganizacion). Un rename no introduce guiones. El hook (y `scripts/pre-commit.template`) ahora separa `MD_CONTENT` (bytes que cambiaron: `A`, `M`, `C`, y `R` no-100) para las reglas de contenido, mientras refs/ADR siguen corriendo con cualquier markdown staged. El gate no se debilito: contenido editado sigue chequeado.

### Notes
- **Deuda registrada (no resuelta):** `memory/` ya tenia **225 archivos con guiones largos historicos**, en `archive/` (dailies + sesiones), `dreaming/`, y ~5 dailies raiz. El hook los ignora correctamente al moverlos, pero al editarlos volveran a bloquear. Normalizarlos es una tarea aparte (masiva, sobre registro historico).
- **Backup:** `/tmp/memory-backup-20260929-162454/memory.tar.gz` (15 MB).

## [2026-09-29] - 6 LaunchAgents huerfanos regeneraban `workspace/projects/` (resaca de ADR-075)

### Fixed
- **`projects/` del workspace se regeneraba al borrarlo:** ADR-075 (2026-09-27) movio los proyectos a `~/projects/<slug>` y el workspace dejo de hospedar el arbol, pero **6 LaunchAgents quedaron apuntando a la ruta vieja** `~/.openclaw/workspace/projects/<slug>`:
  - `dev.gonzoblasco.kanam-spec` y `-watchdog`
  - `dev.gonzoblasco.kanam-os` y `-watchdog`
  - `dev.gonzoblasco.langchain-starter` y `-watchdog`
- **Mecanismo del bucle:** `kanam-spec` tiene `KeepAlive=true` con `ProgramArguments` al `server/index.mjs` viejo (ausente). Arranca, falla con `MODULE_NOT_FOUND` y launchd lo relanza cada 10 s. Cada arranque abre su `WorkingDirectory` y `StandardErrorPath` -> **recrea `projects/kanam-spec/logs/`**. Por eso reaparecia apenas se borraba.
- **Evidencia:** `projects/kanam-spec/logs/service.err` con 21 KB de stacktraces `MODULE_NOT_FOUND`; `launchctl print` mostraba `working directory` viejo en los 6 jobs, mientras `lsof -a -p <pid> -d cwd` mostraba que los 3 procesos vivos corrian en `~/projects/...` (la mudanza ocurrio con los procesos ya levantados).

### Changed
- **`.openclaw/portals.json` corregido (mismo patron):** el portal `kanam-os` declaraba `./projects/kanam-os/scripts/dashboard.sh`, una ruta dentro del workspace que ya no existe. El `cwd` del archivo es **relativo a la raiz del workspace** (docs), asi que resolvia al arbol muerto. Ahora usa el **path absoluto** `/Users/gonzoblasco/projects/kanam-os/scripts/dashboard.sh` con `cwd: "."`. Verificado: `dashboard.sh status` responde `health: OK`. Unico otro ref vivo de `./projects` en el workspace era ese; el resto son dailies historicos.
- **Ruta vieja reemplazada en 3 capas** (18 archivos): los 6 `.plist` de `~/Library/LaunchAgents`, los 6 canonicos de `~/projects/*/config/`, y los 6 scripts `service.sh`/`watchdog.sh`/`dashboard.sh` de los proyectos. Los canonicos importan: un `bootstrap` desde ahi volvia a romper.
- **Jobs recargados:** `bootout` + `bootstrap` de los 6. Los 3 servicios quedaron corriendo con cwd correcto y respondiendo: kanam-spec :4173 (`{"ok":true}`), kanam-os :4317 (HTTP 200), langchain-starter :8100 (HTTP 200).

### Notes
- **Backup:** plists y canonicos en `/tmp/launchagents-backup-20260929-161611`; carpeta basura en `/tmp/kanam-stale-projects-trash`.
- **Verificado tras 75 s:** `projects/` no se regenera.
- **Regla preventiva:** al mover la ubicacion de un proyecto, ademas del codigo y el `.gitignore`, hay que actualizar **sus LaunchAgents** (la ruta queda hardcodeada en 3 capas).

## [2026-09-29] - Dedupe de daily notes: dos escritores sobre el mismo archivo

### Fixed
- **`scripts/memory-end-session.py` deja de anexar duplicados al daily:** el flush de memoria pre-compactacion de OpenClaw (nativo, `memory-core`) escribe en el mismo archivo que el daily (`memory/YYYY-MM-DD.md`). El flush **anexa** su bloque entero (con su propio `# Daily YYYY-MM-DD`) en cada compactacion, mientras `reconcile_md_into_db` re-escribia el cuerpo crudo del `.md` hacia la DB (secciones repetidas incluidas) y lo volvia a exportar. Resultado: el daily del 2026-09-29 acumulo 5 titulos `# Daily 2026-09-29` (evidencia: `grep -c '^# Daily 2026-09-29' memory/2026-09-29.md`).
  - `_strip_title` ahora descarta **todos** los titulos de nivel 1 iniciales, no solo uno.
  - `_dedupe_sections` conserva solo la primera ocurrencia de cada encabezado `##`; `_normalize_section_body` elimina encabezados `#` de nivel 1 que quedaron enterrados dentro del cuerpo de una seccion.
  - `reconcile_md_into_db` reconstruye el cuerpo desde las secciones ya deduplicadas; nunca re-ingesta el `.md` crudo.
  - `export_daily_to_md` emite siempre exactamente **un** titulo.
  - Nuevo flag `--dedupe-only` (reconcilia + deduplica + regenera el `.md`, sin anexar bloque de sesion) y `dedupe_daily_db` para reparar filas ya dañadas in situ.
- **`ARCHIVED_PROJECTS/kanam-sudoku.md`:** 15 en dash (U+2013) reemplazados por guion comun; el pre-commit (`scripts/check_em_dash.py`) los rechazaba.

### Known limitation
- **El flush nativo no puede fusionar por seccion:** agrega su bloque al final y, si su primer encabezado es `# `, queda enterrado dentro de la seccion previa (observado en el bloque `Session End - react-spectrum-pr-10503`, cortado por `... (truncated)`). La contencion vive en el reconciliador de este workspace; la config `agents.defaults.compaction.memoryFlush` no expone fusion por seccion.

## [2026-09-28] - Politica de modelos cloud-first, integracion Hermes SDD, fin de la publicacion de skills

### Added
- **Regla transversal: esperar el CI antes de seguir (2026-09-28, `AGENTS.md`):** despues de cada push, en cualquier proyecto, hay que esperar a que el CI termine y todos los actions pasen antes de pasar a otra tarea o cerrar la sesion. Un job `pending` no es verde; no se cierra la sesion con CI pendiente. Pasa a `AGENTS.md` seccion Git & Commits.
- **ADR-076 - ningun agente hereda un modelo local:** los modelos cloud primero, locales como ultimo recurso. Corrige la causa real de los fallos de automatizacion (`defaults.model.primary` apuntaba a `gemma4:26b`, local y desinstalado, que `kanam-mind` y `kanam-studio` heredaban).
- **ADR-077 - pipeline A/B asimetrico:** Agente A (ejecutor) liviano en `gpt-oss:120b-cloud`; Agente B (evaluador y corrector) grande en `deepseek-v4.1-flash:cloud` con 1M de contexto. La asimetria es intencional: el revisor ve mas que el ejecutor.
- **ADR-078 - la salida de un sub-agente es un auto-reporte, no un hecho:** `status=done` significa que el proceso termino limpio, no que el resultado sea cierto. Rutas absolutas en los briefs; el padre reproduce la verificacion.
- **ADR-079 - la coleccion de skills deja de publicarse:** `kanam-skills` archivado en GitHub; `publish-skills` marcada `status: archived`.
- **Skills nuevas:** `sdd-agent-loop` (loop por etapas + confidence gate), `verification-gates` (las 3 reglas anti falso-verde), `trust-vocabulary-report` (vocabulario de confianza por etapa). Extraidas de Hermes SDD.
- **9 skills `hermes-*`** (architect, builder, discovery, openspec, planner, pr-reviewer, qa, release, reviewer).
- **`scripts/verify-delegation.sh`** + suite interna + `tests/bash/verify-delegation.bats`: gate de verificacion de artefactos. Codigos de salida `0`/`1`/`3`; **cero artefactos nunca es un pase**. Enganchado al pre-commit.
- **`docs/checklists/delegation-brief.md`:** plantilla obligatoria para tareas delegadas.
- **83 specs de Hermes** importadas a `wiki/main/sources/hermes-sdd/`, con fidelidad verificada contra el origen.

### Changed
- **`openclaw.json` (config del gateway):** `defaults.model.primary` a cloud; `kanam-mind` y `kanam-studio` con modelo explicito; fallbacks de `main` 27 -> 13 (cloud primero, locales instalados al final); 8 referencias a modelos no instalados limpiadas. Backup: `openclaw.json.bak-20260928-112321-pre-cloud-models`.
- **`scripts/model-router.sh`:** ruta `pipeline_ab` a la division asimetrica A/B.
- **`skills/agent-orchestration-pipeline/SKILL.md`:** documentada la division de modelos por rol.

### Fixed
- **Automatizaciones que fallaban por modelo:** `gateway-jobs-watcher` (15 corridas fallidas) y `skill-collection-review:kanam-mind` pasan a `ok` tras el cambio de modelos, verificado forzando la corrida.
- **Gate de verificacion endurecido tras review adversarial:** rechaza patrones con forma de path y el patron universal (verificado: permitian evadir la verificacion).
- **Reporte del sprint 7 reescrito:** el sub-agente habia entregado evidencia fabricada (JSON inventado; dos jobs dados por fallidos que estaban `ok`).

### Notas de metodo
- **Los comandos de `plugins` re-rompen los triggers de automatizacion.** Los jobs quedaron `ok` y volvieron a `error` tras inspecciones posteriores. Los "hallazgos del watcher" eran efecto de la propia investigacion. Agrupar los comandos en una pasada; la estabilidad la decide la corrida programada.
- **El registro de plugins queda `stale`** (desacuerdo de `workspaceDir`), no reparable por CLI ni `doctor`: es intervencion de estado del gateway, pendiente de decision del owner.

---

## [2026-09-27] - Recuperacion de datos y cierre de la migracion multi-agente (ADR-073)

### Added
- **ADR-075 - los proyectos viven en `~/projects`, fuera del worktree:** documenta el movimiento del 2026-09-26 que nunca se registro, y cierra la pregunta de la memoria de proyecto: el `.knowledge/` es parte de cada proyecto y viaja con el (decision de Gonzo).
- **Los 4 workspaces de agente trackeados** (`agents/kanam-dev`, `kanam-mind`, `kanam-ops`, `kanam-studio`): 145 archivos. Sus `.git` anidados vacios (0 commits, 0 remote) se removieron: hacian que el git del workspace viera cada agente como bloque opaco.

### Fixed
- **`memory.db` recuperada (perdida de datos real):** no existia en disco, solo en HEAD, tras el barrido de la migracion. Restaurada con `memory/archive/` (425 dailies), `SKILLS-INDEX.md` y **20 archivos curados** que no se regeneran de la DB (`user-profile.md` entre ellos, referenciado por `USER.md`).
- **24 skills CORE restauradas** (`session-lifecycle`, `engineering-governance`, `agent-orchestration-pipeline`, etc.): activas segun el indice, no migradas a `agents/<rol>/`, y ausentes del disco. Repararon 3 refs rotas en `AGENTS.md` y el pipeline (`check-refs`: 276 rutas, todas existen).
- **`studies/` estaba regresionado:** el working tree revertia el caso 02 (Batman Begins) de 4/4 a 2/4 ejes, byte-identico al commit previo, 103 lineas de analisis ya hecho borradas. Descartado con `git restore`, no se commiteo.
- **Indice de ADRs reconciliado:** ADR-074 estaba en disco sin fila. `check-adr-integrity.py` ahora limpio (75 ADRs).
- **17 guiones no separables (U+2011) limpiados** de ADR-071 y ADR-072 - los propios ADRs de la regla del guion.
- **`hyphen_enforcer.sh`:** portabilidad (`mapfile` no existe en el bash 3.2 de macOS), bit ejecutable, y sus propios 5 guiones raros normalizados.
- **Daily 2026-09-27 deduplicado:** tenia 4 copias del mismo bloque de sesion. Deduplicado DB-first.

### Changed
- **El arbol viejo `skills/` y `projects/` retirado del workspace** (284 bajas commiteadas): 43 skills migradas tienen copia identica en `agents/<rol>/skills/`; 17 sin destino eran placeholders. `projects/` se movio a `~/projects` (ADR-075).
- **`AGENTS.md`**: la seccion de proyectos describe `~/projects` y declara que la memoria de proyecto es del proyecto.
- **`.gitignore`**: el bloque de excepciones de `projects/` (60 lineas) reemplazado por una sola regla de ignorado.
- **`aggregate-sync.sh`**: apunta a `~/projects` (override con `PROJECTS_DIR`) y falla con las instrucciones exactas de inicializacion del agregado.

### Notes
- **Causa raiz (diagnostico de Gonzo, confirmado por los datos):** la migracion se hizo con modelos chicos locales de poco contexto durante dia y medio. El registro quedo mal y el trabajo se reescribio sobre contexto incompleto, lo que dejo cuatro capas de dano (la DB, las skills CORE, `studies/` y el daily duplicado).
- **Pendiente (backlog todo #61):** sincronizar los proyectos a un repo nuevo. Hoy 135 archivos `.knowledge/` viven solo en disco, sin respaldo en git. Diferido a proposito.

## [2026-09-26] - Gates de accesibilidad y refs rotas antes del push

### Added
- **`scripts/check-a11y-trigger.py`:** dispara la validacion manual de accesibilidad cuando el diff toca lo que ANUNCIA el screen reader (posinset, setsize, live regions, activedescendant, roles de widget). Cableado al pre-commit y al CI, con override consciente `A11Y_VALIDATED=1`. Antes ese boundary vivia solo en la skill `a11y-at-validation`, sin respaldo mecanico.
- **Gate de a11y en CI** (`.github/workflows/skills-ci.yml`): segunda barrera via `--range`, porque el pre-commit se saltea con `--no-verify`.
- **Tests:** `tests/python/test_check_a11y_trigger.py` (18) y cobertura de links markdown en `tests/python/test_check_refs.py`.

### Fixed
- **`check-refs.py` ahora valida links markdown**, no solo rutas entre backticks `docs/` y `scripts/`. Encontro 6 refs rotas en ADR-001 a ADR-005.
- **14 referencias colgantes de la migracion multi-agente:** 12 links `../<skill>` en `skills/*/SKILL.md` y el path de script en `tests/bash/word-count.bats`.
- **`frontmatter_validator.sh` corrompia skills:** insertaba un bloque `---` encima del front-matter real en los SKILL.md que empiezan con el comentario de proyecto, y usaba `title: SKILL` en vez del slug. Las 11 skills afectadas eran invisibles para el loader de OpenClaw (verificado: 152 a 163 tras el fix).
- **El pre-commit arrastraba bajas ajenas:** `git add $(git ls-files ...)` expandia como glob el path literal `skills/*/SKILL.md`, stageando las bajas de la migracion. Corregido con `--literal-pathspecs` y re-stage acotado a lo que se commitea.
- **`test-skills.sh` secciones D y E** solo miraban `skills/`: al mover skills a `agents/<rol>/skills/` quedaban verdes sobre links rotos.

### Docs
- `AGENTS.md`: los 6 links de skills apuntan a su ubicacion real.
- `docs/adr/README.md`: filas de ADR-071, ADR-072 y ADR-073 reconciliadas (el indice desreconciliado bloqueaba el pre-commit).
- `docs/pipeline/2026-08-30-spin-review-migration.md`: corregido, 5 de los 6 scripts que declaraba "creados" nunca funcionaron.

### Notes
- La migracion multi-agente (ADR-073) queda intacta para su sesion dedicada: este commit no toca `agents/` ni las bajas de `skills/`.

## [2026-09-25] - kanam-spec: spec skeleton completed

### Added
- Created detailed `spec.md` in `projects/kanam-spec/openspec/specs/kanam-spec/` with Overview, Goals, Requirements (functional \u0026 non-functional), Non-goals, Scenarios, Acceptance Criteria and extended functional requirements FR-4 - FR-7 covering UI input, generation process, preview/export, validation, UX flow, edge-case handling, performance, security, accessibility, and compatibility.
- Updated `CHANGELOG.md` to record this addition.

## [2026-09-24] - SoporteML se reabre: definicion de la nueva generacion (ADR-067 + ADR-068)

### Added
- **ADR-067 - los ADRs del workspace no pertenecen a un proyecto.** Ante el pedido de "eliminar los ADRs que referencian versiones previas de SoporteML", se midio antes de borrar: **0 de 68 ADRs tienen SoporteML como sujeto**; los 11 que lo mencionan solo lo citan. Dos dicen lo contrario (ADR-048: "la familia soporteml queda fuera de todo barrido"). Borrar "los 47 que citan tecnologia" habria eliminado decisiones que sostienen entre 7 y 20 proyectos (ADR-048 -> 20, ADR-037 -> 15, ADR-036 -> 7). La decision fija el procedimiento: distinguir sujeto de cita, medir blast radius, y archivar antes que borrar.
- **ADR-068 - la nueva generacion de SoporteML es greenfield y se basa en v1.** Inventario medido de las cuatro generaciones: **v1 es la mas completa** (54 migraciones, 24 tablas, 25 Edge Functions, 81 componentes, 18.889 lineas). v3 y v4 son **podas**, no sucesoras. v4 copio los 3 ADRs de v3 byte-identicos (checksum `83022a062fdc`): heredo el stack sin decidirlo. Deja 6 pendientes explicitos para Gonzo (encuadre, alcance contable, nombre, app OAuth de MeLi, destino de ADRs de v3/v4, y la pregunta de demanda sin responder en 4 generaciones).

### Changed
- **`projects/portfolio-strategy/.knowledge/ADR-001` - enmienda seccion 7:** SoporteML se reabre por pedido explicito de Gonzo, que es la clausula de reapertura prevista por el propio ADR ("no se vuelve a abrir salvo que Gonzo lo pida explicitamente"). **Sigue vigente** que queda fuera de la narrativa publica / del CV y fuera de barridos automaticos. **No entra a la tabla de anclas.** Encuadre: producto privado.
- **`MEMORY.md`:** la entrada de SoporteML actualizada (decia "v4 es el reinicio actual" y "es hora de dejarlo ir"). La regla del 2026-08-28 matizada: sigue aplicando a la narrativa publica, ya no prohibe trabajarlo.
- **`docs/adr/README.md`:** indice con ADR-067 y ADR-068.

### Notes
- **La demanda sigue sin probar en cuatro generaciones.** v1 nunca cobro: su billing esta escrito y jamas fue operativo (secrets sin configurar, plan de preapproval sin crear). La pregunta "por que esta vez tendra usuarios" queda registrada como pendiente, no resuelta.
- **Mercado verificado (web_fetch):** Buin ERP ya vende "facturacion ARCA + stock + contabilidad + integracion MeLi". El diferencial imaginado esta ocupado; el contable ademas es dominio regulado (responsabilidad legal).
- **La nueva generacion es, literalmente, la "Fase 4" de v1** ("salir de Lovable") que v1 declaro en su propio PLAN.md y nunca ejecuto.

## [2026-09-24] - kanam-insight: Handoff Synthesizer y reparacion del indice

**Regla:** cada vez que se modifique la estructura del workspace (AGENTS.md, MEMORY.md, SOUL.md, USER.md, TOOLS.md, HEARTBEAT.md, scripts/, estructura de proyectos, skills), actualizar este archivo en el mismo commit.

---

## [2026-09-24] - kanam-spec: verificacion en dos capas (linter + revision con modelo)

### Added
- **Linter determinista (`projects/kanam-spec/src/lib/lint.ts`):** detecta sin modelo secciones sin contenido o en esqueleto, requisitos sin criterio de verificacion (cita el ID de fila), plantillas sin completar (TBD/TODO/FIXME, corchetes de ejemplo) y celdas de tabla vacias, con severidad y resumen "listo para entregar".
- **Revision cruzada con el modelo, cableada (`src/lib/review.ts` + `ReviewPanel.tsx`):** `buildReviewMessages` existia desde el primer commit y no estaba conectado a nada. Ahora la revision corre con streaming, se cancela, se persiste con marca de vigencia (`docUpdatedAt` vs `updatedAt`) y avisa cuando quedo desactualizada.
- **Panel de verificacion** (`src/components/ReviewPanel.tsx`): las dos capas separadas y etiquetadas, salto del hallazgo a su seccion, estado vacio explicito.
- **Export con estado de verificacion:** el Markdown lleva los hallazgos abiertos y la marca de la ultima revision; no bloquea la descarga. La entrada del modelo excluye esa seccion para no sesgar su analisis cruzado (fix aplicado en revision sobre el trabajo del subagente).
- **OpenSpec en el proyecto:** `openspec/` con el change `add-spec-review` completo (proposal, specs de las capacidades `spec-lint` y `spec-review`, design con 5 decisiones, tasks 18/19 completas) y `openspec validate --strict` en verde. ADR de proyecto: `.knowledge/adr/0001-verificacion-en-dos-capas.md`.

### Notes
- Pipeline: T=12 -> subagente escribio el nucleo (lint/review/types/storage/spec + 21 tests nuevos), Kanam reviso el diff, cableo la UI y corrigio un sesgo (el modelo recibia los hallazgos del linter y tendia a repetirlos). 33/33 tests, typecheck limpio, build OK.
- Decision de Gonzo en el debate: herramienta personal, la verificacion es LA etapa (no futura), OpenSpec/ADR porque va en serio.
- Pendiente: tarea 5.3 (recorrido de punta a punta en el navegador, con click del usuario), `openspec archive`, repo en GitHub.

---

## [2026-09-24] - kanam-spec: verificacion en dos capas (linter determinista + revision con modelo)

### Added
- **Linter determinista (`projects/kanam-spec/src/lib/lint.ts`):** reglas sin modelo que detectan secciones sin contenido o en el esqueleto, requisitos sin criterio de verificacion (citando el ID de fila), plantillas sin completar (TBD/TODO/FIXME, corchetes de ejemplo) y tablas con celdas vacias. Es valor derivado: se recalcula sobre el documento, nunca se guarda, asi que no puede quedar desincronizado.
- **Revision cruzada cableada a la UI:** `buildReviewMessages` existia en el primer commit, con tests, y nunca se habia conectado a ningun boton. Ahora corre con streaming, con aviso de "el modelo esta razonando" y cancelacion.
- **Estado de revision con marca de vigencia:** el documento guarda `review` con el `updatedAt` que tenia al revisarse; la vigencia se resuelve comparando dos campos. Guardar la revision no toca `updatedAt`, o se marcaria desactualizada a si misma.
- **Panel de hallazgos (`ReviewPanel.tsx`):** separa los chequeos automaticos de la revision del modelo, con severidad y salto a la seccion afectada.
- **Verificacion en el export:** el Markdown lleva una seccion con los hallazgos abiertos y la ultima revision. Informa, no bloquea la descarga.
- **OpenSpec inicializado en el proyecto:** el change `add-spec-review` es el primero, con proposal, spec deltas (`spec-lint`, `spec-review`), design y tasks. Valida con `--strict`.
- **ADR del proyecto:** `.knowledge/adr/0001-verificacion-en-dos-capas.md`, con las alternativas descartadas.

### Fixed
- **Anclas del indice del export (bug preexistente del primer commit):** el indice derivaba el anchor del label del catalogo (`#contexto-y-problema`) mientras el cuerpo emitia el heading del esqueleto (`## Contexto`). 12 de 14 anclas apuntaban a un destino inexistente. **Lo encontro la revision con el modelo sobre un documento real**, que es exactamente lo que la capa de juicio tiene que aportar. Cubierto con 2 tests de regresion.

### Notes
- **Metodo:** pipeline A/B (T=12, bucket low). Un subagente escribio el nucleo puro (`src/lib/`) y Kanam reviso, cableo la UI, y encontro el bug de anclas al probar la revision contra el servicio vivo.
- **Verificacion:** 35/35 tests en verde, `tsc --noEmit` limpio, build de produccion OK, `openspec validate --strict` OK, scan de guion largo OK. La revision se probo de punta a punta contra Ollama por el proxy del servicio: devolvio 4595 caracteres y detecto el TBD y las contradicciones del documento de prueba.
- **Pendiente honesto:** el click-through en el navegador (tarea 5.3) NO esta hecho. No hay plugin de browser habilitado en el gateway. Lo verificado sin navegador: el servicio sirve el build actual y ese bundle contiene el panel y las reglas del linter.
- **Techo del proyecto:** la app sigue sin repo en GitHub (falta decision de visibilidad de Gonzo).

---

## [2026-09-24] - kanam-spec: servicio permanente con LaunchAgent y watchdog

### Added
- **LaunchAgent `dev.gonzoblasco.kanam-spec`** (`projects/kanam-spec/config/`): levanta la app al boot con `KeepAlive` incondicional, puerto 4173, logs en `logs/`. El comando real vive en `ProgramArguments` (no detras de un wrapper, que saldria 0 por diseno y dejaria el job sin revivir).
- **LaunchAgent `dev.gonzoblasco.kanam-spec-watchdog`:** cada 60 s revive el servicio si se cayo (kickstart -k si esta cargado, bootstrap si no) y respeta el apagado deliberado via `config/.intentional-stop`.
- **`scripts/service.sh`** (`start|stop|restart|status`) y **`scripts/watchdog.sh`:** operan el servicio por `launchctl`, sin procesos node sueltos peleando por el puerto.

### Fixed
- **`server/index.mjs` sale con codigo 1 si el puerto esta tomado:** sin eso una colision de puerto dejaba el servicio a medio levantar.

### Notes
- Causa del incidente de las 19:10: la app corria como proceso de sesion de exec y el runner la mato al vencer su timeout de 30m. Nada se rompio; el trabajo del usuario vive en `localStorage` del navegador.
- Verificado en las TRES rutas, observadas y no asumidas: `pkill` -> KeepAlive revive con pid nuevo; `stop` deliberado -> sigue caido tras 75 s y el marcador lo frena; caida accidental -> recuperado por bootstrap con una linea `RECOVERED` en `watchdog.log`.
- El marcador de apagado intencional queda en `.gitignore`: es estado local de la maquina, y el workspace se sincroniza entre el Mini y la Air.

---

## [2026-09-24] - Nuevo proyecto: kanam-spec (generador de especificaciones tecnicas)

### Added
- **`projects/kanam-spec/` (nuevo proyecto):** app web que convierte un brief corto en una especificacion tecnica completa, con IA local (Ollama) y catalogo de 14 secciones. Estructura triple-git: `.knowledge/` en el workspace, codigo en el repo del proyecto.
- **`.knowledge/BRIEF.md` y `.knowledge/STATUS.md`:** alcance, stack y las decisiones de fondo (IA local en vez de cloud, catalogo fijo de secciones en vez de generacion libre, plantillas + IA, proxy local en vez de fetch directo a Ollama).
- **`src/lib/sections.ts`:** fuente unica de la estructura de la spec: esqueleto de headings e instruccion por seccion.
- **`server/index.mjs`:** servidor sin dependencias que sirve `dist/` y proxea `/api/ollama/*`. Evita CORS y `OLLAMA_ORIGINS`, y deja el puerto de Ollama en una variable de entorno.

### Notes
- Verificacion: 10 tests en verde (runner nativo de Node sobre TypeScript), `tsc --noEmit` limpio, build productivo OK, y smoke test del proxy contra Ollama (22 modelos, chat con y sin streaming).
- Dos bugs reales encontrados y corregidos durante la verificacion: el proxy reescribia `/api/ollama/tags` a `/tags` (404 de Ollama) en vez de `/api/tags`; y el export a Markdown incluia los esqueletos de las secciones sin generar.
- Pendiente de decision de Gonzo: crear el repo en GitHub y pushear (el workspace todavia no tiene el agregado `projects/` configurado en esta maquina).

---

## [2026-09-24] - ADR-066: los guardias del workspace no leen codigo de proyectos (CI en rojo)

### Added
- **`docs/adr/ADR-066-guardias-no-dependen-de-codigo-de-proyecto.md`:** la decision de fondo detras del fix. Ningun chequeo ni test del workspace lee codigo de proyectos como fuente de verdad: los tests prueban la logica con un fixture versionado, el anti-deriva es opt-in por presencia, y el guard de una paleta real vive donde vive la paleta.
- **`tests/python/fixtures/kanam-os-themes.css`:** el contrato de temas (dos temas, 16 variables cada uno) extraido del `globals.css` real, no transcrito a mano. Es la base de los tests de `check-contrast.py`.

### Fixed
- **`tests/python/test_contrast.py` leia `projects/kanam-os/app/globals.css`:** ese archivo no esta versionado (el workspace trackea solo `projects/<slug>/.knowledge/`), asi que la suite pasaba local y fallaba en CI. 12 tests en rojo durante **12 runs seguidos**, empujados como `memory:`, `docs:` y `chore:` porque "solo cambio documentacion". Ahora corren contra el fixture.
- **`test_paleta_actual_pasa` -> `test_paleta_del_fixture_pasa`:** el nombre decia "actual" y verificaba una paleta que la suite no puede ver. Ademas el contrato de esa paleta (que cumple AA) es lo que hace inequivocos los mutation tests de abajo.
- **`test_fixture_no_deriva_del_css_real` (nuevo):** compara las CLAVES del fixture contra el CSS real cuando el proyecto esta clonado, y se saltea en CI. Probado por mutacion: quitando `--badge-comment-text` del fixture, falla con el diagnostico exacto.

### Notes
- **Diagnostico con evidencia:** `git ls-files projects/kanam-os` devuelve solo los dos `.knowledge/`; el pre-commit hook no lo puede ver porque localmente el archivo existe (confianza falsa, la misma familia que la auditoria de contraste que reportaba "0 fallas").
- **Segunda falla, misma familia, el mismo dia:** `docs/LANGCHAIN_STRATEGY.md` citaba `scripts/ingest.py` y compania sin el prefijo del proyecto; se corrigio en `bc060729`. Queda documentado que calificar la ruta arregla el sintoma pero **no** vuelve existente un archivo que no se versiona, asi que un test no debe exigirlo.
- **Verificado en un checkout limpio de `HEAD` sin el proyecto clonado** (simulacion del checkout de CI): 187 tests, 1 skip, 0 fallas. Antes: 12 fallas.
- **Deuda declarada:** la paleta real de kanam-os no tiene guard automatico hasta que el repo kanam-os monte el suyo (pendiente de la Decision 3 del ADR-066). No se oculta como si estuviera cubierta.

---

## [2026-09-24] - check-adr-integrity.py: el corpus de ADRs ahora se verifica solo

### Added
- **`scripts/check-adr-integrity.py`:** valida que el corpus de ADRs y su indice esten reconciliados. Cubre cuatro clases de defecto: (1) ADR en disco sin fila en el indice, (2) fila del indice que promete un archivo inexistente, (3) numero duplicado (dos decisiones con una direccion = una cita resuelve ambigua, peor que un hueco), (4) ref cruzada a un ADR que no existe. Los huecos de numeracion se reportan como **informativos y no fallan**: un hueco puede ser una decision retirada a proposito, un duplicado nunca es intencional.
- **`tests/python/test_check_adr_integrity.py`:** 9 tests. Cada uno **siembra el defecto** que el checker debe cazar en un corpus falso, mas el contrapeso (corpus limpio -> sin defectos). Incluye los dos casos de exit code (1 con defecto, 0 sin el): juntos prueban que el codigo de salida discrimina.

### Fixed
- **Enganchado al pre-commit hook** (`scripts/pre-commit.template` + hook instalado, mantenidos identicos): corre junto a `check_em_dash.py` y `check-refs.py` cuando hay markdown staged.
- **`docs/SETUP.md`:** fila del script en la tabla.

### Notes
- **Hueco que cierra, con evidencia:** ADR-063 existia y estaba commiteado, pero sin fila en el indice, y **nada lo detectaba**. `check-refs.py` valida que una ruta citada exista, no la direccion inversa (que todo ADR este en el indice). Se encontro leyendo. Un ADR fuera del indice es un ADR que nadie encuentra.
- **Probado por mutacion:** desactivando el chequeo 1, fallan exactamente los 2 tests que lo cubren. Un test que no puede fallar no verifica nada.
- **Dos decisiones de diseño que evitan trampas:** (1) las rutas son inyectables, asi los tests usan un corpus desechable en `tmp_path`; la primera version sembraba el defecto editando el README real y restaurandolo con `git checkout`, y si fallaba a mitad dejaba el indice del workspace roto - el mismo riesgo que el script existe para prevenir. (2) Usa `Optional` en vez de `X | None`: este equipo corre **Python 3.9.6**, y las uniones PEP 604 son 3.10+.

---

## [2026-09-24] - memory-wiki activado + regla DB-first vs doc-only + ADR-064/065

### Added
- **`docs/adr/ADR-064-memory-wiki-capa-analitica.md`:** se activa `memory-wiki` (bundled v2026.9.5) como capa analitica de memoria en modo `isolated`. Estaba instalado pero deshabilitado, con una skill del workspace que lo asumia activo y un pendiente abierto desde el 2026-09-22. Documenta la diferencia con memory-core, la verificacion end-to-end (incluida la sonda de detectores) y la politica de ingesta: arranca por `docs/`, nunca `memory/` ni `docs/entrevistas/` sin decision explicita.
- **`docs/adr/ADR-065-db-first-vs-doc-only.md`:** formaliza las dos clases de superficie de la memoria. DB-first (el dato vive en la DB, el `.md` es vista regenerable) vs doc-only (el archivo ES la fuente de verdad). Verificado: `memory.db` tiene 20 tablas y ninguna de ADR; los ADR solo aparecen como texto incidental.
- **`docs/SETUP.md`:** seccion "Regla: DB-first vs doc-only" con la tabla de documentos por clase y la regla practica de busqueda.

### Fixed
- **`docs/adr/README.md`:** agregadas las filas de ADR-064 y ADR-065. Corpus en 65/65, sin duplicados ni huecos.

### Notes
- **Hallazgo central de memory-wiki:** la ingesta sola NO alimenta los reports. `provenance-coverage` lo dijo explicito ("No structured claims with provenance coverage yet"): el analisis opera sobre la capa de **claims**, no sobre texto crudo. El flujo real es `ingest` (evidencia) -> `entities con claims` (conocimiento) -> `compile/lint` (analisis). Sin el paso intermedio el vault es evidencia inerte.
- **Detectores probados con sonda deliberada** (claim sin evidencia, confianza 0.2, `contested`, fecha vieja): `claim-health`, `low-confidence` y `stale-pages` reportaron los tres defectos y `lint` paso de 0 a 3 issues. Borrada la sonda, los reports se limpiaron solos.
- El plugin pide grants amplios (`allowConversationAccess`, `allowPromptInjection`): es bundled, pero conviene saberlo.
- `~/.openclaw/wiki/main` **no esta en el workspace git**: el conocimiento compilado ahi no tiene backup por versionado.

---

## [2026-09-24] - ADR-063 agregado al indice (corpus 63/63)

### Fixed
- **`docs/adr/README.md`:** faltaba la fila de `ADR-063` (kanam-insight en Python sobre LangChain). El archivo existia y estaba commiteado desde el 2026-09-24 14:11, pero el indice quedaba en 62: un ADR fuera del indice es un ADR que nadie encuentra. Corpus reconciliado: 63 en disco, 63 indexados, sin duplicados ni huecos.

### Notes
- Detectado durante la prueba de memory-wiki: la ingesta del indice de ADRs dejo el hueco a la vista. Es el tipo de contradiccion entre documento y estado real que el wiki deberia detectar solo, y que en este caso se encontro leyendo.
- El ADR lo creo otra sesion (kanam-insight, apuesta 1). No se toco su contenido, solo se agrego la fila faltante una vez que esa sesion termino, para no pisar trabajo en curso.

---

## [2026-09-24] - Regla DB-first vs doc-only documentada en SETUP.md

### Added
- **`docs/SETUP.md` seccion "Regla: DB-first vs doc-only":** la memoria del workspace tiene dos clases de superficie y confundirlas manda a buscar en el lugar equivocado. Se documenta explicito, porque la distincion se reconstruyo a mano el 2026-09-24 (pregunta de Gonzo).
  - **DB-first (dentro del ciclo de `memory.db`):** el dato vive en la DB y el markdown es vista regenerable; si discrepan, gana la DB. Aplica a dailies, `todos.md`, `inbox.md`, `OSS-TRACKER.md` y `learnings/`.
  - **Doc-only (fuera del ciclo):** el archivo ES la fuente de verdad, sin tabla ni export. Aplica a `MEMORY.md`, `AGENTS.md`, `SOUL.md`, `USER.md`, `IDENTITY.md`, `NORTH.md`, `ROADMAP.md`, el corpus de ADRs y el resto de `docs/`.
  - **El caso de los ADR:** no existe tabla `adr` ni `decision`; los ADR solo aparecen en la DB como texto incidental (alguien los nombra en un daily o leccion), nunca como registro consultable. Para auditarlos hay que leer los archivos. Su camino a un almacen de conocimiento es el wiki (`openclaw wiki ingest`), no `memory.db`.

### Notes
- **Verificado, no asumido:** se confirmo contra el esquema real de `memory.db` (20 tablas, ninguna de ADR) y contra el flujo de scripts (`export-*` solo cubre dailies/todos/inbox/oss/learnings).
- Origen del hallazgo: al verificar la hipotesis de Gonzo ("los ADRs van en direccion opuesta, de los documentos a la DB"). La intuicion era real pero el nombre estaba corrido: los ADR no van hacia la DB, van **fuera** del ciclo de la DB.

---

## [2026-09-24] - Dashboard de Kanam OS como servicio permanente (LaunchAgent)

### Added
- **`projects/kanam-os` corre como LaunchAgent** (`dev.gonzoblasco.kanam-os`), accesible en tres URLs: `http://192.168.100.7:4317` (LAN, IP actual de `en0`), `http://mac-mini-de-gonzalo.local:4317` (LAN, resuelve por IPv4) y `http://127.0.0.1:4317` (local). Existe porque correrlo desde una sesion del agente no servia: el dev server muere con el turno y el link del portal muere cuando reinicia el Gateway. Ahora sobrevive al Gateway, a la sesion y al reboot.
- **Escucha en la red local** (pedido de Gonzo 2026-09-24). Bindea a `0.0.0.0` y NO a la IP fija: `en0` es DHCP, asi que `192.168.100.7` puede cambiar y un servicio atado a una direccion que ya no existe quedaria escuchando en el vacio. Escuchando en todas sobrevive al cambio y sigue respondiendo en `127.0.0.1`, que es lo que necesita el portal del Gateway.
- **`scripts/dashboard.sh`** (`start|stop|restart|status|url`): control para humanos. Maneja el servicio via `launchctl` y NUNCA arranca un server por su cuenta (un `next start` suelto chocaria con el de launchd).
- **`scripts/watchdog.sh`** + su plist: recuperacion cada 60s que respeta la parada deliberada (marcador `config/.intentional-stop`, que `stop` deja y `start` saca). Sin ese escape, apagar el dashboard seria imposible.
- **`app/health/route.ts`**: health check con `force-dynamic`, para que no se cachee. Un health cacheado responderia "ok" con el server caido, o sea lo contrario de lo que tiene que detectar.

### Changed
- **`.openclaw/portals.json`** apuntaba a `npm run dev`, que choca con el servicio: un `next dev` pelea por el directorio `.next` con el `next start` de launchd y tumba ambos (paso durante esta sesion, tres veces). Ahora apunta a `scripts/dashboard.sh start` y lo explica en la descripcion.

### Notes
- **Dos decisiones que evitan los fallos clasicos de LaunchAgent.** (1) `KeepAlive <true/>` sin condicion: `{SuccessfulExit: false}` no cubre el caso mas probable, y el test de matar el proceso no lo detecta porque SIGTERM es una salida anormal. (2) El comando real va en el plist, no detras de un wrapper: un script con guard "ya esta corriendo -> exit 0" termina el job limpiamente y nada lo revive.
- **Hallazgo al probar la salida limpia:** SIGTERM da **exit 143**, que es anormal, asi que ese test NO prueba el caso limpio. Medido aparte: un `next start` con el puerto tomado sale con **codigo 1**, no 0. El intento de probar el caso limpio con un agente de prueba fallo dos veces por error de bootstrap (5: Input/output error) y se abandono; queda documentado que el caso limpio no se verifico de forma directa.
- **Verificado en vivo:** arranca y sirve (8 vistas 200 + `/health` ok); `kill -9` -> revivido en ~8s; parada deliberada -> tras un tick completo (68s) el servicio sigue abajo y el watchdog no registro intento; `restart` deja todo arriba.
- **Las ESCRITURAS se verificaron por LAN, no solo la lectura.** Un POST de server action contra el host LAN devolvio `Set-Cookie`, o sea que paso la validacion de origen de Next: con server actions, cambiar el host de acceso es justo el caso que rompe por mismatch de `Origin`.
- **ALCANCE ABIERTO (decision explicita de Gonzo):** la app **no tiene autenticacion** y tiene superficies de escritura (`settings`, `inbox`, `todos`, `fichas`). Queda accesible desde cualquier equipo de la LAN, y el firewall de macOS esta **deshabilitado**, asi que nada filtra. Es aceptable en una red domestica; si la red deja de ser confiable, hay que volver a `127.0.0.1` (una linea en el plist).
- Si el Gateway se reinicia, esta URL sigue viva (no depende del portal). El portal puede seguir usandose para verlo embebido en el Control UI, pero ya no es la unica via.

---

## [2026-09-24] - Temas dark y light en kanam-os + guardia multi-tema

### Added
- **Selector de tema en kanam-os (dark / light):** pedido de Gonzo. El tema se guarda en una cookie y lo resuelve el **servidor** en `app/layout.tsx`, escribiendo `<html data-theme>`. La via de cliente (localStorage + script) pintaria primero el tema por defecto y despues saltaria al elegido: un flash visible en cada carga. El selector es un `<form>` con server action, asi funciona tambien sin JS, y usa `aria-pressed` (son dos opciones de un grupo, no dos botones sueltos).
- **`app/globals.css` con dos bloques de tema:** los MISMOS nombres de variable (`--bg`, `--text`, `--accent`...), asi ningun componente sabe que tema esta activo. Los valores NO son simetricos: el accent del tema oscuro (`#6ee7a0`) sobre blanco da 1.54:1, ilegible.

### Fixed
- **Seis colores hardcodeados pasaron a variables por tema.** `.badge-open`, `.badge-waiting_review`, `.badge-comment`, `.btn-warn` y `.chip-clear` tenian hex escritos a mano dentro de sus reglas. Dos son **controles** y incumplian WCAG 1.4.11 (1.24:1). Ademas un hex a mano esquiva cualquier validacion que solo mire las variables, y con dos temas el problema se duplica.
- **`scripts/check-contrast.py` ahora cubre TODOS los temas.** Revisar uno solo deja el agujero abierto justo al agregar el segundo. Descubre los temas del CSS (`:root` + cada `[data-theme="X"]`), y evalua los hardcodeados contra todos: un color a mano tiene que cumplir en ambos.
- **`iter_top_blocks` calculaba offsets sobre el CSS sin comentarios y los aplicaba al original.** Los indices quedaban corridos y una mutacion de prueba cambiaba la variable equivocada. Se detecto porque un test daba OK cuando tenia que fallar. Ahora `block_spans()` recorre con conciencia de comentarios.
- **Cinco tests quedaron atados a un estado concreto** (asumian 1 ocurrencia por variable, o buscaban hex que ya no existian). Reescritos para buscar por **nombre** de variable y mutar un solo tema.

### Notes
- **Hallazgo de medicion:** recorriendo los grises, el unico que llega a 3:1 en los dos temas es `#888888` (min 3.07). Ese limite no es casualidad: es la razon de que cada tema tenga su propia paleta en vez de compartir colores fijos. Un hardcodeado "neutro" como `#000000` es ilegible en el tema oscuro (1.47:1).
- **Claridad medida (CIE L*):** el tema oscuro quedo en bg L* 17.4 (referencia: VS Code dark+ 11.6, Dracula 17.2) y el claro en 97.7. Gonzo habia reportado DOS veces que estaba "demasiado oscuro": el primer ajuste subio de 4.0 a 6.6 y no se percibio (2.6 puntos no se notan).
- Los 17 errores de `biome check` en kanam-os son **preexistentes**: verificado con `git stash`, identicos con y sin estos cambios. No se tocaron (fuera del alcance).

---

## [2026-09-24] - Guardia de contraste WCAG para la paleta de kanam-os

### Added
- **`scripts/check-contrast.py`:** revisa el contraste WCAG 2.1 del CSS real de kanam-os y falla con exit 1 si el texto baja de 4.5:1 (AA), el borde de un CONTROL baja de 3:1 (1.4.11), el indicador de foco baja de 3:1 (1.4.11 + 2.4.7), o desaparecen las reglas `:focus-visible`. Existe porque el contraste se habia revisado a mano UNA vez y una revision manual no protege nada: el proximo cambio de color lo rompe sin que nadie note.
- **`tests/python/test_contrast.py`:** 10 tests. El central es `test_detecta_la_paleta_vieja`, que prueba que el chequeo PUEDE fallar usando la paleta que tenia el defecto real.

### Fixed
- **La auditoria manual de contraste estaba rota.** Comparaba claves con `--` contra claves sin `--`, asi que nunca encontraba un par y reportaba "0 fallas". Detectado al correrla y ver que devolvia cero pares sobre un CSS con 9: un chequeo que no puede fallar no verifica nada. El script nuevo extrae las variables quitando el `--` en un solo lugar.
- **Un test nacia ciego, igual que el bug que previene.** `test_detecta_falta_de_foco_visible` renombraba `focus-visible` a `focus-visible-x`, que contiene el original como substring: el check seguia viendolo y el test fallaba. Ahora reemplaza el token completo y verifica con un assert que desaparecio.

### Notes
- El defecto real que motiva el guardia: `.input`, `.btn` y `.chip` usaban `--border` (#24302d) como limite de componente = **1.31:1** sobre panel, cuando 1.4.11 pide 3:1. Y `.input:focus` tenia `outline: none` con borde accent-dim (**2.97:1**): navegar con teclado era a ciegas.
- La app tiene su propio commit (`kanam-os` 997a5a4) con la paleta corregida. El workspace ignora `projects/*/*`, asi que el codigo de la app no viaja en este repo: por eso el chequeo se registra como test de la suite, no como hook del pre-commit.

---

## [2026-09-24] - Handoff Synthesizer: el tercer pilar (kanam-insight completo)

### Added
- **`kanam-insight/scripts/handoff.py`:** responde "donde esta parado este proyecto y que sigue?" y detecta la desalineacion entre STATUS (que paso), HANDOFF (punto de retorno) y ROADMAP (que falta). Estructural, sin vectores ni LLM.
- **Checks:** `SIN_PUNTO_DE_RETORNO` (sin HANDOFF ni ROADMAP), `HITO_SIN_ESTADO` (hitos despues de uno completado sin marcador), `FASE_FUERA_DE_ORDEN`, `ROADMAP_VIEJO` (roadmap mas viejo que el estado).
- **`docs/insights/handoff-2026-09-24.md`:** primer reporte. 26 proyectos, **11 con desalineacion**.
- **8 tests nuevos** (32 en total, eran 25).

### Fixed
- **`STATUS_VIEJO` y `ROADMAP_VIEJO` eran codigo muerto.** `parse_date` no matcheaba `ACTUALIZADO` en mayusculas, y varios docs lo escriben asi: el check **nunca disparaba**. Corregido con `IGNORECASE`. Ahora `create-stack` (66 dias sin actualizar) aparece como debe.
- **`HITO_SIN_ESTADO` estaba condicionado a que existiera STATUS/HANDOFF**, pero la consistencia interna del ROADMAP no depende de eso. Lo destapo un test, no la corrida real.
- **`last_phase_line` devolvia el heading** (`## Estado actual`) en vez de su contenido, y arrastraba marcas de markdown. Corregido, cuidando no mutilar contenido real ('Fase 1 (lectura)' se preserva).

### Notes
- **Kanam-insight queda completo:** los tres pilares (Pattern Radar + Debt Detector + Handoff Synthesizer) operativos, 32 tests, 2 repos sincronizados.
- **Un tercer bug de metodo, y van cuatro hoy:** la mutacion destapo que un test mio era debil. La asercion `not startswith("Nota")` pasaba igual con el valor mutado, porque el string venia con marcas (`**Nota Fase 0:**`). Reforzado con una asercion que si discrimina; la mutacion ahora falla como debe.
- **Hallazgo real del sintetizador:** 11 de 26 proyectos no tienen HANDOFF ni ROADMAP. No es alarma (muchos estan cerrados o archivados), pero explica por que retomar un proyecto viejo cuesta: no hay punto de retorno escrito.

## [2026-09-24] - Fase 5.2: ingesta real (el radar ahora cruza todo el conocimiento)

### Added
- **`kanam-insight/scripts/scan.py`: escaneo de 3 fuentes.** Antes solo los `.knowledge/` de proyectos (122 archivos); ahora tambien `docs/` estrategicos y `skills/` (445 archivos, 2.496.240 chars). Nuevo flag `--source {all,projects,docs,skills}`.
- **4 tests nuevos** (25 en total, eran 21): escaneo multi-fuente, exclusion de `insights/` y `archives/`, aislamiento de `--project`, y deteccion del tipo `SKILL`.

### Changed
- **Indice: de 1243 a 4423 vectores.** Reindexado con el corpus extendido.
- **`kanam-insight/README.md`:** la seccion de alcance refleja las 3 fuentes y documenta las exclusiones.
- **`kanam-insight/.knowledge/STATUS.md`:** numeros reales y fase 5.2 cerrada.

### Fixed
- **Bug en `scan_workspace()` encontrado por los tests:** la primera version usaba las constantes `DOCS_DIR`/`SKILLS_DIR` del modulo, asi que ignoraba el `tmp_path` de los tests y leia los docs reales del workspace. Corregido derivando las rutas de `WORKSPACE` en cada llamada. **En produccion habria pasado desapercibido:** el escaneo funcionaba igual, solo era intesteable.
- **Bug de IDs duplicados en `index.py` (encontrado al verificar el indexado, horas despues):** los IDs de chunk se generaban con el **nombre de archivo**, asi que archivos homonimos en carpetas distintas colisionaban (`docs/README.md` vs `docs/adr/README.md` -> ambos `docs::README.md::0`). Eran 142 colisiones reales. Chroma rechaza IDs repetidos dentro de un lote y **abortaba el indexado a la mitad**. El indice quedo con 1920 vectores y se reporto 2557 como exito: **el numero era de una corrida parcial, no completa.** Corregido: IDs por **ruta relativa** (unica) + un guard que valida la unicidad **antes** de tocar la coleccion, para que falle ruidoso en vez de dejar el indice a medias. Reindexado completo: **4423 vectores**, verificado con busqueda y radar.
- **`metadata.source_kind`:** el metadata no guardaba la fuente, asi que las consultas por fuente devolvian `None`. Agregado.

### Decisions
- **El criterio de 5.2 tal como estaba escrito ya se cumplia** ("preguntar algo de una sesion pasada con cita de fuente"): `memory.db` ya indexa los dailies y las sesiones (1144 secciones `daily` + 843 `session`). Verificado ANTES de indexar, para no duplicar. Se indexo lo que faltaba de verdad: docs estrategicos y skills.
- **Excluidos a proposito:** `docs/insights/` (reportes del propio Debt Detector: indexarlos es ruido auto-referencial y quedan vencidos) y `docs/archives/` (historico).

### Notes
- **Fase 5 CERRADA** (5.1 deuda de base + 5.2 ingesta real + 5.3 red de seguridad). El hito se cumple: el servicio responde sobre nuestro propio historial con cita de fuente, y es reproducible en otra maquina.
- **Cruce nuevo que antes era imposible:** el radar acerco `docs/ADR-057` (SQLite local con BLOB float32) con `soporteml-v3` (Postgres con ivfflat) para el mismo problema de vectores, resuelto distinto segun escala. Ese par de decisiones vivia en silos.
- **Lo que sigue (Fase 6):** multi-cliente (Supabase Vector, namespaces por tenant, auth) o el Handoff Synthesizer (tercer pilar de kanam-insight).

## [2026-09-24] - Auditoria de la base: la deriva que el propio detector no veia

### Changed
- **`LANGCHAIN_STRATEGY.md` movido de la raiz a `docs/`.** Es documentacion estrategica, no bootstrap del agente: junto a NORTH, ROADMAP y APUESTAS. Referencias actualizadas en `projects/langchain-starter/README.md`, su HANDOFF y `docs/APUESTAS.md`.
- **Fases 1 y 2 marcadas como COMPLETAS** (estaban sin marcar desde el 2026-09-22 pese a estar hechas). 1.2 (secretos) pasa a "no aplica hoy": no hay API keys que gestionar con Ollama local.
- **Seccion 2 (stack) corregida:** declaraba Supabase Vector + Docker + Python 3.11; lo construido es ChromaDB local + LaunchAgent + Python 3.12. Se distinguio el plan del estado real.
- **Seccion 5 (deuda):** 6 de 8 items pasaron a cerrados con evidencia. Quedan 2 abiertos: la ingesta real y el `requirements.txt` propio de kanam-insight.
- **5.3 (red de seguridad) marcada como hecha.**

### Added
- **`projects/kanam-insight/requirements.txt`:** hallazgo de la auditoria. kanam-insight es un repo independiente pero **dependia del venv de langchain-starter**: clonarlo solo y hacer `pip install` no alcanzaba. Ahora se reproduce solo (verificado con un venv limpio desde cero: 21 tests en verde y el radar leyendo el indice).
- **Seccion 5b del documento: causa raiz de la deriva.** El doc vive en la raiz y el Debt Detector solo escanea `projects/*/.knowledge/`: era **ciego a la documentacion de nivel workspace**. Tres derivas acumuladas sin que la herramienta que construimos para detectar derivas las viera.
- **Debt Detector: cobertura de `docs/` del workspace.** Nuevo check `REF_ROTA_DOC_WORKSPACE`. Al agregarlo aparecieron 5 refs rotas y **4 eran falsos positivos de la misma clase ya conocida** (en un doc estrategico, `scripts/ingest.py` es del proyecto que describe, no del workspace; y `<repo>-<numero>-draft.md` es un placeholder, no un path). Corregidos, con 3 tests nuevos que fijan los limites.

### Fixed
- **`.gitignore` de ambos proyectos:** el patron `venv3*/` era demasiado estrecho y no cubria `venv-test-standalone`. Ahora `venv*/` y `.venv*/` cubren cualquier nombre auxiliar.

### Notes
- **Tercera vez en el dia que aparece el mismo patron:** documentacion que declara un estado vencido, sin nada que lo verifique. Las tres veces el problema lo encontro una persona preguntando, no una herramienta.
- **Leccion:** un verificador con alcance limitado da falsa sensacion de cobertura. El Debt Detector escaneaba 26 proyectos pero era ciego a la documentacion mas estrategica, la de nivel workspace.
- **Verificado por mutacion:** reintroducir el falso positivo hace fallar el test nuevo.

## [2026-09-24] - Migracion del venv a Python 3.12 (era 3.9.6)

### Changed
- **`projects/langchain-starter/venv` migrado de 3.9.6 a 3.12.14.** El venv es compartido con `kanam-insight`, asi que la migracion alcanza a los dos proyectos.
- **`requirements.txt`:** la cabecera ya no declara 3.9.6 como deuda.
- **`README.md` de langchain-starter:** la seccion de estado refleja 3.12.14.
- **`.gitignore` de ambos proyectos:** ahora cubren `venv3*/` y `venv3*-backup/` (los nombres que usa una migracion de version). Sin esto, un venv de backup habria aparecido en `git status`.
- **`LANGCHAIN_STRATEGY.md`:** el item de Python en la deuda tecnica marcado como cerrado; **5.1 (deuda de base) queda completa** (requirements pinneados + 3.12 + repo git + README + .env.example).
- **`docs/adr/ADR-063`:** la consecuencia negativa sobre 3.9 marcada como cerrada.

### Notes
- **Proceso sin downtime:** el venv 3.12 se construyo aparte y se valido ANTES del swap (10 tests del starter + 18 de kanam-insight en verde, el indice Chroma de 1243 vectores legible desde 3.12, busqueda funcionando, embeddings de 1024 dim). Recien entonces se swapeo.
- **El venv nuevo se creo DIRECTO en la ruta final** (`venv`), no renombrado: renombrar un venv rompe los shebangs del binario (leccion del 2026-09-22 aplicada).
- **Venvs temporales a Trash**, no `rm`: recuperables si algo salia mal.
- **Verificacion end-to-end post-migracion:** RAG via API (`POST /chat`) y agente con tools, ambos funcionando. El proceso del servicio corre bajo `python@3.12`.

## [2026-09-24] - Tests: red de seguridad para ambos proyectos (28 tests)

### Added
- **`langchain-starter/tests/test_starter.py`** (10 tests): chunking con metadata de fuente, **overlap entre chunks**, prompt restringido al contexto, `/health` sin depender del LLM, input vacio sin gastar llamada al modelo, `--ingest` con 404 explicito, y RAG end-to-end (marcado, se salta si Ollama no responde).
- **`kanam-insight/tests/test_insight.py`** (18 tests): scanner (tipo de doc, ADR con sufijo, frontmatter, subcarpetas), chunking semantico, y los **tres limites aprendidos del Debt Detector** fijados como propiedades.

### Fixed
- **`langchain-starter/requirements.txt` no declaraba pytest.** Los tests no corrian desde un clone limpio. Deuda cerrada en el mismo paso.

### Notes
- **Los tests se verificaron mutando el codigo a proposito** (romper cada propiedad y confirmar que el test falla). No alcanza con que esten en verde.
- **Hueco encontrado por mutacion:** poner `chunk_overlap=0` pasaba los 9 tests originales **en verde**. El overlap es lo que evita perder una idea que cae en el borde entre dos chunks, y su falla es silenciosa (la busqueda simplemente deja de encontrar cosas del borde). Se agrego el test faltante; la mutacion ahora falla como debe.
- **Los tests de kanam-insight testean funciones puras con `tmp_path`**, sin depender del corpus real del workspace: un test que cambia cuando cambia el contenido no sirve como red de seguridad.
- Los tres falsos positivos del Debt Detector quedaron fijados como propiedades testeables: sin repo clonado no se puede afirmar que un doc falte; un basename igual en otro proyecto no es el mismo archivo; los globs no son paths.

## [2026-09-24] - Versionado: kanam-insight y langchain-starter van a GitHub

### Added
- **`gonzoblasco/kanam-insight`** (PRIVADO): repo que ya existia desde el 2026-08-30 pero **vacio** (nunca se le pusheo nada). Ahora con codigo: `scripts/{scan,index,radar,debt}.py`, README, `.gitignore`.
- **`gonzoblasco/langchain-starter`** (PRIVADO, nuevo): `app/`, `scripts/`, `config/*.plist`, `Dockerfile`, README, `.env.example`, `requirements.txt`.

### Fixed
- **`langchain-starter/requirements.txt` estaba VACIO (0 bytes).** Ahora con 15 dependencias de nivel superior con version fija, tomadas del venv real. Sin esto el repo no era reproducible.
- **`langchain-starter/README.md` tenia 8 bytes** (la palabra "FastAPI"). Reemplazado por documentacion real: arquitectura, instalacion, endpoints, uso del servicio.
- **`langchain-starter/.env.example` estaba vacio.** Ahora con el contrato de configuracion completo.

### Notes
- **Regla del triple git respetada:** cada repo de proyecto excluye `.knowledge/` via `.git/info/exclude`; esa memoria sigue viviendo en el workspace git.
- **Lo que NO se versiono (y por que):** `venv/` (332 MB), `logs/`, `config/chroma_db/` de ambos proyectos, y `.env`. Cubiertos por `.gitignore` propio de cada proyecto.
- **Scan de secretos previo al push:** limpio. No hay API keys en el codigo (el proyecto usa Ollama local, sin proveedores cloud).
- **Brecha cerrada.** Hasta hoy, el codigo de ambos proyectos existia **solo en disco**: el workspace git trackea `projects/*/.knowledge/`, no el codigo. El Debt Detector lo habia señalado horas antes.

## [2026-09-24] - kanam-insight: Debt Detector operativo

### Added
- **`projects/kanam-insight/scripts/debt.py`:** deteccion estructural de deuda en los 26 proyectos del workspace. Sin vectores ni LLM (comparar fechas, refs y backlog no requiere semantica). Checks: doc base ausente, doc fuera de `.knowledge/` (no versionado), STATUS viejo/sin fecha, pendientes acumulados, referencias rotas, docs sin fecha. Reporte en `docs/insights/YYYY-MM-DD.md`.
- **`docs/insights/2026-09-24.md`:** primer reporte del detector.

### Fixed
- **Tres clases de falso positivo del detector**, detectadas al verificar cada hallazgo contra los archivos reales (la primera corrida reporto 27 hallazgos de severidad alta que no eran todos ciertos):
  1. Docs base en la raiz del proyecto contados como ausentes (existen, fuera de `.knowledge/`).
  2. Refs con glob (`scripts/*.py`) tratadas como paths concretos.
  3. Refs de proyectos sin repo clonado tratadas como rotas (pueden vivir en GitHub).

### Notes
- **Hallazgo real:** el ADR de Lucide fue **renumerado de 030 a 037** (commit `1769ecc1`); dos docs de `soporteml-v4` siguen apuntando al numero viejo. Deuda invisible a la lectura manual. El detector ahora la señala con el numero actual.
- **Hallazgo real:** `quienes_quedan/BRIEF.md` y los docs base de `kanam-fixer-v2` viven en la raiz de su proyecto, **no en `.knowledge/`**, asi que el workspace git no los trackea (`.gitignore` solo incluye `projects/*/.knowledge/`). Sin repo propio, esos docs no estan versionados en ningun lado.
- **Regla que quedo:** sin el repo del proyecto clonado no se puede afirmar que un doc falte. Solo la renumeracion de ADR es señal inequivocamente nuestra. Un detector sin verificacion propia produce deuda de credibilidad.
- Solo 6 de 26 proyectos tienen repo git local (`kanam-fixer`, `kanam-lab`, `kanam-os`, `kanam-skills`, `kanam-tetris`, `soporteml`).

## [2026-09-24] - kanam-insight arrancado (apuesta 1): Pattern Radar operativo

### Added
- **`projects/kanam-insight/scripts/scan.py`:** scanner de los `.knowledge/` de todos los proyectos. Solo stdlib, sin dependencias. Verificado: 122 archivos, 24 proyectos, 768.465 chars.
- **`projects/kanam-insight/scripts/index.py`:** indexado con chunking por unidad semantica (ADR-062: secciones de markdown con el titulo al frente, no ventana ciega). Coleccion propia `insight_knowledge`, separada de la del starter. Verificado: 1243 vectores.
- **`projects/kanam-insight/scripts/radar.py`:** Pattern Radar (cruce de patrones entre proyectos + sintesis con LLM) y busqueda semantica con citas de fuente.
- **`projects/kanam-insight/README.md`:** superficie del proyecto (que hace, stack, alcance, privacidad, ejemplo de salida).
- **`docs/adr/ADR-063-kanam-insight-python-langchain.md`:** decision de stack.

### Changed
- **`projects/kanam-insight/.knowledge/`** (BRIEF, STATUS, HANDOFF): spec corregido al stack real. El original (2026-08-30) declaraba TS + Bun + SQLite-vec "confirmado", pero quedo **anterior** a la construccion de `langchain-starter` (2026-09-22). Se reusa la capacidad existente en lugar de reconstruirla en otro lenguaje.

### Decisions
- **Python + LangChain, no TypeScript + Bun** (ADR-063). Razon: el starter ya resuelve ingesta, chunking, embeddings y retrieval; el stack de memoria del workspace ya es Python con vectores funcionando (ADR-062). Construir en TS duplicaria la capacidad.
- **Solo `.knowledge/` de proyectos** en esta fase. `docs/` y `memory/` quedan afuera: los dailies son ruido para el retrieval, las entrevistas no aportan al cruce.
- **Solo el Pattern Radar es semantico.** El Debt Detector y el Handoff Synthesizer seran estructurales (comparar fechas y estados, no similitud), segun el hallazgo del ADR-062.

### Notes
- **Hallazgo del radar:** `kanam-fixer` y `kanam-story` coinciden, por vias distintas, en que los tests verdes no alcanzan para validar el anuncio de un lector de pantalla. Verificado contra los archivos fuente.
- **Deuda registrada:** el codigo de kanam-insight (scripts, README) **no esta en ningun repo** - el workspace git solo trackea `projects/*/.knowledge/`. Misma brecha que `langchain-starter`. Pendiente: repo en GitHub.
- **Leccion de metodo:** un spec que declara un stack "confirmado" puede estar vencido si se escribio antes de construir la alternativa. Los specs con fecha vencen; se revisan al arrancar.

## [2026-09-24] - Registro de apuestas + punto de retorno pre-kanam-insight

### Added
- **`docs/APUESTAS.md`:** registro durable de las apuestas evaluadas con orden de prioridad confirmado por Gonzo (1. kanam-insight, 2. soporteml-v4, 3. kanam-fixer), las cuatro capas (infraestructura / uso interno / producto / personal), el razonamiento de cada lugar en el orden, lo descartado explicitamente (el encuadre "enciclopedia de accesibilidad") y el principio rector. Incluye el punto de retorno.

### Changed
- **`LANGCHAIN_STRATEGY.md` seccion 6:** corregido el encuadre que titulaba una "primera apuesta comercial" sobre accesibilidad, lo que sugeria que era la unica apuesta. Ahora referencia `docs/APUESTAS.md` como registro unico y deja escrita la correccion.
- **Fases 1-4 marcadas como completadas** en el mismo documento (incluye el despliegue real por LaunchAgent + watchdog, no Docker). Agregadas secciones 5 (deuda tecnica detectada) y 6 (fases 5-7).

### Notes
- Tag `etapa-2026-09-24-pre-kanam-insight`: sellado para poder volver a esta etapa sin perder estado. Cubre lo trackeado por el repo del workspace; NO cubre el codigo de proyectos (viven en sus repos) ni `langchain-starter` (aun sin repo propio).
- El repo agregado (`projects/` -> `projects_openclaw`) no esta clonado en esta maquina; el script `aggregate-sync.sh` fallaria si se invoca aca.

## [2026-09-24] - Provisioning de browsers de Playwright: el zip a mano y los markers

### Added
- **`scripts/playwright-provision.sh`:** provisiona un browser de Playwright cuando `playwright install` se cuelga al extraer o deja el build incompleto. Saca la URL con `--dry-run`, baja el zip con `curl`, lo descomprime en el install location y crea los dos markers. Idempotente: si el build ya esta completo, no hace nada.

### Fixed
- **Un build completo en disco sin `INSTALLATION_COMPLETE` es borrado por el siguiente `playwright install` de CUALQUIER engine.** Verificado dos veces el mismo dia: el instalador de firefox borro el `webkit-2227` que se habia extraido a mano (quedo con solo `libwebrtc.dylib`), y el `firefox-1497` real estaba en 888K cuando el build completo pesa 253M. El script detecta el build incompleto, lo reemplaza y escribe los markers.

### Notes
- **Validado reparando el cache real:** el `firefox` paso de 888K a 253M y su suite de browser, que antes crasheaba al lanzar, quedo verde. Los tres motores (chromium, firefox, webkit) corren el mismo set de tests.
- **Los dos markers importan:** `INSTALLATION_COMPLETE` **y** `DEPENDENCIES_VALIDATED`. Con uno solo, el build se considera incompleto.
- **`trash` antes que `rm`:** es cache regenerable, pero el camino reversible es el default.

---

## [2026-09-23] - Vectores re-cortados por unidad semantica, sin duplicar el texto

### Added
- **`scripts/rechunk-vectors.py`:** re-corta los vectores por unidades semanticas. 781 vectores de ficha (eran 136 con corte ciego) + 2352 de seccion.
- **`scripts/chunk-util.py`:** el corte de texto, en un solo lugar. `rechunk-vectors.py` (que genera) y `memory-search.py` (que muestra) lo comparten.
- **Busqueda en dos niveles:** la busqueda devuelve fichas y fragmentos de seccion, estos ultimos con su fecha y hora.

### Fixed
- **El corte ciego de 1500 caracteres partia el 29% de los chunks a mitad de frase.** Un fragmento que empezaba en `'should be archived to...'` no representa su contenido, y la busqueda lo devolvia por parecido con cosas sin relacion.
- **El 15% de los chunks era el volcado del harness** (`# Session: ... Session Key`): se vectorizaba metadata en vez de contenido.
- **18 fichas no tenian vectores.** El script las salteaba por no tener unidades de tema; medido antes de descartarlas, 17 tienen contenido propio y 0 estan duplicadas.
- **`chunk_text` duplicaba 2.16 MB.** El 75% era identico al cuerpo de su seccion, que ya vive en el padre. Se elimino la columna: el texto se reconstruye desde los offsets. Importa porque **memory.db esta trackeada en git**: la duplicacion crecia la historia del repo en cada commit.
- **`split_large` y `strip_harness_header` estaban duplicadas en dos scripts.** Ahora hay una sola fuente, y un test prohibe redefinirlas.
- **`memory-search.py` reconstruia el texto con `chunk_idx * 1500`**, asumiendo el corte viejo. Ahora usa el mismo modulo que lo genera.

### Notes
- **La busqueda mejora de verdad.** La consulta sobre "mantener la confianza del usuario" traia ".v1.0.0 released"; ahora trae fragmentos del tema (0.733 en una consulta sobre TreeList a11y).
- **Los vectores NO son la herramienta principal.** Medido: el SQL estructurado gana para topics, TODOs y estados (exacto y rapido); los vectores sirven para cuando no se recuerda la palabra exacta. Queda pendiente estudiar como se enseña esa distincion.
- **La DB subio de 4.4 a 19.1 MB** (los 2352 vectores de seccion pesan 9.6 MB). El ahorro de no duplicar texto fue 1.7 MB.
- **`learnings` sigue con vectores en JSON** (22 KB cada uno, el formato viejo, contra 4096 bytes en BLOB). Migrarlo es trabajo pendiente.
- **Verificado:** 156 tests, 0 violaciones de FK, 0 chunks con volcado del harness, 0 chunks semanticos sin titulo, 0 huerfanos.
- ADR-062.

---

## [2026-09-23] - Campos interpretados con revision: el LLM propone, la persona aplica

### Added
- **Ciclo completo en `interpret-entries.py`:** `--review` (ver), `--approve` / `--reject` (decidir), `--apply-dry-run` (simular), `--apply` (escribir). Nada se aplica sin pasar por la aprobacion humana.
- **Columna `session_entries.activity`:** el eje interpretado (`trabajo` / `estudio` / `reflexion`), separado del determinista.
- **Filtro de centralidad:** un proyecto solo se acepta si esta en el titulo o aparece 2+ veces en el cuerpo.

### Fixed
- **`kind` mezclaba dos ejes en una columna.** Las 8 unidades interpretadas pisaron su clasificacion determinista: 408 `tema` pasaron a 400, y una query `WHERE kind='tema'` dejaba de traerlas. Ahora `kind` es determinista (`tema`/`boilerplate`) y `activity` es el interpretado. Los 408 quedaron restaurados.
  - Es **el mismo defecto ya documentado** para `contributions.tier` (mezcla numeros 1/2/3 con categorias external/collab/pr). Se documento el error y se cometio dos horas despues, en una tabla nueva. Regla: un eje por columna.
- **Falso positivo de proyecto, medido.** La unidad "libros OpenClaw + sync workspace + post LinkedIn" recibio `project=soporteml` porque el cuerpo decia una vez "seccion SoporteML del remote" al resolver un conflicto de git. Era incidental, no el tema. De 8 propuestas de proyecto, 1 fue falsa (12%).

### Notes
- **La calibracion movio el filtro, no el prompt.** El modelo si detecto que SoporteML aparecia; el error fue no exigir que fuera central. Se arregla en la validacion (determinista y testeable), no en el prompt (probabilistico).
- **Separacion de destinos:** `project` va a la ficha (es atributo del dia); `topic`, `activity` y `summary` van a `session_entries` (una unidad no define el resumen de la ficha entera). Si dos unidades del mismo dia proponen proyectos distintos, se toma el primero y se avisa.
- **Verificado:** 111 tests, 0 violaciones de FK, `--apply` idempotente, 25 propuestas aplicadas y 1 rechazada sin contaminar la ficha.
- ADR-061.

---

## [2026-09-23] - Foreign keys activas: la integridad del schema pasa a aplicarse

### Added
- **`scripts/db.py`:** punto de entrada unico a `memory.db` con las FK activas (`connect()`), mas `check()` para verificar violaciones.
- **Tabla `session_entries`:** las 521 unidades de nivel 2 que estaban aplanadas dentro del texto de las fichas (408 temas, 113 boilerplate), con offsets en vez de copia.
- **Columnas `project` y `daily_id`** en las fichas, capturadas donde el dato existe.
- **`scripts/migrate-entries.py`** y **`scripts/interpret-entries.py`** (el LLM propone campos, no los escribe), con 27 tests.

### Fixed
- **6 foreign keys declaradas y 0 activas.** `PRAGMA foreign_keys` es por conexion y viene apagado por defecto: los `ON DELETE CASCADE` **nunca dispararon**, y por eso ADR-058 tuvo que limpiar 20 huerfanos a mano. Ahora el pragma se activa en todas las conexiones que escriben.
- **`memory-catalog.sh` estaba roto desde ADR-058:** su `INSERT` referenciaba `agent_id`, columna que se elimino por estar siempre vacia. El mismo bloque tenia mas valores que placeholders. Los dos corregidos.
- **`memory-db.sh` ahora respeta `MEMORY_DB`.** Lo ignoraba (lo tenia hardcodeado), asi que no se podia probar sobre una copia: la prueba escribio en la DB real. Los scripts de Python ya lo respetaban; esto los alinea.

### Notes
- **Se corrigio una advertencia previa demasiado amplia.** ADR-058 decia que activar las FK era riesgoso por los `INSERT OR REPLACE`. Medido el patron real: los que hay usan **id=None** (nunca reemplazan) o tocan tablas **sin hijos**. El riesgo pedia un id explicito existente, que ningun escritor usa. La prueba que sugeria lo contrario era un escenario construido.
- **Verificado sobre una copia**, con el pragma activo: los 3 migradores corren con 0 violaciones, las escrituras reales (`add-todo`, `add-inbox`, `update-ficha`) dejan los hijos intactos (13/3/7), y `foreign_key_check` da 0. 122 tests.
- **`migrate-learnings.py` queda marcado como peligroso:** borra `learnings` entero y perderia `learning_tags` por CASCADE. No se usa; queda documentado.
- **Un `DELETE` sobre un padre ahora borra hijos.** Es lo correcto, pero es un cambio de comportamiento a tener presente.
- ADR-060.

---

## [2026-09-22] - Contenido descompuesto: secciones y TODOs que estaban enterrados en el markdown

### Added
- **`scripts/content-parse.py`:** parser del markdown de la DB (`doc_kind`, `harness_fields`, `split_sections`, `extract_checklist`).
- **Tabla `sections`:** 1987 secciones consultables por titulo, nivel y rango horario. **Con offsets, no con copia del texto.**
- **Tabla `checklist_items`:** **102 items rescatados** (67 abiertos) que hasta hoy solo existian dentro de la prosa y no aparecian en ningun listado.
- **Columnas de metadatos en `daily_notes`:** `doc_kind`, `session_key`, `session_id`, `source`.
- **`tests/python/test_content_migration.py`:** 30 tests.

### Fixed
- **`type` mentia en 6 filas:** seis dumps del harness estaban marcados `type='daily'`. Ahora el tipo se **recalcula desde el contenido**, que es la fuente de verdad. La app filtraba por esa columna.
- **17 filas con `content` guardado como BLOB** (no corrompidas: eran UTF-8 valido, pero con el tipo de dato equivocado). Cualquier lector que asumiera `str` fallaba. Lo destapo un regex que tiro `cannot use a string pattern on a bytes-like object`.

### Notes
- **El texto no se duplica.** La primera version copiaba el `body` de cada seccion y la DB pasaba de 3.8 a **6.5 MB**: el texto copiado era el **95% del contenido ya presente en el padre**. Era exactamente el defecto que ADR-058 acababa de eliminar. Con offsets (`content[char_start:char_end]`), `sections` pesa **140 KB** y la DB queda en 4.2 MB.
- **Los offsets no se invalidan** porque el contenido solo crece por append (`memory-end-session.py` hace `content + block`). Matiz documentado: el `char_end` de la **ultima** seccion si avanza. El test que lo cubre fallo dos veces al escribirlo, y las dos veces el error era del test, no del parser.
- **Lo que NO se extrajo:** entidades (repos, PRs) del texto libre. Medido: de 5143 matches de `owner/name`, los mas frecuentes son `dist/stacks`, `memory/archive`, `origin/main`, `28/08` - rutas de archivo y fechas, no repos. **Regex sobre prosa fabrica datos falsos.**
- **Migrado primero sobre una copia** (`--db`), y fue lo que destapo lo de los 6.5 MB. Sobre la DB real solo se aplico la version corregida.
- **Verificacion:** busqueda `"em dash guion"` identica (57.5%, 52.0%); 0 secciones huerfanas; 0 offsets invalidos; 0 docs sin `doc_kind`; el `content` original intacto (la migracion es aditiva). App 200 en las 5 vistas. 95/95 tests.
- **Un numero que reporte mal y corregi:** dije "108 mismatches en `type` (95%)" y era artefacto de mi propia regex de clasificacion. Con la definicion correcta eran **6**. Se corrigio antes de actuar.
- ADR-059.

---

## [2026-09-22] - Refactor de schema: taxonomia normalizada y una FK espuria desarmada

### Added
- **`scripts/migrate-schema.py`:** el refactor completo, con `--dry-run` y `--db`. Repara cinco defectos de modelado con la reparacion correcta para cada uno.
- **Tablas `tags` + `learning_tags`:** vocabulario controlado con 157 tags y 233 vinculos. Un tag real es un token (minuscula, sin espacios, `[a-z0-9._-]`).
- **Tabla `categories` con columna `kind`:** distingue los DOS ejes que antes se llamaban igual (`learning` vs `topic`).
- **`tests/python/test_schema_migration.py`:** 20 tests, uno por propiedad. Incluye el que cazo un bug de idempotencia en mi propio script.
- **Vista de Learnings con chips de tag** (`getLearningTags`), con conteo por tag y filtro real.

### Changed
- **`learnings_enriquecido` absorbida y eliminada.** Duplicaba el 94% del texto (112 de 119 filas identicas byte a byte). El vector ahora vive en la misma fila que su texto: `learnings.learning_vector`.
- **Lectores parcheados** para la tabla que desaparece: `memory-search.py`, `memory-reembed.py`, `memory-catalog-v2.py`, `memory-catalog.sh`, `memory-db.sh`.

### Fixed
- **`tags`: 0 de 121 filas cumplian el contrato "JSON array".** Y 48 eran **titulos pegados** por un bug de carga. Ahora la fuente de verdad es la junction; la columna vieja queda como legacy documentada. El filtro por tag paso de devolver ruido a ser confiable: `tag=oss` -> 6, `tag=config` -> 9, inexistente -> 0.
- **20 violaciones de foreign key reparadas.** Y el hallazgo que importa: no eran un problema sino **tres**, con reparaciones distintas.
  - **9 hijos huerfanos promovidos** (no borrados): tenian contenido valido, sus ids estaban libres.
  - **7 vinculos colgados eliminados** (apuntaban a la sesion 73, nunca catalogada).
  - **FK `sessions_relacional.id -> daily_notes.id` ELIMINADA: era espuria.** Verificado: de los 47 vinculos que resuelven, **0 comparten fecha** con su daily. Los escritores pasan `id=None` y las dos secuencias coinciden por numeracion. Ningun codigo hace JOIN entre esas tablas.
- **La FK espuria era una bomba de tiempo.** Los `ON DELETE CASCADE` nunca dispararon (`PRAGMA foreign_keys = 0`). Si se hubiera activado el pragma sin quitarla, borrar la daily 53 habria destruido la sesion 53 (otra cosa) con 8 topics y 2 vectores. **Arreglar la integridad era desarmar la FK, no activar el pragma.**
- **2 columnas muertas eliminadas** (`learnings_enriquecido.query_vector`, `sessions_relacional.agent_id`): siempre NULL. Es higiene, no espacio.

### Notes
- **Verificacion que importa:** la busqueda `"em dash guion"` devuelve **57.5% y 52.0%, identicos** antes y despues. 0 violaciones de FK (eran 20). 128 vectores preservados. Las 51 sesiones y los indices sobrevivieron el rebuild. App 200 en las 5 vistas. 65/65 tests.
- **Migrado primero sobre una copia**, comparado, y despues sobre la DB real. Backup: `memory/memory.db.pre-schema`.
- **Dos bugs propios cazados por los tests:** la promocion de huerfanos consultaba la tabla gemela sin verificar que existiera (rompia la segunda corrida), y los tests de la migracion de vectores apuntaban al schema viejo (fallaron correctamente al cambiar `learnings_enriquecido` -> `learnings`).
- **Lo que NO se hizo:** no se fusionaron `daily_notes` y `sessions_relacional` (juntas son el 53% del peso) porque son **capas distintas** - conversacion cruda vs sesion curada, verificado con contenido distinto por id. No se activo `foreign_keys=1`: 5 lugares usan `INSERT OR REPLACE` (= DELETE + INSERT) que dispararia CASCADEs; es un pase propio.
- **No es un refactor por espacio** (sale 0.2 MB). Es por correccion: el 53% del peso esta bien donde esta.
- ADR-058.

---

## [2026-09-22] - Refactor de la DB: embeddings de JSON a BLOB float32 (12 MB -> 4 MB)

### Changed
- **Los embeddings pasan de JSON de texto a BLOB float32.** Medido con `dbstat` antes de tocar nada: **el 77% de los 12 MB eran 264 vectores en JSON.** Un vector de 1024 dims ocupaba ~22.700 chars en JSON y ocupa 4096 bytes en float32 (ratio real: 0.18, -82%). Resultado: **memory.db paso de 12 MB a 4 MB (-67%)**.
- **La tasa de crecimiento baja 5x:** de ~3.6 MB/mes a ~0.66 MB/mes en vectores, con el ritmo actual (~168 vectores/mes).
- **`idx_learnings_vector` eliminado.** Pesaba 3.2 MB - mas que la columna que indexaba - porque indexaba el texto completo del vector. Su unico uso real era responder "que filas tienen vector", y para eso el valor no hace falta: se reemplazo por `idx_learnings_vec_present`, un indice parcial sobre `id` que pesa KB.

### Added
- **`scripts/vector-util.py`:** codec compartido (`encode`, `decode`, `is_json`, `dims`, `cosine`). El `decode` acepta **ambos formatos**: los vectores viejos siguen leyendose durante la transicion. Antes el formato JSON era un detalle implicito del que dependian 4 scripts por `json.loads` suelto.
- **`scripts/migrate-vectors.py`:** conversion + limpieza de indice + VACUUM, con `--dry-run` y `--db`. **Verifica el invariante antes de escribir cada fila** (decodifica el BLOB y lo compara con el original); si no coincide, no escribe.
- **`tests/python/test_vector_migration.py`:** 16 tests (roundtrip, compat con JSON, dims, coseno, conversion end-to-end sobre una DB real, idempotencia, que el dry-run no escriba, que no dropee una columna con datos).

### Fixed
- **4 scripts parcheados para leer ambos formatos:** `memory-search.py`, `memory-topics.py`, `memory-reembed.py`, `memory-catalog-v2.py`. Sin esto la busqueda semantica se rompia al migrar. `memory-reembed.py` ahora escribe BLOB, asi que re-embeddear tambien migra el formato.
- **DDL de `memory-catalog-v2.py`:** las DB nuevas nacen con las columnas en BLOB, no en TEXT.
- **`.gitignore`:** los backups de migracion (`*.db.pre-*`) no se versionan. Un backup de 12 MB habria entrado al commit.

### Notes
- **Verificacion que importa:** no es el tamano, son los resultados. La busqueda `"em dash guion"` devuelve **57.5% y 52.0%, identicos antes y despues** de migrar. Ademas: 45/45 tests, la app sirve 200, los conteos de todas las tablas intactos.
- **Migrado primero sobre una copia**, comparados los resultados, y recien despues sobre la DB real.
- **Hallazgo colateral: 20 violaciones de foreign key preexistentes** (9 `learnings_enriquecido`, 7 `topic_sessions`, 4 `sessions_relacional`). Causa raiz: **`PRAGMA foreign_keys = 0`**, nadie lo activa, asi que los `ON DELETE CASCADE` del schema **nunca dispararon**. No se corrigio: limpiar huerfanos es una decision aparte y activar el pragma haria cascadear borrados sobre datos existentes. **Queda como deuda con evidencia.**
- **Limitacion documentada, no escondida:** un byte-string arbitrario cuyo largo sea multiplo de 4 decodifica a float32 y es indistinguible de un vector. En esta DB la columna contiene JSON legacy o BLOB (garantizado por la migracion), asi que no se presenta. Si alguna vez pudiera tener otra cosa, haria falta una columna `format`.
- **Dos bugs de mis propios tests**, cazados al correrlos: uno usaba floats cortos (medía 0.8 en vez de 0.18) y el otro asumia que bytes basura no decodifican. El segundo destapo la limitacion de arriba.
- ADR-057.

---

## [2026-09-22] - Auditoria #2: referencias rotas, guiones y un guard que estaba ausente

### Added
- **`scripts/pr-thread-brief.sh`:** el script que `docs/AGENTS-DETALLE.md` citaba como "verificacion mecanica" de la regla de atribucion por login - **y que nunca existio**. Clasifica cada evento de un hilo de PR (comentarios, reviews, inline) en `OURS` / `BOT` / `THIRD` por el `user.login` de la API, resume por actor y nombra quien tiene la pelota. Solo lectura (`gh api` GET). Probado contra PRs reales de astryx.
  - La regla que respalda existe por un error real: en astryx #4690 el `CHANGES_REQUESTED` de un maintainer se reporto como nuestro por proximidad de contexto. Una regla que dice tener verificacion mecanica sin tenerla es peor que una sin respaldo: da confianza falsa.
- **`scripts/check-refs.py`:** verifica que cada ruta citada con backticks (`docs/...`, `scripts/...`) exista de verdad. Ignora placeholders (`<repo>-<n>`), directorios, globs y los directorios historicos (`docs/archives/`, `docs/conversations/`): una ruta rota ahi es un dato del pasado, no una promesa vigente.
- **`tests/python/test_check_refs.py`:** 11 tests (deteccion, no falsos positivos, end-to-end, que falle ante una rota, que ignore historicos).
- **Chequeos baratos en el pre-commit, para TODO markdown staged:** guion comun (sobre el contenido staged, no el del disco) y rutas citadas. Antes corrian solo sobre `skills/`.

### Fixed
- **44 en dash y 2 em dash en `docs/`.** La regla del guion comun se cumplia solo dentro de `skills/` porque `test-skills.sh` mira unicamente `$SKILLS_DIR`. Resultado: los docs de trabajo acumularon 44 en dash sin que nada los viera. Normalizados a guion comun en `cpacc-mini-doc.md`, `cpacc-documentation-assessment.md`, `cpacc-improvements.md`, `cpacc-week-1-plan.md` y `pipeline/2026-08-30-spin-review-migration.md`.
  - No se toco U+2011 (guion no separable): la regla nombra U+2013/U+2014, y U+2011 aparece en rangos tipo "1-5", donde es separador de rango, no puntuacion.
- **`docs/cpacc-improvements.md`: 5 celdas de tabla con `\n` literales.** El texto se habia escrito con escapes en vez de saltos reales; un `\n` real dentro de una celda rompe la tabla. Pasados a `<br>`. Ademas, la referencia a `docs/cpacc-weekly-plan.md` apuntaba a un archivo que no existe: el real es `docs/cpacc-week-1-plan.md`.
- **Bug propio cazado por su propio test: `check-refs.py --all` no escaneaba nada extra.** El filtro de argumentos descartaba todo lo que empezara con `-`, incluido `--all`, que caia al default en silencio: reportaba "OK: 19 rutas" creyendo haber revisado todo. Corregido; ahora escanea 133 y fue lo que destapo las 2 rotas. Es exactamente la clase de falla que este checker existe para encontrar.
- **Falso positivo en la deteccion de bots de `pr-thread-brief.sh`:** el glob `*bot` clasificaba `abbot` y `talbot` como bots. Ajustado a la convencion real de GitHub (`[bot]`) mas unos pocos nombres conocidos.

### Notes
- **Metodo:** grep de los valores repetidos, y **cada candidato contra su fuente** antes de tocarlo. Verificar evito romper datos correctos: `docs/SETUP.md:44` ("el harness usa deepseek-v4-flash:cloud") parecia drift y **no lo es** - `scripts/model-router.sh` lo confirma.
- **Un guard que nunca falla es un guard que miente.** El hook nuevo se probo en negativo: aborta con un en dash y con una ruta rota, verificado con archivos temporales (no solo que pase en limpio).
- `AGENTS.md` en 15791 chars (limite de bootstrap: 20000). Suite completa: 29/29.

---

## [2026-09-22] - Auditoria de drift: AGENTS.md se contradecia a si mismo

### Fixed
- **`AGENTS.md` afirmaba dos cosas falsas sobre los modelos, en el bloque que leen TODOS los subagentes.** El "Resumen operativo" decia: "`deepseek-v4-flash:cloud` es el default de OpenClaw" y "Kanam en thinking `max`". Las dos son incorrectas: el config real (`~/.openclaw/openclaw.json`) tiene `model.primary = ollama/deepseek-v4.1-flash:cloud` y `thinkingDefault = high`, y ADR-053 unifica el thinking en `high` para todos los roles.
  - **Gravedad:** es el peor lugar posible para un dato stale. Los subagentes reciben **solo `AGENTS.md`** (no `docs/SETUP.md` ni `MEMORY.md`), asi que ese resumen es toda su fuente de contexto sobre que modelo corre. Y el archivo **se contradecia a si mismo**: la linea 119 (bloque managed) decia `v4.1-flash`, la 179 decia `v4-flash`.
  - **Resuelto con el mecanismo, no a mano:** la linea paso a ser el bloque managed `model-operativo` (nuevo), atado a un setting `model_pipeline` agregado a la tabla. Ahora dice: primario `deepseek-v4.1-flash:cloud`, thinking `high` para todos los roles (ADR-053), motor del pipeline A/B `deepseek-v4-flash:cloud`.
- **`docs/SETUP.md` linea 26:** la afirmacion vieja (thinking `max`) ya se habia preservado marcada como `historico` al insertar el primer bloque. Se mantiene asi: es registro de lo que regia el 2026-08-30, no una afirmacion vigente.

### Notes
- **Tercer candidato auditado y descartado: `docs/SETUP.md:44`** ("el modelo que carga el harness usa `deepseek-v4-flash:cloud` default"). **No es drift:** el router real (`scripts/model-router.sh`, `"default": "deepseek-v4-flash:cloud"`) lo confirma. Verificar antes de "corregir" evito romper un dato correcto.
- **Metodo de la auditoria:** no se busco por intuicion. Se grepearon los valores que se repiten entre archivos (modelos, thinking, rutas), y cada candidato se contrasto contra la fuente autoritativa: el config del gateway para el runtime, `scripts/model-router.sh` para el routing, y los ADRs para las decisiones. Solo se corrigio lo que la fuente desmintio.
- Registro de bloques tras esta fase: `model-triple` y `model-operativo` en `AGENTS.md`; `model-triple` en `docs/SETUP.md`. `AGENTS.md` quedo en 15791 chars (limite de bootstrap: 20000).

---

## [2026-09-22] - Fase 3: bloques managed (settings de la DB propagados a los archivos)

### Added
- **`scripts/managed-blocks.py`:** mecanismo que propaga valores globales desde la tabla `settings` de `memory.db` a bloques delimitados por marcadores `MANAGED` dentro de los archivos. Subcomandos: `list`, `seed`, `set`, `check`, `apply [--dry-run]`. Reglas duras: solo reescribe lo que esta entre marcadores; si faltan, **no inserta nada** y muestra el snippet exacto para pegar; idempotente; `set` y `apply` son pasos separados.
- **Tabla `settings`** en `memory/memory.db` (key, value, description, updated_at) con 4 claves semilla: `model_primary`, `model_auxiliary`, `model_alternative`, `thinking_default`.
- **`tests/python/test_managed_blocks.py`:** 9 tests que cubren las propiedades criticas (idempotencia, no tocar el texto de afuera de los marcadores, no adivinar cuando faltan, que el cambio de un setting propague al bloque).
- **`projects/kanam-os/app/settings`:** vista que lista los settings, permite cambiarlos, ver el diff y propagar. En dos pasos visibles: cambiar el valor no toca archivos; propagar si, y avisa.
- **`docs/adr/ADR-055-bloques-managed-settings-db.md`:** la decision, con la frontera explicita respecto de ADR-038.
- **Primer bloque aplicado:** `model-triple` en `AGENTS.md` y `docs/SETUP.md`.

### Fixed
- **`docs/SETUP.md` contradecia a ADR-053 desde que se escribio.** Declaraba default `deepseek-v4-flash:cloud` y Kanam en thinking **`max`**, cuando el config real (`~/.openclaw/openclaw.json`: `thinkingDefault: "high"`) y ADR-053 dicen primario `deepseek-v4.1-flash:cloud` con thinking `high` para todos. Nadie lo habia notado porque nadie compara archivos a mano. Resuelto sin editar a mano: se inserto el bloque managed y la linea vieja se preservo marcada como historica. Es exactamente el drift que ADR-055 viene a hacer detectable.
- **`lib/actions.ts`: prefijo de interprete equivocado.** Al unificar los dos scripts en un solo helper quedo `python3 <script>` para ambos, lo que rompia `memory-db.sh` (es un script de shell). Ahora se invocan directo por shebang: `python3 memory-db.sh` falla, verificado.

### Notes
- **Verificacion:** 9/9 tests; `check` sobre los archivos reales reporta ambos bloques "al dia" y `apply` no cambia nada (idempotente); propagacion probada cambiando `thinking_default` a `max` (mostro el diff correcto) y **revertida en el acto** porque ADR-053 dice `high`.
- `AGENTS.md` quedo en 15696 chars, bajo el limite de bootstrap de 20000.
- **Limite respetado:** los documentos narrativos (MEMORY.md, SOUL.md, AGENTS.md, USER.md) no se migran a la DB (ADR-038), pero ahora pueden contener un bloque generado. La distincion: un valor unico y verificable repetido en varios archivos es un dato mal modelado; la prosa alrededor es interpretacion.

---

## [2026-09-22] - Kanam OS: app local para ver la memoria como fichas, tablas y grafos

### Fixed
- **`projects/kanam-os`: el server escuchaba en `0.0.0.0:4317` (sin token, accesible desde la LAN).** `next dev` bindea por default a todas las interfaces. La app lee y **escribe** `memory.db` y tiene botones de escritura, asi que cualquier dispositivo en la red local podia modificarla. El portal tiene token, pero ese token solo protege su propio listener (55149), no el puerto directo del server. Verificado: `curl http://192.168.100.7:4317/` daba 200. Fix: `--hostname 127.0.0.1` en los scripts dev/start. Verificado: loopback 200, LAN 000. Leccion guardada en `docs/learnings/infraestructura.md`.
- **`scripts/init-project.sh` - falla silenciosa al trackear el `.knowledge/` de un proyecto nuevo.** El script imprimia `✅ .knowledge/ tracked as blob in workspace` sobre un `git add` que no stageaba nada: en cuanto `projects/<slug>/.git` existe, el repo del workspace ve el directorio como *embedded repository*, no desciende al `.knowledge/` y el add sale con **codigo 0 y sin efecto**. Se reprodujo en sandbox y se verifico que el patron de `.gitignore` no incide (tres variantes, todas fallan). Fix: el `git add`/`commit` del `.knowledge` se movio a **antes** del `git init` del proyecto, mas un guard (`git diff --cached --quiet` -> `exit 1`) que hace ruidosa la falla en vez de falsa. Verificado el ciclo completo: add antes del init, init despues, y updates posteriores del `.knowledge` funcionando. Los proyectos ya trackeados (`kanam-lab`, `langchain-starter`, `kanam-pulse`) no estaban afectados porque su `.knowledge` entro antes del init. Leccion guardada en `docs/learnings/infraestructura.md`.
- **`scripts/memory-db.sh` - guard de id inexistente que salia con exit 0.** El `exit 1` corria dentro del subshell de un pipe, asi que no cambiaba el codigo de salida del script: imprimia el error y devolvia exito. La UI habria mostrado "ok" sobre una operacion fallida. Fix: se saco el pipe y se captura el resultado con `n=$(sqlite3 ...)`, dejando la decision en el shell principal. Verificado con `execFile` (el mecanismo real de las server actions): 7/7 casos correctos.

### Added
- **`projects/kanam-os/`:** app local que lee `memory/memory.db` y la muestra como fichas, tablas y grafos. Fases 1 (lectura), 2 (escritura) y filtros completas. Vistas: resumen, fichas (+ detalle con cuerpo de la sesion), topics (tabla + grafo bipartito topics-sesiones en SVG puro, sin dependencias), learnings por categoria, TODOs, inbox, OSS y daily navegable. **Filtros server-rendered en todas las vistas con volumen** (TODOs, fichas, learnings, OSS, inbox): los filtros viven en la URL, son links compartibles y no necesitan JS de cliente. Stack: Next.js 16.3.6 (App Router) + Tailwind 4 + Biome + TypeScript. Repo privado `gonzoblasco/kanam-os` creado y pusheado; el workspace trackea solo su `.knowledge/`, segun la convencion existente.
- **`scripts/memory-db.sh`: 6 subcomandos de escritura nuevos** (`done-todo`, `reopen-todo`, `set-todo-priority`, `triage-inbox`, `update-ficha`). Cada uno valida el efecto y **regenera el espejo markdown** en el mismo paso. Con guard de id inexistente que sale con exit 1.
- **`.openclaw/portals.json`:** declaracion del server de desarrollo de kanam-os (puerto 4317) para que el portal del Control UI lo levante en un click.
- **`docs/adr/ADR-054-kanam-os-app-local-memoria.md`:** Kanam OS como app local de lectura sobre `memory.db` (Next.js + `node:sqlite`). Extiende ADR-038 (DB manda, markdown espejo) a una UI; ADR-050 sigue vigente sin revisar.

### Decisions
- **Next.js y no FastAPI**, aunque el pedido original sugeria Python "para cosas de IA": la UI no calcula embeddings, los proyecta (ya estan persistidos en `session_vectors` y `learnings_enriquecido`). FastAPI habria agregado un segundo runtime, un segundo puerto y un bridge HTTP para leer un SQLite que Node 26 lee nativo. Python queda como **unico escritor** de la DB.
- **`memory.db` se queda trackeada en git.** Sacarla del repo romperia el sync entre el Mac Mini y el MacBook Air (pedido explicito de Gonzo). El riesgo real de `-wal`/`-shm` ensuciando el repo se mitiga abriendo la DB en `readOnly`: verificado que no se crean tras el build y las 9 vistas servidas. `journal_mode=WAL` descartado por el mismo motivo.
- **La UI nunca escribe SQL crudo.** La fase CRUD (2) agrega botones que disparan los scripts de Python existentes, no un escritor nuevo: un `UPDATE` directo dejaria los markdown mintiendo respecto de la DB.
- **`next telemetry` deshabilitada** en el proyecto, coherente con local-first.
- **Next 16.0.0 descartado** por CVE-2025-66478; se uso 16.3.6.

### Notes
- Verificacion fase 1: `next build` OK (typecheck + 9 rutas), smoke test HTTP 200 en las 8 vistas con datos reales (55 dailies, 51 fichas, 118 learnings, 66 contribuciones OSS, 11 topics).
- Verificacion fase 2: los 6 subcomandos probados en sandbox (escriben + regeneran el `.md`); guards de id inexistente 7/7 con `execFile`; path y permisos verificados contra el workspace real.
- **El click real quedo verificado por el log del servidor**: `POST /todos 200` con `doneTodo`/`reopenTodo` en `lib/actions.ts`. El transporte de las server actions funciona end-to-end (lo ejecuto Gonzo desde el portal).
- Verificacion de filtros contra la DB: `learnings?q=guion` -> 2 en la UI y 2 en la DB (coincidencia exacta); `fichas?model=gemma4:e4b-mlx->deepseek-v4-flash` -> 1 de 51. Los filtros que devuelven 0 son dato correcto, no bug: 50 de 51 sesiones tienen `model_used = 'unknown'` y ningun titulo contiene "kanam-os".
- **Las server actions se llaman a mano** (en un `useTransition`), no via el prop `action` de `<form>`: ese prop exige `Promise<void>` y las actions devuelven `ActionResult`, que es lo que permite mostrar el error en el lugar en vez de tragarlo.
- El grafo de topics es layout determinista (topics a la izquierda, sesiones a la derecha, grosor = confianza del vinculo) en vez de force-directed: con decenas de nodos se lee mejor y no cambia en cada render.
- Roadmap: fase 3 bloques managed (settings en DB propagados a `USER.md`/`AGENTS.md`/`.knowledge/`), fase 4 busqueda semantica sobre los vectores persistidos.

---

## [2026-09-22] - Auditoria de deuda de ADRs: revalidacion, ADR-053, duplicado 048 y docs mal ubicados

### Fixed
- **`docs/adr/ADR-049` revalidado:** dos enunciados del 2026-09-15 quedaron stale (el "bug" de `ollama launch claude --model` y la ausencia de binario global `qwen`/`claude`). Ambos eran ciertos al escribirse: el binario de Ollama es del 2026-09-19 (posterior al ADR) y `qwen` se instalo el 2026-09-22. Se documenta como dato caducado, no como error del autor. Se agrega el camino `ollama launch claude` (verificado end-to-end) y el enmascarado de modelos.
- **`docs/adr/ADR-048` duplicado resuelto:** dos decisiones compartian el numero 048. `ADR-048-kanam-lab-ui-choice` era de alcance de PROYECTO (mantener Gradio en kanam-lab), no global, y colisionaba con `ADR-048-shadcn-radix-stack-ui`. Se movio a `projects/kanam-lab/.knowledge/adr/0002-ui-framework-gradio.md` y se renumero como 002. El corpus global queda sin duplicados y sin huecos.
- **`docs/adr/ADR-041`, `ADR-046`, `ADR-040`:** se marcaron las secciones superseded por ADR-053 (roles de modelo y nivel de thinking).
- **`AGENTS.md`:** la regla de razonamiento decia "Kanam SIEMPRE en MAX", contradiciendo el config vigente. Reemplazada por la regla de HIGH unificado.
- **`docs/SETUP.md` y `skills/agent-orchestration-pipeline`:** se corrigio el dato stale de `ollama launch claude` y la ruta embebida como unico camino.
- **`docs/adr/ADR-047`:** usaba `Decisor` (singular) donde los otros seis ADR en español usan `Decisores`; era el unico de los 53 sin campo `Origen`. Ambos normalizados.
- **`docs/adr/README.md`:** la seccion Formato describia solo las secciones del cuerpo y dejaba sin documentar los campos del header, que es la causa de que cada generacion los inventara. Se agrega la tabla de campos obligatorios y opcionales.
- **Docs estructurales mal ubicados (movimiento incompleto):** el commit `5c2e3b03` movio `AGENTS-DETALLE`, `NORTH`, `ROADMAP` y `SETUP` de la raiz a `docs/`, pero dejo cuatro atras: `LEARNINGS.md`, `OSS-TRACKER.md`, `METHODOLOGY-AUDIT.md` y `MAPA-PROXIMOS-PASOS.md`. Se completo el movimiento a `docs/`.
  - **Bug activo que esto causaba:** `scripts/memory-db.sh` escribe `docs/OSS-TRACKER.md` y `scripts/migrate-learnings.py` lee `docs/LEARNINGS.md`, mientras los archivos vivian en la raiz. Los scripts apuntaban a un path inexistente.
- **`docs/LEARNINGS.md`:** los 7 links internos apuntaban a `docs/learnings/...`, que desde `docs/` resolvian a `docs/docs/...`. Corregidos a `learnings/...`.
- **`docs/adr/ADR-037`:** citaba el mockup `projects/soporteml-v4/mockups/identidad-v4.html` como si estuviera en disco. Existio y se valido (commit `b450ebda`), pero se removio al limpiar el proyecto terminado (el cleanup borra codigo y conserva `.knowledge/`). Se documenta como removido en cleanup, con la instruccion para recuperarlo desde git.

### Added
- **`docs/adr/ADR-053-modelos-primario-auxiliar-alternativo.md`:** primario `deepseek-v4.1-flash:cloud`, auxiliar `gemma4:cloud`, alternativo `glm-5.3-flash:cloud`, thinking `high` para todos los roles. Cierra el drift silencioso que encontro la auditoria (el primario habia rotado cuatro veces sin registro, y `minimax-m2.7` corria pese a que ADR-040 lo excluia explicitamente).
- **`projects/kanam-lab/.knowledge/adr/`:** directorio nuevo para ADRs de alcance de proyecto, trackeado por el workspace git (no `docs/`, que `projects/*/docs` ignora).

### Notes
- **Dos correcciones a mi propio reporte inicial de la auditoria:** (1) los tres "artefactos prometidos y ausentes" NO eran artefactos nunca creados: `LEARNINGS.md` y `METHODOLOGY-AUDIT.md` existian mal ubicados, y el mockup existio y se borro en el cleanup del proyecto. (2) El "drift de formato" de headers NO es deuda: el corte ingles/español esta limpio (ADR-001 a ADR-046 en ingles hasta 2026-09-14; ADR-047 en adelante en español), consistente con la regla de idioma por capa.
- Config aplicada via `openclaw config patch` (8 updates, sin restart) y verificada live con `openclaw models status`. Los tres modelos pasaron smoke test contra el daemon.
- Se documento que la lista local y el catalogo cloud de Ollama NO coinciden en nomenclatura (`gemma4:cloud` vs `gemma4:31b`): la disponibilidad se chequea contra ambas.

---

## [2026-09-22] - Nuevo proyecto: langchain-starter (RAG + API + LaunchAgent)

### Added
- **`projects/langchain-starter/`:** proyecto Python nuevo, integracion LangChain completa en 4 fases (estrategia en `LANGCHAIN_STRATEGY.md`):
  - Fase 1: venv + Hello World via Ollama (`gemma4:cloud`, `langchain-ollama`).
  - Fase 2: RAG - `scripts/ingest.py` (chunking semantico), embeddings `qwen3-embedding:0.6b` (1024d), ChromaDB local (`config/chroma_db/`), `scripts/query.py` cadena RAG con respuesta restringida a contexto.
  - Fase 3: `app/api.py` FastAPI - `/health`, `/chat` (streaming), `/ingest`; docs en `/docs`.
  - Fase 4: `scripts/agent.py` agente ReAct con tool-calling (LangGraph: `search_knowledge` + `word_count`), `scripts/service.sh` + LaunchAgent `dev.gonzoblasco.langchain-starter` en `~/Library/LaunchAgents/` (KeepAlive, RunAtLoad, auto-restart verificado), automation OpenClaw `langchain-starter-health-watch` (cada 15m).
- **`projects/langchain-starter/Dockerfile`:** escrito para futuro, NO desplegado (decision: LaunchAgent nativo para Mac Mini).
- **`app/config.py`:** configuracion centralizada via env vars (OLLAMA_BASE_URL, LLM_MODEL, EMBED_MODEL, CHUNK_SIZE, CHUNK_OVERLAP, API_PORT).

### Decisions
- Python (no JS) para LangChain por madurez del ecosistema; Ollama local (no OpenAI) porque el gateway ya corre modelos locales; ChromaDB local primero, Supabase PGVector como evolucion posterior; LaunchAgent sobre Docker para servicio permanente del Mac Mini.

### Notes
- El servicio corre en `127.0.0.1:8100` gestionado por LaunchAgent (pid auto-reparado ante kill, verificado).
- Pendientes: migracion Chroma -> Supabase Vector, ingesta de documentos reales mas alla del doc de estrategia.
- Los docs estructurales raiz (AGENTS-DETALLE, NORTH, ROADMAP, SETUP) se movieron a `docs/` (cambios de otra sesion incluidos en este commit).

## [2026-09-18] - Limpieza de la raiz del workspace - deuda tecnica y reordenamiento

### Changed
- **Eliminados (recuperables via git history + Trash de macOS):** `useMemoryStream.ts` (duplicado del hook real en `projects/kanam-pulse/packages/web/src/hooks/`), `src/` (spike simulado de a11y-fixer: analyzer.ts + a11yHandler.ts; proyecto archivado), `scripts/wip/` (5 scripts completos pero sin ninguna referencia: spinreview, hideak, pre-push-hook, daily-auto-archive, session-template-generator), `.zcode/` (plan scratch de CLI externa), `.DS_Store`, `public/` (directorio vacio), `pipeline-state.json` (estado rancio de pipeline viejo, regenerable por `pipeline-track.sh`).
- **Reubicados:** `kanam-lab/` (perfil del asistente creado en la sesion 2026-09-16, NO el proyecto Gradio) -> `docs/profiles/kanam-lab/` para eliminar la colision de nombre con `projects/kanam-lab`; `migration-spin-review-changes.md` -> `docs/pipeline/2026-08-30-spin-review-migration.md`; `docs/conversation_2026-09-16_kanam_lab.md` -> `docs/conversations/conversation_2026-09-16_kanam_lab_summary.md` (junto a su version full).

### Notes
- Verificado pre-movimiento: cero referencias a los paths eliminados/reubicados en AGENTS.md, docs/, skills/, scripts/, memory/.
- Tests node del workspace: 3 PASS / 0 FAIL post-limpieza.

## [2026-09-16] - Limpieza de la cola Kanam OS + todos 9 y 10 (#9/#10 done)

### Changed
- **Cola de todos depurada** (DB `memory.db`): fuera 2/3/4 (kanam-skills), #6 eliminado de verdad (kill, no marcado done), #27-30 + #36 olvidados, y los 4 OBSERVAR (17/22/24/25) quitados por pedido de Gonzo. Cola abierta reducida de 18 a 2: **#31 (re-cata de modelos) y #35 (envoltorio nativo kanam-pulse)**.
- **#40 (kanam-studio world-building / Slice 5) -> done**: recon en repo real (clon en aislamiento) confirmo que el Slice 5 YA estaba implementado y superado (repo en v0.15.0, slices 5-6 + hitos 5/6/7 completos). No habia trabajo pendiente real; se cerro y se restauro el texto completo del todo.
- **#9 (sandbox/) -> done**: carpeta `sandbox/` creada en la raiz del workspace; ya cubierta por `.gitignore` (linea 128-129) - verificada con `git check-ignore`.
- **#10 (analizar github-workflow) -> done + mejora aplicada**: el plugin ya habia sido analizado (08-24) y sus risk signals portados a `github-pr-risk.sh`. Lo que faltaba (agrupacion de PRs) se anadio a `scripts/pr-dashboard.sh`: cada PR ahora trae `bucket` (draft/needs_review/stale/ok) + resumen `by_state`. Aditivo y compatible (no toca los campos existentes). Verificado real: 19 PRs open, by_state {needs_review:12, ok:2, stale:5}.

### Notes
- El clon de `kanam-studio` y `kanam-pulse` local en `projects/` estan corruptos (remote apunta a workspace_openclaw, solo .knowledge/); se trabajo sobre repos GIT de GitHub en aislamiento.
- Residuo sin tocar (sesion paralela): ADR-048, dailies 09-15/16, MEMORY.md - no commiteados aqui.

## [2026-09-16] - Todo #34: politica de backup del gateway - respaldo git automatizado

### Changed
- **Backup local verificado** creado en `~/Backups/2026-09-16T09-53-59.695-03-00-openclaw-backup.tar.gz` (321M, `--verify` passed).
  - Via que funciona (verificado en el intento): `openclaw backup create --no-include-workspace --verify`. El workspace ya esta cubierto por git; el primer intento SIN el flag fallo por un symlink absoluto en `projects/kanam-lab/.venv` (OpenClaw rechaza a proposito symlinks absolutos que escapan del root; los venvs son regenerables).
- **Git backup automatizado**: repo inicializado en `~/Backups/openclaw-git` + schedule `openclaw backup enable --every 24h --agent main`. Commit de prueba `35edbcb` (`backup git create --all --exclude-secrets`).
- **Politica definida (con datos, no teoria):**
  - **Que:** estado/config/credenciales/SQLite de `~/.openclaw` (el workspace NO - ya vive en git via workspace_openclaw).
  - **Como:** 2 vias complementarias - archivo tar.gz local (`backup create --no-include-workspace`, con `--verify`) + snapshots SQLite versionados en git (`backup git create --exclude-secrets`).
  - **Cada cuanto:** schedule diario 24h (git backups) automatizado; archivo tar a demanda con `--verify`.
  - **Donde:** `~/Backups/` (local, sin push remoto - bajo control de Gonzo).

### Notes
- El schedule `backup enable` provisiona un automation del gateway (no visible en el inventario restringido de esta sesion - confirmado por el CLI).
- Todo #55 (backup local) ya estaba done; esto lo EXTENDIO con la via git versionada + automatizacion.

## [2026-09-15] - Todo #32: kanam-pulse core migrado de JS a TypeScript

### Changed
- **kanam-pulse `packages/core` JS -> TS completo** (commit `597b7ac` en gonzoblasco/kanam-pulse): 15 modulos src + 8 tests tipados.
  - Recon previo (todo #32): el clon local `projects/kanam-pulse` esta corrupto (remote apunta a workspace_openclaw, sin packages/) - se trabajo sobre el repo real clonado en aislamiento.
  - Contrato de resolucion corregido: core ahora emite a `packages/core/dist/` (el tsconfig heredaba outDir a la raiz) y `main`/`exports` -> `dist/index.js` compilado, porque Node no carga `src/index.ts` en runtime (verificado RESOLVE OK).
  - 2 fixes TS2783 (spread redundante en disk/memory: `{usedPct, ...stats}` -> `{...stats}`) + cast de exec via `unknown` - todos behavior-identicos.
  - Agregado `@types/node` + script build (tsc) a core.

### Fixed
- **server importa `@kanam-pulse/core` por nombre**: verificado que resuelve tras el cambio a dist (build server exit 0, tests 21/21).

### Notes
- **Verificado end-to-end:** core 61/61, server 21/21, web 36/36, `npm test` del monorepo verde, `import('@kanam-pulse/core')` -> RESOLVE OK.
- El clon en aislamiento se limpio con trash; el clon local corrupto en `projects/kanam-pulse` queda (fuera de alcance, anotado).
- Todo #32 -> done en la DB.

## [2026-09-15] - Todo #38: cliente MCP para Lovable - decidido (nativo de OpenClaw)

### Changed
- **`docs/adr/mcp-lovable-decision.md`** - decision del todo #38: cliente MCP real para Lovable.

### Fixed
- El #38 pedía evaluar 3 caminos (nativo, SDK @modelcontextprotocol, via Claude Code). **Respuesta verificada:** la integracion NATIVA de OpenClaw existe y cubre el caso entero (`openclaw mcp` con add/login/probe/status y `--auth oauth`, `--transport streamable-http`, `--include` para restringir al contrato read-only get_project/list_projects/query_database). Endpoint Lovable verificado vivo (v1.18.7, "Auth with API key or OAuth", fetch status 200). No hace falta SDK propio ni Claude Code.
- Estado previo: `openclaw mcp list` reporta 0 servers; `mcp.servers` en openclaw.json vacio.

### Notes
- **Pendiente de Gonzo (bloquea el cableado, no la decision):** el `openclaw mcp add lovable --url https://mcp.lovable.dev --transport streamable-http --auth oauth --include get_project,list_projects,query_database` + `openclaw mcp login lovable` requieren el OAuth de la cuenta Lovable de Gonzo. NO se ejecuto ni se toco config para respetar esa dependencia.
- Todo #38 -> done en la DB (decision definida y documentada; el paso OAuth queda anotado como accion de Gonzo).

## [2026-09-15] - Todo #37: scripts spin-review cuarentenados (rojos desde 2026-08-30)

### Changed
- **5 scripts rotos movidos a `scripts/wip/`:** `spinreview.sh`, `hideak.sh`, `pre-push-hook.sh`, `daily-auto-archive.sh`, `session-template-generator.sh`. Los bugs documentados el 30/08 (HANDOFF) seguian presentes y fueron verificados: find -maxdepth 1 -name '*/' no matchea, jq malformado (comilla de mas), git log format invalido, date -d inexistente en BSD/macOS, overwrite de HANDOFF.md sin preguntar.

### Notes
- **Siguieron los 6 scripts del 30/08? No - 1 ya no existe:** `query-schema.mjs` no esta (el HANDOFF lo movio a /tmp como borrador y el cliente MCP real es el todo #38, separado).
- **Decision cuarentenar, no reparar:** ninguno de los 5 esta cableado a hook, cron ni skill (verificado); son tooling muerto con bugs reales. Repararlos seria refactor sin consumidor. Todo #37 dice "reparar O cuarentenar"; frente a scripts sin uso, cuarentenar es lo de bajo riesgo.
- **Skills no referencian los scripts movidos** (validacion: Script refs 53 OK).
- Todo #37 -> done en la DB.

## [2026-09-15] - Deuda de entorno cerrada: npm test corre de un tiro

### Fixed
- **`test:bats` usaba `bats` del PATH, que no existe** - `npm test` fallaba siempre en el 2do paso con `sh: bats: command not found` (bats esta como devDependency pero no en el PATH ni en `node_modules/.bin`). Cambiado a `npx bats tests/bash/` (verificado Bats 1.13.0).
- **`pytest` no estaba instalado en esta maquina** (`python3 -m pytest: No module named pytest`), asi que `test:pytest` nunca corria. Instalado user-local (`pip install --user pytest` -> 8.4.2, reversible, no toca el entorno del sistema).

### Notes
- **Resultado: `npm test` ahora corre COMPLETO de un tiro con exit 0.** Los 4 pasos en serie: `test:scripts` (skills, bash/python/frontmatter/dash/links), `test:bats` (47 tests), `test:node` (15+3 harness scenarios) y `test:pytest` (17 passed). Antes nunca se habia podido correr la suite de un tiro en esta maquina.
- La deuda quedaba documentada en los CHANGELOG previos desde la Fase 0 ("npm test no se puede correr de un tiro hasta resolver esto"); resuelta al fin.

## [2026-09-15] - Prompts versionados (formato con frontmatter + verificador)

### Added
- **Esquema de prompts versionados:** cada archivo en `prompts/` lleva frontmatter `id` (debe coincidir con el slug del archivo), `version` (entero >= 1), `scope` (workspace|project|global) y `tags` (lista no vacia). El cuerpo es el prompt en si.
- **`prompts/complexity-scorer.md`** - primer prompt migrado al formato (version 1, scope workspace, tags scoring/pipeline/complexity/orchestrator).
- **`scripts/check-prompts.py`** - verificador de todos los `prompts/*.md`: id coincide con filename, version entera >= 1, scope permitido, tags no vacias, ids unicos, cuerpo presente. Exit 0 ok / 1 con los problemas listados.
- **`tests/python/test_check_prompts.py`** - 9 tests (buen caso, id-filename, version, scope, tags, frontmatter ausente, ids duplicados, dir vacio, y que el `prompts/` real siempre valida).

### Notes
- **El formato es aditivo y no rompe `complexity-scorer.sh`:** el script lee `prompts/complexity-scorer.md` via `grep` de las 4 dimensiones (A/B/C/D), y el frontmatter no altera esas lineas del cuerpo. Verificado: el checker pasa (exit 0) y el scorer sigue andando (T=8 en una prueba).
- **Hallazgo de paso (no arreglado, fuera de alcance):** el `grep` de dimensiones en `complexity-scorer.sh` (variable `DIMS`, linea 74) esta **roto desde siempre** - el regex espera `Alcance**` pegado, pero la linea real es `Alcance (A):**`, asi que `DIMS` siempre devuelve vacio. Y es codigo muerto: el script usa un `SYSTEM_PROMPT` en ingles hardcodeado, no `DIMS` (solo la define). Queda anotado como deuda tecnica de `complexity-scorer.sh` para refactor futuro.
- **Los tests pytest no se pudieron ejecutar aca** (pytest no instalado en esta maquina, deuda de entorno ya documentada); la logica del checker se verifico manualmente contra casos buenos/malos (id-filename, version 0, scope invalido, sin frontmatter, tags vacio - cada uno falla con su mensaje, y el caso bueno pasa con exit 0).

## [2026-09-15] - Observabilidad minima del pipeline (ROADMAP 1.1): pipeline-report.sh

### Added
- **`scripts/pipeline-report.sh`** - vista de telemetria **read-only** sobre la cola durable. No captura nada nuevo: agrega y renderiza lo que ya guardaban `pipeline-track.sh` (startTime/endTime/iterations/regressions) y `pipeline-queue.sh` (attempts/pid/lastError). Asi la observabilidad cuesta $0 y agrega cero dependencias (decision de la evaluacion por capas).
  - `--json` para parsear programaticamente, formato legible por defecto.
  - Superficie las senales de ROADMAP 1.1 que nadie habia medido: duracion por unidad (endTime-startTime), total/promedio/max por fase, reintentos (flaky/crash) y **regresiones (bugs que B introduce al "corregir")**.
- **`tests/bash/pipeline-report.bats`** - 7 tests: read-only (no muta el state), resumen, totales agregados, `--json`, faltante/corrupto con exit 2, sin unidades medibles degrada con gracia.

### Fixed
- **Un quirk de jq:** `//` como valor directo de un literal de objeto (`{phase: $r.fase // ""}`) falla en sintaxis; entre parentesis (`($r.fase // "")`) funciona. Documentado por el bug en el desarrollo, no asumido.

### Notes
- Senal de listo del ROADMAP 1.1 (metricas de duracion registradas en 5+ sesiones): este entregable la habilita; falta que se registre en sesiones reales de pipeline, que es trabajo de uso, no de codigo.
- El estado real de `pipeline-state.json` (kanam-fixer S1) tiene startTime/endTime nulos: el report degrada a "sin unidades medibles" hasta que las unidades futuras se midan (pipeline-track las setea con `start`/`done`).

## [2026-09-15] - ADR-049/050/051: motor del pipeline, umbral de datos, regla de lib/ai

### Added
- **ADR-049 - Claude Code como motor del pipeline A/B (Qwen Code a fallback).** Documenta como decision lo que la practica ya venia haciendo desde ~2026-09-11: los ciclos reales (kanam-tetris, duelos atoi, harness) corren con **Claude Code 2.1.260** (embebido en Claude-3p) apuntando al gateway Ollama. Cierra la deriva: `docs/SETUP.md` y la skill seguian afirmando que Qwen Code era el estandar.
- **ADR-050 - La memoria de Kanam OS sigue en SQLite local, con umbral de migracion a Postgres/Supabase.** Fija con numeros (115 vectores, 11 MB) que no migra hoy, y el umbral objetivo para reabrir: concurencia real, ~1 GB, >100k vectores con filtros, acceso remoto, multi-tenant. Senala que el limite que llega primero es la **higiene de git** de `memory.db`, no el rendimiento.
- **ADR-051 - Regla de extraccion de `lib/ai` compartido.** No se construye anticipado: solo con 4 condiciones (2+ proyectos del mismo lenguaje, divergencia real, consumidor en el ciclo, refactor same-behavior). TS y Python no comparten paquete.
- **`docs/adr/README.md`** con los 3 ADRs en el indice.

### Changed
- **`docs/SETUP.md`:** seccion de motor del pipeline reescrita para reflejar ADR-049 (Claude Code estandar, Qwen fallback, ruta fragil del ejecutable de Claude-3p).
- **`skills/agent-orchestration-pipeline/SKILL.md`:** alineada con ADR-049. El comando base ahora es Claude Code headless; Qwen pasa a fallback. Mirror `.github/skills/` sincronizado.

### Notes
- Los 3 cierran decisiones que vivian solo en la practica o la conversacion; con ADR en el repo no se re-abren sin evidencia nueva (regla de oro del ADR).
- ADR-049 no pisa ADR-040/041/045/046: esos deciden *que* modelo; el 049 solo *en que harness* corre.
- **Hallazgo post-ADR (Gonzo):** Claude Code ignora AGENTS.md (verificado con el binario 2.1.260 - issue antrhopics/claude-code #6235). Se adopto el mecanismo `CLAUDE.md` minimo con `@import` de `AGENTS.md` (fuente de verdad unica, verificado que el import relativo y absoluto funcionan y que sube directorios). `CLAUDE.md` creado en el workspace raiz; regla operativa documentada en ADR-049 y SETUP.md.
- **Correccion del alcance (verificado con el binario):** el `CLAUDE.md` de la raiz cubre todo el arbol, incluidos `projects/x/` a 2 niveles - el `@./AGENTS.md` se resuelve relativo al `CLAUDE.md` (no al cwd) y el discovery sube. Y ningun proyecto tiene `AGENTS.md` propio, asi que NO se crea `CLAUDE.md` per-proyecto (seria un import roto); solo si un proyecto introduce su propio `AGENTS.md`.
- **Correccion final de la regla (Gonzo, 2026-09-15):** el objetivo no es cubrir proyectos con la raiz, sino **inicializar el PAR `AGENTS.md` + `CLAUDE.md` por proyecto** cuando el proyecto entra al pipeline. El `AGENTS.md` del proyecto es especializado para su tarea/dominio (fuente de verdad); el `CLAUDE.md` es su espejo que lo `@import` (lo dirige, no lo reemplaza). **Prioridad verificada:** con cwd dentro del proyecto y ambos pares presentes, el del proyecto gana sobre el de la raiz. Piloto: `kanam-fixer` (par creado 2026-09-15). Corrige el commit anterior que decia "no crear per-proyecto" (ese rechazo era solo para el caso de import roto sin AGENTS, no para el par que si se crea).

## [2026-09-15] - Fix del gateway-jobs-watcher ciego (bug silencioso del 08/09)

### Fixed
- **`gateway-jobs-watcher` (job de automations) quedó ciego y nadie lo sabia.** Su `trigger.script` leia `r.output`, pero la forma real del retorno de `exec` en code-mode es `{status, exitCode, exitSignal, exitReason, durationMs, aggregated, noOutputTimedOut, cwd}` - **no existe `output`**, el campo de texto es `aggregated`. Reproducido con harness: con `r.output` el exitCode quedaba siempre en `-1`, la condicion `exitCode === 1` jamas se cumplia y el watcher **nunca habria disparado aunque `gateway-jobs-check.sh` fallara**. Llevaba 80 evaluaciones en `triggerState.lastResult = error--1`.
  - Ahora usa `r.aggregated` con fallback a `r.exitCode`, y dispara ante **cualquier** fallo: exit 1 (problemas encontrados) o exit 2 (no se pudo chequear).
- **`scripts/gateway-jobs-watcher-trigger.js`** - trigger corregido, versionado en el repo.
- **`tests/node/gateway-jobs-watcher-trigger.test.js`** - 3 escenarios (exit 0 sano -> quiet, exit 1 -> FIRE, exit 2 -> FIRE para no quedar mudo).

### Notes
- **Forma del retorno de `exec` verificada empiricamente**, no leida de docs: un job temporal (`pq-shape-probe`, ya borrado) imprimio su propia forma de retorno. El ejemplo de `docs/automation/cron-jobs/schedules.md` ya usa `res.aggregated`; el job existente no.
- **`runMode:"force"` NO evalua el trigger** - saltea el gate y ejecuta el payload directo. La unica prueba valida del gate es una evaluacion natural del scheduler (se bajo el intervalo a 30s, y luego se resto a 2h). Verificado: 3 evaluaciones naturales con `lastResult:"ok"` - la primera vez en la vida del watcher.
- El trigger esta cableado en `npm test` como parte de `test:node`.

## [2026-09-15] - Fase 0 cableada: watcher de la cola durable + bug del watchdog existente

### Added
- **Job `pipeline-queue-watcher` (automations, cada 15m, isolated).** Cablea la cola durable a la ejecucion: `trigger` headless que corre `orphans` y lee el estado, y solo entonces gasta modelo. El payload corre `tick` (reencola huerfanas), reporta estado y avisa por Telegram. **Habilitado y verificado end-to-end:** el gate se evaluo 4 veces de verdad (`triggerEvalCount: 4`) y devolvio `fire:false` / `last:"idle"` / `stallCount:0` sobre la cola sana.
- **`scripts/pipeline-queue-trigger.js`** - el trigger versionado en el repo (no solo en la DB del scheduler). Read-only: la recuperacion vive en el payload.
- **`tests/node/pipeline-queue-trigger.test.js`** - 15 escenarios con `exec` mockeado: idle, cola detenida en 1er y 2do check, dedupe, trabajando, huerfana, transicion, post-tick, estado corrupto, exec fallido, JSON no-array, failed. Cableado en `npm test` como `test:node`.

### Fixed
- **`gateway-jobs-watcher` estaba CIEGO y nadie lo sabia.** Su `trigger.script` leia `r.output`, pero la forma real del retorno de `exec` en code-mode es `{status, exitCode, exitSignal, exitReason, durationMs, aggregated, noOutputTimedOut, cwd}` - **no existe `output`**, el campo de texto es `aggregated`. Resultado: `out = ''`, el regex nunca matcheaba, `exitCode` quedaba en `-1` y el estado persistido era `error--1` en **80 evaluaciones consecutivas**. El watchdog nunca habria disparado aunque `gateway-jobs-check.sh` fallara: habria que haber descubierto el problema por otro lado.

### Notes
- **Forma del retorno de `exec` verificada empiricamente, no leida.** Se creo un job temporal (`pq-shape-probe`, ya borrado) que imprimio su propia forma de retorno en `state`. Evidencia: `{"status":"completed","exitCode":0,"aggregated":"hello-probe\\n__EXIT__:0",...}`. Esto es lo que permitio detectar el bug del watcher antes de heredarlo: el ejemplo de `docs/automation/cron-jobs/schedules.md` ya usa `res.aggregated`, y el job existente no.
- **`runMode:"force"` NO evalua el trigger.** Un run forzado saltea el gate y ejecuta el payload directo: por eso la primera prueba forzada reporto una falsa alarma con la cola sana, y por eso `triggerEvalCount` seguia en `None`. La unica prueba valida del gate es esperar una evaluacion natural (se bajo el intervalo a 30s y luego se restauro a 15m).
- **La cola no es (todavia) el driver de ejecucion:** el pipeline A/B corre por `sessions_spawn`, y `running` solo se setea si alguien llama `claim`. Por eso un "stall" de un solo check es normal y no debe alertar: el trigger exige **2 checks consecutivos** del mismo conjunto de unidades antes de gritar `persistentStall`. Huerfanas y estado ilegible si son señales duras (disparan al primer check).
- **Dedupe por nombres de unidades**, estable frente al `tick` (running -> queued no cambia el conjunto), asi que la recuperacion automatica no re-dispara en loop.
- **Ruido de prueba aceptado:** el force run de prueba envio un mensaje real a Telegram ("falsa alarma, cola sana"). Es el comportamiento documentado de `announce`, no un bug.
- **Verificacion:** harness 15/15 PASS; gate real evaluado 4 veces con `fire:false` sobre estado sano; `check_em_dash.py` OK; trigger con sintaxis valida como funcion async (top-level `await`, igual que el executor).

## [2026-09-15] - Fase 0: cola durable del pipeline A/B

### Added
- **`scripts/pipeline-queue.sh`** - capa aditiva sobre `pipeline-track.sh` que da continuidad de ejecucion al pipeline: seleccion de proxima unidad (`next`), deteccion de huerfanas por `kill -0` (`orphans`), reintentos acotados (`PIPELINE_MAX_ATTEMPTS`, default 3) y un estado `failed` terminal que **no bloquea** el resto de la cola. Campos nuevos en el mismo `pipeline-state.json`: `attempts`, `pid`, `lastError`. Comandos: `enqueue`, `next`, `claim`, `release`, `done`, `review`, `orphans`, `tick`, `report`, `status`.
- **`tests/bash/pipeline-queue.bats`** - 17 tests: enqueue, orden de `next`, salto de `failed`, claim idempotente, reintento, agotamiento del cap, huerfanas, compatibilidad con planes viejos sin `attempts`/`pid`.
- **`docs/architecture/fase0-cola-durable-spec.md`** - spec de la fase (T=14 high).
- **`docs/architecture/kanam-os-layers-evaluacion.md`** - evaluacion de la arquitectura por capas propuesta.

### Fixed
- **`scripts/pipeline-queue.sh` - dos defectos CRITICOS que habian quedado sin arreglar, encontrados por el review cruzado adversarial del Agente B (su reporte llego despues del cierre anterior; no modifique el script a mano, reproduje cada hallazgo y lo verifique):**
  1. **Race condition en `claim`: doble ejecucion.** `read_state`/`write_state` eran `cat` + redireccion, sin lock ni atomic rename. Veinte claims concurrentes sobre la misma unidad imprimian **todos** `[claim] U1 -> running` con exit 0 - dos agentes podian creer ambos que poseian la unidad (doble ejecucion), y el pid que sobrevivia era el de un claim que perdio (huerfanas calculadas sobre un pid fantasma). Fix: **lock por `mkdir` atomico** (macOS no tiene `flock`) tomado por todo comando que muta el plan, mas **escritura atomica** via temp file + `mv`. Verificado: 10 claims en paralelo -> **1 ganador, 9 ignorados, attempts=1**.
  2. **`write_state` fallaba en silencio: falso exito.** La redireccion rota no mataba el pipeline (`echo`/`jq` terminan 0 pese a `pipefail`), asi que el comando imprimia exito y salia 0 sin haber escrito nada. Con un archivo read-only o un `enqueue` a un directorio inexistente: `Pipeline encolado: 0 unidades` + **exit 0** sobre un plan que no existia. Un job de automations que leyera ese exit code habria seguido como si el plan estuviera creado. Fix: `write_state` escribe a un temp y valida cada paso (serializacion, escritura, `mv`); `enqueue` ademas rechaza un plan de 0 unidades; `acquire_lock` detecta el directorio padre faltante de entrada. Verificado: ambos casos ahora salen con **exit 2**.
- **`scripts/pipeline-queue.sh` - tres defectos mas del barrido adversarial del orquestador:**
  1. **Estado corrupto borraba la cola en silencio.** `read_state` hacia `cat` sin validar; con JSON invalido, `jq` fallaba y el `|| echo` de las ramas devolvia una cola vacia -> `next` no devolvia nada y las unidades pendientes desaparecian sin aviso. Ahora `require_valid_state` aborta con exit 2 y mensaje explicito en todo comando que lee el estado (`enqueue` queda exceptuado: es la via de recuperacion).
  2. **`PIPELINE_MAX_ATTEMPTS` no numerico desactivaba el cap.** `[ "$NA" -gt abc ]` emitia `integer expression expected` y la comparacion seguia evaluando, con lo que el tope de reintentos dejaba de aplicarse (reintentos infinitos). Un valor `0` o negativo tampoco tenia sentido. Ahora el valor se sanitiza al arranque: si no es entero >= 1, avisa y usa 3.
  3. **Pids `0` y `-1` se leian como siempre vivos.** `kill -0 0` y `kill -0 -1` **devuelven exito** (grupo de procesos / todos los procesos), asi que una unidad con esos pids jamas se detectaba como huerfana y quedaba `running` para siempre. Ahora solo un entero `> 0` se considera candidato; pids no numericos, `0` y negativos se tratan como muertos.
- **Lock huerfano (defecto introducido por mi propio fix del lock):** un lock cuyo dueño moria entre el `mkdir` y la escritura del pid file quedaba sin dueño identificable y **nunca se rompia** - todo comando posterior se estancaba hasta el techo de reintentos y fallaba. Detectado en la verificacion del fix, no en teoria. Ahora se rompe tras ~2s de gracia sin pid file, y el caso con pid muerto ya se rompia por `kill -0`.
- **`scripts/pipeline-queue.sh`:** se agrego el bit de ejecucion (`chmod +x`). El Agente A lo dejo en `-rw-------` y los tests no lo detectaron porque invocan con `bash "$SCRIPT"` explicito - un CLI sin bit de ejecucion falla para cualquier consumidor real.

### Notes
- **El diagnostico original estaba desactualizado:** la evaluacion nombro el gap como "SIGKILL de Qwen Code a ~3 min". Verificado el 2026-09-15: el harness migro a **Claude Code 2.1.260** (binario en `Claude-3p/`, valida headless contra el gateway Ollama), que maneja mejor las sesiones largas. El gap real **no es el SIGKILL: es la falta de continuidad** - nada reencolaba una unidad interrumpida.
- **El review cruzado del Agente B fue el que mas valor aporto.** Su reporte llego despues de que yo creyera que habia settleado sin entregar nada; encontro los dos defectos criticos que mi propia verificacion no cubria (race + falso exito), y su reproduccion del race con 400 unidades fue mejor que la mia de 10. Leccion: un subagente que tarda no es un subagente que fallo - el reporte tardio tiene valor real, y "settled sin reporte" fue una conclusion prematura mia.
- **`pipeline-track.sh` NO se modifico.** Consume y escribe el mismo archivo; verificado el flujo mixto sin que se pisen. OJO: `pipeline-track.sh` conserva el patron read-then-write sin lock, asi que la race sigue viva si se lo invoca en paralelo con la cola (documentado, no resuelto).
- **Verificacion real:** `bash -n` limpio; `npx bats tests/bash/pipeline-queue.bats` -> **30/30**; suite completa de bats -> 40/40; `check_em_dash.py` OK; `test-skills.sh` OK (84 skills); race verificado con 10 claims concurrentes; locks huerfanos (sin pid y con pid muerto) verificados; estado real verificado byte-identico tras cada corrida.
- **Deuda de entorno (preexistente, no introducida aca):** `npm test` falla en `test:bats` con `sh: bats: command not found` porque `bats` esta declarado como devDependency pero **no esta en el PATH ni en `node_modules/.bin`**; con `npx bats` corre verde. `python3 -m pytest` tampoco existe en esta maquina. La suite completa via `npm test` no se puede correr de un tiro hasta resolver eso.

## [2026-09-15] - Evaluacion de arquitectura por capas para Kanam OS

### Added
- **`docs/architecture/kanam-os-layers-evaluacion.md`** - evaluacion de la arquitectura por capas propuesta por Gonzo (frontend -> BFF -> orquestacion IA -> datos -> workers), contrastada contra el estado real del sistema. Conclusion: 4 de 5 capas ya existen; el gap real es la ejecucion sin cola durable (SIGKILL de Qwen a ~3 min) y los prompts sin versionar. Se rechazan explicitamente monorepo, migracion a Postgres/pgvector, Redis y BullMQ/Celery por no resolver ningun problema a esta escala (regla 2026-09-14: el precedente no es motivo). Incluye plan de 6 fases y 5 decisiones abiertas para ADR.

### Notes
- **Verificacion previa con fuentes reales:** config de OpenClaw (loopback:18789, auth token), `ollama list` (3 locales + 8 cloud), compat OpenAI de Ollama (`/v1/models` operativo), RAG (SQLite + `qwen3-embedding:0.6b` 1024 dims), `model-router.json` (6 rutas), grep de keys en frontend (0 resultados), `prompts/` (1 solo archivo).
- **Nombre acunado por Gonzo:** "Kanam OS" designa el conjunto del sistema (workspace + gateway + pipeline + memoria + constelacion), alineado con la capa 1 de `docs/NORTH.md`.
- Escaneado con `scripts/check_em_dash.py`: OK.
- No se tomo ninguna decision de arquitectura: el doc deja 5 decisiones abiertas que, al cerrarse, merecen ADR.

## [2026-09-15] - Fix del guard de idempotencia en memory-end-session.py

### Fixed
- **`scripts/memory-end-session.py` - el guard de idempotencia matcheaba por substring.** La comprobación era `marker in row["content"]` con `marker = "## Session End - {project}"`. Como `"## Session End - workspace"` es **substring** de `"## Session End - workspace-general"`, guardar una sesión con el slug corto quedaba **silenciosamente bloqueado** cuando el día ya tenía una entrada del slug largo (y al revés, cualquier slug prefijo de otro). Hoy bloqueó dos guardados consecutivos. Corregido a match por **línea completa** (`any(ln.strip() == marker ...)`).

### Notes
- **Bug encontrado por uso real, no por test:** el síntoma fue el mensaje `ℹ️ Ya existe un Session End para 'workspace' en 2026-09-15 - sin duplicar` cuando ese marker no existía en el archivo. La verificación fue directa: `'## Session End - workspace' in '## Session End - workspace-general'` devuelve `True`.
- **Impacto del bug:** cualquier proyecto cuyo slug sea prefijo de otro del mismo día (`workspace` / `workspace-general`, y potencialmente `kanam-*`) podía perder su registro de cierre sin aviso. Los datos no se corrompían - el guard simplemente no escribía.
- Verificación del fix: `py_compile` OK + test unitario de la lógica (el marker largo matchea, el corto no) + `test-skills.sh` (84 skills, 0 fallos) + bats vía npx (10/10).

## [2026-09-15] - Limpieza de legacy agent dirs + fix de la skill session-context

### Fixed
- **`skills/session-context/SKILL.md` - frontmatter inválido.** Era la **única** skill del workspace con `description` anidada dentro de `metadata` en vez de top-level; el loader la rechazaba con `description is required` (`dist/local-loader-CR9dHge0.mjs:175` lee `frontmatter.description`). Movida a top-level y mirror `.github/skills/` sincronizado. Ahora carga: `session-context ✓ Ready`.

### Notes
- **Limpieza de infraestructura:** los 6 directorios `agents/main/agent.legacy-*` (17 MB) movidos a `trash`. Verificados uno por uno antes: cada uno contenía un solo archivo `bin/fd`, idéntico byte a byte al del agente actual, y cero datos únicos. Backup previo en `/tmp/openclaw-agents-backup-20260915-101128.tar.gz` (7.4M).
- **`doctor --fix` verificado (corrido por Gonzo a las 09:26):** las startup migrations quedaron **resueltas** - 0 ocurrencias del aviso, sin finding en `doctor --json`. Config válida, backup en `openclaw.json.bak`.
- **NO se tocó `agents/openclaw/`:** el doctor lo marca como directorio sin entrada en `agents.list`, pero el gateway **lo tiene abierto** (4 handles verificados con `lsof`). No se borra sin confirmar.
- **Recordatorios abiertos:** no hay backup registrado (`openclaw backup create`) ni command owner configurado (`commands.ownerAllowFrom`).

## [2026-09-15] - Watcher Guidepup Darwin 27 (kanam-fixer S3 se cierra solo)

### Added
- **Automation `guidepup-darwin27-watcher` (cada 12h, `sessionTarget: isolated`, `delivery: none`).** Copia el patron del `base-ui-stable-check`: chequea `dist-tags.latest` de `@guidepup/guidepup` en npm; cuando hay version nueva baja el tarball y mira el `manifest.json` buscando un asset de VoiceOver para `platformVersion 27` (la maquina de Gonzo es Darwin 27). Tambien cuenta los comentarios del issue `guidepup/guidepup#149`. Avisa a Gonzo por Telegram SOLO con novedad real (asset 27 o comentario nuevo en el issue), deduplicado por archivo de estado `tmp/guidepup-darwin27.json`.

### Notes
- **Por que existe:** kanam-fixer (ciclo `0.0.1` cerrado en `88ca9ff`) tiene S3 bloqueado por un tercero: Guidepup 0.34.0 no tiene asset de VoiceOver para Darwin 27 (su manifest cubre 21-25). El issue ya se reporto upstream (`guidepup/guidepup#149`). Cuando el asset exista, S3 se cierra corriendo el test sin tocar codigo - es el reemplazo del "acordarse a mano de chequear".
- **Verificado con force-run real (no asumido):** el job creo `tmp/guidepup-darwin27.json` con `{"latest_checked": "0.34.0", "platform27_announced": false, "last_comment_count": 0}` - deteccion correcta (0.34.0 no tiene 27), dedup escrito, y NO aviso (no habia novedad). El tarball temporal se limpio solo.

## [2026-09-15] - kanam-fixer: corrección del blocker de S3 (es upstream, no permisos)

### Fixed
- **`projects/kanam-fixer/.knowledge/STATUS.md` - la fila S3 de la tabla resumen quedaba stale.** Decia "Blocker: permisos de macOS", cuando la seccion detallada del mismo archivo (mas abajo) ya documentaba la causa correcta. Se alineo la fila a la seccion, con los dos commits (`b98bf1b`, `a080a27`).

### Notes
- **El blocker de S3 NUNCA fueron los permisos de macOS.** Verificado de forma independiente: macOS 27.0 / kernel `27.0.0` (Darwin 27); `@guidepup/guidepup@0.34.0` y `@guidepup/setup@0.25.3` (ambos ya en la ultima version); `npx @guidepup/setup install voiceover` -> *"The requested screen reader asset is not available for this platform: VoiceOver on darwin 27"*; el `manifest.json` del paquete lista `platformVersion: 21, 22, 23, 24, 25` - **sin 26 ni 27**. El marcador `/private/var/db/Accessibility/.VoiceOverAppleScriptEnabled` **existe** (root:wheel, creado 10:39), o sea que el permiso se otorgo y el fallo siguio.
- **Una receta equivocada se le paso a Gonzo** (permisos de macOS) y el la ejecuto. No desperdicio el dato: su marcador es ahora la evidencia de que no era ese el problema. Registrado para que no se repita.
- **Leccion de debugging (causa raiz del desvio):** el mensaje `VoiceOver cannot be started` **ocultaba un `cause` anidado** (`macOS version not supported`). Se corrigio la funcion que reportaba solo el mensaje externo; ahora aplana la cadena de causas y el skip del test dice las dos. Un cause anidado que no se lee es un diagnostico perdido.
- **Sesion duena inactiva:** la correccion se aplico desde otra sesion porque la duena del proyecto ya habia cerrado su turno y dejo la inconsistencia. Verificado `status: done` antes de escribir (sin riesgo de pisada).

## [2026-09-15] - kanam-fixer: repo público + pin del perfil pendiente (limitación de API)

### Changed
- **`gonzoblasco/kanam-fixer` - repo cambiado a PÚBLICO** (decisión de Gonzo, 2026-09-15). Descripción del repo ya poblada con el pitch real ("Asserts what a screen reader actually announces..."). Sin código todavía - el repo del proyecto se puebla en el slice S1.
- **`projects/PROYECTOS.md`:** `kanam-fixer` pasa de `PRIV` a `pub`.

### Notes
- **El pin del perfil NO se puede cambiar por API.** Verificado contra el schema GraphQL de GitHub: las únicas mutations de pin son `pinEnvironment`, `pinIssue`, `pinIssueComment`, `unpinIssue` y `unpinIssueComment` - **no existe ninguna para pinnear repositorios**. Cambiar los pinned (quitar `a11y-fixer`, poner `kanam-fixer`) requiere hacerlo a mano en la UI del perfil. Estado actual de los 6 pinned: `create-stack`, `a11y-fixer`, `kanam-skills`, `kanam-forge`, `kanam-solitaires`, `kanam-story`.
- **Decisión de Gonzo sobre el paquete npm:** se deja publicado a propósito, sin deprecar. Razón textual: "puede servir de entrada a alguien quien llegue a él por error". El paquete `@gonzoblasco/a11y-fixer@0.6.0` queda sin cambios (verificado: `deprecated: no`). Esto **cierra** el último pendiente de la enmienda ADR-001.

---

## [2026-09-15] - Cierre de la enmienda ADR-001: a11y-fixer y a11y-playground archivados + kanam-fixer formalizado

### Changed
- **`gonzoblasco/a11y-fixer` - repo ARCHIVADO en GitHub** (`isArchived=true`, 2026-09-15). Acción en superficie pública, con OK explícito de Gonzo ("confirmo todo").
- **`gonzoblasco/a11y-playground` - repo ARCHIVADO** (`isArchived=true`). **Veredicto con evidencia:** era un scaffold que nunca pasó de M0 - repo privado creado el 2026-08-30, **un solo commit** (`chore: initial scaffold`), **size 0** (solo `.gitignore` + README, cero código). Su única dependencia declarada era `a11y-fixer`, hoy archivado. Gonzo no recordaba el proyecto; la evidencia mostró que no había nada que recordar.
- **`projects/portfolio-strategy/.knowledge/ADR-001-portfolio-strategy.md` - sección 6 cerrada.** Los 4 pendientes de la enmienda pasan a RESUELTOS con su fecha: (1) alcance de `kanam-fixer` definido y **dirección confirmada por Gonzo** el 2026-09-15; (2) relación con el código de `a11y-fixer` = **greenfield**, no hereda; (3) repo archivado, **resto acotado al paquete npm** (sigue publicado, requiere `npm login`); (4) `a11y-playground` archivado.
- **`projects/PROYECTOS.md`:** `a11y-playground` movido a ARCHIVADOS; `a11y-fixer` con la nota de repo archivado; `kanam-fixer` con repo creado (privado) y alcance definido.
- **`projects/a11y-playground/.knowledge/`** (BRIEF + STATUS): marcados como archivados, con la dependencia hacia `a11y-fixer` anotada como ya no aplicable.

### Added
- **Repo `gonzoblasco/kanam-fixer` creado** (privado, 2026-09-15) para reservar el nombre. Sin código todavía - el repo del proyecto se puebla en el slice S1. El nombre sigue libre en npm (404).

### Notes
- **Superficies públicas tocadas en esta entrada:** archivado de 2 repos + creación de 1. Todo con OK explícito de Gonzo.
- **Sin tocar a propósito:** el paquete npm `@gonzoblasco/a11y-fixer@0.6.0` (requiere credencial que no está en la máquina) y el pinned del perfil de GitHub (decisión de vidriera, de Gonzo).

---

## [2026-09-15] - kanam-fixer: material de lanzamiento guardado (DISTRIBUTION.md)

### Added
- **`projects/kanam-fixer/.knowledge/DISTRIBUTION.md` (NUEVO):** conserva el material de lanzamiento redactado el 2026-09-14 para `a11y-fixer`, que nunca se uso porque el proyecto se archivo ese mismo dia. Contiene: la investigacion verificada de canales (awesome lists con stars y requisitos reales de cada CONTRIBUTING + hallazgos del GitHub Marketplace), los 3 textos (release/Marketplace, awesome-a11y, awesome-actions) y el checklist previo a publicar.
- **`projects/kanam-fixer/.knowledge/BRIEF.md`:** seccion "Documentos del proyecto" con el puntero al material nuevo.

### Notes
- **Advertencia de procedencia en el documento:** los textos se escribieron para un **GitHub Action**; `kanam-fixer` es una **asercion sobre el anuncio del lector de pantalla**. Se marca que **no se reciclan tal cual** y hay una tabla de "que sirve y que no" (la entrada de `awesome-actions` solo aplica si shippea un `action.yml`; el BRIEF marca el comentario automatico en PRs como fuera de alcance).
- **Congelado por diseno:** el ROADMAP de `0.0.1` declara publicar como fuera de alcance ("el ciclo prueba, no distribuye"). El material queda guardado hasta que exista evidencia del caso testigo (S4).
- **Ninguna accion publica ejecutada.** Los 3 textos quedan sin enviar por decision explicita.
- **Nota de proceso:** el turno que creo el archivo se corto por un reinicio de gateway. Se verifico el contenido en disco (165 lineas, integridad head/tail, scan de guiones OK) antes de continuar - el write no se dio por exitoso sin comprobacion.

---

## [2026-09-15] - `doctor --fix` resuelve las startup migrations + skill rota arreglada

### Changed
- **`docs/ROADMAP.md` 0.1 - migraciones RESUELTAS (verificado).** Gonzo corrió `openclaw doctor --fix` + restart a las 09:26 del 15/09. El aviso `Startup migrations need attention` **desapareció** (0 ocurrencias en `status`, sin finding en `doctor --json`). Lo que el fix hizo: relocalizó las credenciales compartidas a SQLite, normalizó 9 `num_ctx`, deshabilitó 34 skills inutilizables y copió el `allowFrom` de Telegram al allowlist de grupos. Config válida, backup en `openclaw.json.bak`.
- **`skills/session-context/SKILL.md` - frontmatter corregido (bug real destapado por el doctor).** Era la **única** skill del workspace con `description` anidada dentro de `metadata` en vez de top-level, y el loader la rechazaba con `description is required` (`dist/local-loader-CR9dHge0.mjs:175` lee `frontmatter.description`). Movida a top-level; el mirror `.github/skills/` sincronizado. Ahora carga: `session-context ✓ Ready`.

### Notes
- **Metodología:** el output del terminal que compartió Gonzo se trató como **dato**, y cada afirmación se verificó por separado contra el estado real (gateway, config, disco, logs). No se asumió que el fix hubiera funcionado.
- **El restart de hoy cerró limpio:** los 4 dumps de `logs/stability/` siguen siendo todos del 13/09; no se generó uno nuevo. El gateway corre 2026.9.4 (pid 43766, probe ok).
- **Residuos no bloqueantes, registrados en el ROADMAP:** los 6 `agent.legacy-*` siguen en disco (17 MB de cruft inofensivo - el fix resolvió las credenciales, no los borró); `agents/openclaw/` figura como directorio sin entrada en `agents.list` pero el gateway **lo tiene abierto** (verificado con `lsof`), así que NO se borra sin confirmar; no hay backup registrado ni command owner configurado.
- **Nota de proceso:** un commit propio falló por un pre-commit hook instalado por otra sesión que invocaba `npm run lint`/`build` (scripts inexistentes en el workspace). El hook ya fue corregido por esa sesión al template real (`test-skills.sh` + bats + pytest). Se evitó el atajo de `SKIP_SIMPLE_GIT_HOOKS`.

## [2026-09-14] - a11y-fixer: BRIEF alineado al archivado + topics y homepage del repo

### Changed
- **`projects/a11y-fixer/.knowledge/BRIEF.md` - alineado a la enmienda de ADR-001.** El BRIEF se habia escrito ~2h antes de que Gonzo archivara el proyecto, y quedaba contradiciendolo: decia "Ancla del pilar: Accesibilidad como diferenciador". Ahora declara **ARCHIVADO (2026-09-14)** en el header, reemplaza "Por que es ancla" por "Por que fue ancla (y por que ya no lo es)", y suma a la deuda el **estado de cierre incompleto**: el repo sigue `isArchived=false` y el paquete npm sigue publicado (ambos pendientes del todo id=54). El aprendizaje de "cero adopcion pese a estar tecnicamente listo" queda anotado como transferible a `kanam-fixer`.
- **`gonzoblasco/a11y-fixer` (repo) - `topics` poblados.** Estaban vacios (`[]`). Ahora: `a11y, accessibility, accessibility-testing, axe-core, ci, github-action, github-actions, playwright, typescript, wcag`. Descubrimiento gratis que no se estaba usando.
- **`gonzoblasco/a11y-fixer` (repo) - `homepage` limpiado.** Apuntaba a `https://github.com/gonzoblasco/a11y-fixer-v2`, que hace 301 de vuelta al mismo repo. Resto de una version vieja; ahora vacio.

### Notes
- **Tension registrada, no resuelta:** publicar en el Marketplace y submitir a awesome lists son actos de *lanzamiento*, y contradicen el archivado recien decidido. Se prepararon los textos pero **no se ejecuto ninguna accion publica**. Requiere decision de Gonzo.

---

## [2026-09-14] - ADR-001 enmendado: a11y-fixer archivado, kanam-fixer como proyecto nuevo

### Changed
- **`projects/portfolio-strategy/.knowledge/ADR-001-portfolio-strategy.md` - sección 6 agregada (enmienda formal).** Decisión de Gonzo: `a11y-fixer` queda **archivado** y su sucesor es **`kanam-fixer`, un proyecto nuevo** (no un renombre). El **texto original de la sección 3 se conserva sin cambios** - la enmienda agrega, no reescribe (el historial de decisiones importa). Se declara explícito que **no se asume** que `kanam-fixer` hereda el rol de engine de fixes a11y: eso es lo que falta decidir. Consecuencia: el pilar **Accesibilidad como Diferenciador queda sin ancla formal** hasta que el alcance se defina.
- **`docs/NORTH.md` - 5 referencias alineadas.** El conteo de la constelación pasó de "3 anclas" a "2 anclas vigentes + 1 en transición"; el Horizonte 1 y la constelación ahora nombran `kanam-fixer` (alcance sin definir) en lugar de `a11y-fixer`; la dirección de Comunidad se reescribió para no afirmar que kanam-fixer ya es open source con usuarios.
- **`docs/ROADMAP.md` 2.1 - acción de enmienda marcada como hecha** + acción abierta nueva: definir el alcance de `kanam-fixer`, que es lo que desbloquea reasignar el ancla del pilar Accesibilidad.
- **`projects/PROYECTOS.md` - `a11y-fixer` movido a ARCHIVADOS** (con la nota de que el repo en GitHub sigue `isArchived=false`), y `kanam-fixer` listado como proyecto nuevo sin repo aún. Fecha del índice actualizada.

### Notes
- **`memory/HANDOFF.md` NO se tocó a propósito:** es un snapshot fechado (2026-08-30). Reescribir el estado de proyectos de un handoff histórico falsifica el registro - se aplica el mismo criterio que "no editar el body de un PR para limpiarlo".
- **Dato verificado (no asumido):** el repo `gonzoblasco/a11y-fixer` sigue con `isArchived=false` en GitHub. Archivarlo requiere OK explícito de Gonzo (acción en superficie pública).
- **Seguimiento:** todo id=54 en la DB de memoria (`project=kanam-fixer`) con los 4 pendientes: alcance, relación con el código, archivado del repo + paquete npm, y destino de `a11y-playground`.

---

## [2026-09-14] - Diagnostico read-only de las startup migrations (causa raiz encontrada)

### Notes
- **Causa raíz identificada, sin tocar nada.** El aviso "Startup migrations need attention" del `doctor`/`status` sale de `dist/state-migrations.messages-CxjvWU23.mjs`: es un `startupMigrationWarning` guardado cuando las migraciones corren con warnings. En el log del gateway (`/tmp/openclaw/openclaw-2026-09-13.log`, 3 eventos a las 21:02, 21:56 y 22:16) el mensaje exacto es `Left legacy agent dir at .../agents/main/agent.legacy-<ts>`.
- **Qué son:** **6 directorios `agent.legacy-*`** (17 MB en total, 2.8 MB cada uno) bajo `agents/main/`. Cada uno contiene **un único archivo, `bin/fd`**, idéntico byte a byte al `agent/bin/fd` del agente actual (`cmp` OK, mismo sha256) y **cero archivos fuera de `bin/`**.
- **Por qué se conservan a propósito:** en `dist/state-migrations.doctor-J5ZgjZY8.mjs:2876`, `inspectLegacyAgentDir` busca `openclaw-agent.sqlite`; si no está pero hay un archivo que no reconoce (`bin/fd`), devuelve `status: "payload"` y la migración deja el directorio con warning en vez de borrarlo. Es cruft de reinstalaciones, **no hay datos únicos en riesgo**.
- **Reparación (requiere al owner):** `openclaw doctor --fix` + `openclaw gateway restart`. El agente no reinicia el gateway hospedador.
- **Metodología:** diagnóstico 100% read-only, siguiendo `diagnose-gateway` (prohíbe `--fix`, restarts y matar listeners). Se leyeron logs, dumps y código fuente; **ninguna reparación ni migración de estado fue ejecutada**.
- **Estado del agente:** sano. `openclaw-agent.sqlite` de 499 MB, gateway corriendo (pid 80466, probe ok). El aviso es persistente, no un gateway roto.

## [2026-09-14] - 0.1: swap de version verificado y cierre de items abiertos

### Changed
- **`docs/ROADMAP.md` 0.1 - swap de version resuelto (verificado, no asumido).** Gonzo indico que las dos acciones pendientes ya estaban hechas. Verificado con datos: el gateway corre **2026.9.4** (`gateway.self.version`, `runtimeVersion` y `gatewayService.layout.packageVersion` los tres coinciden). El proceso (pid 80466) arranco 13/09 22:16, **despues** del install manual de 2026.9.4 (package.json mtime 13/09 20:40), asi que quedo tomada. La linea "The gateway is running 2026.9.3" del `status` es un **registro historico obsoleto** del run automatico fallido (creado 13/09 11:51, con `before`/`after` en 2026.9.3), superado por el install manual posterior.
- **`qwen3.8:27b-mlx`: decision de Gonzo (14/09) - dejar como esta.** Se cierra la accion de evaluarlo/descargarlo. Sigue instalado (18 GB).
- **Contradiccion propia corregida:** quedaban dos acciones opuestas sobre `qwen3.8` (una que la cerraba y otra que pedia evaluarla). Se elimino la duplicada.

### Notes
- **Sigue abierto (item aparte del swap):** `openclaw doctor` reporta "Startup migrations need attention" y pide `openclaw doctor --fix` + restart. El swap de version esta resuelto; las migraciones no. Requiere al owner (el agente no reinicia el gateway).
- **Validacion del fix de bootstrap (doctor):** `USER.md` ahora reporta 3,985 chars = 20% del limite, y el doctor **ya no emite el finding `bootstrap-size`** que antes marcaba el truncado. Total inyectado 23.915 chars (40% del cap de 60.000).

## [2026-09-14] - USER.md bajo el cap fijo de bootstrap (10.008 -> 3.986)

### Changed
- **`USER.md`: 10.008 -> 3.986 chars.** OpenClaw le aplica un **cap fijo de 4.000 chars** (`USER_BOOTSTRAP_MAX_CHARS = 4e3` en `dist/bootstrap-DYYMCrXY.mjs`) que **no se puede subir** por config: verificado en codigo, gana sobre `bootstrapMaxChars`. Con 10.008 chars se descartaban ~6.000 en cada bootstrap (el truncado era observable en el contexto de la propia sesion). Ahora entra completo.
- **`MEMORY.md`: punteros corregidos.** Dos referencias mandaban a "USER.md > Trayectoria profesional", seccion que ya no existe ahi; apuntan a `memory/user-profile.md`.

### Added
- **`memory/user-profile.md`:** el detalle ampliado que salio de `USER.md` - trayectoria profesional completa (EY, Super7ui, Minutentag + el conteo de a11y y la nota sobre PHP 2001-2008), perfil diferenciador con el pitch, marca personal y alcance en LinkedIn, estilo en issues/PRs de terceros, y reglas de interaccion con su detalle y casos.
- **Por que en `memory/` y no en `docs/`:** `memory_search` indexa `memory/` y **no** `docs/`. Poner el detalle ahi lo mantiene recuperable por busqueda semantica en vez de solo por lectura explicita.

### Notes
- **Verificacion de cero perdida:** se comparo linea por linea el `USER.md` anterior contra el nuevo + `memory/user-profile.md`. Detecto una perdida real ("Quiere que maneje su vida, archivos y proyectos") que se restauro. El resto de las diferencias son reescrituras deliberadas para entrar en el cap.
- **Estado de los archivos de bootstrap (14/09):** AGENTS.md 15.059 (cap 20.000), MEMORY.md 16.361 (cap 20.000), USER.md 3.986 (cap fijo 4.000). **Los tres dentro de sus limites por primera vez desde el 28/08.**

## [2026-09-14] - Re-diagnostico de 0.1 (estabilidad del gateway) contra evidencia

### Changed
- **`docs/ROADMAP.md` 0.1 reescrito con evidencia dura.** La hipotesis original ("el gateway se reinicia solo bajo sesiones long-running, disparado por auto-compaction") **no se sostiene** contra los datos del 13-14/09:
  - Los **19 reinicios registrados son TODOS `source=cli`** (intencionales); cero espontaneos.
  - **`gateway.restart_close_failed` no es un crash:** verificado en `dist/run-fzUO4BXB.mjs:1088` - si `server.close()` lanza durante un restart, marca `shutdownFailed` y fuerza la salida con stability bundle. Es cierre sucio de un restart pedido.
  - **La compactacion no aparece:** los 4 dumps tienen `compaction_events=0`. El gatillo del 28/08 no se reproduce.
  - Los 4 dumps son una cascada de 1h36m (23:40 / 00:02 / 00:56 / 01:16) y el primero (uptime 55h) coincide con el update fallido. Errores de modelo en la ventana: 3x `qwen3.8:27b-mlx` de ~50s + 1x `deepseek-v4-flash`.
  - Runtime: npm/CLI en **2026.9.4** pero el gateway corre **2026.9.3** con update fallido y startup migrations pendientes - swap de version a medio hacer.

### Added
- **Hallazgo: `USER.md` se trunca en cada arranque.** Tiene un **cap fijo de 4.000 chars** (`USER_BOOTSTRAP_MAX_CHARS = 4e3`, `dist/bootstrap-DYYMCrXY.mjs`), NO configurable por `bootstrapMaxChars`, y el archivo real tiene **10.008 chars** -> se descartan ~6.000 chars de preferencias en cada bootstrap. Detectado con `openclaw doctor`. Es el mismo problema de fondo que tenia AGENTS.md, en un archivo sin margen.

### Notes
- **Ningun archivo se edito fuera del workspace.** El diagnostico fue 100% lectura (logs, dumps via `jq` selectivo, codigo fuente, `doctor --json`).
- **Criterio de señal de listo corregido:** "15+ POST + 11 GET sin reinicio" no probaria nada sobre reinicios espontaneos (no los hay). La señal util es **0 dumps nuevos en `logs/stability/` tras una sesion pesada**.
- Acciones nuevas en 0.1: bajar `USER.md` a <=4.000, completar el swap de version, redefinir la señal, y evaluar `qwen3.8:27b-mlx` (17-18 GB en una Mini de 24 GB).

## [2026-09-14] - AGENTS.md bajo el limite de bootstrap (regresion resuelta)

### Changed
- **`AGENTS.md`: 24.638 -> 15.167 chars.** La seccion `## Tools` (11.334 chars, el 46% del archivo) era el cheat sheet de entorno migrado desde el viejo `TOOLS.md` - scripts, modelos, maquinas, memoria, red - no reglas de conducta. Se movio intacto a **`docs/SETUP.md`** y en su lugar quedo un puntero con un resumen operativo minimo. AGENTS.md vuelve a estar bajo el limite de inyeccion de contexto (20K chars) por primera vez desde el 28/08.

### Added
- **`docs/SETUP.md`:** cheat sheet del entorno (maquinas, modelos Ollama local+cloud, pipeline de agentes, tabla completa de scripts del workspace, memoria SQLite + espejos, red/remoto). Es el destino de la seccion `## Tools`, consistente con la convencion de OpenClaw (las notas de entorno viven en `## Tools` de AGENTS.md, que es lo unico que reciben los subagentes - por eso AGENTS.md conserva el resumen minimo).

### Notes
- **Verificacion de cero perdida:** las 170 lineas de reglas de AGENTS.md quedaron identicas byte a byte (`diff` contra el backup en `/tmp`), y las 74 lineas significativas del bloque `## Tools` viejo se compararon una por una contra `docs/SETUP.md` - las 3 diferencias restantes son cosmeticas (dos encabezados viejos de TOOLS.md descartados a proposito y el footer de fecha actualizado).
- **Contexto:** AGENTS.md habia bajado a 8.890 chars el 28/08, pero volvio a 24.044 el 14/09 y seguia creciendo (24.638 al momento del corte). El truncado era observable en el propio bootstrap de la sesion. Esta es la accion P0 de 0.1 (estabilidad del gateway) del `docs/ROADMAP.md`.
- `MEMORY.md` queda en 16.483 chars, dentro del limite.

## [2026-09-14] - Regla: el precedente no es un motivo (dependencias de UI/stack)

### Changed
- **`USER.md` - regla de dependencias.** Ninguna dependencia de UI o stack se adopta, se mantiene ni se cita como justificada por el solo hecho de estar ya presente o de haberse usado antes. Orden obligatorio antes de citarla como fundamento: (1) que hace, (2) por que se elige hoy, (3) decision explicita (ADR si corresponde), (4) recien entonces se cita. Origen: Gonzo marco que Radix/shadcn entraron por el template, sin decision, y hoy se citan como si fueran un hecho del stack.
- **`AGENTS.md` - seccion 3 (Ingenieria).** Nueva subseccion "Dependencias: el precedente no es un motivo" junto a Existing Solutions Preflight, con la regla operativa y el caso que la motiva.

### Added
- **ADR-048: Radix/shadcn como capa de UI** (`docs/adr/ADR-048-shadcn-radix-stack-ui.md`). El ADR de adopcion que no existia: hasta hoy la eleccion venia del template y `ADR-037` la citaba como si fuera una decision tomada. Documenta las 4 alternativas evaluadas con datos verificados (Radix vs Base UI vs Ariakit vs HTML nativo), 7 reglas de uso (incluida **cuando NO usar Radix**) y 4 disparadores de revision. Nace de la regla "el precedente no es un motivo" (mismo dia).
- **`docs/adr/ADR-037` - nota de respaldo:** la cita al "ecosistema shadcn/Radix" dejo de ser circular; apunta al ADR-048.
- **Estudio `radix-primitives` COMPLETO** (`studies/radix-primitives/`): 5 niveles, 46 topics, 460 XP. Cuadernos 1-5. Hallazgos verificados: `kanam-pulse` es a11y-first y no usa Radix a proposito; solo 2 de 4 proyectos lo usan de verdad; dos generaciones de shadcn conviviendo (`forwardRef` vs `data-slot`); el dist-tag `latest` de Ariakit apunta a un prerelease de 2023.
- **Leccion `metodologia`:** el precedente fabricado - una eleccion implicita del template (shadcn/ui + Radix) citada despues como decision tomada en `ADR-037` (Lucide), que el propio ADR admite no haber documentado como decision.
- **TODO:** decidir el destino de Radix/shadcn en el stack UI (aprenderlo, evaluar reemplazo, o dejar la deuda anotada). Verificado: no existe ADR de adopcion de shadcn/Radix en el workspace; `grep shadcn|radix docs/adr/` devuelve solo ADR-037.

### Notes
- **Verificacion negativa registrada:** no hay paquetes `@radix-ui`, lockfiles ni `package.json` en el workspace (el codigo vive en repos aparte), asi que el uso real de Radix no se puede confirmar desde aca. Una afirmacion previa de esta sesion ("Radix si lo usamos") se apoyo en menciones declarativas de docs, no en evidencia de instalacion - corregida antes de escribir la regla.

---

## [2026-09-14] - Limpieza y revision real de docs/ROADMAP.md

### Changed
- **`docs/ROADMAP.md` - reescritura de estado contra fuentes reales.** El documento no se tocaba desde el 28/08 y tenia 22 checkboxes abiertos bajo encabezados que declaraban los 11 items en 🟢. Se contrasto cada item contra git, GitHub, hooks y logs:
  - **Tachadas por hechas:** `.gitignore` de archivos de sesion (lineas 10-11); la nota de `init-project.sh` (el script ya excluye `.knowledge/` via `.git/info/exclude`, lineas 26-28 y 203 - la premisa de la nota era falsa); los tres items de 2.1 (resueltos por ADR-001).
  - **Borradas por obsoletas:** cambios sucios de `kanam-forge`/`kanam-mind` (ninguno tiene `.git` propio); los tres items fechados de busqueda laboral del 31/08-01/09 (vencidos).
  - **Regresion detectada:** AGENTS.md volvio a **24.044 chars** (habia bajado a 8.890 el 28/08) -> otra vez sobre el limite de bootstrap de 20.000. MEMORY.md en 16.099. Por eso 0.1 vuelve de 🟢 a 🟡, con 4 dumps `gateway.restart_close_failed` del 13/09 y reinicios los dias 08, 11, 13 y 14/09.
  - **Auditoria de hooks (1.3):** **0 de 21** proyectos tiene `pre-commit` hook o `simple-git-hooks`. La senal de listo de 1.3 no se cumple -> 🟡.
  - **2.3 Busqueda laboral:** actualizada al estado real (oferta EIT/HTC/Disney aceptada el 11/09, arranque 01/10). El criterio de exito esta cumplido.
  - **Estados corregidos:** 0.1, 1.1, 1.2, 1.3 y 2.2 pasan de 🟢 a 🟡.

### Added
- **`docs/checklists/roadmap-review-checklist.md`:** procedimiento de revision del ROADMAP contra fuentes reales (git, GitHub, filesystem, logs, DB). Define cuando correrlo, la tabla de veredictos (hecho / pendiente / obsoleto / regla / restriccion cerrada), que fuente usar por tipo de item, el recalculo de estados y la reconciliacion de la tabla de prioridad. Incluye los antipatrones observados (marcar 🟢 por optimismo, usar el ROADMAP como backlog, confiar en el encabezado, revisar de memoria).

### Notes
- **Rol del documento explicitado:** el ROADMAP define decisiones y estado por capa; el "para que" de largo plazo es `docs/NORTH.md`, y la lista de tareas es `memory/memory.db` (`todos`). Se agrego el encabezado "Que NO es este documento" para cortar la duplicacion de backlog, y el puntero al checklist de revision.
- **Regla nueva:** un item solo pasa a 🟢 con evidencia de su senal de listo, y la revision se hace contra fuentes reales - no contra lo que creiamos recordar.
- **`kanam-skills` reverificado:** el item abierto de 0.2 se corrigio con el estado real - el repo vive en `projects/kanam-skills` con `.git` propio y remote a `gonzoblasco/kanam-skills`, excluido a proposito en `.gitignore:113`. No es "sin trackeo" por olvido: la exclusion es deliberada.

## [2026-09-14] - Alineacion de anclas del portfolio (NORTH + ROADMAP + BRIEF a11y-fixer)

### Fixed
- **`docs/NORTH.md` - conteo de anclas inconsistente:** la tabla de la constelacion decia "2 anclas, 5 activos, 2 experimentos" mientras la seccion siguiente listaba **3** anclas (kanam-forge, a11y-fixer, kanam-pulse, segun ADR-001). Corregido a "3 anclas, 3 de infraestructura interna, 3 en la linea narrativa, 2 experimentos".
- **`docs/ROADMAP.md` 2.1 - accion stale:** la accion abierta proponia "Definir los 2-3 proyectos ancla (candidatos: SoporteML, kanam-forge, a11y-fixer)", con SoporteML ya EXCLUIDO por decision cerrada (ADR-001 seccion 4 + MEMORY.md) y sin kanam-pulse. Actualizada a los 3 anclas reales de ADR-001, con la exclusion de SoporteML marcada como cerrada. Las tres acciones de 2.1 pasan a `[x]` (las tres estan resueltas por ADR-001 del 2026-08-28).

### Added
- **`projects/a11y-fixer/.knowledge/BRIEF.md`:** era la unica de las tres anclas sin BRIEF (solo tenia HANDOFF autogenerado). Contenido verificado contra `package.json`, releases de GitHub, la API del repo, el registry de npm y el README real - no contra memoria.

### Fixed (revision del HANDOFF, 2026-09-14 - pedido de Gonzo)
- **`BRIEF.md` reescrito tras revisar el HANDOFF de verdad.** El HANDOFF del 2026-08-02 listaba 3 Next Steps y los tres quedaron **invalidados** al contrastarlos con el repo:
  - **Paso 1 ("definir roadmap v0.7: baseline comparison, AI explanations, config validation") - obsoleto desde el momento en que se escribio.** Las tres features ya estaban en v0.6.0 (released 2026-07-29, nueve dias antes del HANDOFF): baseline = Epic 1.5.3, AI explanations = Epic 3.1, config validation = Zod schema en Epics 1.1.3/1.1.4.
  - **Paso 2 ("abrir issues para gaps conocidos") - parcial.** Los issues #10 y #11 existian. **#11 cerrado el 2026-09-14** (documentacion verificada completa: `CONTRIBUTING.md` + los 4 ejemplos existen en el repo). **#10 NO se cierra** - su premisa es falsa (ver abajo).
  - **Paso 3 ("sumar session-context save al ritual de cierre") - hecho.** El repo versiona su `.knowledge/` y tiene commits de update del 02/08.
- **Correccion de marco en el BRIEF:** el proyecto **no esta abandonado a mitad de camino, esta feature-complete**. El `docs/TRACKER.md` del propio repo marca **40/40 tareas** completas en las Fases 1-4. Lo que falta no es codigo: es **adopcion**. El BRIEF anterior lo presentaba como "ancla fria" sin el dato de que esta terminado.
- **HALLAZGO VERIFICADO - el action NO esta publicado en GitHub Marketplace.** El check `4.1.2` del issue #10 y de `docs/TRACKER.md` lo dan por hecho, y es falso. Verificado con prueba de control (el fetch directo no alcanzaba: la pagina se renderiza por JS):
  - `marketplace/actions/checkout` (control positivo) = **200**
  - `marketplace/actions/definitely-not-a-real-action-xyz123` (control negativo) = **404**
  - `marketplace/actions/a11y-fixer` / `-action` / `gonzoblasco-a11y-fixer` = **404** los tres
  - En el listado de acciones de accesibilidad del Marketplace aparecen `a11y-check`, `a11yguard`, `accessibility-scanner` y otros; `a11y-fixer` no aparece.
  - El branding en `action.yml` (icon: eye, color: green) es el **preparativo** para publicar, no la publicacion. Falta cortar un release con la opcion "Publish this Action to the GitHub Marketplace" tildada - eso requiere accion de Gonzo en la UI, no es automatizable.
- **Consecuencia:** el issue #10 queda abierto en lugar de cerrado. Una tarea marcada como hecha que nunca se hizo es peor que una tarea abierta: infla el progreso real.
- **Dato verificado:** `@gonzoblasco/a11y-fixer@0.6.0` **esta publicado en npm** (registry.npmjs.org, 2026-07-29) y el README no lo menciona - hay un canal de distribucion activo que la documentacion no explota. *(Esto es npm, distinto del Marketplace.)*

### Notes
- **Gap operativo documentado en el BRIEF:** el codigo de a11y-fixer NO esta clonado en el workspace - `projects/a11y-fixer/` contiene solo `.knowledge/`. Para trabajar en el hay que clonar el repo aparte. El repo si versiona su propio `.knowledge/` (HANDOFF + session-context).
- **Leccion de metodo:** "leer el HANDOFF" no es "revisar el HANDOFF". El primer BRIEF se escribio con los Next Steps copiados y marcados como "sin revisar"; al verificarlos contra el repo, los tres estaban vencidos o ya hechos. Un handoff es una hipotesis con fecha - se valida contra la fuente, no se transcribe.
- Auditoria de consistencia entre `docs/NORTH.md`, `docs/ROADMAP.md` y `projects/portfolio-strategy/ADR-001`, a raiz de la pregunta de Gonzo sobre el para que del proyecto (2026-09-14).

## [2026-09-14] - Fix del export DB->.md (pisada de contenido) + causa raiz del drift

### Fixed
- **`scripts/memory-end-session.py` - el export DB->.md pisaba contenido del `.md`:** `export_daily_to_md` regeneraba `memory/YYYY-MM-DD.md` DESDE la DB sin comparar, y la DB no siempre es la fuente mas completa. Repro real: 17 lineas del daily del 14/09 (secciones de dos sesiones paralelas) se borraron, y el mismo flujo amenazaba los dias 12-14. **Guard nuevo `reconcile_md_into_db`:** corre ANTES del export, compara secciones `.md` vs DB, mergea hacia la DB las que solo viven en el `.md` y preserva las solo-en-DB; si la fecha no tiene fila, la crea desde el `.md` entero. Backup del `.md` en `/tmp/daily-<fecha>.backup.md` antes de regenerar. Escape hatch `--no-reconcile` reproduce el comportamiento viejo (opt-in). **Probado con 6 escenarios:** A (md-only mergea, seccion sobrevive), B (DB cubre el `.md`: guard silencioso, sin merge espurio), C (DB-only preservado), D (sin fila en DB: la crea desde el `.md`), E (`--no-reconcile`), F (idempotencia).
- **`scripts/memory-end-session.py` sin permiso de ejecucion:** estaba `644` y se invocaba como `./scripts/memory-end-session.py` - fallaba con `permission denied`. Ahora `755`.

### Changed
- **`AGENTS.md`:** protocolo de "guardar sesion" ahora dice explicitamente que el daily se escribe con `session-end.sh` / `memory-end-session.py`, **nunca editando el `.md` a mano**; tabla de scripts actualizada con el guard y `--no-reconcile`.
- **`skills/session-lifecycle/SKILL.md`:** documentado el guard de reconciliacion (por que el export era lossy y como se reconcilia ahora).
- **`.github/skills/session-lifecycle/SKILL.md`:** mirror sincronizado (`SKILLS-INDEX.md` restaurado tras el rsync).
- **`memory/todos.md` / `docs/learnings/`:** regenerados desde la DB.

### Added
- **Leccion `infraestructura`:** causa raiz doble del drift 12-14 - (1) flujo: guardar sesion es manual y los dias 12/13 el daily se edito directo en el `.md` sin correr el script, asi que la DB no recibio fila; (2) bug del script: export a ciegas sin comparar superficies.
- **`docs/learnings/infraestructura.md`:** protocolo de reconciliacion previa al export.

### Notes
- **Causa raiz del flujo cortado (evidencia):** la DB tenia como ultima fila `2026-09-11` (13:41) mientras los `.md` de 12, 13 y 14 existian. Los dias 12 y 13 se commiteo el daily (`track(oss)`, `docs(prefs)`, `c5f6f07`) **sin** un `chore(session)`/`docs(session)` de cierre, y sin `## Session End` en el `.md` (0 blocks en 12 y 13, contra 5 en el 11). Conclusion: se edito el `.md` a mano y nunca se corrio el guardado.

## [2026-09-14] - Fix de CI en PR #10503 + recuperacion de drift en daily_notes

### Fixed
- **`daily_notes` desincronizado de los `.md` (drift detectado 14/09):** la ultima fila de la DB era `2026-09-11`, mientras `memory/2026-09-12.md`, `-13.md` y `-14.md` existian con contenido. Correr `memory-end-session.py` tal cual habria regenerado el `.md` desde una DB sin la fila del dia, pisando el contenido. Se sembraron las filas faltantes desde los `.md` antes de escribir. **Verificado sin perdida:** 100/100 lineas originales del 09-13 y 34/34 del 09-12 presentes post-regeneracion.
- **Consolidacion de sesion perdida:** `memory/2026-09-13-2041.md` (y su duplicado `-2041-2.md`, generados por un `sessions.reset`) contenian la sesion del update de OpenClaw por terminal que el daily del 09-13 NO tenia. Consolidada al daily y ambos sueltos movidos a `memory/archive/`.

### Added
- **Leccion `oss`:** cambio en helper compartido -> grepear consumidores por simbolo Y por asercion, no solo el archivo editado (caso #10503: `SearchAutocomplete` consume `useComboBox` y quedo con aserciones del comportamiento viejo).
- **Leccion `infraestructura`:** protocolo para el drift `daily_notes` vs `.md` (comparar, sembrar la DB, backup, verificar linea por linea).
- **Leccion `infraestructura`:** entorno local para correr los tests de adobe/react-spectrum (yarn 4 vendorizado, `postinstall` obligatorio por los iconos, `STRICT_MODE=1 VIRT_ON=1`, lint via `oxlint`/`oxfmt`).
- **Leccion `metodologia`:** precision al reportar fallos de herramienta - nombrar el comando exacto, no mezclar binarios (caso `git push` vs `gh`).

### Changed
- **`AGENTS.md`:** nueva regla 0b en "Feedback en PRs/issues ajenos" - alcance: un ticket por vez, tickets como entidades individuales salvo pedido explicito. Referencia si, sentencia no: se puede referenciar trazabilidad de otro ticket, nunca concluir su estado sin verificacion directa.
- **`CONTRIBUTING.md`:** seccion nueva "Alcance: un ticket por vez" con la regla, la prohibicion de cerrar/dar por resuelto un ticket no pedido, el matiz "referencia si, sentencia no" y la excepcion unica (dependencia real entre tickets).
- **`USER.md`:** regla "Verificar antes de descartar" (agregada 13/09, se commitea junto con este cierre).
- **`docs/OSS-TRACKER.md`:** contribuciones id=46 e id=58 (#10503) actualizadas con el diagnostico y fix del CI.
- **`memory/2026-09-12.md`, `-13.md`, `-14.md`:** regenerados desde la DB (ahora con las filas sembradas) + secciones nuevas del 14/09.
- **`projects/kanam-lab/.knowledge/BRIEF.md`:** fases renumeradas (v1/v2/v3 -> Fase 1/1.5/2/3).

## [2026-09-11] - ADR-046: revert del motor del pipeline A/B a deepseek-v4-flash (por costo)

### Added
- **`docs/adr/ADR-046-motor-pipeline-revert-deepseek-v4-flash.md`:** el motor de los agentes A/B del pipeline vuelve a `deepseek-v4-flash:cloud`. Revierte ADR-045 (v4.1 como motor) por costo: medido en el uso semanal de Ollama Cloud, v4.1 consumia mas por request que v4 y glm (1.348 requests con la barra mas alta, contra 1.631 de v4 con la mas baja). v4.1 baja a fase de escalada para analisis complejo.
- **Convencion `Status: Superseded`:** primer uso del campo en ADR-045 (antes ningun ADR lo usaba; los superseded se marcaban solo con nota al pie).

### Changed
- **`docs/adr/ADR-045`:** `Status: Accepted` -> `Superseded por ADR-046` + nota de actualizacion. Las reglas tecnicas sobre v4.1 (think:false en roles mecanicos, API /api/chat con stream:false) siguen vigentes solo al escalar a v4.1.
- **`docs/adr/ADR-041`:** nota de actualizacion del 11/09 reapuntada de ADR-045 a ADR-046.
- **`docs/adr/README.md`:** agregado ADR-046 al indice; ADR-045 marcado como superseded.
- **`MEMORY.md`:** motor del pipeline = `deepseek-v4-flash:cloud` (ADR-046). Nueva leccion: nombres de modelo no intercambiables - `deepseek-v4-flash:cloud` resuelve en Ollama (motor del pipeline), `deepseek-v4-flash:0731` es solo del runtime de OpenClaw y NO resuelve en Ollama.
- **`docs/pipeline/kanam-product-pipeline.md`:** nota de modelo actualizada con el revert por costo.
- **`docs/learnings/pipeline-agentes.md`:** nota de actualizacion en la leccion de v4.1 - el valor del review por ejecucion y de la autoverificacion del motor no depende del modelo.

### Fixed
- **`model-router.json`: overrides sticky pineando v4.1.** El estado runtime del router tenia `overrides.code`, `overrides.review` y `overrides.pipeline_ab` en `deepseek-v4.1-flash:cloud` (seteados el 11/09 al promover v4.1 como motor). **Ese era el mecanismo real que forzaba v4.1 en el pipeline.** Reseteados los tres: el router vuelve a las rutas por defecto (v4-flash). Verificado con `model-router.sh list` (Overrides: ninguno).
- **`model-router.json` agregado a `.gitignore`:** estado runtime del router (generado por `model-router.sh`), machine-local. Estaba sin trackear pero SIN regla de ignore.

### Notas operativas
- **Watcher `ds-v4.1-rollout-watcher` deshabilitado:** su proposito (avisar cuando v4.1 saliera del rollout) quedo cumplido el mismo dia y obsoleto por este ADR. Se deshabilito, no se borro.
- **Sin cambios en `openclaw.json`:** el motor del pipeline no vive ahi. Se fija por el `--model` de la invocacion (Claude Code / Qwen Code) y por el router. El default de OpenClaw ya era v4-flash desde el revert de las 19:15.

## [2026-09-11] - Unificacion del modelo de embeddings: todo el workspace a qwen3-embedding

### Changed
- **9 scripts alineados a `qwen3-embedding:0.6b` (1024 dims):** `memory-catalog-v2.py`, `memory-catalog.sh`, `memory-catalog-simple.sh`, `memory-topics.py`, `memory-search.py`, `skill-router.py`, `semantic-search.js`, `semantic-search-json.js`, `memory-reembed.py`. Antes usaban `nomic-embed-text:latest` (768 dims) mientras `openclaw.json` usaba qwen3: dos espacios vectoriales incomparables entre si.
- **`memory-reembed.py` ahora detecta por dimension objetivo**: hace un probe del modelo y re-embebbea todo vector cuyo dim no coincida con el output real, en vez de solo cazar los fallbacks de 32 dims. Asi tambien sirve para migrar de modelo.
- **Vectores migrados:** 207 filas re-embebidas (`learnings_enriquecido` 104 + `session_vectors` 103), todas a 1024 dims. Cero vectores de 32, cero de 768.

### Fixed
- **`memory-search.py` y `memory-topics.py` tenian el mismo bug de `requests`** que `memory-catalog-v2.py` (importaban `requests`, ausente en el python del sistema -> fallback silencioso a hash SHA-256). Pasados a `urllib.request`.
- **`memory-catalog.sh` y `memory-catalog-simple.sh`**, mismo bug dentro de sus heredocs Python.
- Queda **cero** uso de `requests` en `scripts/`.

### Notes
- Verificado end-to-end: catalogo completo 20/20 sin regenerar fallbacks, `memory-search.py` y `semantic-search*.js` devuelven texto y scores coherentes, `memory-topics.py --list` corre, y `skill-router.py` ahora resuelve por embedding real (no solo keyword).
- **Documentacion alineada:** `AGENTS.md` (modelos locales, tabla de scripts), `skills/skill-router/SKILL.md` + su espejo en `.github/skills/`.
- **Correccion de un error mio:** en el CHANGELOG anterior afirme que `nomic-embed-text` no estaba instalado. Si esta (768 dims). Y `qwen3-embedding:0.6b` es de **1024** dims, no 768.
- Backups: `/tmp/db-before-qwen3.db` (pre-migracion), `/tmp/db-before-reembed.db`, `/tmp/db-before-catalog-fix.db`.

---

## [2026-09-11] - Fix raiz: el catalogo de memoria generaba vectores basura (requests ausente)

### Fixed
- **`scripts/memory-catalog-v2.py` > `get_embedding()`**: cada llamada caia al fallback SHA-256 de 32 dims, incluso con Ollama arriba. Causa: `import requests` dentro de la funcion - el python del sistema (`/usr/bin/python3`, 3.9.6) **no tiene `requests` instalado**, asi que la excepcion `ModuleNotFoundError` se tragaba silenciosamente y devolvia el hash. Por eso cada corrida del catalogo regeneraba vectores inutiles, y los centroides de categoria quedaban construidos sobre ruido.
- **Fix:** reemplazar `requests` por `urllib.request` (stdlib, cero dependencias). Ademas, cuando el fallback se activa ahora imprime un aviso explicito a stderr indicando que el vector NO sirve para busqueda semantica y como repararlo.
- **`scripts/memory-reembed.py` (nuevo)**: re-embebbea los vectores fallback existentes contra Ollama. Deliberadamente **no** tiene fallback: si el modelo falla, deja la fila intacta y la reporta, para no volver a escribir basura. Uso: `./scripts/memory-reembed.py [--dry-run] [--limit N]`.

### Notes
- Reparados **325 vectores fallback** (177 + 148 en dos pasadas: la primera corrida del catalogo intermedio regenero algunos antes del fix de raiz).
- Estado final verificado: `learnings_enriquecido` 104/104 y `session_vectors` 103/103 en 768 dims, cero de 32. Re-correr el catalogo completo ya no regenera ninguno.
- La busqueda semantica paso de devolver `text: ""` a devolver contenido y scores mas altos y coherentes (0.61 en a11y vs 0.58 previos sobre embeddings falsos).
- Backups: `/tmp/db-before-reembed.db`.

### Pendiente (no aplicado, requiere decision)
- **Modelo de embeddings inconsistente en el workspace.** `scripts/memory-catalog-v2.py`, `memory-catalog-simple.sh` y `semantic-search*.js` usan `nomic-embed-text:latest` (**768** dims), pero `openclaw.json` (`memory.search.model` y `models.providers.ollama-local`) usa `qwen3-embedding:0.6b` (**1024** dims). Son dos espacios vectoriales distintos: las dos rutas de busqueda no son comparables. Alinear a uno solo.

---

## [2026-09-11] - Fix: memory-catalog-v2.py crasheaba por dimensiones mixtas de embeddings (+ chunk_text NULL)

### Fixed
- **`scripts/memory-catalog-v2.py` > `compute_category_centroids()`**: crasheaba con `IndexError: list index out of range` (linea 222) y el catalogo entero no corria. Causa: mezcla de dimensiones en `learnings_enriquecido`. 85 filas tenian vectores de **32 dims** (fallback SHA-256 del script, cuando Ollama no responde o se usa `use_ollama=False`) y 4 filas **768 dims** (modelo real). El loop inicializaba el centroide con la dimension del primer vector de la categoria y despues indexaba con la de los siguientes -> IndexError. `compute_topic_centroids()` ya tenia el guard; `compute_category_centroids()` no.
- **Fix:** mismo guard que topic centroids (el vector de dimension distinta se omite y se cuenta), mas un aviso a stderr con el total omitido por categoria, para que la deuda de vectores viejos sea visible.
- **`session_vectors` > `chunk_text` NULL**: el catalogo nunca escribia esa columna (el INSERT no la incluia) y la tabla creada por v2 no la tenia. Resultado: **108 de 108 filas con `chunk_text` NULL**, y la busqueda semantica devolvia matches con `text: ""`. Se agrego la columna al CREATE TABLE, una migracion `ALTER TABLE` para DBs viejas, y la columna al INSERT.

### Notes
- Verificado: catalogo completo 20/20, busqueda semantica devuelve texto real.
- Backfill de historicos: 46 filas recuperadas desde `sessions_relacional.content_bare`. 5 filas quedaron fuera: 3 con `chunk_index` mas alla del contenido actual (vectores de texto que ya no existe) y 2 huerfanas de una sesion borrada -> eliminadas. `session_vectors` 108 -> 103, cero vacias, cero huerfanas.
- **Deuda pendiente:** quedan 103 vectores de 32 dims (fallback) y 1 de 768. Los fallback no sirven para similitud semantica real. Re-embeddear con `qwen3-embedding:0.6b` (768) reincorporaria esas filas y mejoraria el ranking.
- Backups: `/tmp/db-before-catalog-fix.db` (pre-fix) y `/tmp/db-before-chunktext-fix.db` (pre-chunk_text).

## [2026-09-11] - Revert parcial de modelos: primary vuelve a deepseek-v4-flash

### Changed
- **`MEMORY.md` + `agents.defaults.model.primary`**: primary de `ollama-cloud/deepseek-v4.1-flash` a `ollama-cloud/deepseek-v4-flash:0731`. Motivo: uso semanal medido (v4.1 consume mas que GLM 5.3 Flash y v4 con menos requests; v4 el mas eficiente por request). Roles definidos con Gonzo: v4 = primary, glm-5.3-flash = fallback + vision, v4.1 = fase de escalada para analisis complejo (entre glm y Kimi K2.7 Code en costo). v4 deja de existir en unas semanas - a reevaluar entonces.

## [2026-09-11] - kanam-tetris v0.3: refactor estructural + red de tests

### Changed
- **`projects/kanam-tetris/`**: el single-file de 901 líneas se parte en módulos ES sin build ni dependencias. `src/core.js` (530) queda puro -sin DOM, canvas, reloj ni storage-, con `step(deltaMs)` determinista y `rng` inyectable. `index.html` baja a 193 líneas y monta `src/main.js` como módulo.
- **`projects/kanam-tetris/test/`**: red nueva con `node --test` nativo, cero dependencias. 33 tests: las reglas del core (los bugs que costaron dos ciclos de pipeline en v0.2) más el cableado del browser.
- **`projects/kanam-tetris/package.json`** (nuevo): `type: module` y `npm test`.
- **`projects/kanam-tetris/README.md`**: cómo correrlo (necesita `python3 -m http.server`, porque `file://` bloquea módulos ES), estructura de módulos y contrato del core.

### Fixed
- **`blur` registrado en `document` en vez de `window`**: `blur` no burbujea y el foco de ventana se dispara en `window`, así que el handler nunca corría. Con una flecha apretada, salir con Cmd+Tab dejaba el DAS vivo y la pieza seguía deslizándose. `attachInput` acepta `blurTarget` inyectable para que la costura sea testeable en Node.

### Notas
- Cero features nuevas: comportamiento observable idéntico a v0.2, con la excepción del fix de `blur`.
- Verificado por mutación: reintroducir cada uno de los bugs históricos hace fallar el test que le corresponde. El guard de `clearing` en `rotate()` sobrevive la mutación porque es defensa en profundidad inalcanzable, no un agujero de cobertura.
- Pendiente: validación visual en browser real (píxeles de canvas, rampa del flash, centrado de previews). El review comparó el código, no midió render.

## [2026-09-11] - Trayectoria verificada de Gonzo en USER.md/MEMORY.md + voz-gonzo v2 (reglas 9-12)

### Added
- **`USER.md` > Trayectoria profesional (verificado)**: nueva seccion con las empresas, fechas y logros reales (Minutentag/EULAS 2016-2019, Super7ui 2020-2021 con 1 ano dedicado a a11y, EY 2021-2025 como referente enterprise), mas la lectura correcta para propuestas a11y y el unico gap real (certificacion IAAP). Antes esta data solo vivia en `memory/archive/2026-08-19-0951.md` y se perdia entre sesiones.
- **`MEMORY.md`**: regla nueva - antes de afirmar algo sobre la trayectoria de Gonzo, buscar en memoria primero; marcar gaps solo con evidencia. Entrada de trayectoria en "Sobre Gonzo".
- **`docs/voz-gonzo.md`**: 2 casos nuevos (EIT, en ingles) y 4 reglas consolidadas (9-12). Alcance extendido a ingles cuando el hilo es con un tercero en ingles.

### Changed
- **Skill `voz-gonzo`** (workshop): paso explicito de definir longitud antes de escribir y filtro de recorte que incluye preguntas que no bloquean el arranque. La version que se entrega es la mas corta que hace el trabajo, no la mas completa.
- **`docs/entrevistas/`**: seguimiento de EIT/HTC/Disney + CV a11y unico (markdown + PDF generado con `scripts/pdf-tool.sh md2pdf`).

## [2026-09-11] - Registro de voz de Gonzo (espanol) + skill viva `voz-gonzo`

### Added
- **`docs/voz-gonzo.md`**: registro vivo de como Gonzo se expresa en espanol. Estructura por caso (contexto, borrador Kanam, edicion final, que cambio, patron) + seccion "Reglas consolidadas" que la skill aplica por defecto. Primer caso: respuesta a rechazo de OpenSistemas (2026-09-11).
- **Skill `voz-gonzo`** (`~/.openclaw/agents/main/agent/workshop-skills/voz-gonzo/`, creada via `skill_workshop`): redactar en espanol en nombre de Gonzo y aprender de cada edicion suya. 7 pasos: leer corpus -> identificar objetivo real (presente vs futuro) -> redactar -> entregar con variantes -> registrar la edicion -> consolidar solo si el patron cambio -> escanear guiones.

### Notas
- Alcance: interacciones en espanol (LinkedIn, mails, mensajes directos, entrevistas). Fuera de alcance: GitHub y repos (ingles, rige USER.md + AGENTS.md).
- Reglas consolidadas iniciales: presente no futuro; alcance amplio; calido sin adornos; no exponer urgencia; sin numeros por escrito; cerrar con confianza; honestidad emocional medida; guion comun siempre.

## [2026-09-11] - kanam-tetris v0.2: segundo ciclo del pipeline A/B con deepseek-v4.1-flash

### Added
- **`projects/kanam-tetris/index.html` (v0.2):** seis features nuevas sobre la base v0.1, implementadas por el Agente A (deepseek-v4.1-flash:cloud via Claude Code + gateway Ollama) y revisadas por el Agente B con un harness instrumentado:
  - Hold piece (`C`), un hold por pieza clavada.
  - Lock delay con cap de 15 resets (move reset, guideline SRS).
  - DAS 170ms / ARR 50ms con re-step inmediato al cambiar de direccion.
  - Flash de 180ms al limpiar lineas antes de removerlas.
  - Pausa (`P`/`Esc`) con overlay.
  - High score persistente en localStorage.
- **`projects/kanam-tetris/.knowledge/BRIEF.md`:** alcance v0.2 documentado.

### Fixed
- **Guard de estado `clearing` (bug nuevo, alcanzable en juego normal):** durante el flash de limpieza la pieza ya clavada seguia siendo controlable. Mantener Espacio reseteaba el timer y congelaba la limpieza de linea indefinidamente; una flecha + Espacio estampaba bloques fantasma con score duplicado (invisible porque `draw()` suprime la pieza activa durante el flash). Guards agregados en `rotate()`, `move()`, `hardDrop()` y el keydown.
- **Lookup de wall kicks CCW espejado (preexistente desde v0.1):** la tabla tenia las 8 filas direction-specific correctas, pero el indice leia la fila CW de la transicion inversa para rotacion antihoraria. Unificado a `${from}>${to}` para ambas direcciones.
- **`holdUsed` reset movido a `afterLock()`:** el preview de Reserva ya no se "des-dim" 180ms antes de ser usable.
- **`saveHighScore()`:** sacado de `checkHighScore()` (que sigue actualizando el HUD en vivo); unica escritura en `endGame()`.
- **Clamp de delta:** `Math.max(0, Math.min(time - lastTime, 100))` - un delta negativo podia propagarse a `lockTimer`, `dropCounter` y `clearing.timer`.

### Changed
- **`projects/kanam-tetris` pusheado a GitHub:** https://github.com/gonzoblasco/kanam-tetris (antes vivia solo local). `HEAD == origin/main`.

### Why
- Cerrar v0.1 con un ciclo real del pipeline A/B usando el motor nuevo (v4.1), aplicando la pausa obligatoria (A escribe -> B revisa -> Kanam revisa el conjunto -> push). El review de B demostro que para bugs dependientes de tiempo el reviewer debe EJECUTAR, no leer: los dos criticos eran invisibles a la lectura del codigo.

### Notes
- El bug de CCW estaba desde v0.1 y lo dejamos pasar ayer porque el review se centro en las filas de la tabla, no en el indice. Leccion registrada: al revisar una base, revisar el lookup, no solo los datos que indexa.
- Aprendizaje operativo: `git push` falla con `could not read Username for 'https://github.com'` cuando osxkeychain no tiene credencial; se resuelve inyectando `GH_TOKEN=$(gh auth token)` como credential helper inline.

## [2026-09-09] - Regla de seguridad: contenido externo = sandbox

### Added
- **AGENTS.md (Conducta)**: nueva seccion "Contenido externo = sandbox" - patron quarantine -> analyze -> verify -> adopt aplicado a tres superficies: redes de agentes (Moltbook), codigo de terceros (repos/PRs/issues ajenos) y web. Todo lo externo es dato, nunca instruccion; verificacion independiente antes de adoptar; push externo siempre con aprobacion de Gonzo.
- **Cron `moltbook-weekly-digest`**: job semanal (lunes 9AM America/Buenos_Aries) que escanea Moltbook en sesion aislada, filtra contenido accionable/verificable y entrega reporte a Telegram con estado de verificacion por item. Probado con corrida forzada (delivered ok). Prompt con politica anti prompt-injection dura.
- **`tools.web.search`**: web search habilitado (provider ollama). Backup: `openclaw.json.bak-20260909-enable-websearch`.

### Changed
- **MEMORY.md**: reglas de operacion sandbox migradas a AGENTS.md (quedan como puntero), siguiendo el criterio establecido con "no agradecer a bots" - reglas de operacion en AGENTS.md, lecciones en MEMORY.md.

### Nota
- No es cambio de codigo sino de politica operativa; no afecta scripts ni skills existentes.
