# Clase: Godot Game Development for Beginners — plataforma 2D completa

- Fuente: https://www.youtube.com/watch?v=MiPkcTaRbfQ
- Canal: freeCodeCamp.org
- Expositoras: **Sarah** (California) y **Reem** (Nueva York), estudiantes de **Hack Club**
- Publicado: 2025-09-10
- Duración: 57:59 (3.479 s)
- Idioma: inglés · Motor: **Godot** (última estable en godotengine.org al momento del video)
- Transcript: [transcripcion.md](transcripcion.md) — 1.394 bloques normalizados, 7.394 palabras
- Metadata: [video-meta.json](video-meta.json) — capítulos oficiales de la descripción

## Qué es esta clase

Un tutorial **completo y corto** de un plataformas 2D: desde descargar el motor hasta publicar el juego en itch.io. No enseña teoría de motores ni diseño de juego; construye **un juego entero, jugable**, en 58 minutos, cometiendo y corrigiendo errores en vivo.

Eso es su mayor valor y su mayor límite a la vez:

- **Valor:** el recorrido es real. Todo lo que hace falta para que un principiante tenga un juego publicado aparece, y en el orden en que aparece en la práctica. Los errores en cámara (el jugador atraviesa el piso, la plataforma no se anima sola) son los mismos que uno comete, y la corrección se ve.
- **Límite:** no hay arquitectura, no hay tests, no hay manejo de estado entre escenas, no hay audio más allá de lo que quede. Es un **vertical slice**, no un curso de ingeniería de juegos. Quien quiera hacer un juego grande va a necesitar otra cosa.

## Resultado esperado

Al terminar la clase, sin saltarse bloques:

1. Un proyecto de Godot con **autotiling** (tiles con física y *terrains*) usable como base para cualquier plataforma 2D.
2. Un **personaje con FSM mínima** (idle / run) dirigido por input, con cámara que lo sigue.
3. Un **sistema de checkpoints y muerte** con una regla única y reutilizable: la zona de muerte reubica al jugador en el último checkpoint, no lo reinicia.
4. **Enemigos** con zona de visión (`Area2D` circular) que persiguen al jugador cuando entra y lo dejan ir cuando sale.
5. **HUD** con puntaje y tiempo, **coleccionables** que suman puntos y desaparecen, **plataformas móviles** sobre `Path2D`.
6. **Dos niveles encadenados** por un nodo de "siguiente nivel" que resuelve la ruta de la escena en tiempo de ejecución.
7. El juego **exportado en HTML y publicado en itch.io**, jugable en el navegador.

## Cómo estudiar esta clase

El video es una sola corrida sin pausas naturales. Para trabajarlo conviene partirlo en **cuatro sesiones** en lugar de mirarlo de una sentada:

| Sesión | Tramo | Qué se lleva |
|---|---|---|
| 1 | 00:00 – 11:51 | Motor, tilemap, autotiling, jugador, input, cámara. **El juego se puede jugar.** |
| 2 | 11:52 – 20:41 | Checkpoints, muerte, obstáculos. **El juego tiene reglas.** |
| 3 | 20:42 – 33:38 | Fondo parallax, animaciones, plataformas móviles. **El juego se ve como un juego.** |
| 4 | 33:39 – 57:59 | Enemigos, puntaje, coleccionables, niveles, export. **El juego es un juego.** |

Cada sesión termina con una compilación posible. Ninguna tarea queda a medias.

---

## Módulo 1 — Instalar Godot y crear el proyecto (00:00 – 02:06)

### Objetivo

Tener el motor instalado y el proyecto vacío creado, sin tocar todavía nada del juego.

### Contenido

- Qué es Godot: «Godot is a free open-source game engine that helps you build 2D and 3D games» (00:01:04).
- Descarga desde `godotengine.org`, descompresión del `.zip` y ejecución del primer `.exe` (00:01:14 – 00:01:37).
- En Windows, el paquete trae dos ejecutables: el del **project manager** y el del editor. Se corre el primero.
- Creación del proyecto desde el project manager con un nombre arbitrario (00:01:47).

### Lo que el video no dice

