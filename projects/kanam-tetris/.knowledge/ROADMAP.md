# ROADMAP - kanam-tetris

Objetivo vigente (decisión de Gonzo, 2026-09-14): **hacer que brille y sea perfecto.** El juego es el producto; el pipeline A/B es el vehículo.

"Perfecto" se define en tres capas, en este orden: (1) fidelidad a la guideline de Tetris, (2) pulido que se siente, (3) calidad de código sostenida. El orden importa: pulir sobre una base equivocada es deuda.

## Dónde estamos (auditoría contra la guideline)

| Mecánica | Estado | Nota |
|---|---|---|
| SRS + wall kicks | OK | ambas series, 8 transiciones, testeado |
| 7-bag | OK | con `rng` inyectable |
| Hold (1 por pieza) | OK | reset en `afterLock()` |
| DAS 170ms / ARR 50ms | OK | con re-step inmediato |
| Lock delay 500ms | PARCIAL | cap "por descenso", no por pieza (v0.6) |
| Ghost + hard drop | OK | hard drop paga 2/celda (guideline) |
| Soft drop 1/celda | OK | |
| Scoring base | PARCIAL | solo single..tetris x nivel; faltan T-spin, combo, B2B |
| Flash de limpieza | OK | 180ms, congelando la simulación |
| Next visible | PARCIAL | solo 1 pieza; guideline muestra 5 |
| High score | OK | localStorage con try/catch |

---

## v0.4 - Scoring de guideline + visión (T-spins, combos, B2B, 5 next)

El paquete coherente: la detección de T-spin habilita el scoring completo, y la cola expuesta habilita la planificación. Todo es lógica pura del core - exactamente lo que la red de tests cubre mejor.

### R1 - Detección de T-spin

**Requisito.** Clasificar cada lock de una T como T-spin full, mini, o ninguno. Regla (guideline, "3-corner rule"): la T está en T-spin si su última acción fue una rotación exitosa y al menos 3 de sus 4 esquinas (incluido el centro del bounding box) están ocupadas o fuera del tablero. Full vs mini: full si el kick usado fue el de la tabla de index 4 (el kick "propio" del T-spin) o si ambos lados frontales están bloqueados; mini si no.

**Solución en el core:**
- `rotate()` exitoso setea `state.lastAction = { type: "rotate", kick: i }` (i = índice del kick que funcionó). Hoy devuelve `true/false` pero no lo registra: es el único dato que falta.
- Cualquier movimiento (move, gravedad, soft/hard drop) setea `lastAction = { type: "move" }`.
- En `lockPiece()`, si `current.type === "T"` y `lastAction.type === "rotate"`: contar esquinas ocupadas con `collides` contra el bounding box de la T. `>= 3` -> T-spin. El kick 4 (o frontales bloqueados) distingue full de mini.
- Exponer `state.lastClear = { type: "tspin_full" | "tspin_mini" | "normal", lines: n }` para el renderer y el scoring.

**Tests obligatorios:** T en hueco de 3 lados -> full; T rotada al último momento en el piso -> mini; T que rota y luego cae una fila por gravedad -> normal (la rotación "expira"); T en espacio abierto -> normal. Cada caso con tablero forzado del harness.

**Scoring (guideline):** T-spin single 800, double 1200, triple 1600, mini single 200, mini double 400 (x nivel). T-spin sin líneas: full 400, mini 100.

### R2 - Combos

**Requisito:** limpiezas consecutivas (una por pieza clavada) acumulan combo. Pieza clavada sin limpiar lo resetea a -1.

**Solución:** `state.combo` en el core; en cada lock con líneas: `combo++`, bonus `50 * combo * level`; sin líneas: `combo = -1`. El HUD lo muestra desde combo >= 1.

**Tests:** secuencia limpia-limpia-limpia = combo 1,2 con bonuses acumulados; intercalar un lock sin clear lo resetea.

### R3 - Back-to-back

**Requisito:** limpiezas "difíciles" (tetris o cualquier T-spin con líneas) consecutivas multiplican x1.5 el bonus de la limpieza difícil. Un clear normal rompe la cadena (pero un lock sin clear NO la rompe - guideline).

