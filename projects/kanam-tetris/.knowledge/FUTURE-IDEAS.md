# FUTURE IDEAS - kanam-tetris

Estas son propuestas que NO entran al roadmap comprometido (v0.4-v0.6). Cada una con: qué es, qué aporta, y por qué está acá y no allá. El orden interno es el orden en que las consideraría si "perfecto" algún día las pide.

## Juego

### I1 - Modos de juego
- **Sprint (40 líneas):** cronómetro, estadísticas de PPS. El modo competitivo estándar de la comunidad; primer modo con objetivo distinto de "sobrevivir".
- **Ultra (2 minutos):** máxima puntuación en tiempo fijo. Reutiliza todo el scoring de v0.4; agrega solo reloj y fin por tiempo.
- **Zen (infinito):** sin game over - el stack se limpia al tocar el techo. Para practicar T-spins sin presión.
- *Por qué acá:* reutilizan el core intacto; son modos, no reglas nuevas. El riesgo es de UI (selección de modo), no de simulación.

### I2 - Estadísticas de partida
PPS (puntos por segundo), T-spins por partida, mejor combo, duración. Solución: objeto `stats` acumulado en el core (lógica pura, testeable) + panel en el HUD. Aporta la sensación de mejora medible que hace que uno vuelva.

### I3 - Tabla de high scores
Top 5 local con fecha y modo (hoy hay un solo récord). localStorage + panel. Sensación de progresión.

### I4 - Daily challenge con semilla del día
Semilla derivada de la fecha -> `rng` inyectable ya existe; leaderboard local del día. Rejugable y comparable entre amigos, sin backend.

### I5 - Input de guideline completo
- Rotación en ambas direcciones (Z / X), como la guideline moderna.
- Accesibilidad de input: remapear teclas. La base ya distingue intenciones del core del mapeo del teclado, así que el remapeo es solo configuración.

## Presentación

### I6 - Temas visuales
`src/themes.js`: paleta por pieza + colores de UI, 3-4 presets (clásico oscuro, CRT, neón, papel), persistido. Riesgo bajo: render puro.

### I7 - Efectos avanzados
Trail de la pieza, líneas que cruzan el tablero en un tetris, partículas con física. La línea entre "brilla" y "cansa" es fina: prototipar y decidir en browser.

### I8 - Música
Loop generativo con Web Audio (Korobeiniki sintetizado o acordes que siguen el nivel). Riesgo: es la feature más subjetiva de todas. Prototipo corto y decisión tuya.

### I9 - Replays
Guardar la secuencia de inputs + semilla -> replay determinista (el core ya lo es). Compartible como texto/URL. Es la feature más alineada con el origen del proyecto: la demostración perfecta de que la simulación es determinista.

### I10 - PWA + móvil
Manifest + service worker (instalable, offline) + controles touch (swipe = move, tap = rotate, swipe down = soft/hard drop). **Es el hueco más grande que queda: hoy el juego no es jugable en el teléfono.**

## Meta / portfolio

### I11 - El post del pipeline
"Cómo construí un Tetris con agentes" - metodología, hallazgos, mutación, la regla del blur. La pieza de portfolio de más apalancamiento. Requiere sanitizar las 3 menciones de "Gonzo" del BRIEF antes de publicar.

### I12 - Bot jugador
Un bot sobre el core puro (misma API `createGame`): heurística de evaluación de posiciones o búsqueda simple. Demuestra que el core es lo bastante limpio para ser conducido, y es un demo encantador.

### I13 - Multiplayer local
Dos tableros, un teclado (o dos ventanas sincronizadas). Riesgo: rompe la suposición "una partida, un estado" del core. Factible como instancias separadas; el garbage cruzado es el cambio real de diseño.

### I14 - PWA instalable + integración de sistema
Ícono, ventana propia, atajo. Capa final de "se siente app".

## Descartadas (con la razón, para no re-proponerlas)
- **Multiplayer online:** backend + matchmaking, contradice cero-dependencias. Si hay multiplayer, es local (I13).
- **Build step / TypeScript:** contradice el espíritu módulos ES nativos. JSDoc si algún día hace falta.
- **Canvas con librerías (PixiJS, etc.):** el canvas puro ya alcanza y es parte del encanto.