- No menciona que la versión del motor fija la sintaxis: los nodos `TileMapLayer` y `Parallax2D` que usa después son de **Godot 4.3+**. Un proyecto abierto con un Godot 4.0 no tiene esos nodos con ese nombre.
- No explica por qué hay dos ejecutables ni cuál conviene instalar (el video asume Windows; en macOS es un solo `.app`, en Linux el binario del editor).

### Ejercicio

Instalar Godot, crear el proyecto y anotar **qué versión exacta** quedó instalada (menú *Ayuda → Acerca de*). Ese número va a explicar la mitad de los problemas de los módulos siguientes.

---

## Módulo 2 — Tilemaps, autotiling y física de tiles (02:07 – 07:53)

Este es el módulo más denso del curso en relación a su duración: en menos de seis minutos pasan por atlas, tamaño de tile, capas de física y terrain sets.

### Objetivo

Un mapa dibujable que el jugador **pueda pisar**, sin volver a elegir tiles a mano cada vez.

### Contenido, en orden

1. **Traer el arte.** El repositorio de arte se descarga como `.zip` y se arrastra el contenido a la carpeta del proyecto (02:07 – 03:15). Esto deja los PNG visibles en el *FileSystem* del editor.
2. **La escena y el nodo.** Escena 2D nueva, `TileMapLayer` como hijo (03:17 – 03:23).
3. **El TileSet.** En el inspector el tileset «currently says empty» (00:03:42); se crea uno nuevo y se agrega un **atlas** desde el PNG (03:58). Un *atlas* es una sola imagen con muchos tiles; el editor la corta por grilla.
4. **El tamaño.** Los tiles se ven demasiado chicos porque el proyecto no sabe cuánto mide cada celda: se ajusta a **32×32** en el TileSet y se repite el `texture region` del atlas a 32×32 (04:23 – 04:54). *Los dos ajustes son necesarios y son dos lugares distintos*: uno dice cuánto mide una celda en el mundo, el otro cómo se recorta la imagen.
5. **Física por tile.** Para que un tile sea sólido se le asigna una **physics layer** (05:08 – 05:21) y después se pinta cada tile con la tecla `F`; «when it's shaded in red, you'll know that your tile has officially become a solid» (00:05:33).
6. **Selección múltiple.** «To select multiple tiles, I'll hold shift and drag my mouse over all of the tiles» (00:05:50) y después `F` una sola vez: los 20 tiles quedan sólidos.
7. **Terrain sets (autotiling).** El problema motivador: para dibujar una forma básica hay que volver a elegir tile por tile, y «this can get really tedious really quickly» (00:06:25). La solución: crear un *terrain set* con un *terrain* adentro (06:36), pintar en cada tile su patrón de vecindad — «a grid-like pattern that looks like this» (00:07:05) — y desde ese momento dibujar rellena solo «it'll just fill it in for itself» (00:07:24).
8. **Guardar como escena principal.** Guardar la escena y renombrar el nodo raíz a `main`; al correr el juego por primera vez Godot pide la escena principal y se elige la actual (07:34 – 07:51).

### La idea que hay que llevarse

**El autotiling no es una comodidad, es un contrato.** Al pintar el patrón de vecindad en cada tile, uno le está diciendo al mapa *qué forma tiene el tile en cada contexto*, y desde ahí el editor puede decidir qué tile poner en una esquina, un borde o un centro. Si el mapa se ve roto al dibujar, el error está casi siempre en el patrón, no en el dibujo.

### Lo que el video no dice

- No explica **qué significa cada una de las 16 combinaciones** del patrón de vecindad. Es el punto donde más gente se traba, y acá se ve pintar el patrón sin explicar el criterio.
- No menciona las **capas de colisión** (*collision layers/masks*): todo tile sólido choca con todo. Sirve para el tutorial; no sirve cuando hay enemigos que atraviesan paredes.

### Ejercicio

Dibujar un nivel de 20×10 celdas con autotiling y **romperlo a propósito**: borrar un tile del centro de un bloque para ver qué decide el terrain. Documentar qué pasó y qué patrón faltaba.

---

