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

## Dirección visual (decisión de Gonzo, 2026-09-14)
**"Wireframe de cajitas"** - el lenguaje elegido sobre 6 propuestas (3 paletas D1-D3, 3 wireframes V1-V3). Elementos:
- **Rejilla de puntos** como piso del tablero (reemplaza las líneas de grilla).
- **Piezas wireframe:** contorno + relleno apenas perceptible del color de la pieza. Las formas identifican la pieza; el color queda libre para codificar ESTADO (activa, lock inminente, clear, T-spin) - el hallazgo de diseño del ciclo.
- **Perspectiva sutil** (V2 calibrada suave, ~10-15° rotateX insinuado en piso y marco; las celdas siguen en grid recto para no perder lectura de columnas).
- Ghost punteado; paneles laterales planos (instrumento) frente al tablero con profundidad (contraste de planos).
- Pieza activa: glow breve solo en el lock.
Descartadas con razón: V3 isométrico (modelo de exhibición, no partida - queda como tema futuro), D2 CRT (glow permanente cansa).

## Alcance v0.4-visual - IMPLEMENTADA (2026-09-14) - wireframe de cajitas, sin features de juego

**La dirección visual decidida por Gonzo se implementa:** solo `src/render.js` (147 -> 196 líneas) e `index.html` (193 -> 220). El core NO cambió; los 33 tests siguen en 33/33.

### Qué se implementó
- **Rejilla de puntos** como piso (arc en centros de celda, alpha 0.06) - reemplaza las líneas de grilla.
- **Cajitas wireframe:** fill del color al 10% + contorno al 80% (strokeRect con inset de lineWidth/2). Clavadas: stroke 1px. Activa: stroke 2px.
- **Ghost punteado:** `setLineDash([3,4])`, fill al 4%, stroke al 30%. Mismo `gy !== cur.y`.
- **Glow de lock inminente:** cuando la pieza está apoyada (`grounded`), shadowBlur = 6 + 22 * (lockTimer / LOCK_DELAY_MS). Información de estado, no decoración. Decisión de diseño: en vez del glow post-lock (el lock es instantáneo y `clearing` es el estado visible), se eligió el glow PRE-lock - la pieza anuncia que se va a clavar.
- **Flash de limpieza adaptado:** pulso de contorno blanco (stroke 2.5px, alpha 0.35+0.6*pulse, shadowBlur 14*pulse con `pulse = sin(pi*t)`), fill de soporte al 5% - nunca el blanco sólido viejo.
- **Perspectiva sutil en contenedor CSS:** `perspective: 1000px` + `rotateX(12deg)` con `transform-origin: 50% 20%` y sombra de losa. Las celdas del canvas siguen en grid recto (no se deforman) - regla dura de lectura de columnas.
- **Jerarquía de paneles:** Puntuación es `panel primary` (valor más grande), Récord/Nivel/Líneas son `panel secondary` (más chicos, dim). El tablero se distingue con `--board-border` nuevo.
- Tokens: `--bg` #0d0f12 -> #0a0c0f, `--panel` -> #0f1217, `--text-dim` -> #848d9e, nuevo `--board-border` #3a4658.

### Verificación por EJECUCIÓN (harness mock ctx, no lectura - el Agente B cayó otra vez sin entregar)
El Agente B (deepseek-v4-flash) volvió a morir a mitad de la revisión (ver nota de pipeline abajo). La verificación la hizo Kanam con un harness de mock canvas 2D que registra cada llamada:
| Check | Resultado |
|---|---|
| Dots: ~200 arcs (COLS*ROWS) | ok |
| Cero moveTo/lineTo (sin líneas de grilla) | ok |
| Celda clavada: strokeRect + fill (alpha 0.10) + stroke 0.8 | ok |
| Ghost usa setLineDash | ok |
| En el aire: cero asginaciones de shadowBlur | ok |
| Apoyada timer~0: blur ~6 | ok |
| Apoyada 80%: blur ~23.6 (6+22*0.8) | ok |
| Flash: stroke grueso presente, sin fill blanco sólido masivo | ok |
| IDs DOM: todos los de main.js existen en index.html | ok |

