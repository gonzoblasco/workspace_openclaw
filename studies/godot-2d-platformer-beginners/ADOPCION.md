# Adopción: Godot Game Development for Beginners (plataforma 2D)

Fecha de revisión: 2026-11-11
Curso: [outline.md](outline.md) · [transcripcion.md](transcripcion.md)
Proyecto usado como caso: `projects/reinos-de-la-frontera` (RTS medieval, Godot 4.7)

## Veredicto

**Adopción parcial, un artefacto.**

El curso construye un plataformas 2D con `CharacterBody2D`, `TileMapLayer`, `Area2D` y cambio de escena por nombre de archivo. El proyecto que tenemos es un RTS 3D con simulación por ticks separada de la vista, así que casi todo el contenido técnico **no aplica**: no hay tiles que pisar, no hay parallax, no hay salto, y el cambio de escena no es progresión de niveles sino menú ↔ partida.

Lo que sí muerde es **una idea de arquitectura**, no un nodo: la forma en que el curso conecta el `Checkpoint` con el `CheckpointManager` y la forma en que el HUD del juego habla con el mundo.

## La idea, con la cita

En el Módulo 4, el nodo `Checkpoint` se hace de su manager subiendo por la jerarquía de padres **dos veces** y bajando por nombre (00:13:51):

> «checkpoint manager is equal to get parent dot get parent dot get node checkpoint manager»
> — (00:13:51)

Y en el Módulo 8, el `HUD` se toma por nombre desde el colector:

> «then we increase our score» (00:45:03) y «HUD.score plus equal like» (00:45:05)

Ese patrón —*un nodo busca a otro por la forma del árbol*— es cómodo y es frágil por definición: la relación existe mientras el árbol no se mueva. El curso lo usa porque el juego tiene tres nodos; el workspace tiene un proyecto con nueve `*.tscn` y tres sitios donde ya se usa el mismo patrón.

## Tabla de adopción

| Idea del curso (con t=) | Qué hacemos hoy | Artefacto verificable |
|---|---|---|
| «checkpoint manager is equal to get parent dot get parent dot» (00:13:51) y «HUD.score plus equal like» (00:45:05) — la comunicación entre nodos se resuelve por **profundidad fija** (`get_parent().get_parent()`) o por **búsqueda por nombre desde un hermano** (`get_parent().get_node("World")`) | `view/hud.gd:67` hace `runner.get_parent().get_node("World")`; `view/overlay.gd:19` hace `runner.get_parent().get_node_or_null("World")`; `view/world_view.gd:29` hace `get_parent().get_node("Floor")`. Ninguno de los tres rompe hoy; los tres dependen de que `World`, `Floor` y `SimRunner` sigan siendo hermanos y sigan llamándose así | `check-hierarchy-coupling.py` — corrido abajo, **falla** contra el repo actual con 3 hallazgos |

## El artefacto, corrido

Salida pegada de la corrida real del 2026-11-11:

```console
$ python3 studies/godot-2d-platformer-beginners/check-hierarchy-coupling.py projects/reinos-de-la-frontera
FAIL: 3 referencia(s) por jerarquia en /Users/gonzoblasco/.openclaw/workspace/projects/reinos-de-la-frontera
  - view/hud.gd:67  [get_parent() + get_node (depende del nombre y del hermano)]
      minimap.setup(runner.state, runner.get_parent().get_node("World"))
  - view/overlay.gd:19  [get_parent() + get_node (depende del nombre y del hermano)]
      var world_view = runner.get_parent().get_node_or_null("World")
  - view/world_view.gd:29  [get_parent() + get_node (depende del nombre y del hermano)]
      floor_mi = get_parent().get_node("Floor")
...
EXIT=1
```

EXIT `1`. Ninguno de los tres hallazgos es un bug latente *declarado*: el juego hoy funciona. Lo que el gate mide es la **deuda de acoplamiento** — que el día que `World` deje de ser hermano de `SimRunner`, los tres archivos fallan en runtime y ninguno avisa antes.