## Módulo 3 — El jugador: cuerpo, colisión, input y cámara (07:54 – 11:51)

### Objetivo

Un personaje que se mueve con el teclado, salta, choca con los tiles y tiene la cámara encima.

### Contenido

- Nodo `CharacterBody2D` renombrado `player`, con `CollisionShape2D` rectangular e `Sprite2D` con el `icon.svg` del proyecto (07:54 – 08:40).
- Script adjunto al `player`. El template de Godot no apareció; la expositora lo trae de su repo (08:44 – 08:57).
- Guardado como `player.tscn` e instanciado en la escena principal (09:03 – 09:19).
- **El primer error, en cámara:** «we can see that our player fell through» (00:09:22). Causa: «our player does not have a shape» (00:09:27) — el `CollisionShape2D` había quedado bajo un `Area2D` en lugar del cuerpo. Corregido, el jugador pisa el mapa.
- **El input map.** El personaje no se mueve porque el proyecto no sabe qué teclas son "izquierda" o "derecha": se configuran en *Project Settings → Input Map* con `A`, `D` y espacio (09:46 – 10:16). «what we want um» (00:09:54).
- **La cámara.** `Camera2D` como hijo del jugador con un script que, en cada frame, copia la posición global del jugador — «we're going to say our global position» (00:10:54). Sin `offset` ni suavizado.
- **Ajuste de "feel".** Si el salto no llega o es demasiado alto, se cambia el número en el script y se vuelve a correr (11:11 – 11:36).

### La idea que hay que llevarse

**El error del piso es el mejor contenido del módulo.** El jugador atravesó el mapa no porque el código estuviera mal, sino porque el nodo físico no tenía forma. En Godot, un `CharacterBody2D` sin `CollisionShape2D` es un cuerpo sin volumen: la física no lo detiene. La jerarquía correcta (`CharacterBody2D` → `CollisionShape2D`) **es** el contrato.

### Lo que el video no dice

- La cámara copia la posición **en `_process`**, no en `_physics_process`: en un juego con plataformas móviles eso produce jitter (el problema aparece, de hecho, en el Módulo 6 con las plataformas).
- No se usa `Camera2D` con sus *drag margins* ni *position smoothing*, que resuelven el mismo problema en el editor sin script.
- No se habla de **delta**: el movimiento del player no se multiplica por el tiempo transcurrido. En el tutorial funciona porque la máquina es rápida; en una compilación web (Módulo 9) la velocidad cambia según el equipo.

### Ejercicio

Cambiar la cámara a `Camera2D` con *position smoothing* y *drag margins* activados, borrando el script. Correr el juego y comparar: ¿se nota la diferencia en un tramo recto y en uno con plataformas?

---

## Módulo 4 — Checkpoints y muerte (11:52 – 19:06)

El bloque más largo de la primera mitad (7 minutos y medio) y el que introduce el patrón de arquitectura del curso: **un manager con un solo dato compartido.**

### Objetivo

Que caerse tenga una consecuencia, y que la consecuencia sea **volver al último checkpoint**, no reiniciar el juego.

### Contenido

1. **`CheckpointManager`** — un `Node2D` en la escena principal con un script que guarda una sola variable: `last_location`. En `_ready` la inicializa con la posición del jugador (12:02 – 13:02). «This is the built-in Godot function that runs the first time your game loads up» (00:12:48).
2. **`Checkpoint`** — un `Area2D` con `CollisionShape2D` y un `Marker2D`, convertido en escena guardada (`checkpoint.tscn`). Su script busca el manager subiendo por la jerarquía de padres dos veces y bajando por nombre (13:23 – 15:19). Se conecta la señal `body_entered` (14:16 – 14:25).
3. **La condición única:** «we're going to check if the body is equal to our player» (00:14:36). Si entra cualquier otra cosa, no pasa nada.
4. **El punto de reaparición no es el checkpoint, es su `Marker2D`:** `last_location` se guarda como la posición global del **marker** (00:15:11), no del área. Así el checkpoint se dibuja donde conviene y el jugador reaparece un poco más adelante.
5. **`DeathZone`** — otro `Area2D` con forma rectangular. Cuando entra el jugador, llama a `kill_player()`, que reposiciona al jugador en `checkpoint_manager.last_location` (15:23 – 17:37). Probado: «when you go over here, it'll kill you» (00:18:29).
6. **Reutilización por escena:** la muerte no se dibuja con tiles manuales, se arrastra la escena `death_zone` a la *Scene Collection* del tilemap y se pinta con ella. «Our death zones are also really easy to reuse» (00:18:58). Ese es el truco de nivel del módulo: una zona de muerte pintable como si fuera un tile.

