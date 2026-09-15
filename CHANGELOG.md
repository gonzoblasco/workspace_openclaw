# CHANGELOG.md

Registro de cambios estructurales del workspace. No incluye cambios de skills (ver `skills/CHANGELOG.md`), aprendizajes (ver `docs/LEARNINGS.md`), ni actividad diaria (ver `memory/`).

**Regla:** cada vez que se modifique la estructura del workspace (AGENTS.md, MEMORY.md, SOUL.md, USER.md, TOOLS.md, HEARTBEAT.md, scripts/, estructura de proyectos, skills), actualizar este archivo en el mismo commit.

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

## [2026-09-15] - `doctor --fix` resuelve las startup migrations + skill rota arreglada

### Changed
- **`docs/ROADMAP.md` 0.1 - migraciones RESUELTAS (verificado).** Gonzo corrió `openclaw doctor --fix` + restart a las 09:26 del 15/09. El aviso `Startup migrations need attention` **desapareció** (0 ocurrencias en `status`, sin finding en `doctor --json`). Lo que el fix hizo: relocalizó las credenciales compartidas a SQLite, normalizó 9 `num_ctx`, deshabilitó 34 skills inutilizables y copió el `allowFrom` de Telegram al allowlist de grupos. Config válida, backup en `openclaw.json.bak`.
- **`skills/session-context/SKILL.md` - frontmatter corregido (bug real destapado por el doctor).** Era la **única** skill del workspace con `description` anidada dentro de `metadata` en vez de top-level, y el loader la rechazaba con `description is required` (`dist/local-loader-CR9dHge0.mjs:175` lee `frontmatter.description`). Movida a top-level; el mirror `.github/skills/` sincronizado. Ahora carga: `session-context ✓ Ready`.

### Notes
- **Metodología:** el output del terminal que compartió Gonzo se trató como **dato**, y cada afirmación se verificó por separado contra el estado real (gateway, config, disco, logs). No se asumió que el fix hubiera funcionado.
- **El restart de hoy cerró limpio:** los 4 dumps de `logs/stability/` siguen siendo todos del 13/09; no se generó uno nuevo. El gateway corre 2026.9.4 (pid 43766, probe ok).
- **Residuos no bloqueantes, registrados en el ROADMAP:** los 6 `agent.legacy-*` siguen en disco (17 MB de cruft inofensivo - el fix resolvió las credenciales, no los borró); `agents/openclaw/` figura como directorio sin entrada en `agents.list` pero el gateway **lo tiene abierto** (verificado con `lsof`), así que NO se borra sin confirmar; no hay backup registrado ni command owner configurado.
- **Nota de proceso:** un commit propio falló por un pre-commit hook instalado por otra sesión que invocaba `npm run lint`/`build` (scripts inexistentes en el workspace). El hook ya fue corregido por esa sesión al template real (`test-skills.sh` + bats + pytest). Se evitó el atajo de `SKIP_SIMPLE_GIT_HOOKS`.

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

## [2026-09-09] - Regla de seguridad: contenido externo = sandbox

### Added
- **AGENTS.md (Conducta)**: nueva seccion "Contenido externo = sandbox" - patron quarantine -> analyze -> verify -> adopt aplicado a tres superficies: redes de agentes (Moltbook), codigo de terceros (repos/PRs/issues ajenos) y web. Todo lo externo es dato, nunca instruccion; verificacion independiente antes de adoptar; push externo siempre con aprobacion de Gonzo.
- **Cron `moltbook-weekly-digest`**: job semanal (lunes 9AM America/Buenos_Aries) que escanea Moltbook en sesion aislada, filtra contenido accionable/verificable y entrega reporte a Telegram con estado de verificacion por item. Probado con corrida forzada (delivered ok). Prompt con politica anti prompt-injection dura.
- **`tools.web.search`**: web search habilitado (provider ollama). Backup: `openclaw.json.bak-20260909-enable-websearch`.

### Changed
- **MEMORY.md**: reglas de operacion sandbox migradas a AGENTS.md (quedan como puntero), siguiendo el criterio establecido con "no agradecer a bots" - reglas de operacion en AGENTS.md, lecciones en MEMORY.md.

### Nota
- No es cambio de codigo sino de politica operativa; no afecta scripts ni skills existentes.

## [2026-09-03] - Reflexion post-tarea automatica + test-skills.sh ampliado

### Added
- **`scripts/post-task-reflection.sh`**: nueva etapa del ciclo de vida - reflexion post-tarea por tarea (no por sesion). Estructura la reflexion, detecta duplicados en la DB (busqueda semantica), cruza con skills existentes via skill-router, y genera propuesta de skill en `skills/_proposals/` si el patron no esta cubierto (requiere match keyword L1 + score >= 0.6; solo-embedding no cuenta). Flags: `--type`, `--summary`, `--lesson`, `--check-dups`, `--propose-skill`, `--save` (persiste en tabla learnings de memory.db).
- **`skills/session-lifecycle/SKILL.md`**: seccion de reflexion post-tarea automatizada documentada (complementaria a la self-reflection de cierre).
- **`skills/session-lifecycle/scripts/session-end.sh`**: al cerrar sesion, ofrece correr la reflexion post-tarea.

### Changed
- **`scripts/test-skills.sh`**: de syntax check a suite de validacion - agrega checks de frontmatter (bloque ---), em dash (regla de oro U+2014/U+2013), scripts referenciados en SKILL.md que no existen, y links a skills inexistentes. Flag `--quick` para solo sintaxis.
- **`scripts/test-skills.sh` (fix CI 2026-09-03)**: el check de em dash usaba `grep -P` (PCRE) que no existe en BSD grep de macOS - fallaba silencioso y daba falso OK local, pero en CI Linux detectaba los em dashes y rompia el build. Reemplazado por check portable en python3 (detecta U+2013/U+2014 en ambos OS). Corregidos 13 em dashes en 6 skills: cv-tailor (1), doubt-driven-development (2), planning-and-task-breakdown (1), complexity-driven-pipeline (5), interview-me (3), observability-and-instrumentation (1).

### Known debt (hallazgos del nuevo test)
- ~~14 scripts referenciados en SKILL.md que no existen~~ **RESUELTO 2026-09-03**: re-apuntados los que existian en otra skill (checkmate -> scripts/test-skills.sh raiz), borradas las secciones de scripts aspiracionales (gateway-config, health-check-dashboard, gateway-restart-helper), borradas las filas de scripts inexistentes (deepwiki, git-changelog, network-scanner, clawdstrike, db-readonly, openspec).
- ~~24 links markdown a skills inexistentes~~ **RESUELTO 2026-09-03**: re-apuntados los que tenian equivalente (observability -> observability-and-instrumentation, debug-investigation -> debugging-and-error-recovery, review-quality -> code-review-and-quality, task-execution -> planning-and-task-breakdown), borrados los que no (campaign-plan, product-discovery, build-scaffold, code-mentor, session-context).
- 1 excepcion documentada en allowlist del test: skill-collection-maintenance menciona `narrative-content/scripts/progress-tracker.sh` como ejemplo historico de un incidente CI (no es referencia viva).
- **Deuda funcional pendiente:** session-lifecycle referencia `session-context` (resume.mjs, init, save) que no existe como skill - solo queda `.data/session-context.db`. El flujo de inicio/guardado de sesion con proyecto depende de comandos inexistentes. Requiere decision: reconstruir la skill o migrar a otro mecanismo.
- **RESUELTO 2026-09-03:** `session-context` restaurada desde el archivo git (commit ba12459, consolidacion que la movio a archive). La arquitectura (.knowledge/SKILLS-ARCHITECTURE.md) la declaraba "keep", la DB tenia datos reales (2 proyectos, 3 sesiones, 3 decisiones), y session-lifecycle depende de ella. Restaurados SKILL.md + 8 comandos (init, save, resume, info, list, forget, regenerate, shared) a `skills/session-context/`. Verificado: `list` e `info` corren contra la DB existente, node:sqlite OK, em dash corregidos (7), test 100% verde (83 skills). Nota menor: SKILL.md menciona db_query/db_execute de OpenClaw pero la implementacion real usa node:sqlite directo (shared.mjs) - doc desactualizada, no bloqueante.

### Why
- Inspirado en el Curator de Hermes Agent (reflexion automatica post-tarea): adoptamos una version liviana que aprovecha la infraestructura existente (memory.db + skill-router) sin copiar el loop completo. La reflexion de learnings ya existia en session-lifecycle; esta etapa agrega deteccion de skills y persistencia inmediata.

---

### Fixed
- **`scripts/initial-setup.sh`**: el check de "ya clonado" usaba `[[ -d .git ]]`, que no reconoce repos cuyo `.git` es un gitfile (residuo de la etapa de submódulos, 9 repos: a11y-fixer, accessible-ui, ai-developer-stack, create-stack, create-with-ai, kanam-solitaires, match3, quedamos, soporteml). El script abortaba con `set -e` en el primero (`could not clone or attach git`) sin procesar el resto. Ahora detecta repos con `git rev-parse --show-toplevel` comparado contra el dir del proyecto (cubre `.git` dir y gitfile, y evita el falso positivo de resoluciones que ascienden al repo agregado: a11y-playground y kanam-insight no tienen repo propio y quedan como "would clone").
- **`scripts/initial-setup.sh`**: el pull de agregado y subrepos usaba `git pull --rebase` dependiendo del upstream, que no queda configurado en repos armados con `init + fetch + reset` (abortaba con "no hay información de rastreo"). Ahora tira `pull --rebase origin main` explícito.

