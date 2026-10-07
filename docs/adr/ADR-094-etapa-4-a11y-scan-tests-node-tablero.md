# ADR-094: Etapa 4 de Kanam OS - medir accesibilidad (a11y-scan), cablear tests/node, y cerrar el Tablero

**Fecha:** 2026-10-06
**Estado:** Aceptado
**Decisores:** Gonzo / Kanam
**Origen:** sesión 2026-10-06 - Gonzo: *"El camino de madurez del sistema (Kanam OS, por etapas)" -> "etapa 4"*. Cierra/reubica los tres componentes de la Etapa 4 declarados en `docs/NORTH.md`.
**Relacionado:** ADR-073/074 (arquitectura multi-agente y despacho), ADR-090 (niveles de modelo), ADR-093 (plan de sesión)

---

## Contexto

La Etapa 4 ("Expansión y refinamiento") del blueprint absorbió en `docs/NORTH.md` tres componentes:

| Componente | Prioridad declarada |
|---|---|
| Módulo de especialistas (roles de dominio del Academic System) | Media |
| Validación a11y técnica (`axe-core`) | Media |
| Tablero de control del backlog | **Alta** |

El relevamiento (2026-10-06) mostró que el estado real no coincidía con "en curso" en ninguno de los tres:

1. **Tablero: ya construido, pero no reconocido como tal.** `kanam-os` corre (LaunchAgent `dev.gonzoblasco.kanam-os`, 200 OK con navegación real) y su vista **`/todos` es exactamente "el backlog como objeto visible"** que pedía el §2.5 de `DECISIONS.md`. La decisión seguía listada como *"decisión pendiente"* y el Tablero como *"en curso"*: un falso pendiente de seis días.
2. **A11y: la decisión estaba tomada, la pata automática no existía.** El §2.8 ya concluyó *"axe-core OSS + la tool `browser` alcanza"* y descartó `axe-devtools` (pago). Pero eso nunca se implementó: había tres piezas (contraste de paleta, validación manual, gate de trigger) y **ninguna medía una página viva**. La brecha no era de decisión, era de ejecución.
3. **Especialistas: ya absorbido.** El ADR-073 ("núcleo Kanam + Crew") y el ADR-074 (protocolo de despacho) ya adoptaron el patrón de roles. El §2.7 de `DECISIONS.md` cierra por sí solo: *"los 13 roles del sistema académico son demasiados para nuestro caso; el esqueleto transferible es Planner/Critic/Writer + SHARP"*. **Ese esqueleto ya está implementado** (Critic, Auditor, Planner + SHARP son las Etapas 1 y 3, completadas).

**Hallazgo de infraestructura:** `tests/node/` tenía tres suites (pipeline-queue, gateway-jobs-watcher, y el nuevo clasificador de a11y) y **ninguna corría en CI ni en el pre-commit**. Solo bats y pytest estaban cableados. Es el mismo patrón de la Etapa 2: artefactos que existen y nadie invoca.

## Decisión

### 1. La accesibilidad se MIDE, no se declara (`scripts/a11y-scan.mjs`)

**Se implementa el gate que el §2.8 ya había decidido:** axe-core OSS sobre una página viva, con playwright-core, sin suscripción.

- **Uso:** `node scripts/a11y-scan.mjs <url> [--json] [--impact serious] | --file <html>`.
- **Exit:** `0` pasa; `1` gate falla (violaciones >= umbral); `2` **error de infraestructura**. El exit 2 es deliberado: un gate que no puede correr (sin playwright, sin axe) **no es un verde** - es la "barrera que no corre y no lo dice" ya registrada el 2026-09-28.
- **El juicio es una función pura** (`classify`): se prueba en CI sin browser ni red, y se prueba que **puede fallar** (un check que no puede fallar no verifica nada - lección de `check-contrast.py`).
- **Cero dependencias nuevas en el workspace:** playwright-core se resuelve del propio OpenClaw (viaja con el gateway) o por `OPENCLAW_PLAYWRIGHT_CORE`; axe-core se usa local si está, si no se trae pineado y se cachea.
- **Corre LOCAL, no en CI:** el escaneo necesita chromium; CI no lo tiene. Se documenta la separación: clasificador en CI, medición real local (como la skill `a11y-at-validation`, que exige AT humano).

**Primera corrida (evidencia real):** sobre `kanam-os` en vivo encontró **`aria-allowed-attr` nivel `critical`** en `/todos`, `/fichas` y `/learnings` - `aria-pressed` sobre `<a href>` (chips de filtro), atributo ARIA no permitido en un enlace. Es un bug real, no cosmético: un control con estado que el lector de pantalla no puede interpretar correctamente. Se registra como TODO de `kanam-os` (no se arregla en esta sesión: el CORE no escribe código de proyecto, ADR-083).

### 2. `tests/node/` se cablea (runner + pre-commit + CI)

- **`tests/node/run.sh`:** punto de entrada único; cada `*.test.js` es autónomo (corre con `node`, sale con exit != 0 si falla). Sin framework.
- Cableado al **pre-commit** (junto a bats y pytest) y al **CI** (nuevo step "Node functional tests").

### 3. El Tablero se cierra como decisión (§2.5) y NO se adoptan los especialistas

- **§2.5 resuelto:** la superficie visual del backlog **es** `kanam-os /todos`. El modelo es **pull** (la app lee `memory.db` read-only); la discusión "push vs pull" de la ronda del ecosistema queda saldada: **pull**, y la fuente de verdad sigue siendo `memory.db` (no se muda a `tasks.json`).
- **Especialistas: diferido, no construido.** Ya está el esqueleto (Crew + SHARP). Añadir roles de dominio (Anthropologist, Geographer, ...) sin un dominio que los requiera es dispersión - lo contrario del criterio del H0 ("terminar, no empezar"). Queda anotado, con esta razón.

## Consecuencias

- **Positivas:** la accesibilidad pasa de "declarada" a "medida" (la brecha que el análisis marcó como `axe-devtools` "descartado por costo" hoy se cubre gratis). `tests/node/` deja de ser código muerto. Dos falsos pendientes (Tablero, especialistas) quedan resueltos/diferidos con motivo escrito.
- **Positivas (evidencia):** el gate encontró un bug real en la primera corrida. Es la prueba de que medía algo.
- **Coste:** nulo en deps. El escaneo es local (documentado).
- **Deuda abierta:** (a) el `aria-pressed` de kanam-os (TODO del proyecto); (b) el escaneo no corre en CI - limitación declarada, no silenciosa; (c) los especialistas siguen diferidos.

## Alternativas consideradas

1. **Instalar `axe-devtools` (pago).** Rechazada por el §2.8 (costo/cobertura): axe-core OSS + playwright cubre lo que se necesita.
2. **Escaneo en CI con `@axe-core/playwright` como dependencia.** Rechazada por ahora: mete playwright + chromium en el workspace cero-deps y en CI (~300 MB por corrida). El clasificador puro sí corre en CI; la medición con browser es local. Se puede promover si el workspace adopta un runner de browser (p. ej. vitest browser, como en react-spectrum).
3. **Construir los 13 roles del Academic System.** Rechazada: el §2.7 ya decidió que son demasiados y el esqueleto ya está.