**Contraste WCAG re-verificado (tokens nuevos):** text vs bg 14.33:1 AAA, dim vs bg 5.86:1 AA, accent vs panel 12.68:1, board-border vs bg 2.05:1 (marco visible), y las 7 piezas 7.1:1 a 12.25:1 contra el panel nuevo (todas >= 3:1 bloque gráfico, varias AA).

### Pendiente (paso 7 del protocolo) - CERRADO
**Validación visual de Gonzo en browser real: OK (2026-09-14, "muy bien, me gustó mucho").** Con eso queda cerrado v0.4-visual: la primera iteración visual completa del proyecto, con el lenguaje wireframe de cajitas validado por el ojo de su dueño. **v0.4-visual CERRADA.**

### Nota de pipeline (patrón a vigilar)
El Agente B cayó **por tercera vez** en medio de una revisión (v0.3 B original, v0.4 B, v0.4 B relanzado... verificar conteo real en dailies). El patrón: muere en tareas largas de revisión con el motor default. Consecuencia práctica: cuando B no entrega, la verificación de ejecución la hace Kanam - que era el paso 5 del protocolo de todas formas. Anotar como hallazgo operativo del pipeline.

## Alcance v0.4-scoring - CERRADA (2026-09-15) - T-spins, combos, B2B y cola de 5

**Validada en browser real por Gonzo (paso 7).** El ciclo destapo 3 bugs de costura que la suite del core no podia ver (game over entre frames, panel de cola vacio, overlay tapado por el contexto 3D) y agrego `test/dom.test.js` como primera red de la capa UI. Leccion central del ciclo: **core verde no significa juego sano** - toda la clase "wiring" necesitaba red propia y no la tenia.

### R1 - Deteccion de T-spin (3-corner rule)
- `state.lastAction = { type: "rotate", kick: i }` en cada rotacion exitosa (i = indice del kick que la logro). **Solo una maniobra LATERAL (`move`) lo pisa** con `{ type: "move" }`; la rotacion fallida no lo toca. `spawn` lo limpia a `null`: una pieza nueva no hereda la historia de la anterior.
- **Correccion de guideline (2026-09-14/15, error de la spec inicial, corregido por Kanam con doble fuente):** la primera version hacia que `hardDrop`, `softDrop` y la gravedad invalidaran la rotacion. MAL: la guideline premia "A T is dropped" - el TSD canonico de Tetris 99 / PPT / Effect es rotar en la cavidad y hard-dropear (TetrisWiki "T-spin": el ejemplo canonicoliteral es una T dropeada; FOUR: "the last action was a rotation", la caida no es una maniobra). Solo el slide lateral rompe el spin. Tres mutaciones de test fijaban el comportamiento equivocado; reescritos: gravedad preserva, hard drop ES T-spin, soft/hard drop preservan. La regla de las esquinas corre en la posicion final (resolveLock), no en la de la rotacion.
- En el lock, si la pieza es T y la ultima accion fue rotar, se cuentan las 4 esquinas del bounding box. `>= 3` bloqueadas u fuera del tablero -> T-spin.
- **Coordenadas (hallazgo critico):** el origen `(x, y)` de la pieza es la esquina SUPERIOR IZQUIERDA de la matriz, no su centro. Las esquinas del 3x3 son `(x,y)`, `(x+2,y)`, `(x,y+2)`, `(x+2,y+2)`. La primera version leyo `centro +/- 1`, un box corrido una fila y una columna: toda la deteccion quedaba silenciosamente mal. Lo destapo el escenario de prueba (reportaba 0 esquinas bloqueadas en un slot real).
- **Full vs mini (decision documentada):** FULL si (a) el kick fue el indice 4 (el kick tardio que solo entra en una cavidad), o (b) el nub apunta hacia abajo, o (c) las dos esquinas frontales Y las dos traseras estan bloqueadas (slot 1x1 que la T solo entra kickeando). MINI en cualquier otro caso con 3+ esquinas. El kick 4 se acepta como senal de full pero NO se exige: una T rotada contra una pared en kick 0 tambien puede ser full.
- `state.lastClear = { type, lines, tspin, b2b, combo, points }` en cada lock, tambien cuando no limpia lineas. El evento `clear` lleva el tipo.
- Scoring x nivel: full single 800, double 1200, triple 1600; mini single 200, mini double 400; sin lineas full 400 / mini 100. La tabla normal (100/300/500/800) no cambia.