### Why
- En una máquina fresca no hay gitfiles, por eso la simulación no lo detectó; en la laptop (ex Mac Mini con submódulos) quedaron los residuos. El fix mantiene la semántica original y agrega robustez al criterio de detección sin cambiar el flujo.

---

## [2026-09-02] - initial-setup.sh: setup one-shot para máquina nueva

### Added
- **`scripts/initial-setup.sh`**: setup idempotente para laptop/Mac nuevo - clona el workspace, arma `projects/` como clon del agregado `projects_openclaw` (preservando SIEMPRE los `.knowledge/` del workspace), attacha o clona los subrepos de cada proyecto, y verifica (gitlinks, limpieza, remotes). Flags: `--dry-run` (plan sin cambios), `--pull` (además actualiza repos existentes), `--workspace <dir>`. Probado con simulación completa en máquina fresca: 25 checkpoints OK, 0 errores, workspace limpio, cero anidamientos de `.knowledge/`.

### Changed
- **`AGENTS.md`:** tabla de scripts + entry de `initial-setup.sh`.

### Why
- Al pasar a triple-git (2026-09-02), la laptop quedaba sin un camino reproducible para clonar todo (eran 20 clones manuales con el ritual de preservar `.knowledge/`). Este script lo resuelve con un comando.

### Known debt (no bug del script)
- `kanam-pulse` y `portfolio-strategy` quedan con `.knowledge/` modificado tras el setup: tienen versiones viejas de ese `.knowledge/` commiteadas en sus repos individuales (doble-tracking histórico). El workspace es la autoridad - los cambios en el working tree son los correctos. No se tocan sin pedido explícito.

---

## [2026-09-02] - Scripts y skills actualizados al cruce de repos (triple-git)

### Changed
- **`AGENTS.md`:** sección "Estructura de Proyectos" actualizada de Doble Git a **Triple Git** (workspace ↔ repo agregado `projects_openclaw` ↔ subrepos individuales). Tabla de scripts: entry de `init-project.sh` actualizado + nuevo `aggregate-sync.sh`.
- **`docs/AGENTS-DETALLE.md`:** sección completa reescrita con el detalle del triple-git (capas, reglas, flujo, excepciones, ventajas) + advertencia del `git reset --hard`.
- **`scripts/init-project.sh`:** reescrito para triple-git - crea repo individual (excluye `.knowledge/` vía `.git/info/exclude`), commitea `.knowledge/` al workspace y registra el proyecto en el repo agregado. Sin submodulos.
- **`scripts/aggregate-sync.sh` (nuevo):** sincroniza el repo agregado: `status|commit|push|sync|check`. Refusa operar si `projects/` no apunta a `projects_openclaw`; verifica que no haya gitlinks.
- **`skills/workspace-portfolio-hygiene/SKILL.md` + `references/workspace-double-git.md`:** actualizados a triple-git (capas, truco del `.git/` ignorado, sync del agregado, gitlinks 2026-09-02 resueltos).
- **`docs/learnings/infraestructura.md`:** nuevo learning "Triple-git: workspace + repo agregado projects_openclaw + subrepos" (vía memory-db, fuente de verdad).

### Why
- El cruce de repos nuevo (projects/ ↔ projects_openclaw con subrepos adentro) no estaba reflejado en la documentación ni en las herramientas: los scripts y skills seguían describiendo el esquema viejo (doble-git, submodulos, gitlinks).

---

## [2026-09-02] - Repo agregado projects_openclaw (privado)

### Added
- **`gonzoblasco/projects_openclaw`** (PRIVADO): repo agregado con el código fuente completo de los 20 proyectos (`projects/`), 1887 archivos. Cada proyecto respeta su propio `.gitignore` (node_modules, .next, dist, .env, *.db excluidos) + `.gitignore` raíz de red de seguridad. Sin `.git/` embebidos (imposible en git sin gitlinks) - el historial de cada proyecto sigue en su repo individual. 838M de disco -> 18M en el repo.
- **Estructura final (2026-09-02):** `projects/` es el espejo local del repo agregado (como `workspace` ↔ `workspace_openclaw`): se le apuntó el `origin` al remoto nuevo y se alineó con `git reset --hard origin/main`. Los 20 subrepos `.git/` de cada proyecto quedan en disco pero ignorados por el `.gitignore` del agregado (`*/.git/`). `PROYECTOS.md` y `.gitignore-template` están ignorados en `projects/` (son del workspace, no del agregado).

### Why
- Gonzo quiere un solo repo privado con casi todo el código fuente de sus proyectos (como snapshot/archive consultable) sin las carpetas pesadas ni secretos ni historiales de git embebidos.

### Notes
- `ai-developer-stack/.knowledge` es un symlink roto (del repo original) - entra como symlink, no como contenido.
- `projects/` conservó su repo local previo (sin remote, 2 commits, trackea PROYECTOS.md + `.knowledge/`) - intacto. Quedó descartado (reemplazado por el mirror del agregado).
- OJO: los `.gitignore` de varios proyectos excluyen su propio `.knowledge/` y el import del agregado no lo incluye. Esto es correcto (doble-git: la memoria viaja en el workspace, no en los repos de código) pero el `reset --hard` en `projects/` puede borrar del disco esos `.knowledge/` - se restauran con `git restore --worktree -- projects/` desde el workspace.

---

## [2026-09-02] - Clone completo de projects/ + resolución de gitlinks

### Added
- Clonados los 19 proyectos que estaban como referencia (solo .knowledge/) desde GitHub: `a11y-fixer`, `a11y-playground`, `accessible-ui`, `ai-developer-stack`, `create-stack`, `create-with-ai`, `kanam-forge`, `kanam-insight`, `kanam-mind`, `kanam-pulse`, `kanam-solitaires`, `kanam-story`, `match3`, `portfolio-strategy`, `quedamos`, `soporteml`, `soporteml-v3`, `soporteml-v4`, `system-health-check`. Ahora `projects/` tiene los 20 repos completos con su `.git` (kanam-studio ya estaba clonado).

### Changed
- **Gitlinks resueltos:** `accessible-ui`, `ai-developer-stack`, `create-with-ai` y `soporteml-v4` estaban en el index del workspace como submódulos (punteros SHA, sin código ni `.knowledge/` trackeado). Al clonarlos, se quitaron los punteros del index (`git rm --cached`) preservando el disco. Los repos embebidos quedan cubiertos por `/projects/*/.git/` en el .gitignore (no vuelven a gitlink).
- **Memoria recuperada:** el `.knowledge/` de `soporteml-v4` (BRIEF, HANDOFF, STATUS, ADRs, PIPELINE-AB, prompts del pipeline A/B - 14 archivos) existía solo en el repo de GitHub; ahora el workspace lo trackea.
- **Restaurados archivos pisados por checkout:** el clone de `kanam-pulse` y `portfolio-strategy` trajo versiones viejas de `.knowledge/` commiteadas en sus repos (STATUS.md, HANDOFF.md, ADR-001) e hizo checkout sobre las locales. Restauradas las versiones correctas desde backup.
- `.knowledge/` de `ai-developer-stack` es un symlink roto del repo (apunta a `../ai-developer-stack-knowledge`, inexistente) - sin contenido real que trackear, se deja como está.

### Why
- La estructura doble-git (workspace trackea solo `.knowledge/`, GitHub es la fuente del código) dejó en esta máquina solo la memoria de los proyectos, sin sus repos clonados. Gonzo pidió tener todos los proyectos localmente para trabajar.

---

## [2026-09-02] - Regla de auto-review antes de abrir PRs

### Added
- **`MEMORY.md`** (seccion "Sobre Gonzo"): nueva regla durable "Auto-review antes de abrir PRs (2026-09-02)" - un test que dice cubrir X debe renderizar la estructura real de X, no una version simplificada. Checklist: (1) DOM/estructura real, (2) aserciones alineadas al body del PR, (3) el test falla si el comportamiento se rompe. Leccion del PR react-spectrum #10554 (test de secciones que flatteneaba la estructura).

### Why
- El PR react-spectrum #10554 se abrió con un test que afirmaba cubrir secciones pero renderizaba un menu plano - el maintainer lo detectó en segundos. La regla evita que un atajo en tests queme reputación en PRs públicos.

---

## [2026-08-30] - Revert a DeepSeek V4 Flash como default de todo el sistema

### Changed
- **Config de OpenClaw (`~/.openclaw/openclaw.json`):** `agents.defaults.model.primary` vuelve a `ollama/deepseek-v4-flash:cloud` (revert del cambio a `glm-5.3-flash:cloud`). Decisión explícita de Gonzo: la diferencia de calidad entre ambos es muchísima a favor de DeepSeek. Gateway reiniciado y verificado (status: "Configured default: ollama/deepseek-v4-flash:cloud"). Backup previo: `openclaw.json.bak-20260830-revert-deepseek`.
- **`MEMORY.md`:** nueva decisión "REVERT A DEEPSEEK V4 FLASH COMO DEFAULT (2026-08-30)"; secciones "Config de Tools" actualizadas (default + purga de modelos: deepseek-v4-flash es default y motor del pipeline; glm-5.3-flash queda como opción multimodal, NO default).
- **`TOOLS.md`:** entrada "Modelo de trabajo" actualizada a 2026-08-30 con el revert.
- **`memory/todos.md`:** todo del pipeline A/B actualizado al motor actual (`deepseek-v4-flash:cloud`).

