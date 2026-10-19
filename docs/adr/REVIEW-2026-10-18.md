# Review profundo del corpus de ADRs (2026-10-18)

**Revisor:** kanam-critic. **Alcance:** los 69 ADRs vivos de `docs/adr/` + `README.md`, tras la jubilación masiva de hoy. Guards de integridad (`check-adr-integrity.py`, `check-adr-supersede.py`) pasan; referencias cruzadas a ADRs retirados: **cero** (grep sobre 004, 006, 016, 018-019, 022-024, 026-027, 029-033, 035-036, 039-041, 045-046, 053, 068, 071-072, 075, 081 - sin resultados en archivos vivos).

---

## Hallazgos ALTA

### A1. ADR-090 contradice el runtime (la política vigente de modelos mentiría hoy)
**File:** `ADR-090-pensamiento-nivel-configuracion.md:51-79` (secciones "Decisión 2" y "Estado de implementación").

ADR-090 declara -con ✅ por fila- que el runtime aplica: main/dev/planner/studio/mind/ops en `nemotron-3-super:cloud`, critic/auditor en `deepseek-v4.1-flash:cloud`. **Verificado contra `~/.openclaw/openclaw.json` (leído hoy):**

| Agente | Declara ADR-090 | Runtime real HOY |
|---|---|---|
| main | `nemotron-3-super:cloud` | `deepseek-v4.1-flash:cloud` |
| kanam-dev | `nemotron-3-super:cloud` | `gpt-oss:120b-cloud` |
| kanam-planner | `nemotron-3-super:cloud` | `gpt-oss:120b-cloud` |
| kanam-studio | `nemotron-3-super:cloud` | `gemma4:cloud` |
| kanam-mind | `nemotron-3-super:cloud` | `deepseek-v4.1-flash:cloud` |
| kanam-ops | `nemotron-3-super:cloud` | `gpt-oss:120b-cloud` |
| kanam-critic | `deepseek-v4.1-flash:cloud` | `gpt-oss:120b-cloud` |
| kanam-auditor | `deepseek-v4.1-flash:cloud` | ✅ coincide |
| defaults | (implícito) | `nemotron-3-super:cloud` |

**Es el único ✅ de la tabla.** El ADR que el contexto declara "HOY la política vigente" describe un config que **no corre**. Además ADR-080 (`kanam-studio` = `deepseek-v4.1-flash:cloud` + fallback `glm-5.3-flash:cloud`, verificado 2026-09-28) también contradice al runtime (`gemma4:cloud` / `glm4:9b`) y a ADR-087 (que validó `gemma4` en studio). Tres ADRs "vivos y aceptados" (080, 087, 090) describen tres estados distintos y ninguno coincide con el config real.

**Fix mínimo propuesto:** opción A - si ADR-090 sigue siendo la decisión vigente, **aplicar y verificar el config** (la deuda es del runtime, no del ADR) y añadir en ADR-090 una línea: "actualizado <fecha>: reaplicado tras deriva detectada". Opción B - si el runtime actual es la decisión real (por ejemplo una cata posterior no registrada), **editar la tabla de Decisión 2 de ADR-090 con los valores del runtime y fecha nueva**, y resolver el estado de ADR-080 (¿vigente o supersedido por ADR-090?). No puede quedar el triple-✅ sobre valores falsos: es exactamente el anti-patrón que ADR-095 castigó en el design system ("declarado verificado sin medirlo").

### A2. ADR-001/002/003 citan skills que no existen en el repo
**Files:** `ADR-001-product-pipeline-integration.md:19-24` (tabla "Skills reales que ejecutan el ciclo: `spec-discovery-creation`, `spec-draft-creation`, `product-definition-cycle`, `spec-validation`"); `ADR-002-openspec-primary-doc-format.md:96-98`; `ADR-003-product-reset-triggers.md` (secciones "Modo PIVOT" y "Referencias").

**Verificado:** `find skills agents/*/skills -maxdepth 1 -type d` sobre el repo real - **ninguna de las cuatro existe**. Lo único cercano: `kanam-spec-v2/specs/`, `kanam-spec/openspec/` y `agents/kanam-dev/skills/spec-driven-development`. Estos ADRs se "reescribieron 2026-10-15" precisamente para "eliminar skills ficticias" y en el mismo movimiento **consagraron como reales cuatro skills que el disco no contiene**. ADR-003 incluso documenta flags (`product-definition-cycle --mode PIVOT`) de una herramienta inexistente.