### R2 - Combos
`state.combo` arranca en -1. Lock con lineas: `combo++`, bonus `50 * combo * level` solo si `combo >= 1`. Lock sin lineas: `combo = -1`. **El bonus de combo ya lleva el nivel multiplicado y NO se vuelve a multiplicar por nivel** (bug encontrado en esta iteracion: `(base + b2b + combo) * level` aplicaba el nivel dos veces al combo; el test de escalado por nivel lo cazo).

### R3 - Back-to-back
`state.b2b` bool. Limpieza dificil (tetris, o T-spin con 1+ lineas) con b2b previo: `+ floor(base * 0.5)`. Dificil setea `b2b = true`; limpieza normal lo rompe; lock sin clear NO lo rompe; T-spin sin lineas NO lo rompe (guideline). Test de mutacion: quitar el `else if (lines > 0)` y el caso "lock sin clear mantiene la cadena" muere.

### R4 - Cola de 5
`game.queue` como getter: `[nextType, ...bag]` con refill garantizado (`while (bag.length < NEXT_QUEUE_SIZE) refillBag()`). Leer la cola nunca consume el bag. El renderer dibuja las 4 siguientes en un canvas vertical en cascada; la 1ra sigue siendo el panel "Siguiente" grande.

### HUD y feedback
- **T-spin:** anuncio flotante en el canvas ("T-SPIN" / "T-SPIN MINI") + pulso del marco del board, y el flash de la limpieza usa el color de la T (violeta) en vez de blanco. Elegido sobre particulas o banner por coherencia con el lenguaje wireframe: es texto y un borde, nada nuevo. El timestamp vive en `state.announce` (lo setea `main.js` desde el evento `clear`), asi el core sigue sin reloj.
- **Combo:** contador junto al score, visible solo con `combo >= 1`.
- **B2B:** badge cuando `b2b` esta activo.

### Costuras (bugs encontrados y corregidos en este ciclo)
0a. **Overlay tapado por el tablero inclinado (paso 7, captura de Gonzo):** el overlay SI se mostraba (el fix del evento `gameover` funcionaba), pero el canvas lo tapaba. Causa: `#board-wrap` tiene `perspective: 1000px`, que crea un contexto de renderizado 3D compartido; el canvas con `rotateX(12deg)` trae su mitad inferior hacia el espectador y se compone por encima de un hermano plano en z=0. El overlay era ese hermano, dentro del mismo contexto. **La captura fue clave: sin pieza activa (partida realmente perdida) pero sin overlay visible - dos sintomas que parecian uno.** Fix: wrapper `#board-stack` plano que contiene al wrapper con perspectiva y al overlay, sacandolo del contexto 3D, mas `z-index` explicito (`39d67db`). Pinchado con tests estructurales que leen `index.html` (el angulo se mantiene en 8-16 grados). Mutacion verificada: mover el overlay adentro de `#board-wrap` mata el test.
0b. **Panel COLA siempre vacio (paso 7, captura de Gonzo):** `render.js` leia `state.queue` pero el core exponia la cola como getter del objeto devuelto (`game.queue`). Los tests del core leian `game.queue` y pasaban; el render nunca veia nada. Fix: la cola vive en `state` (el objeto que el render recibe), una sola fuente de verdad (`9d6e61c`). Misma familia que el `blur` de v0.3 y el game over: **contrato desalineado entre capas**.
0c. **`test/dom.test.js` (nuevo, 9 tests):** primera cobertura de la costura UI. Arranca `main.js` contra un DOM falso, corre frames reales, keydowns y clicks. Caza los dos bugs de v0.4 por mutacion: restaurar el frame-diff mata el test del overlay; quitar `state.queue` mata los de la cola. **Leccion: core verde no significa juego roto-no.** Toda la clase "wiring" necesitaba red propia, y no la tenia.
0. **Game over sin anuncio (paso 7, reportado por Gonzo):** el overlay de fin de partida nunca aparecia. Causa: la UI detectaba la transicion comparando `state.gameOver` entre frames de rAF, pero un hard drop termina la partida SINCRONICAMENTE dentro del keydown - entre frames. El frame siguiente veia `wasGameOver` ya en true y la transicion nunca se detectaba. El core SIEMPRE emitio el evento `gameover`; nadie lo escuchaba. Fix: la UI reacciona al evento, no al diff de frames (`3fee4b0`). Leccion: el diff de frames solo caza transiciones que ocurren DENTRO de step(); todo lo que corre en handlers de input necesita el evento.
1. **`findFullRows()` corria ANTES de estampar la pieza:** una I que completaba la fila de abajo no registraba limpieza. Regresion introducida al reordenar `lockPiece` para que la deteccion leyera el board pre-estampado. Fix: deteccion -> estampar -> `findFullRows()`. Las 3 pruebas de `clearing` lo cazaron.
2. **`applyClear` duplicada** tras un patch, con la primera definicion ganando y salteandose el scoring. Un `node -e` contando definiciones la encontro.
3. **El nivel se aplicaba dos veces al bonus de combo** (ver R2).
4. **`resolveLock` reemplazaba la pieza antes de puntuar** en el camino sin clear.