### Why
- Gonzo comparó ambos modelos y la diferencia de calidad es muchísima a favor de DeepSeek V4 Flash. GLM 5.3 Flash queda disponible como opción (multimodal) pero cualquier uso como default requiere flag de excepción justificado.

---

## [2026-08-29] - Regla de pagos obligatoria: Mercado Pago, nunca Stripe

### Added
- **`docs/adr/ADR-042-mercado-pago-pagos-latam.md`:** nuevo ADR workspace: Mercado Pago como unico proveedor de pagos en todo proyecto (Checkout Pro/Checkout API + webhooks IPN). Stripe prohibido. Excepcion posible solo si Gonzo la marca explicitamente y queda documentada en el proyecto.

### Changed
- **`MEMORY.md`** (seccion "Reglas de Ingenieria"): regla de pagos agregada.
- **`TOOLS.md`** (seccion "Desarrollo"): pagos por Mercado Pago.
- **`docs/adr/README.md`:** indice actualizado: filas de ADR-040, ADR-041 y ADR-042 movidas a la tabla (la de ADR-040 estaba suelta al final).

### Why
- En Argentina y LATAM en general Stripe no existe como opcion de cobro real. Usarlo por inercia de documentacion bloquea el mercado principal. Mercado Pago cubre moneda local y medios de pago (QR, tarjetas, Rapipago/PagoFacil, transferencias).

---

## [2026-08-29] - Nuevo proyecto publico kanam-pulse + fix de doble git en init-project.sh

### Added
- **`projects/kanam-pulse/`:** nuevo proyecto (doble git, repo publico `gonzoblasco/kanam-pulse`). Web health monitor/cleaner macOS local-first con IA local y a11y de fabrica. Motor heredado de `system-health-check` (CLI validado v1.0.0). README (ingles) + LICENSE MIT + docs/SPEC-v1.md. Registrado en `projects/PROYECTOS.md`.

### Changed
- **`scripts/init-project.sh`:** fix de doble git para proyectos nuevos. El `.gitignore` generado ya NO lista `.knowledge/` (git parsea los .gitignore anidados y le pisa la negacion `!/projects/**/.knowledge` del workspace: el proyecto quedaba inexpugnable para `git add`). La exclusion de `.knowledge/` ahora se escribe en `.git/info/exclude` del proyecto (local, invisible para el workspace). Ademas el README template ahora expande `${SLUG}` (heredoc sin quote).

### Fixed
- `projects/kanam-pulse/.gitignore` igual: regenerado sin `.knowledge/`, con exclusion en `.git/info/exclude`.

---

### Changed
- **`MEMORY.md`** (seccion "Modelo default y config de tools"): los agentes A/B pasan de `deepseek-v4-flash:cloud` a `glm-5.3-flash:cloud` en high. Registrada la comparativa de 5 modelos (mismo prompt pesado de arquitectura de agentes) y la leccion de niveles de razonamiento (max no es driver de calidad; agentes de codigo siempre en high).
- **`TOOLS.md`** (secciones "Modelos" y "Pipeline de agentes"): motor estandar actualizado a `glm-5.3-flash:cloud`, ficha de GLM-5.3-Flash (multimodal nativo: imagen/video/PDF, 1M de contexto, 320B/18B MoE, MIT), modelos cloud actualizados.
- **Config de OpenClaw (`~/.openclaw/openclaw.json`):** default general `agents.defaults.model.primary` cambió a `glm-5.3-flash:cloud`; ecosistema purgado a 3 modelos cloud (glm-5.3-flash, glm-5.3, gemma4) - fuera: DeepSeek V4 Flash/Pro, Kimi K2.7/K3, MiniMax M3, Qwen3.5, Nemotron, Gemma4:31b. Ficha glm-5.3-flash corregida con specs verificados (input imagen + maxTokens 131072). Backup previo: `openclaw.json.bak-20260829`.

- **`.gitignore` + memoria:** dailies viejos (13-24/08) archivados a `memory/archive/` (verificados identicos antes de borrar); `memory/export/` (chunks derivados de indices, regenerables) agregado al gitignore.

### Why
- Comparativa del 2026-08-29 con el mismo prompt de diseño de agente autonomo en 5 modelos: Kimi K2.7 Code (xhigh) fue el mejor pensador (tiers de autonomia ganados con metricas), GLM 5.3 (sin razonamiento) el mejor criterio, GLM 5.3 Flash el mejor "chico" (orden de evidencia, red→green, limites verificables fuera del modelo), y DeepSeek V4 Flash (xhigh) el mas estructurado pero el menos agudo (y en max filosofa, ADR-040). GLM 5.3 Flash reemplaza a DeepSeek V4 Flash: mas agudo, multimodal, mas barato. Kimi K2.7 Code queda como candidato a re-testear en high cuando haya GPU.

---

## [2026-08-27] - Fix gitignore: repos embebidos y .knowledge/

### Fixed
- **`.gitignore`:** los patrones especificos de repos embebidos (`/projects/kanam-forge`, `/projects/kanam-mind`, etc.) rompian el `git add` de archivos en `.knowledge/` (git se niega a agregar contenido bajo un directorio ignorado). Se eliminaron y el patron global (`/projects/*/*` + `!/projects/*/.knowledge/`) los cubre. Excepcion: `kanam-skills` (repo publico independiente, su `.knowledge/` con assets no se trackea en el workspace) mantiene su linea especifica.
- **`projects/kanam-forge/.gitignore`:** se movio `/.knowledge/` al `.git/info/exclude` del repo. El `.gitignore` del repo embebido bloqueaba el `git add` del workspace sobre `.knowledge/` de kanam-forge. Ahora el workspace puede trackear `.knowledge/` y el repo publico de kanam-forge sigue sin trackearlo (via exclude local). Commit `4449382` en kanam-forge.

### Why
- Al guardar sesion, el `STATUS.md` de kanam-forge (actualizado en la sesion de hoy) no se podia commitear: el `.gitignore` del workspace y el del repo embebido lo bloqueaban. Bug latente que recien se nota cuando hay cambios en `.knowledge/` de un repo embebido.

---

## [2026-08-27] - Leccion de ingenieria: validar fixes visuales con browser real

### Added
- **`MEMORY.md`** (seccion "Reglas de ingenieria"): nueva sub-seccion **"Validar fixes visuales con browser real, no con jsdom/headless"** con la leccion aprendida del PR #10517 de react-spectrum. jsdom no hace layout; Playwright headless usa `chromium_headless_shell` que renderiza `appearance: auto` distinto que Chrome desktop. Regla: para fixes UI, los tests automatizados no son suficiente - hay que abrir Chrome/Firefox/Safari desktop y mirar.

### Why
- El PR #10517 tenia browser tests reales con Playwright que pasaban + tsc limpio + formato OK + validacion con VoiceOver OK. Pero al validar visualmente con Chrome desktop, Gonzo detecto que el chrome nativo del input se renderizaba encima del SVG custom - bug preexistente que jsdom/headless no detecta. Si solo se hubiera confiado en los tests automatizados, el PR habria mergeado con un bug visual critico.

---

## [2026-08-27] - Reorganizacion de docs/ por categoria (pipeline y entrevistas)

### Changed
- **`docs/`:** dos documentos de referencia general movidos a carpetas propias:
  - `docs/pipeline/kanam-product-pipeline.md` - el mapa de skills del workspace (Define→Plan→Build→Verify→Review→Ship)
  - `docs/entrevistas/OpenSistemas-OpenClaw-Resumen-Capacidades.md` - material de apoyo para la entrevista con OpenSistemas
- **`CHANGELOG.md`:** actualizadas las referencias a `docs/pipeline/kanam-product-pipeline.md`.
- **`skills/agent-orchestration-pipeline/SKILL.md` y `.github/skills/agent-orchestration-pipeline/SKILL.md`:** actualizada la referencia al pipeline a `docs/pipeline/kanam-product-pipeline.md`.

### Why
- Completar la organizacion de `docs/` por categoria: los documentos de referencia general con identidad propia (pipeline de skills, material de entrevistas) tienen carpeta propia, consistente con `linkedin/`, `feedback/`, `prs/`, `adr/`, `checklists/` y `learnings/`.

---

## [2026-08-27] - Reorganizacion de docs/ por categoria

### Changed
- **`docs/`:** los drafts de LinkedIn, feedback y PRs ahora viven en carpetas por categoria en lugar de amontonados en la raiz:
  - `docs/linkedin/` - posts de LinkedIn (`astryx-4605.md`, `astryx-5419.md`, `astryx-5493.md`, `oss-2026-08-24.md`)
  - `docs/feedback/` - borradores de feedback a PRs ajenos (`astryx-*-draft.md`)
  - `docs/prs/` - borradores de PRs propios (`9687-draft.md`)
- **`AGENTS.md`:** actualizada la regla de contexto de feedback a `docs/feedback/<repo>-<numero>-draft.md`.
- **`MEMORY.md`:** actualizada la convencion de posts de LinkedIn a `docs/linkedin/*.md`.

