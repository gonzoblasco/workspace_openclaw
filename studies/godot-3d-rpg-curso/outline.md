# Clase: Godot GameDev Tutorial – 3D RPG Game

- Fuente: https://www.youtube.com/watch?v=ouqgx1qKSdY
- Canal: freeCodeCamp.org
- Expositor: Omar (@CodingQuests). **Invitado:** Lelu (@Le_x_Lu) enseña los VFX (4:31:46 – 5:11:13)
- Publicado: 2024-06-20
- Duración: 5:30:06 (19.806 s)
- Idioma: inglés · Motor: **Godot 4.3** (beta en el momento de grabar; estable era 4.2)
- Transcripción: [transcripcion.md](transcripcion.md) — 7.239 cues
- Curso original: <https://www.codingquests.com/challenge-page/3drpgcourse>
- Proyecto: [starter](https://codingquests.com/3dstarterfiles) · [final](https://codingquests.com/3drpgfiles)

## Resultado esperado

Al terminar el curso:

1. **Montar un nivel con `GridMap`** entendiendo por qué el *mesh library* se construye como escena aparte y no como recurso directo.
2. **Construir un controlador de personaje en tercera persona** con `SpringArm3D`, rotación desacoplada (horizontal/vertical), movimiento relativo a la cámara y `move_and_slide`.
3. **Modelar el estado con dos mecanismos distintos y saber cuándo va cada uno**: `AnimationTree` con condiciones (player) y una **FSM en código** con nodos por estado (monstruo).
4. **Hacer que la animación dispare la lógica**, no al revés: `call_method` tracks habilitando/deshabilitando el `Area3D` del arma en el frame exacto del golpe.
5. **Construir un sistema de inventario dirigido por recursos** (`Resource` como `ItemData`, `@export` para tipar slots) con un nodo propio reusable (`class_name InventorySlot extends PanelContainer`).
6. **Centralizar la economía del juego y el HUD** en un autoload `Game` con señales custom (`health_changed`, `level_up`) en vez de referencias cruzadas.
7. **Leer y escribir shaders de partículas** en Godot: `ParticleProcessMaterial`, `VisualShader` y curvas de escala/color para aura y puff.
8. **Spawnear entidades sobre una grilla validando la celda**, en lugar de lanzar el spawn a ciegas.

## Mapa temporal

39 capítulos oficiales de la descripción. Cada módulo agrupa capítulos contiguos.

| Tiempo | Capítulo oficial | Módulo |
|---|---|---|
| 0:00:00 | Intro | 0 |
| 0:02:14 | Starting The Project | 0 |
| 0:05:46 | GridMap | 1 |
| 0:15:29 | World Environment | 1 |
| 0:19:15 | Adding The Player | 2 |
| 0:22:26 | Camera Controller | 2 |
| 0:36:29 | Player Movement | 2 |
| 0:58:47 | Player Animation | 2 |
| 1:11:07 | Monster Setup | 3 |
| 1:14:21 | Finite State Machines Concept | 3 |
| 1:18:39 | Monster State Machine Setup | 3 |
| 1:24:50 | Monster AnimationTree | 3 |
| 1:27:59 | State Machines (código) | 4 |
| 1:36:43 | Changing States | 4 |
| 1:46:59 | Player Damaging Monsters | 5 |
| 1:57:14 | Monster Damaging Player | 5 |
| 2:04:49 | Custom Theme | 6 |
| 2:11:49 | Game Over overlay | 6 |
| 2:19:53 | GUI Setup | 6 |
| 2:28:00 | Item Resources | 7 |
| 2:39:18 | Inventory Slot | 7 |
| 2:50:39 | Inventory Item | 8 |
| 2:56:42 | Adding Items | 8 |
| 3:07:08 | Equipment and using items | 8 |
| 3:14:54 | Profile | 9 |
| 3:19:52 | Total Stats | 9 |
| 3:25:05 | Custom Health Signals | 9 |
| 3:35:49 | 3D Item Objects | 10 |
| 3:47:19 | Shop | 10 |
| 4:07:09 | Level up | 10 |
| 4:12:23 | Porting to Forward+ | 11 |
| 4:12:40 | Level Design | 11 |
| 4:18:40 | Torch | 11 |
| 4:30:36 | Lelu Intro | 12 |
| 4:31:46 | Lelu VFX Tutorial | 12 |
| 5:11:13 | Applying the VFX | 13 |
| 5:18:18 | Sound Effects | 13 |
| 5:21:27 | Spawning Monsters | 13 |
| 5:27:06 | Next Steps/Outro | 13 |

## Módulos

### Módulo 0 — Arranque y estructura del proyecto (0:00:00 – 0:05:46)

- **Objetivo:** abrir el starter y entender por qué el proyecto se organiza como se organiza antes de tocar una línea de código.
- **Contenidos:**
  - El curso son **cuatro bloques**: player, monstruo con IA, GUI (inventario/equipo/perfil/tienda) y VFX. Cita: «this course is split up into four sections» (00:00:48).
  - Godot **actualiza el proyecto automáticamente** al abrirlo con otra versión; el autor graba en 4.3 beta y avisa que la estable de ese momento es 4.2 (0:02:40).
  - El starter ya trae: `KayKit Adventurers` (personaje), `KayKit Dungeon Remastered` (escenario), `KayKit Skeletons` (monstruo), 16×16 RPG item pack, fuente pixel, VFX terminados y el tema base.
  - Cita: «the reason for that but we'll get to that later» — hay decisiones de setup que solo cierran con el sistema completo; el curso las introduce antes de explicarlas.
- **Ejercicio:** abrir el starter, importar, y anotar **qué versión de Godot** usa el proyecto tras conversión (`project.godot` → `config_version`) y qué assets faltan.

### Módulo 1 — Mundo: GridMap y WorldEnvironment (0:05:46 – 0:19:15)

- **Objetivo:** pintar un nivel en 3D con tiles y darle atmósfera de dungeon sin luces caras.
- **Contenidos:**
  - **`MeshLibrary` no se crea como recurso:** se hace en una escena 3D, arrastrando meshes, `Make Local`, borrando el nodo original, y `Create Collision Shape` sobre el mesh → `StaticBody3D > CollisionShape3D` en ese orden (0:07:10).
  - Cita: «in 3D unfortunately it's not that easy» (00:07:33) — la asimetría 2D/3D del motor, no un capricho del autor.
  - **`WorldEnvironment` sin `Environment` no hace nada**: cita «if I hit play you will see no difference» (00:15:45). Hay que asignar un `Environment` nuevo.
  - Para dungeon: background = **custom color** `(100,100,100)` en vez de negro puro, **volumetric fog** density 0.02, fog density 0.2 y light energy 0.1 (0:17:50).
  - Glow queda **apagado** a propósito: cita «we're actually not going to enable glow just leave it off for now» (00:18:51) — se necesita Forward+ y más luces en escena (ver módulo 11).
- **Ejercicio:** armar un MeshLibrary con 3 tiles (piso, pared, esquina), pintarlos con `Ctrl+F` para relleno y `S` para rotar, y medir FPS con la niebla volumétrica prendida y apagada.

### Módulo 2 — Player: cámara, movimiento y animación (0:19:15 – 1:11:07)

- **Objetivo:** tercer-persona que se sienta bien: cámara orbitando independiente del giro del personaje, movimiento relativo a cámara, y animación que refleja el estado real.
- **Cámaras — la jerarquía es el controlador:**

  ```
  Player (CharacterBody3D)
  └── CamRoot (Node3D)      ← yaw
      └── H (Node3D)        ← pitch horizontal
          └── V (Node3D)    ← pitch vertical, y=2.9 (sobre la cabeza)
              └── SpringArm3D (length=-5)   ← colisión de cámara
                  └── Camera3D (rotY=180, rotX=-10)
  ```

  - Cita: «this essentially represents my horizontal movement and this represents my vertical movement» (00:23:16).
  - El `SpringArm3D` con longitud negativa **es** el zoom: la cámara se retrae cuando hay pared entre el jugador y ella.
- **Movimiento (bloque de movimiento):**
  - `export var gravity := 9.8`, `jump_force := 9`, `walk_speed := 3`, `run_speed := 10`.
  - Cita: «the jump velocity is actually positive and the reason is because the positive is upwards» (00:25:42) — el signo de `jump_force` no es error.
  - Dirección: `Input.get_vector(...)` → `transform.basis * Vector3(dir.x, 0, dir.y)` → `normalized()`. **Se descarta `dir.z`** porque el movimiento horizontal se arma desde X/Y del input.
  - Velocidad horizontal con `velocity.x = move_toward(velocity.x, direction.x * speed, acceleration * delta)`; gravedad con `velocity.y -= gravity * delta`; cierre con `move_and_slide()`.
  - Freno: cita «this is essentially the same as setting my velocity to zero but here it's just using a function called move towards» (00:26:44).
- **Animación — `AnimationTree` con condición explícita, no automática:**
  - `AnimationNodeStateMachine` con estados `idle`, `walk`, `run`, `jump`, `attack1` (BlendTree con `TimeScale` 2×), `death`.
  - Cada transición lleva **condición propia**: `is_in_air`, `is_on_floor`, `is_walking`, `is_running`, `is_not_walking`, `is_not_running`.
  - `attack1 → idle` va con **`Switch Mode = At End`** y *sin* condición: termina sola. Cita: «we're actually going to switch it to at end and that's it» (01:03:42).
  - El jugador gira con `rotate_y` interpolado (`lerp_angle`) solo mientras se mueve; quieto, mira hacia donde apunta la cámara.
- **Ejercicio:** implementar el sprint (shift) y verificar que al soltarlo `is_running` vuelve a `false` antes de que termine la animación de correr; si queda trabado, la condición no está en la transición de vuelta.

### Módulo 3 — Monstruo: setup y el concepto de FSM (1:11:07 – 1:27:59)

- **Objetivo:** tener un esqueleto vivo y entender el patrón **antes** de escribirlo.
- **Contenidos:**
  - `CharacterBody3D` + `CollisionShape3D` (cápsula algo más ancha que el player) + script con **la plantilla recortada**: se borra el input de salto y se deja solo la gravedad. Cita: «we can just delete all this input the jump input and leave the gravity» (01:13:43).
  - **Teoría de FSM:** estados como círculos con su comportamiento adentro (`idle` → `play_idle`; `move` → `play_move`), una variable `current_state` que recuerda dónde estamos, y transiciones con condición. El ejemplo introduce un estado `attack` «que este juego no va a tener» para mostrar el patrón (1:22:30).
  - `AnimationTree` del monstruo **con transiciones automáticas apagadas** (desmarcadas una por una), porque el cambio lo decide el código, no el árbol.
  - Excepción: `attack → idle_combat` queda **automático y sincronizado al final** para que el enemigo tenga cooldown entre ataques. Cita: «so that way it's kind of like a cool down every time it attacks» (01:27:42).
- **Ejercicio:** dibujar el grafo de estados del monstruo en papel (idle, awaken, run, attack, idle_combat, death) y marcar cuáles transiciones son automáticas y cuáles las dispara código, antes de tocar el editor.

### Módulo 4 — FSM en código: nodos por estado (1:27:59 – 1:46:59)

- **Objetivo:** escribir la FSM como **clases**, no con un `match` gigante.
- **Contenidos:**
  - Cada estado es un script `extends State` con `enter()`, `update(delta)` y `physics_update(delta)`; `StateMachine` como nodo padre que llama al actual.
  - Cita: «now the question is what if I want my own signal» → `class_name State` y `class_name StateMachine` son lo que vuelve llamable al nodo desde el inspector (1:29:40).
  - El monstruo guarda `state_controller := $StateMachine` y llama `state_controller.change_state(...)` en cada transición.
  - **La detección usa `Area3D` + grupos**, no distancias: dos áreas (chase con esfera grande, attack con cilindro corto), `body_entered`/`body_exited`, y dentro del handler `if body.is_in_group("player") and not dying`.
  - Cita: «I don't want to change States unless I it's a player and if I'm not» (01:39:48) — el guard `dying` evita que un monstruo muerto vuelva a correr.
- **Ejercicio:** agregar un estado `flee` que se active cuando `health <= 1` y verificar que `change_state` no reentra en sí mismo si `body_entered` dispara dos veces en el mismo frame.

### Módulo 5 — Daño en ambos sentidos (1:46:59 – 2:04:49)

- **Objetivo:** que el golpe duele solo en el frame en que la espada pasa, y que el daño no se apile.
- **Contenidos:**
  - **El arma es un `Area3D` con `CollisionShape3D` animado:** se anima el *property track* `CollisionShape3D.enabled` en el frame de golpe, y se asegura que el track `RESET` la devuelva a `false`. Cita: «this is kind of a more accurate way of detecting for a specific frame» (02:01:19).
  - `BoneAttachment3D` con el hueso del arma, renombrado `RightHandSlot`.
  - **Invulnerabilidad por `just_hit`:** `just_hit = true` al recibir, un timer lo devuelve a `false`. Cita del bug real: «it seems that I'm Invincible now because I never connected the just hit uh timeout» (02:04:54).
  - Daño del monstruo al player: `damage_done = damage - game.player_defense`; si `damage_done > 0` resta salud; si `<= 0` mata. Es **resta plana**, no multiplicativa, y el autor avisa que la fórmula es libre (2:03:20).
- **Ejercicio:** instrumentar el `Area3D` del arma con un contador de entradas por swing; un swing sano da **una** entrada por enemigo (dos entradas = el `enabled` quedó prendido más de un frame).

### Módulo 6 — GUI: tema, game over y pausa (2:04:49 – 2:28:00)

- **Objetivo:** una capa de UI que no se rompa al pausar.
- **Contenidos:**
  - **Tema a mano con 9-patch:** `Texture2D` + `edit region` en `StyleBoxTexture`; las cuatro esquinas no se estiran, el centro sí. Cita: «that is kind of the advantage you can see that these Corners don't get stretched» (02:09:11).
  - **`CanvasLayer` como raíz de GUI**, con `process_mode = PROCESS_MODE_ALWAYS` — sin eso, pausar congela la UI y no hay forma de despausar. Cita: «otherwise I'm not going to be able to unpause my scene» (02:22:38).
  - Pausa: `get_tree().paused = not get_tree().paused`, `mouse_mode` a `VISIBLE`/`CAPTURED`, y un nodo `Container` que se muestra/oculta. La **HP bar queda fuera del container** porque se ve siempre.
  - Game over overlay reemplaza al player destruido: cita la consecuencia, «I don't have a camera 3D anymore because if you remember camera 3D is in our player» (02:05:30).
- **Ejercicio:** pausar con Escape, abrir el inventario, cerrar y despausar; si el mouse queda capturado con el panel abierto o viceversa, el `mouse_mode` se está seteando fuera del handler de pausa.

### Módulo 7 — Items como `Resource` (2:28:00 – 2:50:39)

- **Objetivo:** que un item sea un dato reusable, no un nodo ni un diccionario.
- **Contenidos:**
  - `class_name ItemData extends Resource` con `name`, `description`, `texture`, `type`, `stats`, `health`, `count`. Cita: «this is a very common one I'm just going to put it in here because it's just an example» — el esquema es del curso, no un estándar.
  - **`class_name InventorySlot extends PanelContainer`**: el nodo del slot tiene script, y así el inspector lo lista por nombre. Cita: «the coolest part about this is in my inventory here what I could do now is» (02:40:22) — se instancian slots programáticamente con `InventorySlot.new()`.
  - `@export var type: ItemData.Type` en el slot: **el mismo nodo sirve para inventario y para equipamiento** simplemente eligiendo el tipo en el inspector. Cita: «the reason we're exporting it is because now I can create equipment system using this same slot» (02:42:31).
  - La grilla se llena con `GridContainer` + `custom_minimum_size` igual al tamaño del slot.
- **Ejercicio:** crear dos `ItemData` (arma y poción) como `.tres`, poner una en el inventario y una en un slot de equipamiento, y comprobar que el mismo `InventorySlot.tscn` acepta ambos sin código extra.

### Módulo 8 — Inventario vivo: usar, equipar, contar (2:50:39 – 3:14:54)

- **Objetivo:** que clickear un item haga algo, con contador y borrado correctos.
- **Contenidos:**
  - **Item como nodo hijo del slot**: `get_child_count() > 0` es la prueba de «hay item». El `count` vive en el `ItemData` y se decrementa al usar.
  - Uso con click derecho (índice de botón, `event.button_mask == 0` = release) solo si `type == MISK`; después `queue_free()` del hijo si `count <= 0`.
  - Equipo: empareja `slot.type == item.data.type`; si es `WEAPON`, escribe `game.right_hand_equipped`. Cita: «I have this certain type of data inside of it then I'm going to fill in my right hand equipped» (03:11:44).
  - El `Game` autoload es el punto único donde vive `right_hand_equipped`, `player_health`, `player_defense`.
- **Ejercicio:** usar una poción con `count = 2` y verificar que el label baja a 1 y el nodo **no** se borra; con `count = 1` sí debe desaparecer.

### Módulo 9 — Perfil, stats totales y señales (3:14:54 – 3:35:49)

- **Objetivo:** un HUD que se actualiza solo, sin que cada actor sepa de la UI.
- **Contenidos:**
  - **Señal custom en el autoload:** `signal health_changed(amount)` y `signal level_up`; `emit_signal("health_changed", -amount)` para daño, `+amount` para curación. Cita: «when I emit the signal I'm going to pass through the negative amount the reason is because this is to heal the player» (03:28:48) — el signo *es* la semántica.
  - El que escucha es el label/barra del perfil; el player no conoce la UI.
  - **Stats totales** = base + suma de stats de equipamiento; se recalculan al equipar/desequipar, no por frame.
  - Clamp al curar: `player_health = min(player_health + amount, max_health)` para que no haya sobrecura.
- **Ejercicio:** romper a propósito la conexión `connect` de `health_changed` y observar que la barra no se mueve aunque la salud baje; después reconectar y confirmar que se actualiza con daño **y** con poción.

### Módulo 10 — Items en el mundo, tienda y subida de nivel (3:35:49 – 4:12:23)

- **Objetivo:** cerrar el loop de juego: matar → loot → tienda → subir de nivel.
- **Contenidos:**
  - **Item 3D como objeto pickup:** `Area3D` + `queue_free()` diferido hasta que termina el sonido de pickup (`hide()` primero, `queue_free()` al `finished`). Cita: «I'm going to ceue free once the sound is finished but until then I'm just going to hide self» (05:20:26).
  - **Tienda** como `CanvasLayer` propio, con `current_item`, un slot de preview y `buy`/`close`. La tienda **también pausa** el árbol: eso obliga al `process_mode = ALWAYS` del módulo 6.
  - `level_up`: XP → señal → VFX → recálculo de stats. El VFX se conecta a la señal, no al revés.
- **Ejercicio:** comprar un item con oro insuficiente y verificar que el botón queda deshabilitado *y* que el mensaje de error no pausa dos veces el árbol.

### Módulo 11 — Forward+ y ambiente 3D (4:12:23 – 4:30:36)

- **Objetivo:** pasar de Compatibility a Forward+ para tener glow, y montar iluminación de ambiente.
- **Contenidos:**
  - **El cambio de renderer se hace en Project Settings y requiere reiniciar**; luego aparecen errores que el autor pide ignorar. Cita: «you might have noticed a few errors but don't worry just okay andore them» (04:12:54).
  - Con Forward+ el escenario cambia de aspecto **sin tocar una luz**: cita «you will immediately notice a very big difference» (04:12:59).
  - Glow: `enabled`, `normalized`, `blend_mode = ADDITIVE`.
  - **GridMap con `cell_size = 4,4,4`** y separar **floor** de **walls** en dos GridMaps: con un solo GridMap, pintar una pared borra el piso de esa celda. Cita: «when I start adding walls it's going to remove the floor I don't want that» (04:14:46).
  - **Torch:** mesh + `OmniLight3D` + `GPUParticles3D` con `QuadMesh`, material `unshaded` + `vertex_color`, blend `add`, y `billboard mode = PARTICLES`.
- **Ejercicio:** migrar un proyecto chico de Compatibility a Forward+, anotar cuántos materiales se rompen y confirmar que el glow solo aparece con Forward+.

### Módulo 12 — VFX con Lelu: aura de level up y puff (4:30:36 – 5:11:13)

> Cambia el expositor: **Lelu** enseña shaders y partículas. El tono y el nivel suben; el autor admite «he's much much more talented than I am».

- **Objetivo:** construir dos efectos desde cero, no solo usarlos.
- **Contenidos:**

  **Aura de level up (3 partes):**
  1. Cilindro en Blender con **pivote en la base**, export OBJ (`on_fill` = nothing).
  2. `GPUParticles3D` con `ParticleProcessMaterial` + `Draw Pass` = cilindro; **gravedad 0**, `amount = 1`, `display_scale = 4`, `cast_shadow = off`.
  3. `ShaderMaterial` **visual**: `cull_mode = disabled` (ver ambas caras), `unshaded`, sin sombras; `alpha` desde un **`GradientTexture2D`** vertical.
  4. Onda expansiva: duplicar el sistema, `make unique` en partícula **y** material, `display_scale = 8`, y cambiar la curva de escala para que crezca en XZ pero **se achique en Y**. Cita: «I want it to go to to shrink down so let's change this curve» (04:45:41).
  5. Texto «Level Up» en PNG desde un editor externo → `CPUParticles3D` con `QuadMesh`, `billboard = particle`, `velocity` en Y = 2.5, `color_ramp` transparente en ambos extremos.
  6. Coordinación con un `AnimationPlayer`: todos los emisores en **`one_shot`**, `emitting` keyeado al inicio; el texto se retrasa a mano.

  **Puff effect (3 partes):**
  1. Esfera con `VisualShader`: normal + textura desplazándose con `UV` + `Time`, multiplicada por la normal. Cita: «this is the result of this text controlling the vertices of the of the sphere» (05:02:35). Intensidad −0.6 para que parezca nube.
  2. Sombreado **toon/anime**: `dot(normal, fresnel)` → `smooth_step` con dos constantes (dureza del borde) → `clamp` 0.1–1 (cuánto oscurece la sombra).
  3. `amount = 12`, `explosiveness = 0.85`, posición en anillo (`ring`, altura 0, radio 1), velocidad Y 0.5–1, `color_ramp` HDR violeta.
- **Ejercicio:** recrear el aura **sin mirar** y anotar en qué paso aparece el error más frecuente (en el curso es no hacer `make unique` antes de editar la copia: se rompe la original).

### Módulo 13 — Integración final: VFX, sonido y spawn (5:11:13 – 5:30:06)

- **Objetivo:** meter todo en el juego y que el nivel se pueble solo.
- **Contenidos:**
  - VFX en el player como hijos con `editable_children`, `level_up` y `puff` en `one_shot`; el `AnimationPlayer` del level up se dispara desde la señal.
  - **Audio:** `AudioStreamPlayer3D` para `damage` y `hit`, que se llaman desde `hit()`; `pickup` con `finished → queue_free`.
  - Cita del error real: «nothing happens uh probably because I'm never playing it» (05:20:56) — el sonido no sonaba porque faltaba el `play()` en el `body_entered`.
  - **Spawn sobre grilla, validando la celda:** `while $Monsters.get_child_count() < 10`, `randi_range` en X/Z, y `grid_map.get_cell_item()` == 0 **y** `walls.get_cell_item() != 2`. Cita: «I don't want to spawn it in a wall right so we're going to have to figure out how we can do that» (05:21:36).
  - El spawn pone `y = 3` para que la gravedad lo baje sobre el piso.
- **Ejercicio:** subir el spawn a 100 monstruos y medir; después validar con un contador que **ninguna** celda de pared recibió un enemigo (el `!= 2` es el índice real del `WallArch`, no un valor universal).

## Banco de preguntas

1. ¿Por qué el `MeshLibrary` se arma como escena 3D y no se crea directo desde el FileSystem?
2. ¿Qué dos nodos hacen falta para que `WorldEnvironment` tenga efecto, y cuál es el olvido típico?
3. ¿Por qué `jump_force` es positivo si la gravedad resta en Y?
4. ¿Qué hace exactamente el `SpringArm3D` en la jerarquía de la cámara, y qué pasa si le das longitud positiva?
5. Nombrá tres transiciones del player cuyo `Switch Mode` es `At End` en vez de condicional, y explicá por qué.
6. ¿Cuál es la diferencia de responsabilidad entre el `AnimationTree` del player y la FSM en código del monstruo?
7. ¿Por qué el `Area3D` del arma se habilita con un property track `enabled` en vez de con un timer o un `if` del estado actual?
8. ¿Qué bug produce no volver a poner `just_hit = false`, y cómo se ve en el juego?
9. ¿Por qué `CanvasLayer` necesita `process_mode = ALWAYS`? ¿Qué se rompe sin eso?
10. ¿Qué ventaja concreta tiene `class_name InventorySlot extends PanelContainer` sobre un `PanelContainer` con script pegado a mano?
11. ¿Por qué el mismo `InventorySlot` sirve para inventario y equipamiento? ¿Qué campo lo permite?
12. ¿En qué momento del flujo se emite `health_changed` con signo negativo, y por qué el signo es la semántica?
13. ¿Qué diferencia hay entre usar `queue_free()` inmediato y diferido hasta el `finished` del sonido de pickup?
14. ¿Por qué el GridMap se separa en `floor` y `walls`? ¿Qué pasa si se pinta una pared encima del piso en el mismo GridMap?
15. ¿Qué habilita Forward+ que Compatibility no tiene, y cómo se nota sin tocar luces?
16. En el aura, ¿qué significa hacer `make unique` en la partícula **y** en el material antes de editar la copia?
17. ¿Qué hace el `smooth_step` con dos constantes en el shader toon, y qué controla el `clamp` posterior?
18. ¿Qué dos validaciones de celda hace el spawn de monstruos antes de instanciar, y por qué son dos y no una?

## Lo que el curso no cubre

- **Testing**: no hay un solo test automatizado; toda verificación es «hit play y mirá».
- **Save/load**: el inventario y las stats viven en el autoload y se pierden al cerrar.
- **Caballería / unidades montadas**: el curso usa un solo tipo de personaje (KayKit Knight) y un solo monstruo.
- **Balance y economía**: oro, precios y fórmula de daño son placeholders (`damage - defense` plana).
- **Optimización**: no se mide rendimiento en ningún punto, ni con Forward+ ni con 100 monstruos.
- **Navegación**: el monstruo persigue en línea recta con `Area3D`; no hay `NavigationAgent3D` ni pathfinding alrededor de paredes.

## Recursos del video (descripción oficial)

- Escenario y personajes: [KayKit Adventurers](https://kaylousberg.itch.io/kaykit-adventurers), [KayKit Dungeon Remastered](https://kaylousberg.itch.io/kaykit-dungeon-remastered), [KayKit Skeletons](https://kaylousberg.itch.io/kaykit-skeletons)
- UI: [Golden UI – Bigger than Ever Edition](https://opengameart.org/content/golden-ui-bigger-than-ever-edition)
- Items: [16×16 RPG Item Pack](https://alexs-assets.itch.io/16x16-rpg-item-pack)
- Fuente: [1001fonts – pixel fonts](https://www.1001fonts.com/pixel-fonts.html)
- Lelu: [canal de YouTube](https://www.youtube.com/@Le_x_Lu)

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