### Verificacion
- `node --test test/`: **74 tests, 74 pass, 0 fail** (los 33 originales siguen verdes; no murio ninguno). 62 del core + 12 de `test/dom.test.js` (capa UI).
- **Verificacion en browser real (paso 7, 2026-09-15):** sonda via beacon HTTP servida desde el propio proyecto, abierta en Safari. Resultado: `over0=false | over1=true | fired=1 | ovClass=visible | ovDisplay=flex | ovRect=302x715 | topAtCenter=overlay-sub`. El overlay aparece, tiene tamaño real y esta arriba de todo (`elementFromPoint` en su centro lo devuelve a el, no al canvas). Probado tambien el camino del fin de partida tras un flash de limpieza: emite `gameover` igual.
- **Nota de metodo:** las dos primeras rondas de "fix" se verificaron solo con DOM falso y no alcanzaron. Lo que cerro el diagnostico fue medir el browser REAL (`elementFromPoint` + computed style), no leer el codigo. Cuando un bug sobrevive a un fix verificado, la verificacion es la que esta mal.
- Mutaciones corridas (cada una mata su test, y se restauro el original en cada caso): no invalidar por `move`, por gravedad, por `softDrop`, por `hardDrop`; kick fallido arma el flag; spawn no limpia `lastAction`; esquinas corridas `centro +/- 1`; combo no se resetea en lock seco; b2b roto por lock seco; b2b no roto por clear normal; mini valuado como full; bonus b2b ausente; cola sin refill, con head equivocado y con profundidad corta; tetris no-dificil; T-spin no-dificil. En la capa UI: restaurar el frame-diff mata el test del overlay; quitar el getter de `state.queue` mata los de la cola; meter el overlay dentro del contexto de perspectiva mata el estructural.

## Alcance v0.5 - CERRADA (2026-09-15) - sonido + game feel

Primera feature fuera del core. **`src/core.js` con diff CERO: ni una linea tocada.** 123 tests (74 previos + 49 nuevos).

### R5 - Audio sintetizado (`src/audio.js`, 309 lineas)
- **Cero assets:** todo con osciladores de Web Audio.
- **AudioContext perezoso:** se crea en el primer keydown (los browsers bloquean el audio hasta un gesto). `contextFactory` inyectable = la costura de la casa (`rng`, `blurTarget`).
- **Mute (`M`)** persistido, y al mutear **suelta la referencia al contexto**: no se construye nada mientras esta muteado.
- **Nunca rompe el juego:** sin `AudioContext` o si el constructor tira, el juego sigue jugable en silencio.
- Mapa de eventos: lock = `clear` con 0 lineas; clear 1-3 = arpegio; 4+ = fanfarria; T-spin = acorde; hold = `holdUsed:true` (el `false` del refill es mudo); game over = `gameover`. **Derivados** (el core no los emite): levelup (por cambio de `payload.level`) y hard drop (flag en el keydown de Espacio, consumido por el `clear` sin lineas siguiente). Preferido antes que agregar eventos al core.