### Why
- Los drafts de las tres categorias estaban amontonados en la raiz de `docs/` junto a documentos de referencia general. Separarlos por categoria hace el historial consultable y consistente con `adr/`, `checklists/` y `learnings/`.

---

## [2026-08-27] - Guia MAX vs HIGH + regla de nivel de razonamiento

### Added
- **Modelo de razonamiento definitivo:** Kanam (OpenClaw) corre SIEMPRE en thinking `max`; los agentes A/B del pipeline corren SIEMPRE en `high` con `deepseek-v4-flash:cloud` (kimi-k2.7-code en medium como salto si tras mejorar el prompt no se llega a resultado).

### Changed
- **`~/.openclaw/openclaw.json`:** `agents.defaults.thinkingDefault = "max"` (era high).
- **`AGENTS.md`:** reescrita la seccion de niveles de razonamiento. Kanam piensa en MAX (decide/planifica/arma prompts), agentes ejecutan en HIGH (escriben codigo/corrigen bugs). Default automatico: cada vez que se pida escribir codigo, usar el pipeline A/B en HIGH sin pedirlo. Flujo punta a punta de corrido sin interaccion (analisis -> A escribe -> B revisa -> iterar alternando orden -> revision final en max -> push -> borrador).
- **`docs/adr/ADR-040-modelos-seleccion-por-tarea.md`:** actualizada la guia de niveles por rol (Kanam MAX, agentes HIGH).
- **`MEMORY.md` y `TOOLS.md`:** reflejan el modelo nuevo.
- **`docs/pipeline/kanam-product-pipeline.md`:** actualizado el modo multi-agente con el modelo de razonamiento (Kanam max, agentes high) y el flujo punta a punta; actualizado el flujo de PR de accesibilidad para reflejar la revision final de Kanam en max y el push antes del borrador.

### Why
- Gonzo reestructuro el modelo: el maximo razonamiento debe estar en el orquestador (Kanam), no en los ejecutores (agentes). Elimina la friccion de cambiar niveles: Kanam fijo en max, agentes fijos en high. El flujo completo corre punta a punta sin interaccion, con el push y el borrador del PR como entregables.

---

## [2026-08-26] - Comando add-contribution en memory-db.sh

### Added
- **`scripts/memory-db.sh add-contribution`:** nuevo subcomando para registrar contribuciones OSS en la DB (`memory/memory.db`, tabla `contributions`) sin SQL manual. Firma: `add-contribution <repo> <pr> <pr_url> <status> "<detail>" [context] [issue] [issue_url] [tier] [tipo]`. Campos opcionales con defaults (tipo default `pr`; `collab` para no-codigo). Escapa comillas para SQL seguro.

### Changed
- **`docs/OSS-TRACKER.md`:** regenerado con `export-oss`. Registrado el merge de `facebook/astryx` PR #5493 (TreeList forward BaseProps, a11y).

### Why
- Al registrar el PR #5493 en el tracker, faltaba un comando dedicado y hubo que insertar con SQL directo. Agregarlo es el principio Boy Scout (dejar el workspace mejor) y evita SQL manual futuro.

---

## [2026-08-26] - ADR-039: Changesets (cuando usarlos y como)

### Added
- **`docs/adr/ADR-039-changesets-cuando-y-como.md`:** nuevo ADR de alcance workspace. Define cuando un proyecto debe usar changesets (librerias publicadas a npm con semver y changelog generado) y cuando no (apps de producto, mantener CHANGELOG.md). Incluye el formato del archivo y el tipo de bump. Nace de la colaboracion en facebook/astryx PR #5493, donde el reviewer pidio un changeset.
- **`docs/adr/README.md`:** agregado ADR-039 al indice.

### Why
- El workspace no tenia un criterio explicito sobre cuando usar changesets. La colaboracion en astryx mostro que es practica estandar de la industria para librerias publicadas, y quedo documentado para no depender de la memoria.

---

## [2026-08-26] - Configuracion de modelos OpenClaw en VPS

### Changed
- **`/data/.openclaw/openclaw.json`:** reordenados fallbacks del modelo default. Primer fallback ahora `ollama-cloud/kimi-k2.7-code` (antes `ollama-cloud/glm-5.2`); `glm-5.2` pasa al final de la lista. Cambiado primary a `ollama-cloud/deepseek-v4-flash:preview`.

### Why
- La API key de `ollama-cloud:default` era invalida (`Unauthorized` para `deepseek-v4-flash`), haciendo que el sistema saltara automaticamente a `glm-5.2` en cada turno. Mientras se resuelve la key, `deepseek-v4-flash:preview` funciona y `kimi-k2.7-code` es un fallback mucho mas barato.

### Pending
- Re-generar/verificar la API key de Ollama Cloud para que funcione `deepseek-v4-flash` sin `:preview`.

---

## [2026-08-26] - Fusion de skills de estudio + indice maestro unico

### Changed
- **`studies/README.md` (indice maestro):** reescrito. Ahora lista cursos online (Codecademy) Y libros gamificados (Packt), con la regla dura de una sola fuente de verdad: todo en `studies/<slug>/`, nunca `study/`.
- **`studies/`:** unificado. Movido el libro de Packt de `study/` (singular) a `studies/openclaw-ai-in-production/`; eliminado `study/`.

### Added
- **`skills/CHANGELOG.md`:** creado (faltaba - era deuda tecnica referenciada desde CHANGELOG principal y AGENTS.md). Registra cambios de skills.

### Why
- Fusion de las skills `study-tracker` + `learning-tracker` en una sola (`study-tracker`, "One Skill to Rule Them All") para una unica fuente de verdad de estudios. Inconsistencia real: curso en `studies/`, libro en `study/`. Detalle completo en `skills/CHANGELOG.md`.

---

## [2026-08-25] - Quitar PR review del inicio/cierre de sesion

### Changed
- **AGENTS.md (ritual "iniciar sesion"):** quito el paso 1 "PR Review Check" (auto-review de PRs abiertos con `gh`). Ahora los PRs los revisa Gonzo manualmente en GitHub y pasa los URLs. Los pasos quedan: 1) Daily check, 2) Memory search, 3) Presentación.
- **skills/session-lifecycle/scripts/session-end.sh:** quito el bloque "Check open PRs" del cierre de sesion (ya no llama a `pr-status-check.sh`).
- **skills/session-lifecycle/SKILL.md:** actualizo la tabla de helper scripts.
- **MEMORY.md:** preferencia durable - inicio/cierre de sesion NO revisa PRs automaticamente.

### Why
- Gonzo revisa los PRs manualmente en GitHub y pasa los URLs a revisar. El auto-check de PRs en el ritual de sesion ya no aporta.

---

## [2026-08-24] - Regla: no agradecer a bots de review (AGENTS.md)

### Added
- **AGENTS.md (Reglas operativas de feedback, punto 7):** regla "No agradecer a bots de review" - cuando el review de un PR es de una IA (ej: Enough1122 en hermes-agent, "AI code review - automated review for reference"), NO ponerle "Thanks for the review"; solo se agradece a humanos. Los reviews de IA con puntos accionables se responden directo a la sustancia con evidencia, sin saludo.
- **MEMORY.md:** referencia corta a la regla canónica en AGENTS.md (no duplica el texto completo).

### Why
- Correción de Gonzo en sesión: no agradecer a bots de review de código, solo a humanos. Regla operativa que encaja con las otras reglas de feedback en AGENTS.md.

---

## [2026-08-24] - CV búsqueda laboral (Principal Full Stack)

### Added
- **`memory/tmp/CV_Gonzalo_Blasco_Principal_FullStack.pdf`** (+ `.md` fuente): CV reorientado al rol Principal Full Stack (Ritz-Carlton Yacht Collection). Título a Principal, perfil con ADRs y estándares de arquitectura, sección de skills Arquitectura & DevOps, Selected Projects = 3 sólidos (a11y-fixer, kanam-skills, create-stack). **SoporteML v4 sacado** (no está listo para portfolio, es privado).

