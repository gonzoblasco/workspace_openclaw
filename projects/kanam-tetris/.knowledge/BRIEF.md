# BRIEF - kanam-tetris

## Idea
Tetris clásico como experimento del pipeline de agentes (Claude Code via gateway Ollama). Estrategia "vivo": arrancar minimalista y funcional en un solo archivo, luego refactorizar y agregar features por iteraciones.

## Alcance v0.1 (minimal jugable) - COMPLETO
- Tablero 10x20, las 7 tetrominós estándar (I, O, T, S, Z, J, L).
- Rotación (↑), movimiento (← →), caída suave (↓), hard drop (espacio).
- Ghost piece (sombra de dónde va a caer).
- Líneas completas desaparecen + puntaje + nivel con velocidad creciente.
- Next piece visible. Game over + reinicio.
- Un solo archivo: `index.html` (HTML + CSS + JS + Canvas, cero build, cero dependencias).
- Estética: clásica minimalista oscura.

## Alcance v0.2 - COMPLETO (2026-09-11)
- Hold piece (`C`), un hold por pieza clavada.
- Lock delay con cap de 15 resets (move reset, guideline SRS).
- DAS 170ms / ARR 50ms con re-step inmediato al cambiar de dirección.
- Flash de 180ms al limpiar líneas antes de removerlas.
- Pausa (`P`/`Esc`) con overlay.
- High score persistente en localStorage.

## Alcance v0.3 - COMPLETO (2026-09-11) - refactor estructural, cero features

**Objetivo único:** mismo comportamiento observable, mejor estructura y verificación. Si el refactor cambia cómo se siente el juego, es un bug del refactor.

### Auditoría de v0.2 (901 líneas, single-file)
- **Bien:** separación conceptual por secciones; los 5 fixes de v0.2 con comentario del *por qué*; `clearing` como único estado congelante con guards en los 5 puntos de entrada; tablas SRS correctas (ambas series, 8 transiciones).
- **Problema central: estado global.** 21 variables `let` en scope de módulo, mutables desde cualquier función. Es lo que permitió los bugs de v0.2: nada impedía llamar `move()` durante `clearing`; el guard fue parche a posteriori. Cada feature nueva multiplica las combinaciones de estado a guardar a mano.
- **Dos fuentes de verdad para el tiempo.** `updatePlaying(delta)` avanza lock delay y gravedad, pero `updateDAS(delta)` corre después y puede llamar `move()`, que resetea el lock delay. `softDrop()` resetea `dropCounter` a mano. Simulación no determinista ni testeable sin `requestAnimationFrame`.
- **Cero tests.** El harness instrumentado de v0.2 se construyó a mano. Los 2 bugs encontrados son exactamente la clase que un test unitario de 10 líneas atrapa.

### Arquitectura objetivo
```
index.html          # markup + CSS + <script type="module" src="main.js">
src/core.js         # PURO: estado + simulación. Sin DOM, sin canvas, sin performance.now()
src/render.js       # canvas: dibuja el estado que le pasa el core
src/input.js        # teclado -> intenciones (move/rotate/drop/hold/pause)
src/storage.js      # localStorage con try/catch (high score)
src/main.js         # loop: delta -> core.step() -> render
test/core.test.js   # node:test nativo, cero dependencias
test/harness.js     # helpers: tablero desde string, pieza forzada
```

**Contrato del core:** no sabe que existe un browser. Recibe `step(deltaMs)` y expone el estado. Esa es la decisión que convierte "el reviewer debe EJECUTAR" en algo de 10 líneas.

**Runner:** `node --test` nativo. Sin dependencias, se mantiene el espíritu cero-build.
**Costo asumido:** `file://` bloquea módulos ES por CORS. El juego se sirve con `python3 -m http.server`, no abriendo el archivo.