**Fix mínimo propuesto:** auditar de dónde viven realmente esas cuatro skills (¿plugins? ¿otro directorio? ¿fic­ción residual?). Si existen, citar su ubicación real en la tabla; si no, borrar la tabla y las menciones y dejar el ciclo descrito como procedimiento sin nombres de skill. Un ADR reescrito para eliminar ficción no puede reintroducir otra.

---

## Hallazgos MEDIA

### M1. README.md declara 69 ADRs pero el propio índice no está verificado contra el set real
**File:** `README.md` (índice completo).

Conteo del índice: **67 filas ADR** + `mcp-lovable-decision.md` (todo #38, sin número de ADR, fuera de la tabla). El disco tiene 69 archivos `.md` vivos: 68 ADR-NNN + README + mcp-lovable. El índice omite **ninguno grave**, pero `mcp-lovable-decision.md` es un documento de decisión ("Estado: Definido") que vive en `docs/adr/` **sin entrar al índice ni al esquema de numeración**. Además el índice tiene filas sueltas/separadores rotos entre ADR-005 y ADR-007 (líneas tabla fragmentadas visibles en el archivo).

**Fix:** o bien numerar el doc de Lovable como ADR formal (próximo número libre) o moverlo fuera de `docs/adr/` (p. ej. `docs/decisions/`). Reparar los separadores de tabla rotos.

### M2. ADR-038 cita archivos de learnings; existe un duplicado activo `metodologia.md` / `methodology.md`
**File:** `ADR-038-learnings-mirror-db.md:26-33`.

**Verificado:** `docs/learnings/` contiene **ambos** `metodologia.md` (685 líneas) y `methodology.md` (16 líneas) - dos archivos para la misma categoría. ADR-038 declara la estructura con `metodologia.md`; ADR-086:96 también lo cita. El duplicado corto es ruido o resto de migración, y contradice "un archivo por categoría".

**Fix:** consolidar `methodology.md` dentro de `metodologia.md` (o decidir el nombre canónico inglés) y borrar el sobrante. El README de learnings debe citar el nombre que quede.

### M3. ADR-076/077/087 conservan referencias a modelos retirados como si fueran operativos en secciones "vigentes"
**Files:** `ADR-076-ningun-agente-hereda-modelo-local.md:40-46,75` (tabla "Antes → Después" y fallbacks con `glm-5.3-flash:cloud` como vigente); `ADR-077-pipeline-ab-asimetrico.md` (tabla "Modelos probados" con `qwen3.5:cloud`, `minimax-m2.7:cloud`).

ADR-043 ya modela el patrón correcto: su actualización del 2026-09-29 marca explícitamente qué líneas quedaron históricas tras el retiro de `deepseek-v4-flash`. ADR-076 y ADR-077 no tienen esa nota: la tabla "Aplicado (verificado con `gateway config.get`)" de ADR-076 muestra `main → deepseek-v4.1-flash:cloud` y hoy `main → deepseek-v4.1-flash` (ok) pero `defaults → gpt-oss:120b-cloud` cuando el default real es `nemotron-3-super:cloud`. Un lector futuro no sabe qué parte del ADR describe el presente.

**Fix:** agregar la nota estándar "Nota <fecha>: los valores de config citados son históricos; la política vigente es ADR-090" al pie de ADR-076 y ADR-077 (2 líneas cada uno, sin reescribir).

### M4. ADR-063 declara `langchain-starter` y rutas del proyecto descontinuado sin marcar que el proyecto no existe
**File:** `ADR-063-kanam-insight-python-langchain.md` (Implementación, líneas finales).

La tabla de implementación cita `projects/kanam-insight/scripts/*` y `config/chroma_db/`. **Verificado:** `ls projects/` no contiene `kanam-insight` (el encabezado sí declara "DESCONTINUADO 2026-10-06", pero la sección Implementación sigue leyéndose como vigente). El header lo salva parcialmente; la tabla interna puede confundir.

**Fix:** anteponer a la tabla "Implementación (histórica - el proyecto ya no existe en `projects/`)" o plegar toda la sección bajo el header de discontinuidad.

---

## Hallazgos BAJA

- **B1. `docs/SETUP.md:77`** (cita dentro de corpus ADR, no un ADR) describe `model-router.sh` como "DeepSeek (1-2) → GLM 5.3 Flash (3) → Kimi K2.7 Code (4)". La ruta real del script (verificada) es `pipeline_ab → gpt-oss:120b-cloud / deepseek-v4.1-flash:cloud` + `pipeline_ab_prefilter → gemma4:cloud` (ADR-089). La descripción en SETUP ya estaba stale antes de hoy. **Fix:** reemplazar la línea por la del router real (o dejar solo "consulta `model <tipo>`"). Fuera del alcance estricto de esta review, pero es la referencia que un ADR vivo (ADR-088) apoya.
- **B2. ADR-049:** la parte "`claude-sonnet-4-6` → `deepseek-v4-flash:0731:cloud`" sigue sin la nota de "modelo retirado" en la tabla de enmascarado (línea 96); el retiro se documenta al final (línea 170) pero la tabla del medio miente a la lectura rápida. **Fix:** anotación inline en la tabla.
- **B3. ADR-052:** cita `skills/engram-project-memory` como skill del workspace; **verificado:** vive en `agents/kanam-mind/skills/engram-project-memory` (movida post-ADR-073). Funciona, pero la referencia nominal puede confundir. **Fix:** una línea "(hoy en `agents/kanam-mind/skills/`)".
- **B4. ADR-084:** cita `agents/kanam-dev/skills/cross-engine-css-measurement/scripts/ui-measure.mjs` - **existe, verificado.** Sin acción. (Se lista para registro de chequeo.)
- **B5. ADR-097:** todo verificado contra el repo real salvo el claim "vanilla JS, cero build" - consistente con `projects/kanam-tetris/`. Sin acción.
- **B6. ADR-013/015/021** ("Verificación en proyectos actuales"): `vitest` confirmado en `a11y-fixer/package.json` y `kanam-fixer/package.json`; `@tanstack/react-query` confirmado en `soporteml/package.json`. **OK.**
- **B7. mcp-lovable-decision.md:** formato no-ADR (sin número, sin `Decisores`), pero el contenido es coherente con la realidad (`openclaw mcp` con OAuth pendiente). Manejado bajo M1.

---

## ADRs confirmados sólidos (muestra verificada, no exhaustiva del resto)

- **ADR-043, 049, 077, 088, 089** - pipeline A/B: ruta en `scripts/model-router.sh` verificada línea por línea contra el ADR.
- **ADR-056, 082, 084, 092, 093** - guards y rotación: scripts, tests y hooks existen (`check-refs.py`, `changelog-rotate.py`, `session_plan.py`, `tests/python/test_*`).
- **ADR-057-062** - stack DB: `vector-util.py`, `chunk-util.py`, `db.py`, migraciones y tests presentes.
- **ADR-067** - solo procedimiento, sin claims técnicos.
- **ADR-069/070** - decisión de `kanam-story-bible`, evidencia interna coherente.
- **ADR-090 (sección thinking, no modelo)** - coherente con AGENTS.md.
- **ADR-094, 095, 096, 098** - verificados contra `scripts/a11y-scan.mjs`, `check-design-tokens.py`, design/tokens, y symlink `~/projects`.

---

## Veredicto final

**NO sano todavía - 2 hallazgos ALTA sin resolver.**

La jubilación masiva de hoy fue **exitosa en lo que se propuso** (cero referencias colgantes, guards en verde). Pero el corpus expone su punto frágil exactamente donde la propia tradición del sistema lo predijo: **los ADRs que describen el runtime de modelos**. ADR-090 declara con ✅ lo que el config no corre (A1), y el ciclo de definición de producto describe skills que no existen en el disco (A2). Un nuevo intento de "leer los ADRs para entender cómo opera el sistema" recibe información falsa sobre **el tema más operativo de todos: qué modelo corre cada agente**.

SHARP aplicado al corpus: S=3 (la tabla de ADR-090 es ruido activo contra el config), H=4, A=4, R=3 (los guards de integridad no detectan drift semántico ADR↔runtime), P=4 → **18 pts: VETO hasta resolver A1 y A2**.

Con A1 y A2 resueltos, el corpus sube a "Aprobado" sin reescrituras estructurales: los demás hallazgos son notas de 1-2 líneas.

**Evidencia base de este reporte:** lectura completa de los 69 archivos, verificación cruzada de `~/.openclaw/openclaw.json` (impreso arriba), `ls skills/ agents/*/skills/`, `grep` de rutas y skills citadas por cada ADR, y `scripts/model-router.sh` leído directo.