### La idea que hay que llevarse

**El patrón `manager` + `dato único` + `referencia por jerarquía`** se repite en todo el curso: enemigos, HUD, coleccionables. Es simple, funciona, y tiene un costo explícito: `get_parent().get_parent()` acopla cada nodo a una **profundidad fija** en la escena. Mover el checkpoint un nivel arriba rompe el script sin ningún error de compilación — el juego se cae en tiempo de ejecución.

### Preguntas que el video abre y no responde

- ¿Qué pasa si el jugador cae en una zona de muerte **antes** de tocar el primer checkpoint? Reaparece en la posición inicial del manager, que sí está definida. Funciona, pero por accidente.
- ¿Qué pasa con el puntaje y el tiempo al morir? No se resetean: el HUD (Módulo 7) sigue corriendo. Al principio no importa; cuando hay juego acumulado, sí.
- ¿Qué pasa si se pinta una zona de muerte como tile **del mapa** en vez de instanciar la escena? El `Area2D` de la escena no es un tile de física: el tilemap pinta *texturas + formas de física*, no comportamientos. La exposición muestra las dos cosas mezcladas («go to tile map and start drawing with them», 00:19:02) sin distinguir cuál es cuál. **Es un punto oscuro del video.**

### Ejercicio

Hacer que la muerte **también** reste puntos del HUD y mueva al jugador al checkpoint. Después, dibujar una zona de muerte con el *pincel de escena* del tilemap y verificar en el árbol de la escena si quedó el `Area2D`. Documentar la diferencia entre las dos cosas.

---

## Módulo 5 — Obstáculos (19:07 – 20:41)

### Objetivo

Un objeto con el que el jugador choca y no puede atravesar.

### Contenido

- Escena nueva con `StaticBody2D` como raíz, `CollisionShape2D` circular «the same size as my sun» (00:19:23) y un `Sprite2D` con la textura (19:20 – 19:56).
- Renombrado `obstacle` y guardado, instanciado en la escena principal (20:07 – 20:33).
- Verificación: «my character cannot go past the obstacle» (00:20:38).

### La idea que hay que llevarse

**`StaticBody2D` es para lo que nunca se mueve.** Un obstáculo, una pared, un techo. Si algo se va a mover (una plataforma, una puerta), va con `AnimatableBody2D` o `CharacterBody2D`, no con `StaticBody2D`: la física estática no actualiza su transformación por animación.

### Ejercicio

Convertir el obstáculo en algo que **sí** se mueve (por ejemplo, una puerta que abre con una animación de rotación). Elegir el nodo correcto para que el jugador no lo atraviese y explicar por qué `StaticBody2D` no habría funcionado.

---

## Módulo 6 — Fondo parallax y plataformas móviles (20:42 – 33:38)

El módulo más largo del curso después de los enemigos. Tres cosas diferentes conviven: fondo, animaciones del jugador y plataforma móvil.

### Objetivo

Que el juego deje de verse como un rectángulo de colores y empiece a tener profundidad y movimiento.

### Contenido

**Fondo (20:42 – 23:33)**

- `ParallaxBackground` (mencionado como «parallax background», 00:21:00) con `Parallax2D` adentro, a 1600×900 — el tamaño del arte.
- El arte se alinea contra un rectángulo violeta que marca el **borde de repetición** del fondo: cuando la cámara llega a ese borde, la imagen tiene que continuar. «That's how our screen's going to loop» (00:21:48).
- El `Sprite2D` del fondo debe ser **hijo** del nodo de parallax (00:21:54), no hermano, o no se mueve con la cámara.
- Se amplía el tilemap del nivel (22:41 – 23:10) y el fondo se ajusta verticalmente (23:23 – 23:33).

