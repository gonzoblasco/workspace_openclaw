# Módulo 0 — Arranque y estructura del proyecto

> Estudiado el 2026-11-11. Fuentes: transcript del curso (00:00:00–00:05:46), [doc oficial de migración a 4.7](https://docs.godotengine.org/en/4.7/tutorials/migrating/upgrading_to_godot_4.7.html) y sonda corrida en la Mac mini con **Godot 4.7.2**.

## Qué enseña el curso (y qué tiene de bueno)

El módulo 0 no enseña código: enseña **qué hay en la caja antes de abrirla**. Omar dedica los primeros cinco minutos a mostrar la estructura del starter y avisar de qué es cada cosa. Es el tipo de módulo que uno salta y después se arrepiente.

Los cuatro bloques del curso, de su boca (00:00:48):

1. **Player** — mover, animar, atacar.
2. **Monstruo** — IA simple con state machines (idle → run → attack).
3. **GUI** — inventario + equipamiento + perfil de stats + tienda.
4. **VFX** — efecto simple hecho a mano, después un invitado (Lelu) enseña shaders y partículas.

Cuatro bloques, un juego completo, en 5h30. El alcance es coherente: es un RPG de una sola zona, un tipo de enemigo, y un loop de economía cerrado.

## Lo que el curso da por sentado y ya no es cierto

Este es el punto donde el curso envejeció, y es lo primero que hay que poner sobre la mesa.

| El curso (2024-06) | Hoy (Mac mini, 2026-11) |
|---|---|
| Estable = **4.2**, graba en **4.3 beta** | Instalado: **4.7.2.stable** |
| «it will upgrade whatever it needs to, and it just does it all on its own» (00:02:40) | Cierto para el archivo, **falso para el comportamiento** — ver abajo |

Omar dice que la conversión de proyecto es automática y buena. Lo es para abrir el proyecto. **No lo es para que se comporte igual.** Entre 4.3 y 4.7 hay cambios de comportamiento que compilan sin error y funcionan distinto.

### Verificado en la máquina, no leído

Sonda propia (`practicas/m0/probe.gd`), corrida con `--headless`:

```console
$ /Applications/Godot.app/Contents/MacOS/Godot --headless --path . --script probe.gd
Godot Engine v4.7.2.stable.official.ed1daf0bf

engine_version=4.7.2-stable (official)
major=4 minor=7
stretch_mode=disabled
stretch_aspect=keep
sky_roughness_layers=8
physics_3d=DEFAULT
```

Dos cosas de esa salida importan:

1. **`sky_roughness_layers=8`.** El default *viejo* era 7 y el nuevo es 8. Si el proyecto lee 8 sin que nadie lo haya tocado, es que corre el default nuevo. Comparar ese número es la forma barata de saber **si un proyecto viejo sigue con defaults de 4.3 o ya adoptó los de 4.7**.
2. **`stretch_mode=disabled`** en un proyecto recién creado con `--path .`. En 4.7 el default para proyectos **nuevos** es `canvas_items` / `expand`; que acá lea `disabled`/`keep` significa que está tomando el valor heredado, no el nuevo. Es decir: **los defaults cambiados no se aplican retroactivamente** a un proyecto existente. Eso es bueno, y es exactamente por lo que un proyecto migrado puede parecer sano y no serlo.

### Los tres cambios que sí te van a morder en este curso

Los saqué del doc oficial de migración 4.6→4.7, filtrando por lo que el curso toca:

**(a) `AnimationTree` — el más grave para este curso.**

> `AnimationNodeBlendSpace1D` y `AnimationNodeBlendSpace2D` tienen un `SyncMode` enum nuevo que **reemplaza** la propiedad booleana `sync`. Si usás un `AnimationTree` y las animaciones no transicionan bien después de actualizar, probablemente tengas que setear ese valor en cada blend space.

El curso usa `AnimationTree` en el player (módulo 2) y en el monstruo (módulo 3), con un `BlendTree` para el ataque a `TimeScale` 2×. Si el blend space tiene `sync` en el `.tscn` y ya no existe como bool, el árbol se carga **sin** ese ajuste y la animación se mezcla distinto. Compila. No avisa.

**(b) `AudioStreamPlayer.area_mask` — default cambió de 1 a 0.**

> ...si usás `audio_bus_override` en `Area2D`/`Area3D` **y** el default de `area_mask`, tenés que volver a poner layer 1, si no las overrides dejan de funcionar.

El curso pone `AudioStreamPlayer3D` para golpes y pickups (módulo 13). No usa `audio_bus_override`, así que **este no aplica al curso**, pero sí a cualquier proyecto que sí lo use. Lo dejo anotado porque es el tipo de cambio que aparece recién en la semana 3 de tu juego.

**(c) Input — los device IDs de mouse y teclado dejaron de ser `0`.**

> Los device IDs de mouse y teclado pasaron de `0` a `InputEvent.DEVICE_ID_MOUSE` y `InputEvent.DEVICE_ID_KEYBOARD` porque algunos joysticks usan `0`.

El curso compara `event.button_index` para el click derecho en el inventario (módulo 8). No compara `event.device`, así que **tampoco aplica**. Pero si en algún momento escribís `if event.device == 0` para distinguir teclado de joystick, en 4.7 eso es «cualquier joystick», no teclado.

**Un cambio de comportamiento que no está en la tabla de breaking changes, pero está en la página:** `CanvasItem` ya no agrega el feather de antialiasing al dibujar líneas. El curso no dibuja líneas a mano, así que no aplica. Lo anoto porque es el mismo patrón: *algo que se veía de una forma, se ve de otra, y no hay error.*

## El ejercicio del curso, adaptado

El original pide abrir el starter y anotar la versión. Lo hice, y le agregué la parte que el curso no pide porque en 2024 no hacía falta:

**Sonda de defaults.** `practicas/m0/probe.gd` imprime versión + tres defaults clave. Corrélo en **cualquier** proyecto que heredes o migres, antes de creer que está sano:

```bash
/Applications/Godot.app/Contents/MacOS/Godot --headless --path <proyecto> \
  --script <ruta>/probe.gd
```

**La regla que sale de esto:**

> Que un proyecto abra sin errores después de migrar **no dice nada** sobre si se comporta igual. Los defaults nuevos no se aplican retroactivamente, así que un proyecto viejo abre con mezcla de defaults viejos y nuevos, y la única forma de saber cuál tomó es leerla.

### Comparación con lo que ya tenemos

`projects/reinos-de-la-frontera/project.godot` declara explícitamente:

```ini
config/features=PackedStringArray("4.7", "Forward Plus")
renderer/rendering_method="forward_plus"
```

Ese proyecto **nació** en 4.7 y no arrastra defaults de 4.3 — no necesita la sonda para versionado, aunque le sirve para detectar cambios de default futuros. Es la diferencia entre un proyecto migrado y uno nuevo, y es la razón por la que el curso, escrito para 4.3, pide cosas que en 4.7 ya están resueltas o se hacen distinto.

## Lo que el módulo **no** enseña, y hay que saber

- **Control de versiones.** No hay un `git init` en ningún momento del curso. Cinco horas de trabajo sin red: si en el módulo 12 rompés el shader, no hay vuelta atrás.
- **`project.godot` como contrato.** Omar nunca abre el archivo. Todo es editor. Eso funciona hasta que dos personas tocan el proyecto, o hasta que migrás de versión y querés ver qué cambió.
- **Qué es un `.uid`.** Godot 4.4+ los genera; el curso no los menciona porque en 4.3 eran nuevos y no había problema. Hoy se versionan o se ignoran, y elegir mal rompe referencias. (Nuestro `caesar3-clone` los ignora; `reinos-de-la-frontera` los versiona. Ambas son decisiones, ninguna es «lo correcto».)
- **Nada de testing.** Ya lo dije en el outline: cero tests en 5h30.

## Preguntas del módulo (para que las contestes antes de seguir)

1. ¿Por qué `sky_roughness_layers` lee 8 en un proyecto sin tocar nada, y qué te dice eso sobre si un default nuevo se aplica solo?
2. El curso dice que Godot convierte el proyecto «automáticamente y muy bien». ¿En qué sentido es cierto y en qué sentido no?
3. Nombrá el cambio de 4.7 que más riesgo tiene para **este curso** y explicá por qué compila igual.
4. Si heredás un proyecto de 4.3 que abre sin errores, ¿cómo sabés en dos minutos si está sano?
5. ¿Por qué `reinos-de-la-frontera` no necesita la sonda para versionado?

## Próximo bloque

**Módulo 1 — GridMap y WorldEnvironment** (00:05:46–00:19:15). Ahí arranca lo bueno: el `MeshLibrary` que no es un recurso, y el `WorldEnvironment` que no hace nada sin `Environment`.

Una nota para cuando lleguemos: el curso arma el nivel para **una** zona de dungeon. Si en algún punto querés usar esto para Reinos, el GridMap a `cell_size` 4×4×4 es directamente incompatible con nuestra grilla de simulación (que es lógica, no de tiles 3D). Lo digo ahora para que no lo descubras en el módulo 11.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