### Red mínima de tests
| Test | Qué cubre |
|---|---|
| `clearing` bloquea input | Los 5 guards de v0.2: move/rotate/hardDrop/hold durante el flash |
| Kicks CCW | El lookup espejado, ambas series, las 8 transiciones |
| Lock delay | Cap de 15 resets, reset por descenso, reset por move/rotate |
| Hold | Un hold por pieza, reset en `afterLock()` no en `lockPiece()` |
| High score | Única escritura en `endGame()`, HUD en vivo |

### Decisiones de v0.3
- 2026-09-11: módulos ES sin build (opción B), core puro, red mínima de tests, cero features nuevas. Elegido sobre el refactor quirúrgico single-file (techo bajo para tests) y sobre Vite/Vitest (dependencias y build step en un proyecto que era cero-build a propósito).

### Resultado de v0.3

**La apuesta salió.** El single-file de 901 líneas son ahora módulos ES sin build y sin dependencias, con el core puro (`src/core.js`, 530 líneas) separado del browser. La red de tests pasó de 0 a **33 tests con `node --test` nativo**, y el costo del reviewer bajó de "construir un harness instrumentado a mano" (v0.2) a `node --test test/`.

**Archivos:** `index.html` 193 (era 901), `src/core.js` 530, `src/render.js` 147, `src/input.js` 98, `src/main.js` 117, `src/storage.js` 28, `test/core.test.js` 598, `test/harness.js` 174, `test/input.test.js` 102, más `package.json` (type module, para silenciar el warning de Node y habilitar `npm test`).

**Comportamiento observable: idéntico a v0.2, con una excepción que se encontró y se cerró** - ver la regresión de `blur` arriba. El resto de las costuras (render, input, main, storage) se comparó línea por línea contra el original en git y salió limpio.

**Prueba de mutación (la métrica que importa acá):**
| Mutación | ¿Muere? | Test que la caza |
|---|---|---|
| Quitar guard `clearing` de `hardDrop()` | sí | `clearing: intents are no-ops during the flash` |
| Lookup espejado de kicks (bug de v0.1) | sí | `kicks: the core selects the from>to row for CCW` |
| `holdUsed = false` de `afterLock()` a `lockPiece()` | sí | `hold: the slot refills in afterLock, not in lockPiece` |
| Revertir el fix de `blur` a `document` | sí (3 tests) | `blur is registered on blurTarget`, `regression: losing focus...` |
| Quitar el guard `clearing` de `rotate()` | **no** | - pero es correcto: inalcanzable, ver nota de cobertura |

**Verificado en browser real (paso 7 del protocolo):** Gonzo jugó la v0.3 el 2026-09-11 y reportó que funciona perfecto. Con eso se cierra el único hueco que quedaba abierto - la fidelidad de render (rampa del flash, centrado de previews) no la había mirado nadie, porque el review comparó el código del canvas línea por línea pero no midió píxeles. **v0.3 cerrada.**

## No-alcance (para futuras iteraciones)
- T-spins, combos, sonido, multiplayer, móvil/touch.

## Experimento
Pipeline A/B con agentes. Motor: `deepseek-v4.1-flash:cloud` (Claude Code via gateway Ollama `127.0.0.1:11434`) desde v0.2; v0.1 corrió con GLM 5.3 Flash (`127.0.0.1:11435`).

Protocolo aplicado (pausa obligatoria del AGENTS.md):
1. Kanam planifica (MAX).
2. Agente A escribe (HIGH).
3. Agente B revisa (HIGH) - **ejecutando**, no leyendo.
4. Iterar alternando roles.
5. Kanam revisa el conjunto (MAX).
6. Push.
7. Validación de Gonzo en browser real (regla del workspace).

**Nota v0.3:** desde el refactor, el Agente B tiene una vía barata de ejecución real: `node --test test/`. Ya no hace falta construir un harness instrumentado a mano como en v0.2.

## Hallazgos de los ciclos

### v0.1 (2026-09-09)
- El Agente B revisó filas de la tabla SRS pero no el índice del lookup.