**Animaciones del jugador (23:34 – 27:58)**

- `AnimationPlayer` + `AnimatedSprite2D` bajo el jugador (23:44).
- *SpriteFrames* desde un spritesheet con tiles de **32×32** (24:13 – 24:34).
- **El detalle que arruina el arte pixelado:** «the art is a little blurry» (00:24:44) → textura en filtro **nearest** (24:47).
- **La lógica de animación** va en el `_process` del jugador, no en el `AnimationPlayer`: si hay dirección de input, se reproduce `run`; si no, `idle` (00:25:48: «which would be if you have an input»). Y si la dirección es a la izquierda: «flip horizontal is equal to» (00:27:36) el sprite se espeja.

**Plataformas móviles (33:39 → en realidad 28:14 – 31:53)**

- `Path2D` con dos puntos → `PathFollow2D` → `AnimatableBody2D` (el ASR dice «animated ball body», 00:28:55) → `RemoteTransform2D`, `CollisionShape2D` y `AnimationPlayer`.
- La animación `movement` keyframea el **`progress_ratio`** del `PathFollow2D`: «this is just tracking the progress of our platformer along this path» (00:30:55).
- Se marca **`local_to_scene`** en el `PathFollow2D`: sin eso, cada instancia comparte la ruta y mover una mueve todas (00:30:12 – 00:30:23). El video lo dice de pasada; es el bug más común de plataformas móviles.
- El rebote se logra con el modo *loop* de la animación («bounce back», 00:31:35 – 00:31:42).
- **El segundo error, en cámara:** la plataforma se mueve en el editor pero no en el juego (00:32:30). Causa: la animación no arranca sola. Se agrega un script con `_ready` que llama a `animation_player.play("movement")` (32:39 – 33:12).

### La idea que hay que llevarse

**`local_to_scene` y el `play` inicial son el mismo error con dos máscaras:** el video asume que una escena instanciada "se acuerda" de su configuración y de su estado inicial. No lo hace. Los recursos compartidos necesitan `local_to_scene`, y las animaciones necesitan un `_ready` que las dispare. Es un patrón que se repite en cualquier escena reutilizable de Godot.

### Lo que el video no dice

- No menciona que `RemoteTransform2D` es lo que hace que el `AnimatableBody2D` (o su colisión) **siga** al `PathFollow2D`. Se agrega sin explicar por qué.
- El `AnimationPlayer` de la plataforma y el de las animaciones del jugador son el mismo tipo de nodo con propósitos distintos; el video no hace la distinción explícita.

### Ejercicio

Duplicar la plataforma móvil tres veces y mover cada una. Después **borrar** `local_to_scene` y documentar exactamente qué se rompe. Volver a activarlo.

---

## Módulo 7 — Enemigos con zona de visión (33:39 – 39:27)

### Objetivo

Un enemigo que persigue al jugador cuando entra en su radio de visión y lo deja ir cuando sale.

### Contenido

1. Escena `CharacterBody2D` con `CollisionShape2D` circular («a little smaller than», 00:34:27), `Area2D` para la visión y `Sprite2D` en filtro nearest (33:38 – 34:58).
2. **La regla de la visual:** el `CollisionShape2D` del cuerpo se hace *más chico* que el sprite, y el `Area2D` circular es «the enemy's vision zone» (00:34:44). Un choque del cuerpo con un radio mayor que el visual es un hitbox mentiroso.
3. Señales `body_entered` y `body_exited` sobre el `Area2D` (35:35 – 35:44).
4. Variables: `speed = 200`, `player` (referencia al jugador de la escena principal), y un booleano `follow`: «whenever the player enters, that boolean will be true... and whenever the player leaves, that boolean will be false» (00:36:42 – 00:37:00).
5. La lógica en `_physics_process`: mover siempre con `move_and_slide()` — «this is just how Godot» (00:37:05) — y, si `follow`, decidir la dirección por **comparación de coordenadas X**: «that means our player is in the left» (00:38:00) → `velocity.x = -speed`; si está a la derecha, `+speed`.
6. **La gravedad:** «our enemy is floating» (00:38:39). El cuerpo flotaba porque no se le aplicaba gravedad. Se corrige con un `if not is_on_floor(): velocity.y += gravity * delta` (00:38:49 – 00:39:07).
7. La velocidad se puede bajar para que el juego sea más fácil (39:19 – 39:27).

