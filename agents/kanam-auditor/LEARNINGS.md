# LEARNINGS.md - The UI/UX Auditor 🎨

> Lessons log del agente. Una entrada por aprendizaje, fecha + fuente (commit, run, PR, error). No se actualiza retroactivamente; si una entrada queda obsoleta se marca `superseded` y se deja la nueva. Los LEARNINGS alimentan mi ROADMAP: una lección nueva que no cambia la planificación está mal escrita.

Formato:
```
## L-nnn · AAAA-MM-DD · <frio | caliente>
- **Origen:** dónde lo aprendí (run, commit, error)
- **Lección:** una frase prescriptiva
- **Evidencia:** archivo/commit/pr
- **Efecto en el roadmap:** qué cambió o qué sigue abierto
```

---

## L-001 · 2026-11-06 · caliente

- **Origen:** Primer run real del action en `preflight-a11y#1`. El step "Run surface audit" terminó en exit 1 sin mensaje, aunque el engine había escrito `report.json`.
- **Lección:** Los bloques inline con heredoc o `node -e` dentro de un `run: |` se pliegan al parsear `action.yml` y matan el step sin error. Todo heredoc, comilla anidada o código multinivel va a un script con test.
- **Evidencia:** `.github/workflows/surface-audit.yml` del action (diff antes/después); los scripts en `scripts/`.
- **Efecto:** Añadido el principio "un script con test" al plan de cualquier action nueva. Costó un run real y un comentario de PR en una sola tarde.

## L-002 · 2026-11-06 · caliente

- **Origen:** Simular el job de CI con un checkout limpio. `git archive HEAD` dejó `projects/` vacío porque está gitignored (`.gitignore:58`). El pipeline escaneó 0 archivos y devolvió `APROBADO`.
- **Lección:** Un stage vacío no aprueba. 0 archivos escaneados es una señal de infraestructura rota, no de superficie limpia.
- **Evidencia:** `surface-pipeline/src/stages.js` guard `stage-no-files`; `tests/pipeline.test.js` primer test (`"un path inexistente NO aprueba"`).
- **Efecto:** Reescribió el target del pipeline canónico de `projects/preflight/src` a `agents/kanam-auditor/skills` (la única superficie real que está tracked). Añadió `exclude` al enforcer.

## L-005 · 2026-11-06 · caliente

- **Origen:** Uno-a-uno del roadmap para evitar superar la capacidad del modelo.
- **Lección:** No tomar el portero y los flujos B/C en la misma sesión. Aprendí que el costo de un flujo sin evidencia decretar obvia es más alto que diferir.
- **Evidencia:** `ROADMAP.md` Flujo A probado en dos direcciones; Flujo B y C permanecen como lineas de tremp pendientes.
- **Efecto:** Decidir plantear B por separado (pre-commit, hook harness) y C solo después del flujo.

## L-012 · 2026-11-09 · caliente (auditoria multi-sesion)
- **Origen:** Auditoría de tres días con nuevo modelo. Corriendo `audit-surface` sin piezas activas, el reporte se rompía con `Cannot read properties of null (reading 'routes')` porque `consoleReport`/`stageSummary` asumían `r.stats` no nulo; en stage-error `stats=null`.
- **Lección:** Cualquier detalle en el render debe asumir stage fallido (stats null). El guard `stage-no-files` ya contempla stage-error, pero el reporte olvidaba la defensa en otra etapa.
- **Evidencia:** stack `report.js:45`, `stageSummary()`; corregido con `rs = r.stats || {}`.
- **Efecto:** `pipeline` vuelve a emitir veredicto cuando hay stage-error; el reporte no puede ser la nueva fuente de pérdida (evaluate no multiplicar puntos de falla).

## L-013 · 2026-11-09 · frío (auditoría de self)
- **Origen:** El `design-enforcer` scan detectó su propia tabla de mapeo 1:1 (`TOKEN_MAP`) como valores hardcodeados.
- **Lección:** Todo el hardcode introducido se trata como superficie: o se excluye documentadamente, o se tokeniza. Aquí se whitelisteó la tabla de referencia (mapa determinístico).
- **Evidencia:** 7 warnings (`#f3f4f6`, `#3b82f6`, etc.) → 0 tras whitelist con motivo.
- **Efecto:** `kernel` mantiene invariantes: self-audit sin la propia base.