### v0.2 (2026-09-11)
- **Bug nuevo (alcanzable en juego normal):** sin guard del estado `clearing`, la pieza ya clavada seguía siendo controlable durante el flash de 180ms. Mantener Espacio congelaba la limpieza de línea para siempre; flecha + Espacio estampaba bloques fantasma con score duplicado (invisible: `draw()` suprime la pieza activa durante el flash).
- **Bug preexistente desde v0.1:** lookup de wall kicks CCW espejado. La tabla tenía las 8 filas correctas; el índice leía la fila CW de la transición inversa.
- **Regla derivada:** para bugs dependientes de tiempo (timers, ventanas de input, estado transitorio), el reviewer debe EJECUTAR, no leer. Y al revisar una base, revisar el lookup, no solo los datos que indexa.
- **Sin verificar:** fidelidad de render (píxeles de canvas, rampa de opacidad del flash, centrado del preview). El review fue de lógica, no de medición visual.
- **Deuda conocida:** el cap de lock delay es "por descenso", no "por pieza" (un wall kick hacia abajo re-arma `lockResets`; guideline-correct y acotado por el piso). Cosmético: si el stack llega al techo, el preview de Hold se "des-dim" justo antes del game over.

### v0.3 (2026-09-11) - ciclo del refactor

**Método:** el Agente B corrió prueba de mutación (reintroducir el bug y confirmar que el test muere), más comparación línea por línea de las costuras contra el original.

- **Regresión real encontrada (severidad menor):** el listener de `blur` migró de `window` (v0.2, `:888`) a `document` (`input.js` con `target: document`). `blur` NO burbujea y el foco de ventana se dispara en `window`, así que el handler nunca corría. Impacto: con una flecha apretada (DAS activo), salir de la ventana con Cmd+Tab dejaba `moveDir` vivo y la pieza seguía deslizándose al volver. Confirmado empíricamente por B en Safari (beacon HTTP: `window` recibe el blur, `document` recibe 0).
- **Nota de cobertura (hallazgo propio):** los guards de `clearing` en `move()`, `rotate()` y `softDrop()` son **defensa en profundidad, no cubren un bug alcanzable**. La pieza ya clavada ocupa sus propias celdas en el board durante el flash, así que todo movimiento choca consigo mismo y es no-op *por colisión*, no por el guard. Evidencia: 3603 estados de `clearing` recorridos (7 piezas x 4 rotaciones x tableros con huecos de 2 a 4 celdas) - cero casos donde `move`/`rotate`/`softDrop` cambiaran algo. Consecuencia: **mutar el guard de `rotate()` NO rompe ningún test, y eso es correcto**, no un agujero. Un test no puede distinguir un guard inalcanzable de su ausencia. Vale la pena no confundir "mutación superviviente" con "test malo": acá la mutación sobrevive porque el código mutado es inalcanzable.
- **Las 3 mutaciones que importan mueren:** quitar el guard de `hardDrop()` (test `clearing: intents are no-ops`), volver el lookup espejado de kicks (test `kicks: the core selects the from>to row for CCW`), y mover `holdUsed = false` de `afterLock()` a `lockPiece()` (test `hold: the slot refills in afterLock`). Cada una falla contra su test específico, con mensaje propio.
- **Regla derivada:** la revisión de un refactor sin browser debe atacar las **costuras** (render, input, main, storage), no el core. El core es lógica pura que se copia con seguridad; el riesgo vive en el pegamento, y es donde no hay red. Y: un refactor que promete "comportamiento idéntico" necesita comparación contra el original en git, no solo la suite en verde.

## Decisiones
- 2026-09-08: nace el proyecto por pedido de Gonzo como experimento de agentes. Single-file HTML/Canvas. Ghost + hard drop sí, hold no.
- 2026-09-11: repo pusheado a https://github.com/gonzoblasco/kanam-tetris (antes solo local). v0.2 cerrada y validada por Gonzo en browser.