### La idea que hay que llevarse

**Un enemigo que persigue es una máquina de dos estados y la escena ya la implementa sin una FSM explícita.** `follow` es el estado; `body_entered` / `body_exited` son las transiciones; la posición del jugador es la señal que decide la dirección. Reconocer ese patrón permite agregar un tercer estado (huir, atacar, patrullar) sin reescribir nada: una variable más y un `if` más.

### Lo que el video no dice

- El enemigo **atraviesa las paredes**: usa `move_and_slide()` con velocidad horizontal constante, sin pathfinding ni colisión de navegación. Para un nivel abierto funciona; en un nivel con obstáculos, el enemigo se queda pegado.
- No hay animación del enemigo: el sprite es estático aunque se mueva.
- La comparación por X es solo **horizontal**. Un enemigo no puede saltar, así que un jugador en una plataforma arriba está fuera de su alcance para siempre.

### Ejercicio

Agregar un estado **`patrol`** al enemigo cuando no ve al jugador: que se mueva entre dos puntos hasta que `follow` sea verdadero, y que vuelva a patrullar cuando deja de verlo. Un booleano más y un `if` más.

---

## Módulo 8 — Puntaje, tiempo y coleccionables (39:28 – 45:54)

### Objetivo

Un HUD que muestre puntaje y tiempo, y objetos que sumen puntos y desaparezcan.

### Contenido

1. **HUD** — `CanvasLayer` (que ignora la cámara y se dibuja siempre encima) con dos `Label`: `score` y `time` (00:39:38 – 39:40). Los labels se anclan en la esquina superior derecha y arriba (40:09 – 40:19).
2. Script del HUD con `time` y `score` en cero, referencias a los dos labels con `@onready` (40:39 – 40:58) y dos funciones `update_time()` / `update_score()`. La de puntaje asigna `"Score: " + str(score)` (00:41:26).
3. **El tiempo** no es un acumulador: es `Time.get_ticks_msec() / 1000.0` — milisegundos desde que arrancó el proceso, dividido por 1000. El ASR lo deforma («time.get_fixed in the second by then thousand», 00:42:07); la llamada real es `Time.get_ticks_msec()`.
4. **Por qué el HUD no mostraba nada:** las funciones existían pero nadie las llamaba desde `_process` (00:42:35 – 00:42:44). Al llamarlas, el tiempo sube y el score también.
5. **El bug de raíz:** «our score isn't actually updating» (00:42:51). El `update_score()` multiplica un valor que nunca cambia. Se resuelve en el paso siguiente.
6. **Coleccionables** — `Area2D` con `CollisionShape2D` rectangular y sprite `moon.png` en nearest (43:02 – 43:42). Señal `body_entered` (00:44:01 – 44:09). Si el cuerpo es el jugador: suma `50` puntos al HUD (`HUD.score += 50`) y se elimina con `queue_free()` (00:45:18). Verificado: el coleccionable desaparece y el puntaje sube (00:45:43 – 00:45:48).

### La idea que hay que llevarse

**El HUD es un nodo independiente que el resto del juego toca a través de una variable.** El coleccionable no dibuja un número: incrementa `HUD.score`, y el HUD se refresca en su propio `_process`. Ese desacople es correcto, y es más sano que el patrón `manager` del Módulo 4: no hay `get_parent().get_parent()`, hay una referencia por nombre de nodo.

También es la **deuda** del módulo: `HUD` se busca por nombre desde el coleccionable sin verificarse, y si el HUD no existe, el juego tira `null` en tiempo de ejecución.

### Lo que el video no dice