## L-011 · 2026-11-07 · frío (C.2 documentada)
- **Origen:** Añadí convención baseline en pixel-diff SKILL y score en surface-pipeline SKILL.
- **Lección:** Sin base de capturas aprobada, \`pixel-diff\` solo opina; el path `.kanam/baselines/<slug>.png` reproducible es lo que lo convierte en regla de negocio.
- **Evidencia:** SKILL.md de ambos skills extendidos con convención/formula.
- **Efecto:** Flujo C documentado. Restan exclusivamente decisiones de integración con workspace (check-audit-due.py), fuera de este agente.

## L-010 · 2026-11-07 · frío (C.2/C.4)
- **Origen:** Creación de `surface-score` y su ejecución sobre el último reporte (100/100).
- **Lección:** El score sale del `report.json`, no de la consola. Sin archivos canónicos no hay tendencia.
- **Evidencia:** `surface-pipeline/bin/surface-score` → `score.json` (grade A en el árbol actual).
- **Efecto:** Flujo C parcial con cadencia (scoring). C.3 queda como wiring workspace, no agente.

## L-009 · 2026-11-07 · frío (C.1)
- **Origen:** Helper `pixel-baseline --save <png>` implementado y probado con PNG sintético; crea directorio + copia + manifest incremental.
- **Lección:** El baseline empieza por convención (directorio + manifest), no por almacenamiento inmediato en git (peso y diffs inútiles). Guardar PNG versionado solo cuando un producto adopta el flujo de artefactos.
- **Evidencia:** `pixel-diff/bin/pixel-baseline` smoke test: `home.png` + `manifest.json`.
- **Efecto:** Flujo C arranca con baseline local reproducible. C.2/C.3 queda como orquestación e integración futura.

## L-008 · 2026-11-07 · frío (B.3)
- **Origen:** Implementación de `--fix --apply` 1:1, verificada con dry-run y apply real.
- **Lección:** El `--fix` solo avanza cuando el mapeo es único; un reemplazo parcial (hex sin token) se ignora silenciosamente para no inventar.
- **Evidencia:** CLI smoke: dry-run deja el archivo intacto; `--apply` reemplaza solo #3b82f6; relectura confirma 0 warnings.
- **Efecto:** Flujo B completo (fast lane + watch + fix deterministico). Flujo C (cadencia por producto, baselines, score) es lo que sigue.

## L-007 · 2026-11-07 · frío (B.2)
- **Origen:** Implementación de `--watch` con rotación de archivo, medido en temp repo real.
- **Lección:** `fs.watch(...,{recursive:true})` es suficiente en macOS/Linux. El debounce evita el ruido de rename/re-create del editor; sin lock files el evento del editor generaría falsos positivos.
- **Evidencia:** 2 auditorías reales disparadas al guardar (`run2.log`), latencia <1s.
- **Efecto:** Flujo B.2 cerrado. Flujo B.3 (`--fix` determinístico 1:1, `--dry-run` primero) queda como único pending de la sesión.

## L-006 · 2026-11-07 · caliente (B.1)

- **Origen:** Implementación de la fast lane para pre-commit y medición: 40 staged CSS en ~0.10 s, 0→1 bloquea clean.
- **Lección:** `git diff --cached --name-only --diff-filter=ACM` + filtro de extensión + `analyzeFiles` es suficiente y barato. No hace falta montar un hook framework propio; el cuello es solo la latencia de startup.
- **Evidencia:** `design-system-enforcer/bin/design-enforcer.js` (`--staged`); test tmp ran en ~0.10 s.
- **Efecto:** Flujo B.1 cierra B1 sin wiring externo. Solo falta usabar el flag en un repo y medir en el wild.


- **Origen:** Portero en `preflight-a11y` después de la corrección de L-001.
- **Lección:** Un auditor que solo se probó en "el happy path" no valía lo que esperaba. El rechazo real se clavó cuando se inyectó gradiente + morado genérico + radio 24px, con 4 bloqueantes en 11 s.
- **Evidencia:** `preflight-a11y` PR #1, run #3.
- **Efecto:** Abrió la condición de "probado en las dos direcciones" como criterio explícito para marcar un flujo como cerrado en mi ROADMAP.

## L-004 · 2026-11-06 · caliente

- **Origen:** El auto-scan del propio enforcer reportaba 5 bloqueos. Los 5 estaban en `src/enforcer.js`, `src/color.js` y `enforcer.test.js` — las cadenas literales del motor y las fixtures.
- **Lección:** Un linter de diseño necesita `.eslintignore` equivalente. Las cadenas de una regex están en el motor; al escanear el propio fuente, se auto-rechaza. Un `exclude` no es una comodidad, es una invariante.
- **Evidencia:** `design-system-enforcer/src/enforcer.js` (default exclude); `.kanam/enforcer.config.yaml` (excludes documentados con razón).
- **Efecto:** Añadido `exclude` al `config` del enforcer. Tests: uno que garantiza que *sin* exclude sí bloquea (para que nadie lo borre por gusto).

## L-005 · 2026-11-06 · frío

- **Origen:** Comparar el oracle con `a11y-scan.mjs` y `check-a11y-trigger.py`. La tentación fácil era "unifiquemos en uno". Descubrí que fusionarlos pierde capacidad.
- **Lección:** Medición, política y orquestación son tres capas con dueño distinto. El coste de dependencias (Playwright) de la lane barata define qué pieza va dónde, no la preferencia por un único dueño.
- **Evidencia:** `docs/adr/ADR-111-frontera-a11y-medir-decidir-orquestar.md`.
- **Efecto:** Decidí que `a11y-scan.mjs` NO se absorbe en el oracle. El criterio de cualquier propuesta futura "unificar" tiene que responder qué pasa con Playwright en CI.

## L-006 · 2026-11-06 · frío

- **Origen:** Revisar el retrato de v0.1 de mi ROADMAP. Decía "oracle solo emite console, una sola ruta"; el código hace multi-ruta y reportes HTML/JSON desde el 2026-10-07.
- **Lección:** Un roadmap con filas vencidas miente más que sin roadmap. Si una fila ya se cumplió, se marca con fecha, no se borra (para no repetir el mismo error).
- **Evidencia:** `ROADMAP.md` sección "Corrección de retrato (2026-11-06)".
- **Efecto:** En `MEMORY.md` ahora hay una sección "hitos de mi evolución" con fechas verificables.

---

## Lo que este archivo NO es todavía

No es una base de datos. Cuando el número de entradas pase de ~50 o cuando el historial de veredictos importe, conviene migrar a una tabla `learning (id, fecha, origen, lesson, evidencia, efecto, superseded_por)` compartida con el sistema (o exclusiva por agente — pendiente de decisión). Hoy el MEMORY.md es el source of truth; nada reemplaza el trail de git.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