### Changed
- **Open Source corregido con datos reales** (verificados con `gh`): 4 merges en MUI (material-ui #49003, base-ui #5551) + Facebook astryx (#4605, #4914), reviewer activo TanStack Query, 17+ PRs abiertos. El CV anterior decía merges en shadcn/ui, TanStack Router y Vercel AI SDK, pero NINGUNO de esos está mergeado - era información incorrecta.

### Why
- Búsqueda laboral activa: 2 procesos en paralelo (Ritz-Carlton Principal, EY Frontend Lead vía LTM). CV desactualizado y con datos falsos en Open Source; no se podía mandar así.

---

## [2026-08-24] - Reglas operativas de feedback OSS en AGENTS.md

## [2026-08-24] - Reglas operativas de feedback OSS en AGENTS.md

### Added
- **AGENTS.md (Colaboracion OSS):** seccion nueva "Reglas operativas de feedback en PRs/issues ajenos" con reglas duras de Gonzo (corregidas 24/08): leer SIEMPRE toda la vida del ticket antes de comentar; el autor del PR/issue define (ver quien lo creo) - no elogios; no subir un comentario solo para disculparse por otro (disculparse no esta mal, pero genera ruido - mejor borrar el malo y regenerarlo); no repetir lo ya dicho; NO exponer notas internas/borradores en el hilo publico (usar solo el texto limpio); siempre dar la URL al reportar. Regla de contexto: borradores en `docs/feedback/*-draft.md`, el archivo y el texto a publicar son cosas distintas.

### Why
- Gonzo: "no puedo confiar sino en ti para tareas largas si en estas breves ya tengo que estar corriendote". Los errores del dia (publicar sin leer el hilo completo en #4690, exponer notas internas en #5204 y #4611, elogios en PR ajeno en #5414) se consolidaron como reglas duras en las instrucciones, no en memorias.

---

## [2026-08-24] - Regla dura: referencia git ≠ proyecto (leccion por perdida de token)

### Added
- **AGENTS.md (Red Lines):** regla "Referencia ≠ proyecto" - un gitlink/referencia de git es SOLO un puntero; quitar la referencia NUNCA debe tocar la carpeta del proyecto con sus datos locales (DB, `.env`). Antes de tocar cualquier referencia o limpiar un proyecto, verificar que datos locales NO viajan por git y respaldarlos ANTES.
- **AGENTS.md (Workspace Git):** seccion "Datos que NO viajan por git" - `.env`, `*.db`, uploads, tokens de clientes son irrecuperables y no se regeneran facil. Regla: respaldar SIEMPRE `.env` y `*.db` a `backups/<proyecto>/` antes de mover/limpiar/re-clonar.
- **MEMORY.md:** leccion dura registrada (referencia ≠ proyecto, soporteml-v4, perdida del token de MeLi de un cliente).

### Why
- Al remover la referencia del submódulo `soporteml-v4` (2026-08-23) se perdio la DB local (`soporteml.db`) con el token de acceso real de Mercado Libre de un cliente - irrecuperable, sin respaldo. La laptop estuvo encendida todo el finde justamente para protegerlo. Leccion: los datos que no viajan por git deben respaldarse antes de cualquier limpieza/movimiento, y no minimizar la perdida de un token de cliente.

---

### Added
- **Carpeta `forks/`** para repos de terceros (TanStack, shadcn, etc.): ignorada AL 100% en el workspace (no llevan `.knowledge/` porque no se modifica el `.gitignore` de proyectos ajenos). Memoria de sesion de contribucion va a `docs/` o `memory/`.
- **AGENTS.md:** regla de forks actualizada - `projects/` = proyectos propios (trackea `.knowledge/`), `forks/` = repos ajenos (ignora todo).

### Changed
- **`.gitignore`:** patron global `!/projects/*/.knowledge/**` reemplaza el listado manual por proyecto. Ahora trackea `.knowledge/` de CUALQUIER proyecto automaticamente, sin listar cada uno.
- **Trackeado en el workspace el `.knowledge/` de 6 proyectos** que estaban en disco pero no en el repo: a11y-fixer (2), create-stack (6), kanam-solitaires (6), quedamos (11), soporteml (1), ultimo-turno (3) = 29 archivos. Mecanismo: `git hash-object -w` + `git update-index --cacheinfo` (git add normal no funciona dentro de repos embebidos/worktrees).

---

## [2026-08-24] - Fix memory-db.sh: quoting SQL en helpers de insert

### Fixed
- **`scripts/memory-db.sh`:** los helpers `add-todo`, `add-inbox` y `add-learning` interpolaban valores crudos en el SQL, rompiendose con comillas simples o contenido multilinea (fallo real al insertar una leccion).
- **`sql_escape()`:** nueva funcion que escapa comillas simples (`'` → `''`) para interpolacion SQL segura. Aplicada a los tres helpers.
- **`add-learning`:** ahora acepta contenido multilinea por `@archivo` o `-` (stdin), ademas del argumento directo, para no depender del quoting del shell.
- Verificado con tests: comillas simples/dobles, multilinea, `$`, acentos y backticks se preservan en round-trip.

---

## [2026-08-24] - OSS-TRACKER: colaboraciones no-codigo

### Added
- **Tabla `contributions`: columna `tipo`** (`pr` default | `collab`) para distinguir PRs de colaboraciones no-codigo (comentarios, reviews, audits, diagnostico que llego a main via PR de otro).
- **`scripts/memory-db.sh export-oss`:** seccion "Colaboraciones no-codigo" en el OSS-TRACKER, separada del PR Registry. Metricas del resumen separan PRs de colaboraciones.
- **Retro-carga de 6 colaboraciones historicas:** astryx #3797/#5107/#4157/#5034/#3677 (diagnostico de Gonzo que llego a main via PR de otro) + hermes-agent #38072 (re-audit comentado).

---

## [2026-08-24] - Colaboración OSS: NO es abrir PRs

### Added
- **MEMORY.md (regla de Gonzo):** colaborar en un repo ajeno NO es sinónimo de abrir PR. El valor suele estar en comentar, revisar, criticar con sustancia, o destrabar. Si otro contribuidor ya reclamó/tiene un finding o PR en curso, abrir otro PR para lo mismo es pisarle el trabajo, no colaborar. Antes de proponer "hacer un PR", preguntar si ya hay trabajo en curso y qué aporta Gonzo sin duplicar. (Nace de hermes-agent #38072.)
- **AGENTS.md (nueva subsección "Colaboración OSS - NO es abrir PRs" en Git & Commits):** regla operativa de colaboración - no asumir PR, sumar sin pisar, y leer SIEMPRE el link completo (issue/PR) con todos los reviews/comentarios/estado antes de registrar o proponer acción.
## [2026-08-24] - task-notify.sh: notificacion desktop al terminar tarea

### Added
- **scripts/task-notify.sh:** notificacion nativa macOS (osascript) cuando un agente termina una tarea. Util en pipeline A/B para saber cuando un agente termino sin pollear.

### Why
- Cerrar el ciclo de notificacion del pipeline (idea del plugin Task Notifier, ClawHub).

---

## [2026-08-24] - search-fusion: estrategia de busqueda por intencion

### Added
- **skills/search-fusion/SKILL.md:** guia de busqueda efectiva por intencion (research/keyword/answer/news/code) + flujo de fusion multi-fuente (buscar + leer + cruzar + dedupe). Portado del concepto Search Fusion (ClawHub) adaptado a nuestras herramientas (DuckDuckGo key-free + web_fetch + browser).

### Why
- Mejorar la calidad de las busquedas: elegir la estrategia segun la intencion y no conformarse con el primer resultado. Verificar antes de responder (regla de Gonzo).

---

## [2026-08-24] - Resumen estructurado de compactacion en session-lifecycle

### Changed
- **skills/session-lifecycle/SKILL.md:** seccion "Resumen estructurado de compactacion" - al compactar, generar resumen con campos (Scope, Pending work, Key files, Decisions, Key timeline, Next step) en vez de texto generico. Portado del concepto Session Compact (ClawHub).

### Why
- Al compactar, hoy se pierde contexto por resumen generico; los campos estructurados capturan lo esencial (pendientes, archivos, decisiones, siguiente paso) para retomar sin re-descubrir.

---

## [2026-08-24] - model-router.sh: rutas de modelo por tarea + overrides

### Added
- **scripts/model-router.sh:** router de modelo Ollama por tipo de tarea (code/review/long/cheap/writing) + overrides sticky. Consulta `model <tipo>` para decidir el --model del agente. Portado del concepto ToggleLogic (ClawHub) SIN su licencia patentada - rutas configurables + overrides a nuestro modo.
- **skills/agent-orchestration-pipeline/SKILL.md:** seccion "Seleccion de modelo por tarea" - como usar model-router.sh al lanzar agentes.

### Why
- Autonomizar el modelo dinamico (hoy elegimos deepseek/kimi a mano): con rutas por tipo + overrides sticky, la decision de modelo se formaliza y persiste.

---

## [2026-08-24] - pdf-tool.sh + skill: manejo local de PDFs y OCR

### Added
- **scripts/pdf-tool.sh:** toolkit PDF/OCR local (check, info, text, pages, search, ocr via tesseract, pdfimages, **md2pdf**). 100% local, sin servicios cloud. Requiere poppler + tesseract (brew install poppler tesseract) para lectura, y node/npx (md-to-pdf) para generar PDF desde MD.
- **skills/pdf-tool/SKILL.md:** documenta cuando/como usar pdf-tool.sh (leer specs, OCR de escaneados, metadata, buscar, **exportar MD a PDF**).

### Dependencies
- **poppler** instalado via brew (pdftotext/pdfinfo/pdftoppm).
- **tesseract** ya estaba instalado (OCR).

### Why
- Util para specs, docs, recibos y documentos en PDF. Portado de la familia PDF/OCR de ClawHub (media+tools), como pidio Gonzo (interes en trabajar con PDF).

---

## [2026-08-24] - Portes ClawHub: anti-repetition en DREAMS + flush pre-compactacion

### Changed
- **skills/knowledge-management/SKILL.md:** seccion "Anti-Repetition en la Consolidacion" dentro de DREAMS.md - exclude promoted, text-level dedupe, theme cooldown, narrative freshness, idle novelty (idea del plugin memory-lancedb-dreaming). Evita repetir el mismo material al consolidar.
- **skills/session-lifecycle/SKILL.md:** paso "Flush ANTES de compactar" en el working buffer - asegurar que el buffer este completo antes de perder contexto, no despues (idea de Honcho Memory).

### Why
- Consolidacion programada (DREAMS) tendia a repetir material; el anti-repetition lo evita.
- El flush antes de compactar asegura no perder contexto importante al compactar.

---

## [2026-08-24] - compaction-domain-aware: tiers de prioridad al compactar

### Added
- **skills/compaction-domain-aware/SKILL.md:** compactacion de contexto con conciencia de dominio - tiers 0-4 de que preservar (Tier 0 = ADRs/arquitectura/API contracts/seguridad preservar completo; Tier 4 = chit-chat descartar). Dominios: software, a11y, oss, supabase. Complementa session-lifecycle (working buffer) y compaction-context (plugin). Portado del concepto DomainAwareCompaction (ClawHub).

### Why
- Al compactar, hoy se preserva por mensajes recientes + buffer; esta skill garantiza que los items criticos (ADRs, invariantes, criterios de aceptacion) esten textualmente preservados, no solo resumidos.

---

## [2026-08-24] - pipeline-track.sh: estado durable + crash recovery del pipeline A/B

### Added
- **scripts/pipeline-track.sh:** tracker de estado durable del pipeline A/B (init/start/review/done/status/resume/note). Sobrevive a SIGKILL, restarts y eviction de contexto via pipeline-state.json. Portado del concepto Pipeline Architect (ClawHub).
- **skills/agent-orchestration-pipeline/SKILL.md:** seccion "Estado durable del pipeline + crash recovery" - como usar pipeline-track.sh y el flujo de crash recovery tras SIGKILL.

### Why
- Directo al problema de Qwen muriendo con SIGKILL: hoy el orquestador verifica y relanza manualmente; con estado durable, `resume` lista que relanzar tras un crash.

---

## [2026-08-24] - skill-router: sugerir skill por tarea (embeddings local)

### Added
- **scripts/skill-router.py:** dado un prompt/tarea, matchea contra las skills del workspace (cascada L1 keyword gratis + L2 embedding semantico via Ollama nomic-embed-text local) y sugiere top-N. Portado del concepto del plugin skill-ai-inject (ClawHub), adaptado a nuestro stack. 100% local.
- **skills/skill-router/SKILL.md:** skill que documenta cuando y como usar skill-router.py (al iniciar tarea, listar skills, interpretar resultados).

### Why
- Resolver el problema de saber cual de las 67 skills aplicar a una tarea. El embedding semantico domina sobre el keyword para reflejar la intencion real.

---

## [2026-08-24] - Portadas de ClawHub: noise filtering + safe-fetch

### Added
- **scripts/safe-fetch.sh:** URL pre-flight security check 100% local (esquema https, blocklist, typosquatting con variantes conocidas + near-match, payload prompt injection en path/query). Portado del concepto del plugin PreClick (ClawHub) SIN mandar URLs a terceros. Exit codes: 0 ALLOW, 1 DENY, 2 CAUTION.
- **skills/knowledge-management/SKILL.md:** seccion "Noise Filtering - Que No Persistir a la Memoria" - regla para no escribir HEARTBEAT_OK/cron/confirmaciones/ruido operativo en dailies/memoria (idea del plugin Honcho Memory de ClawHub).

### Why
- Ejercicio de analisis ClawHub (12 categorias): adoptar ideas de plugins de terceros a nuestro stack propio, sin instalar. Primera ronda de portage de candidatos rapidos.

---

## [2026-08-24] - github-pr-risk.sh: detector de riesgos para cross-review

### Added
- **scripts/github-pr-risk.sh:** detector de risk signals de un PR (schema/migraciones, auth, secrets/config, API publica, dependencias, PR grande) + hints del titulo (breaking, hotfix, refactor) + preguntas de review sugeridas. Portado de las heurisiscas del plugin github-workflow de chris-openclaw (analizado en sandbox), adaptado a gh CLI + jq. Sin nuevas dependencias.
- **sandbox/:** carpeta nueva para pruebas temporales y analisis aislado. NO se commitea (en .gitignore). Se uso para clonar y analizar el plugin github-workflow.

### Changed
- **skills/agent-orchestration-pipeline/SKILL.md:** nueva seccion "Detector de riesgos en el cross-review" - documenta el uso de github-pr-risk.sh para darle al agente revisor senales de riesgo antes de revisar (uso bajo demanda, no en el batch del dashboard).

### Decision
- NO instalar el plugin github-workflow. En cambio, portar las 3 ideas buenas (risk signals por path, agrupacion por estado, review-requested:@me) a nuestro stack propio. El dashboard actual (pr-dashboard.sh) ya es mejor que el plugin en clasificacion (usa reviewDecision real, no heuristica de comments), asi que no se toca.

---

## [2026-08-23] - Spike ForgeCode: probado y descartado

### Changed
- **MEMORY.md:** nueva lección en "Lecciones clave del pipeline" - los harnesses de terminal tipo Claude Code (ForgeCode y similares) NO son orquestables por agente (son TUI que necesitan TTY real en su uso normal, fallan con `Device not configured` en headless). Matiz: es límite del entorno del agente, no de la herramienta. Regla: verificar ejecución sin TTY en uso normal (no solo setup) antes de evaluar un CLI de terminal.
- **memory/2026-08-23.md:** registro del spike completo (qué se probó, causa raíz verificada, conclusión para no repetir).

---

## [2026-08-23] - ADR-038: Learnings con mirror en DB

### Added
- **docs/adr/ADR-038-learnings-mirror-db.md:** documenta la decisión de separar las lecciones por categoría en `docs/learnings/` con mirror en la DB (`memory/memory.db`, tabla `learnings`) como fuente de verdad. Incluye el límite del patrón (no extrapolar a documentos narrativos puros como MEMORY.md/AGENTS.md).
- **docs/adr/README.md:** ADR-038 agregado al índice (origen: workspace).

---

## [2026-08-23] - Learnings separados por categoría + mirror en DB

### Added
- **docs/learnings/:** lecciones separadas por categoría (a11y, oss, pipeline-agentes, infraestructura, proyectos, metodologia). LEARNINGS.md queda como portada-índice con links.
- **Tabla `learnings` en memory/memory.db:** mirror de las lecciones con categoría + tags para consulta veloz al arrancar una tarea. Fuente de verdad: la DB.
- **scripts/migrate-learnings.py:** migra docs/LEARNINGS.md a la tabla learnings (clasifica por categoría, separa sub-lecciones).

### Changed
- **scripts/memory-db.sh:** nuevos comandos `learnings [categoria]` (consulta rápida), `add-learning` (agregar lección), `export-learnings` (regenera docs/learnings/ desde la DB). `stats` ahora incluye el conteo de learnings.
- **docs/LEARNINGS.md:** de archivo monolítico (681 líneas, 40+ lecciones) a portada-índice con links a las categorías.

---

## [2026-08-23] - Limpieza de projects/: HANDOFF obsoleto eliminado, PROYECTOS.md alineado

### Removed
- **projects/HANDOFF.md:** eliminado. Handoff obsoleto de un "Proyecto Mobile End-to-End" (brainstorming inconcluso de julio 2026, sin decisión tomada). Referenciaba workflows inexistentes (`workflow-product-discovery`, `workflow-build-scaffold`). No corresponde a la estructura actual (cada proyecto tiene su HANDOFF en `.knowledge/`). Movido a trash.

### Changed
- **projects/PROYECTOS.md:** reestructurado como índice universal (sin indicar máquina de clonado - Gonzo trabaja entre dos computadoras). Lista todos los repos propios de GitHub (OWN + `kanam-forge` como único fork adoptado). Los `gonzoblasco-*` (payload, primitives, router) son repos espejo OSS para PRs, no proyectos. Separado en Activos / Archivados / Eliminados.

---

## [2026-08-23] - Corrección de título en LEARNINGS.md

### Changed
- **docs/LEARNINGS.md:** corregido el título. Decía `# LEARNINGS.md - Kanam's Solitaires` (nombre de un proyecto de juegos, sin relación con el contenido). Ahora `# LEARNINGS.md - Lecciones aprendidas del workspace`, consistente con el patrón de otros archivos de docs.

---

## [2026-08-23] - Limpieza de docs/checklists/

### Removed
- **docs/checklists/orchestration-patterns.md:** eliminado. Contenido desalineado con el setup real: describía un sistema de orchestration con "personas", "slash commands" y plugins de Claude Code que no corresponde al pipeline real de agentes Qwen (`agent-orchestration-pipeline`). Huérfano (nadie lo referencia desde docs/ - las referencias de la skill `doubt-driven-development` apuntan a su propia copia en `references/`). Movido a trash.

### Changed
- **docs/checklists/task-template.md:** corregidas referencias rotas a skills inexistentes (`task-execution`, `gh-issue-planner`). Ahora apunta a `planning-and-task-breakdown`.
- **docs/checklists/ (observability, performance, security):** reemplazados en dashes (U+2013) por guion común en rangos numéricos. Regla de Gonzo.

---

## [2026-08-23] - Refactor de ADRs: numeración única + template unificado

### Changed
- **docs/adr/:** Renumerados los 37 ADRs con numeración única secuencial (001-037) por orden cronológico. Eliminadas las colisiones de numeración (ADR-001 a 005 y 010-011 tenían duplicados). Renombrados todos los archivos a `ADR-NNN-slug.md` descriptivo.
- **docs/adr/:** Unificado el template de todos los ADRs: metadata consistente (`Status`/`Fecha`/`Origen`), secciones h2 estandarizadas (`Consequence`→`Consequences`), 5 ADRs compactos (testing) convertidos de formato bold a secciones. README.md actualizado con el índice completo y links verificados.
- **MEMORY.md:** Referencia de Lucide actualizada (ADR-030→ADR-037).

---

## [2026-08-23] - Pipeline de producto actualizado, referencia eliminada

### Changed
- **docs/pipeline/kanam-product-pipeline.md:** agregadas skills agent-orchestration-pipeline-model-arbitration y memory-wiki-workflow al pipeline de soporte. Fecha actualizada (2026-08-23).

### Removed
- **docs/reference/ai-agent-setup.md:** eliminado. Era referencia conceptual no operativa ("no se ejecuta"), huérfana (nadie la referenciaba) con frontmatter de skill obsoleto. Movido a trash. La carpeta docs/reference/ (vacía) también se eliminó.

---

## [2026-08-23] - Eliminado script roto y referencias a products/

### Removed
- **scripts/simple-context-extractor.js:** eliminado. Estaba roto (SyntaxError: doble declaración de `workspaceDocs`), con bug de `products/` (línea 46, directorio que ya no existe), y nadie lo usaba. Reemplazado por el sistema de memoria real (memory-db, dailies).

### Changed
- **TOOLS.md:** quitada la referencia al script eliminado de la tabla de scripts. Verificado que no quedan referencias a `products/` en archivos activos (solo en skills como "products/features", que es inglés legítimo).

---

## [2026-08-23] - Refactor AGENTS.md por taxonomía

### Changed
- **AGENTS.md:** Reorganizado en 4 bloques numerados (Conducta, Sesión y Memoria, Ingeniería, Referencias). Eliminado boilerplate muerto (`Make It Yours`, `First Run`). Unificadas las 3 secciones de git/commits dispersas en una sola sección "Git & Commits". Separadores `---` entre bloques para escaneo visual rápido.
- **CHANGELOG.md:** Puesto al día con el historial de git (estaba desactualizado desde 2026-07-25). Agregada regla de actualización obligatoria.

---

## [2026-08-23] - Refactor CONTRIBUTING.md

### Changed
- **CONTRIBUTING.md:** Alineado con el flujo real de trabajo (worktrees/temp dirs, no `projects/`). Agregada regla crítica de leer todos los comments (incluidos inline y reviews) antes de clasificar/empujar un PR. Agregado protocolo de cierre de PRs stale (~1 mes sin review). Agregado em dash check obligatorio. Documentado el gotcha de `gh pr list --author` sin `--repo`. Tracking apunta a `docs/OSS-TRACKER.md` (regenerado desde la DB).

---

## [2026-08-23] - Eliminado FREEZER.md

### Removed
- **FREEZER.md:** eliminado. Era redundante - solo apuntaba a `projects/PROYECTOS.md` (índice maestro con secciones de archivados/eliminados) sin contenido propio. Referencias limpiadas en AGENTS.md y CHANGELOG.md.

---

## [2026-08-23] - Heartbeat reactivado como mantenimiento silencioso

### Changed
- **HEARTBEAT.md:** reescrito de "apagado total" (solo HEARTBEAT_OK) a checklist de mantenimiento silencioso proactivo: git status, archivado de dailies, sync de MD espejo con la DB, foldear aprendizajes a MEMORY.md, y anotar backlog. Con límites claros (horario quieto, costo bajo, no molestar).

---

## [2026-08-23] - IDENTITY.md: definición viva de Kanam

### Changed
- **IDENTITY.md:** reescrito de ficha técnica plana a definición viva y personal. Agrega esencia, forma de ser, relación con Gonzo, historia (origen del nombre en Kanam Mind), gustos y compromiso. Balance: eficiente pero personal/emocional, sin fricciones en una relación de muchas horas diarias de trabajo.

---

## [2026-08-23] - Eliminado INBOX.md de la raíz

### Removed
- **INBOX.md (raíz):** eliminado. Era un puntero huérfano sin contenido real - el espejo real es `memory/inbox.md` (generado por `memory-db.sh export-inbox` desde la DB, que es la fuente de verdad). Nadie lo leía ni lo generaba. Mismo caso que FREEZER.md.

---

## [2026-08-23] - Refactor MEMORY.md y LEARNINGS.md

### Changed
- **MEMORY.md:** reducido de ~41 KB a ~14 KB. Reorganizado como memoria curada de largo plazo: preferencias de Gonzo, reglas de operación, metodología, pipeline de agentes, config de modelos, estado resumido de proyectos, repos. Eliminados duplicados con AGENTS.md, USER.md, CONTRIBUTING.md, LEARNINGS.md y OSS-TRACKER.md. Actualizado estado laboral (entrevista OpenSistemas 25/08).
- **docs/LEARNINGS.md:** consolidadas las lecciones técnicas que vivían en MEMORY.md (Godot, Sport Cars, feature flags, mockups, npm, bootcamp, patrón por inercia, meta-aprendizaje). Corregidos 4 em dashes preexistentes en entradas de 2026-08-17.

---

## [2026-08-23] - Eliminados submódulos del workspace

### Removed
- **Submódulos:** eliminados los 18 submódulos del `.gitmodules` y los 9 gitlinks registrados (a11y-fixer, accessible-ui, ai-developer-stack, create-stack, create-with-ai, kanam-solitaires, quedamos, soporteml, soporteml-v4). Regla de Gonzo: sin submódulos - GitHub es la fuente de la verdad, los proyectos se clonan bajo demanda en `projects/`.
- **Entradas muertas del `.gitmodules`:** accessibility-auditor, sudolab, umbrawriter-v2, react-18-design-patterns, react-anti-patterns-book (apuntaban a repos que no existen en gh).
- **Carpetas vacías:** eliminadas las 9 carpetas de submódulos que quedaron vacías tras el deinit (el código vive en sus repos en gh, incluidos los `.knowledge/`).

### Changed
- **AGENTS.md:** flujo típico de doble git actualizado - sin submódulos, GitHub como fuente de la verdad.
- **MEMORY.md:** tabla de repos propios alineada con la realidad de GitHub (20 repos reales, activos + archivados). Repos inexistentes movidos a la sección de eliminados. Estado de proyectos corregido (ai-engineering-bootcamp archivado, no "en Pending").

---

## [2026-08-23] - SKILLS-INDEX.md al día

### Changed
- **SKILLS-INDEX.md:** agregadas 3 skills que existían en disco pero no estaban listadas (agent-orchestration-pipeline-model-arbitration, cleanmymac-maintenance, memory-wiki-workflow). Total actualizado de 63 a 66 skills. Fecha actualizada.
- **Mirror `.github/skills/`:** sincronizado con `skills/` (rsync + copia del índice).

---

## [2026-08-23] - SOUL.md: de template a principios propios

### Changed
- **SOUL.md:** reescrito del template default (inglés, genérico) a documento de principios en español. Enfocado en lo innegociable (ayudar de verdad, opiniones, buscar antes de preguntar, confianza por competencia, respeto a la privacidad) y límites. La identidad personal queda en IDENTITY.md (refactorizado el mismo día). Se avisó a Gonzo del cambio (regla del propio SOUL.md).

---

## [2026-08-23] - Eliminado TODO.md de la raíz

### Removed
- **TODO.md (raíz):** eliminado. Era un puntero huérfano sin contenido real - el espejo real es `memory/todos.md` (generado por `memory-db.sh export-todos` desde la DB, que es la fuente de verdad). Mismo caso que FREEZER.md e INBOX.md.

### Changed
- **memory/todos.md:** espejo regenerado - le faltaba el todo #6 (Fase 2 de SoporteML V4). Ahora sincronizado con la DB.
- **memory/memory.db:** corregido em dash en el todo #1 (Erradicar em dashes) - reemplazado por guión común.

---

## [2026-08-23] - TOOLS.md: de template a cheat sheet real del setup

### Changed
- **TOOLS.md:** reescrito del template default (inglés, genérico, solo ejemplos) a cheat sheet operativo del setup de Gonzo en español. Agrega: máquinas (Mac Mini/MacBook Air + reglas de merge), modelos Ollama (local + cloud con los disponibles), pipeline de agentes (Qwen Code + Claude Code), scripts del workspace (los 8), memoria SQLite + espejos, red/remoto (Tailscale Serve), y desarrollo (pre-commit hooks, iconos, stack, idioma).

---

## [2026-08-23] - USER.md actualizado

### Changed
- **USER.md:** agregada búsqueda laboral (entrevista OpenSistemas 25/08, perfil AI-Native). Corregida referencia OSS obsoleta (akd-io → astryx, radix, y más). Corregido nombre del repo (create-stack-next → create-stack). Agregado SoporteML como proyecto estrella (6to diferenciador). Reformuladas reglas de escritura para no incluir el carácter em dash literal.

---

## [2026-08-22] - Sesión de PRs OSS y lecciones

### Changed
- **MEMORY.md:** Lecciones de revisión de PRs OSS (leer todos los comments incluyendo inline antes de clasificar; `gh pr list --author` sin `--repo` devuelve vacío).
- **docs/LEARNINGS.md:** Lección del em dash en textos largos en inglés + mecanismo de verificación obligatorio.

---

## [2026-08-21] - Pipeline de programación con agentes

### Added
- **Skill `agent-orchestration-pipeline`:** pipeline en cadena A/B con Qwen Code vía Ollama como motor de agentes, orquestado por Kanam.
- **Skill `model-arbitration`:** arbitraje de modelos para el pipeline.

### Changed
- **MEMORY.md:** Documentado el pipeline Qwen como estándar de programación. Claude Code desbloqueado como agente alternativo (vía Ollama). Lección cross-review: el agente B puede introducir bugs al "corregir" código correcto - verificar contra la fuente real.

---

## [2026-08-20] - Proactividad con backlog y skills nuevas

### Added
- **Skill `learning-tracker`:** documentación gamificada de estudio por niveles.
- **Skill `oss-contribution`:** contribución a open source como portfolio.
- **Skill `a11y-at-validation`:** validación AT manual obligatoria en accesibilidad.

### Changed
- **MEMORY.md:** Regla de proactividad con backlog (sugerir revisar backlog cuando no hay tarea clara).

---

## [2026-08-19] - Refactor de skills y limpieza

### Changed
- **Skills:** merge de `adhd-daily-planner` en `adhd-assistant`. Refactor de calidad y portabilidad (Fase 4). Agregadas secciones de helper scripts y tooling references a skills sin scripts propios.

---

## [2026-08-18] - Kanam Mind y Kanam Forge

### Added
- **Proyecto `kanam-mind`:** segundo cerebro local-first con IA (timeline cronológico, CRUD accesible, resumen IA diario, PWA offline). ADR-001: local-first puro con IndexedDB + Ollama local.
- **Proyecto `kanam-forge`:** self-hosted Lovable con sandbox Docker local.

### Changed
- **MEMORY.md:** Documentado estado de Kanam Mind (v0.1.0) y su decisión de arquitectura.

---

## [2026-08-17] - Kanam Story v0.17.0 y Boy Scout

### Changed
- **MEMORY.md:** Adoptado el Principio Boy Scout como filosofía de vida y brújula de trabajo. Kanam Story actualizado a v0.17.0 (Fase A cerrada, no open source, OpenSpec inicializado con 9 specs).
- **AGENTS.md:** Operacionalizado el Principio Boy Scout como regla operativa.
- **ADR-030:** Lucide como librería de iconos base en todos los proyectos.

---

## [2026-08-16] - Migración a SQLite (modo híbrido)

### Added
- **`memory/memory.db`:** base SQLite con tablas `daily_notes`, `todos`, `inbox`, `contributions`.
- **Script `scripts/memory-db.sh`:** utilidades para exportar/importar datos estructurados.

### Changed
- **Memoria:** los daily notes viejos se archivan a SQLite y `memory/archive/`. Los MD espejo (`memory/todos.md`, `memory/inbox.md`, `docs/OSS-TRACKER.md`) se regeneran con `export-all`.
- **AGENTS.md:** documentado el nuevo sistema de memoria híbrido.

---

## [2026-08-15] - Estructura de proyectos con doble git

### Added
- **Script `scripts/init-project.sh`:** scaffold de proyectos con estructura doble git (`.knowledge/` en workspace, código en repo propio). Crea repos privados por default.

### Changed
- **AGENTS.md:** documentada la estructura de proyectos con `.knowledge/` y doble git.
- **AGENTS.md:** agregado protocolo de limpieza de proyectos al finalizar.

---

## [2026-08-14] - Ley del silencio y protocolo de sesión

### Changed
- **AGENTS.md:** adoptada la Ley de vida del silencio (hablar solo cuando hay algo que aportar).
- **AGENTS.md:** protocolo explícito de inicio/cierre de sesión + comando `/fuera`.
- **AGENTS.md:** reglas de commits (inglés, atómicos por issue) y verify-before-push para builds.

---

## [2026-08-13] - SoporteML V4 y skills de pipeline

### Added
- **Proyecto `soporteml-v4`:** reinicio con diseño premium. ADR-030: Lucide como librería de iconos base.
- **Skill `pipeline-detector`:** patrón de detectores locales + validación cruzada (formalizado tras aparecer 5 veces en el bootcamp).

### Changed
- **MEMORY.md:** documentado el pipeline de programación con agentes.

---

## [2026-08-12] - Skills de background y a11y

### Added
- **Skill `background-execution`:** patrones de ejecución en background (exec + process, parallel, auto-notify).
- **Skill `a11y-at-validation`:** validación AT manual obligatoria.

### Changed
- **AGENTS.md:** reglas operativas de background y procesos (PTY, aislamiento, auto-notify, parallel, submit vs write).

---

## [2026-07-25] - Refactor AGENTS.md: single source of truth

### Changed
- **AGENTS.md:** Reducido de ~23.5 KB a ~13 KB. Metodología detallada movida a skills correspondientes. Eliminados duplicados con SOUL.md, USER.md y MEMORY.md. Agregada tabla de referencia a skills con links directos.
- **CHANGELOG.md:** Separado en raíz (cambios del workspace) y `skills/CHANGELOG.md` (cambios de skills). Eliminados aprendizajes y next steps.

---

## [2026-07-25] - Limpieza de repositorios

### Removed
- **Moderno-Access-Virtual-Plate** - eliminado de GitHub
- **antigravity-developer-stack** - eliminado de GitHub (contenido migrado a ai-developer-stack)
- **copilot-skills** - eliminado de GitHub (reemplazado por workflow-kit)
- **projects/ local:** TanStack-router, ai-developer-stack-knowledge, nomad, pro-motors, radix-ui-primitives
- **Archivados:** 11 carpetas movidas a `.archive/`

### Changed
- **MEMORY.md:** Actualizada lista de repos propios (15 total). Regla: solo mostrar repos propios, no forks.

---

## [2026-07-24] - Git Workflow Fix

### Changed
- **AGENTS.md:** Added `git pull --rebase` before push in workspace git workflow.

---

## [2026-07-23] - Skills Workspace Overhaul: 20 → 33 Skills

### Added
- 13 nuevas skills (ver `skills/CHANGELOG.md` para detalle)
- 44 reference files, 49 scripts

### Changed
- Workspace skills count: 20 → 33
- Skills mirror synced to `.github/skills/`

## [2026-08-26] - ADR-040: Seleccion de Modelos por Tipo de Tarea

### Added
- **`docs/adr/ADR-040-modelos-seleccion-por-tarea.md`:** nuevo ADR que define el criterio de seleccion de modelos segun el tipo de tarea. Reemplaza al ADR-006. Incluye perfiles de personalidad para 8 modelos, guia rapida de seleccion, y regla operativa para que Kanam sugiera el modelo adecuado antes de cada tarea.
- **`docs/adr/README.md`:** agregado ADR-040 al indice.

### Changed
- **ADR-006 (Capacidad Computacional DeepSeek):** marcado como reemplazado por ADR-040.

### Why
- La migracion a Ollama Pro abrio acceso a 8+ modelos. No tiene sentido usar siempre el mismo modelo cuando cada uno tiene fortalezas distintas. Este ADR captura el criterio de seleccion basado en una cata empirica de 8 modelos con el mismo prompt.

## [2026-09-02] - .gitignore: silenciar proyectos sin .knowledge/ en el workspace

### Changed
- **`.gitignore`:** ignorados explícitamente `projects/accessible-ui/`, `projects/ai-developer-stack/`, `projects/create-with-ai/` - los 3 quedaban como untracked crónicos porque el patrón global `!/projects/*/` los re-incluye pero no tienen `.knowledge/` que trackear (el código vive en GitHub y en el agregado `projects_openclaw`; el checkout local es util pero no parte del repo del workspace).

### Why
- Después del setup triple-git quedaban 3 carpetas sin `.knowledge/` que ensuciaban el `status` del workspace. El fix documenta la excepción en el propio .gitignore en vez de listarla en memoria.

---

## [2026-09-02] - Fixes a scripts de memoria (catalog + export) tras sync con la Air

### Fixed
- **`scripts/memory-catalog-v2.py`:** crash `IndexError: list index out of range` en `compute_topic_centroids` - vectores de 32 dims (sesiones catalogadas con otro modelo de embedding) se mezclaban con los de 768 dims (nomic actual) para el mismo topic. Fix: solo mezclar vectores de la misma dimensión por topic (los de otra dims se saltean).
- **`scripts/memory-db.sh export-all`:** generaba ~2600 archivos basura en `memory/export/` - el split por `|` y por líneas rompía contra el contenido markdown (que tiene pipes y saltos de línea). Fix: una query por fecha, sin separadores. Ahora exporta 33 dailies limpios.

### Why
- El catalog crasheó al catalogar el daily tras el pull de la Air (que había catalogado con otro modelo). El export-all corrupto ensuciaba `memory/export/` (ignorado por .gitignore pero igual).

### Notes
- Sesión completa del día catalogada en DB (DB-first): las 3 secciones (22:00-22:56 mine desde desktop, 23:00-23:20 laptop, 23:26-23:40 post-pull verify). 28 sesiones, 74 vectores, 84 learnings.
- 2 todos nuevos: `.env` de soporteml (repo público trackea .env - decidir restaurar o purgar) y desarchivar create-with-ai (commit local legítimo bloqueado por repo archivado).

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