- El tiempo que se muestra es **el uptime del proceso**, no el tiempo de partida. Si el juego pausa o el navegador congela la pestaña, el contador sigue corriendo. Para un cronómetro real hace falta acumular con `delta` mientras el juego está activo.
- No se resetea el puntaje entre niveles (Módulo 9): el HUD se instancia por nivel y el valor **se pierde** al cambiar de escena. Funciona de casualidad porque cada nivel tiene su propio HUD.
- No hay audio ni feedback visual al recoger: el objeto desaparece sin más.

### Ejercicio

Convertir el tiempo del HUD en un cronómetro que **acumule `delta` solo mientras el juego se está jugando** (no uptime). Correr los dos y comparar: abrir el juego, esperar 10 s sin moverse, mirar el número.

---

## Módulo 9 — Niveles y cambio de escena (45:55 – 54:49)

El módulo donde el tutorial deja de ser "un nivel" y se vuelve "un juego". También el más frágil técnicamente.

### Objetivo

Dos niveles navegables, con un nodo de paso que lleva del uno al dos, sin duplicar trabajo.

### Contenido

1. **Reestructuración.** Carpeta `levels/` y dos escenas nuevas, `level_one` y `level_two` (45:55 – 46:39). «This will require a little bit of restructuring» (00:46:07).
2. **El nodo `next_level`.** `Area2D` con el sprite del sol y `CollisionShape2D`, con señal `body_entered` (47:03 – 47:48). El video propone hacer el propio arte: «would be a very cool challenge for you guys to make your own art» (00:46:52).
3. **Resolución de la ruta en runtime:**
   - `get_tree().current_scene.scene_file_path` (00:48:19) devuelve la ruta de la escena actual — se imprime para comprobarlo (48:25 – 48:54).
   - La escena principal deja de ser la del juego y pasa a ser el **project manager del editor**: ahora hay que correr "escena actual" desde `level_one`, no "proyecto".
   - El número del nivel sale del nombre del archivo: se incrementa con un parseo del path y se arma `str(number + ...) + ".tscn"` (52:57 – 53:08).
   - El cambio de escena es `get_tree().change_scene_to_file(next_scene)` con el string correspondiente (53:44 – 54:38).
4. **La duplicación inevitable.** El tilemap se exporta como escena propia (`tile_map.tscn`) para no rehacerlo entre niveles (49:46 – 51:28); el resto (jugador, HUD, próximo nivel) se **arrastra a mano** a cada nivel. «You can just copy this over into level two» (00:52:12).
5. **Verificación:** recorrer el nivel uno, tocar el sol y aterrizar en el nivel dos.

### La idea que hay que llevarse

**El nivel es una escena, no una carpeta de datos.** Eso hace que el cambio de nivel sea barato (el motor libera y carga árboles completos) y caro al mismo tiempo (todo lo que vive en una escena se recrea en la siguiente: puntaje, estado del jugador, checkpoints). El tutorial elige esa decisión implícitamente y no la discute.

### Lo que el video no dice

- El parseo del nombre del archivo es **frágil por diseño**: renombrar `level_one.tscn` a `level1.tscn` o meter un nivel en `levels/old/` rompe la aritmética sin aviso. Es la primera cosa que conviene cambiar si el curso se usa como base real.
- No hay **autoload** (singleton) para el puntaje ni el estado del jugador. El patrón `CanvasLayer` del Módulo 8 pierde su valor al cambiar de escena.
- «Only one level» (00:45:53) es literal: hay dos escenas pero el video no pide crear un tercer nivel ni un menú.
- No hay transición (fade) ni carga asíncrona.

### Ejercicio

Reemplazar el parseo del nombre por un **`@export var next_level_path: String`** en el nodo, configurable por escena. Después renombrar `level_one.tscn` a `nivel_uno.tscn` y verificar que el juego sigue funcionando sin tocar código.

---

## Módulo 10 — Export y publicación en itch.io (54:50 – 57:59)

### Objetivo

El juego jugable en el navegador, publicado.

### Contenido