### R6 - Game feel (`src/effects.js`, 142 lineas)
- **Screen shake** (3px, ~120ms) en clear y T-spin. **`prefers-reduced-motion` lo desactiva entero.**
- **Particulas**: cuadraditos del color de la pieza que se desvanecen. Con reduced-motion **bajan de 3 a 1 por celda** pero NO se eliminan: son informacion (que filas se limpiaron), no decoracion.
- El loop avanza `effects`; el renderer solo LEE (`effects.state.shakeX/particles`), asi `render.js` sigue sin mutar estado del juego.
- Overlay con fade de 150ms (CSS), apagado tambien por reduced-motion.

### Consistencia (fix de Kanam sobre el trabajo del agente)
Un **T-spin sin lineas** paga 400/100 y el juego lo anuncia en pantalla con "T-SPIN", pero el sonido caia en el tick de lock comun: imagen y sonido se contradecian. Ahora suena el acorde. El agente lo habia decidido a proposito y documentado ("locks with a tick"); se corrigio porque el cartel contradice esa logica. Test que lo fija y muere al revertir.

### Timbre y musica (v0.5.1, 2026-09-15 - ajuste tras quejarse de tonos "desesperantes")
- Filtro low-pass compartido: cada nota pasa por el filtro, los cuadrados y sierra pierden el filo hiriente. Envolvente con attack chico (sin click) y release musical exponencial.
- **Musica de fondo Korobeiniki** (tema del Game Boy): tabla de notas secuenciadas con los mismos osciladores, cero archivos. Canal de gain propio -> mismo filtro, la SFX no corta la melodia.
- **Tecla M cicla 3 estados**: SFX solo -> SFX + musica -> mute (y al mutear se limpia el flag de musica: desmutear no resucita el tema).
- Fix del crash que congelaba el juego al limpiar lineas: `effects.burst` ahora valida que `rows` sea array. El loop ya no puede morir en un clear.

### Servidor de desarrollo (`serve.py`, nuevo)
`python3 -m http.server` no manda `Cache-Control`, y **Safari cachea heuristicamente los modulos ES**: sirve una version vieja tras editar. Se vio dos veces en este ciclo (un `render.js` viejo con alpha 0.10, y un `storage.js` viejo sin `loadMuted` que rompia el grafo de imports). `serve.py` manda `no-store` en cada respuesta.

### Verificacion
- `node --test test/`: **123 pass, 0 fail**. Desglose: core 29, scoring 29, input 4, dom 18, audio 26, effects 17. Los 74 previos verdes sin tocarlos.
- **Revision de Kanam por ejecucion** (el agente verifico estructura; Kanam verifico comportamiento): 20 aserciones propias con mock de AudioContext (conteo de osciladores por sonido, mute que no construye contexto, degradacion sin `AudioContext`, expiracion de particulas, reduced-motion) mas mutacion del fix de consistencia.
- **Verificacion en browser REAL (Safari, sonda con beacon):** `created_pre_gesture=0 | created_post_gesture=1 | osc_total=6 | osc_started=6 | suena=true | mute_label=MUTE | muted | osc_tras_mute=0`. El contexto se crea SOLO tras el gesto, suena, y el mute corta de verdad.
- **NOTA HONESTA:** que los sonidos *suenen bien* (timbre, volumen, musicalidad) no se puede verificar sin oido humano. Lo verificado es la estructura (que suenen, cuantos osciladores, cuando). El juicio estetico es de Gonzo.

## No-alcance (para futuras iteraciones)
- Sonido, game feel (v0.5). Lock delay por pieza, tabla de gravedad guideline, verificacion visual medida (v0.6). Multiplayer, movil/touch.

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
- **2026-09-14 (PIVOT DE OBJETIVO, decisión de Gonzo):** el proyecto deja de ser solo experimento del pipeline - **ahora ES kanam-tetris. Objetivo: hacer que brille y sea perfecto.** El juego pasa de ratón de laboratorio a producto. Consecuencias: las features del no-alcance (T-spins, combos, sonido, móvil) pasan a roadmap real; "perfecto" se define como fidelidad a la guideline de Tetris + pulido visual/sonoro + calidad de código sostenida (la red de tests crece con cada feature). La metodología A/B sigue siendo el vehículo, no el destino.