**Solución:** `state.b2b = true | false`. Se setea en clear difícil, se rompe solo con clear normal. Bonus: `base * 1.5` redondeado hacia abajo.

**Tests:** tetris-tetris con B2B; tetris-single-tetris sin B2B; tetris-lock-sin-clear-tetris CON B2B (el caso que rompe la intuición).

### R4 - Cola de 5 next

**Requisito:** mostrar las próximas 5 piezas. El bag ya existe (`state.bag`): exponer `state.queue = [current siguientes 5]` manteniendo el refill garantizado (la cola nunca debe quedar corta para el render).

**Solución:** derivar la cola en un getter del core (bag + nextType), y en el renderer un solo canvas vertical con las 5 en cascada. Cambio de layout del panel lateral (previews apiladas, hold arriba).

**Tests:** la cola respeta el 7-bag sin repetir dentro de la ventana; tras hold, la cola no se altera.

### Criterios de cierre de v0.4
- Suite en verde con los tests nuevos de las 4 features (estimado +20 tests).
- Revisión adversarial de Agente B sobre las costuras nuevas (preview de 5, overlay de combo/B2B).
- Validación en browser de Gonzo: un T-spin double puntúa 1200 x nivel, el combo visible sube, el B2B se anuncia.

---

## v0.5 - Sonido + game feel

Primera feature fuera del core: **Web Audio con osciladores sintetizados, cero assets, cero dependencias.** Se mantiene el espíritu cero-build.

### R5 - Motor de sonido
- `src/audio.js`: un `AudioContext` perezoso (se crea en el primer input - los browsers bloquean el audio hasta interacción), funciones `blip(freq, dur, type, gain)` compuestas.
- Eventos y su sonido: lock (tick corto 120ms), clear (arpegio que sube con la cantidad de líneas), tetris (fanfarria 4 notas), T-spin (acorde distinto), levelup (sweep), hard drop (thud grave), hold (blip suave), game over (descendente).
- Toggle de mute (`M`) persistido en localStorage. El core sigue sin saber del audio: main.js se suscribe a los eventos que ya emite (`clear`, `holdUsed`, `gameover`) - el trabajo es escuchar mejor, no emitir más.

### R6 - Game feel
- Screen shake sutil (2-4px, 100-150ms) en tetris y T-spin, respetando `prefers-reduced-motion`.
- Partículas simples al limpiar (cuadraditos del color de la pieza que se desvanecen) - canvas del propio tablero, sin librerías.
- Transición del overlay (fade 150ms) en vez de aparición seca.

**Riesgo acotado:** todo esto vive en render/audio, no toca reglas. El core no cambia; los 33 tests deben seguir verdes sin tocarlos.

---

## v0.6 - Fidelidad fina

### R7 - Lock delay por pieza (deuda registrada desde v0.2)
Hoy el cap es "por descenso": un wall kick hacia abajo re-arma `lockResets`. Guideline-correct pero distinto al estándar moderno (cap por pieza, "move reset" limitado a 15 en total). **Solución:** `lowestY` pasa a ser `spawnY` del piece actual; los resets consumen del presupuesto de la pieza completa. Riesgo: cambia el feel del stall avanzado - medir en browser antes de aceptar.

### R8 - Tabla de gravedad guideline
`dropInterval` lineal (`800 - 70*(level-1)`) por una tabla tipo guideline (frames por fila). Es un cambio de constantes + un test de tabla completa.

### R9 - Verificación visual medida (cierra el hueco histórico)
Harness de screenshots: servir el juego, capturar con el browser de OpenClaw, comparar píxeles del flash y el centrado de previews contra el v0.2 de referencia. El review dejó de comparar código y empieza a comparar render.

---

## Infra transversal (en cada versión)
- Los tests crecen con la feature: no se mergea feature sin su test de mutación.
- `BRIEF.md` documenta los hallazgos del ciclo; `CHANGELOG.md` del proyecto si hay cambio de contrato.
- Validación en browser de Gonzo como paso final, siempre.