1. *Editor → Manage Export Templates* (00:55:14): se descarga e instala el paquete de plantillas (tarda). Sin plantillas no hay export.
2. Exportar el proyecto con preset **Web**, generando `index.html` y los archivos asociados.
3. Comprimir esos archivos en un `.zip` — el nombre del zip es indiferente (00:55:46).
4. En itch.io: *Upload new project*, tipo de proyecto **HTML** (00:56:03), subir el zip.
5. **El detalle que confunde a todos:** después de la primera publicación el proyecto queda **privado**; hay que volver a editarlo y marcarlo público. «There's nothing wrong with your computer, that's just how it works» (00:56:15 – 00:56:25).
6. Verificar que corre en el navegador (56:45 – 57:00).

### La idea que hay que llevarse

**Exportar no es compilar: es empacar un runtime.** El template es el motor ya compilado para la plataforma destino; el zip es `index.html` + el motor + los assets. Ese paquete es lo que itch.io sirve. Si falla, casi siempre falta el template o el preset no es *Web*.

### Lo que el video no dice

- El soporte de **WebAssembly en itch.io** tiene requisitos de *headers* (COOP/COEP) que itch.io resuelve por su lado; en otros hosting, no. Si se publica en GitHub Pages, el juego puede no arrancar.
- No se menciona el peso del build ni que el primer load puede tardar treintena de segundos en conexiones lentas.
- No hay **control de versiones del build**: cada export pisa el anterior y no queda rastro de qué se subió.

### Ejercicio

Exportar el juego y **publicarlo fuera de itch.io**, por ejemplo en GitHub Pages. ¿Arranca sin tocar headers? ¿Qué cambia? Documentar con captura del error o de la consola.

---

## Cierre — qué queda de la clase

### Lo que el curso enseña bien

1. **El circuito completo de un juego:** motor, arte, jugabilidad, publicación. En 58 minutos.
2. **El autotiling como productividad:** cómo un patrón pintado una vez ahorra horas de dibujo manual.
3. **La composición de escenas:** un cuerpo, una zona, un manager, una plataforma. Cada cosa es una escena reutilizable.
4. **El error como material:** cada bug en cámara se explica y se corrige. Es más útil que el código final.

### Lo que el curso deja afuera (y hay que cubrir aparte)

| Tema | Por qué falta | Dónde cubrirlo |
|---|---|---|
| **`delta` / framerate-independence** | El movimiento es por frame, no por segundo | Docs de Godot: *Using delta* |
| **Autoloads / singletons** | Todo el estado vive en la escena | Docs: *Singletons (Autoload)* |
| **`@export` y datos de escena** | El cambio de nivel es aritmético sobre nombres de archivo | Docs: *GDScript exports* |
| **Collision layers / masks** | Un solo grupo de física para todo | Docs: *Collision layers and masks* |
| **Test y separación lógica/vista** | El tutorial es todo vista | `projects/reinos-de-la-frontera/` (simulación headless por tick) |
| **Audio** | No existe en el curso | — |
| **Guardado de partida** | No existe | — |

### Banco de preguntas

1. ¿Por qué el jugador atravesó el piso en el Módulo 3, y qué nodo faltaba exactamente?
2. ¿Cuáles son los **dos** lugares donde se configura el tamaño de 32×32 de un tile, y por qué son dos?
3. ¿Qué hace `local_to_scene` en el `PathFollow2D` de la plataforma móvil, y qué se rompe si se desactiva?
4. El HUD no mostraba nada aunque las funciones existían: ¿qué faltaba llamar, y desde dónde?
5. ¿Por qué el enemigo flotaba, y qué condición del `_physics_process` lo resolvió?
6. En el Módulo 4, ¿qué pasa si el jugador cae antes de tocar el primer checkpoint?
7. ¿Por qué el nodo `next_level` resuelve la ruta del siguiente nivel en runtime en vez de tenerla configurada?
8. ¿Qué nodo usarías para un obstáculo que se mueve, y por qué `StaticBody2D` no sirve?
9. ¿Qué diferencia hay entre los tiles con física del Módulo 2 y el `Area2D` de la zona de muerte del Módulo 4?
10. Después de publicar en itch.io, el juego queda privado. ¿Qué hay que hacer, y por qué?

---

*Clase montada el 2026-11-11 desde los subtítulos automáticos del video (1.394 bloques). Los timestamps de cada cita se verificaron contra el transcript con un barrido de coincidencia literal.*

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