## Por qué el defecto es real y no teórico

El proyecto ya muestra el costo del patrón en su propio código:

- `view/overlay.gd:19` usa `get_node_or_null` en lugar de `get_node`. Esa diferencia no es estilo: es la corrección del síntoma. El autor ya anticipó que `World` podía no estar, y en vez de fijar el contrato, defendió el acceso.
- `view/hud.gd:106` hace `var game = runner.get_parent()` y después comprueba `if game != null`. Es el mismo patrón con la comprobación puesta después.

Un gate que solo mira el código no arregla nada, pero **convierte el acoplamiento en una cifra que no se puede ignorar**. Es exactamente lo que el curso no hace: enseña el patrón sin nombrarlo como deuda.

El arreglo, cuando toque:

1. `SimRunner` emite una señal `world_ready(world)` y el padre la conecta; el HUD recibe el nodo en `setup()`, no lo busca.
2. `world_view.gd` recibe el `Floor` por un `@export var floor: Node3D` asignado en el editor.
3. `overlay.gd` recibe el `world_view` por el mismo camino que ya recibe `camera` en `setup(cam, owner_runner, owner_game)`.

El gate pasa a verde cuando los tres desaparecen, sin cambiar el script: si hay que tocarlo, estaba midiendo la forma y no la conducta.

## Descartados (y por qué)

- **`TileMapLayer` + Terrain Sets (Módulo 2, 00:03:17 – 00:07:53):** el RTS es 3D y usa un `Floor` con `MeshInstance3D`; no hay mapa de tiles. `view/` no lo necesita.
- **Autotiling (Módulo 2, 00:06:29):** es una técnica de nivel, no de juego. El proyecto no tiene pipeline de mapas. Queda como candidato si aparece un modo campaña con niveles de terreno pintable.
- **Checkpoints y `DeathZone` (Módulo 4, 00:11:52):** un RTS no tiene resets por caída; la partida termina con victoria/derrota (`runner.state.winner`). El concepto de "reaparecer en el último punto seguro" no tiene equivalente.
- **Persecución por comparación de X (Módulo 7, 00:37:53):** la IA del RTS ya tiene su propia máquina de estados (`ent.state`) y el comportamiento no es chase. No aplica.
- **`Time.get_ticks_msec()` como reloj del HUD (Módulo 8, 00:42:07):** el proyecto ya mide por tick con su propio reloj (`clock.gd`); usar uptime del proceso sería un retroceso, no una mejora.
- **Cambio de nivel por parseo del nombre de archivo (Módulo 9, 00:52:57):** es el patrón más frágil del curso y el proyecto ya usa `change_scene_to_file` con rutas literales en `menu.gd:7` y `view/game.gd:159`. Adoptar el parseo sería empeorar.
- **Export HTML + itch.io (Módulo 10, 00:55:14):** el proyecto tiene `export_presets.cfg` y una compilación propia. El tutorial de itch.io no aporta al pipeline existente.
- **`local_to_scene` en `PathFollow2D` (Módulo 6, 00:30:12):** no hay plataformas móviles en el RTS. Queda como nota para cualquier escena reutilizable: **es un flag que hay que recordar**, y el curso lo menciona de pasada.

## Lo que el curso no cubre y el proyecto ya resuelve

El curso no menciona `delta`, autoloads, `@export`, collision layers, audio, guardado, ni tests. El proyecto ya tiene separación lógica/vista (`sim/` headless por tick, `view/` de dibujo), que es **más sofisticado** que todo el curso. Eso va en `docs/` del proyecto, no acá.

## Deuda registrada, no arreglada

El artefacto quedó **en rojo**. Es intencional: registra una deuda real de `reinos-de-la-frontera`, no se arregla en la sesión que montó la clase. Se cierra cuando el proyecto reciba señales o `@export` en esos tres sitios; el mismo script debe pasar a verde sin tocarlo.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
