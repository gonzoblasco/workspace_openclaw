# Módulo 1 — GridMap y WorldEnvironment

> Estudiado el 2026-11-12. Fuentes: transcript (00:05:46–00:19:15), doc oficial de Godot 4.7 y **práctica corrida en la Mac mini** (`practicas/m1/`, 4 scripts, 16 checks verdes, captura real).

## Qué enseña

Dos sistemas, y los dos tienen una trampa silenciosa:

1. **`GridMap`** — pintar un nivel en 3D con tiles. La trampa: la `MeshLibrary` **no es un recurso que se crea desde el FileSystem**.
2. **`WorldEnvironment`** — atmósfera. La trampa: **el nodo solo, no hace nada**.

Las dos trampas tienen la misma forma: *un nodo que parece completo y está vacío por dentro*. Es el patrón que se repite todo el curso.

## MeshLibrary: por qué no se puede crear como recurso

Omar: «in order to create a mesh Library I can't just create one like this... in 3D unfortunately it's not that easy» (00:06:10).

El motivo real, que él no da: una `MeshLibrary` es un contenedor de **items**, y cada item es un par (mesh, shapes) más un transform. Eso no se escribe a mano: se **exporta desde una escena 3D** donde cada mesh ya tiene su colisión armada. El editor es el constructor.

Los pasos, en orden, porque el orden importa:

```
Escena 3D nueva  →  arrastrar el mesh  →  Make Local
  →  borrar el nodo original
  →  seleccionar el Mesh → "Create Collision Shape"
  →  verificar la jerarquía resultante:
        StaticBody3D
        └── CollisionShape3D
        └── MeshInstance3D
  →  Escena → Export as MeshLibrary
```

**`Make Local`** es el paso que todos saltean. Arrastrar un mesh desde el FileSystem deja una **instancia heredada** de otra escena; el `MeshLibrary` necesita el mesh como sub-recurso propio. Sin `Make Local`, el export guarda una referencia externa que se rompe si movés el asset.

**`StaticBody3D > CollisionShape3D`** — el orden es la jerarquía, no el orden de creación. Un `CollisionShape3D` suelto, sin `StaticBody3D` padre, no colisiona con nada. El curso lo dice al pasar: «make sure it is the body where we have a static body 3D and then a collision shape» (00:09:04).

### La práctica lo hizo en código

En `build_mesh_library.gd` armé el mismo contenedor sin editor:

```gdscript
var lib := MeshLibrary.new()
lib.create_item(0)
lib.set_item_name(0, "floor")
lib.set_item_mesh(0, _box_mesh(...))
lib.set_item_shapes(0, [_box_shape(...)])
ResourceSaver.save(lib, "res://mesh_library.tres")
```

Y el test (`test_mesh_library.gd`) verifica lo que el editor garantiza a mano:

```console
$ Godot --headless --path . --script test_mesh_library.gd
  OK   mesh_library.tres existe
  OK   carga como MeshLibrary
  OK   3 items en la libreria (floor, wall, stairs)
       nombres=["floor", "wall", "stairs"]
  OK   el item 0 tiene al menos un shape
  OK   el item 0 tiene mesh
M1_MESH_LIBRARY_OK
```

**Lo que aprendí haciéndolo:** el `MeshLibrary` **no puede** tener un item sin mesh, pero **sí puede** tener un item sin shape. Un tile sin collision se ve igual y atraviesa el piso. El editor no te avisa; el test sí.

### La escalera

El curso tiene un detalle que vale oro y lo dice como al pasar (00:12:50):

> «stairs don't exactly collide well with our player»

Y la solución que da: no usar la colisión del mesh de escalera, sino **un `BoxShape3D` rotado a mano** que cubra la pendiente, «so we can smoothly run on the stairs».

Esto es una regla de diseño que trasciende el curso: **la colisión visible no tiene que ser la colisión física**. En un juego moderno la geometría que se ve (escalones) y la que se pisa (una rampa invisible) son cosas distintas. Es más caro de autorar y más barato de ejecutar.

## WorldEnvironment: el nodo vacío

Omar agrega el `WorldEnvironment` y el editor se ve mejor. Después le da play y **no pasa nada**. Su explicación (00:15:45):

> «we need to actually add an environment»

El `WorldEnvironment` es un **contenedor**. La propiedad `environment` es de tipo `Environment` y arranca en `null`. Un `WorldEnvironment` con `environment == null` **no modifica nada** — no es que use defaults: no interviene.

La práctica lo verifica de forma que falla si alguien lo rompe:

```gdscript
check(we != null and we.environment != null, "el Environment esta asignado")
```

### Los valores del curso

| Ajuste | Valor | Por qué |
|---|---|---|
| `background_mode` | `BG_COLOR` | Un dungeon no tiene cielo |
| `background_color` | `(100,100,100)` | Gris, no negro: el negro puro no deja ver silueta |
| `volumetric_fog_enabled` | `true` | Da profundidad |
| `volumetric_fog_density` | `0.02` | Suave |
| `fog_enabled` | `true` | Niebla clásica |
| `fog_density` | `0.2` | ⚠️ ver abajo |
| `fog_light_energy` | `0.1` | Baja, para que no ilumine |
| `glow_enabled` | `false` | Explícito: «we're actually not going to enable glow just leave it off for now» (00:18:51) |

## ⚠️ El hallazgo: `fog_density = 0.2` no es universal

Cuando armé el nivel siguiendo el curso al pie de la letra, **la captura salió gris uniforme**. Nada visible. No era un bug mío: era la niebla.

Lo medí en vez de adivinar (`probe_fog.gd`):

```console
fog_density=0.2 volumetric=0.02
  d=10 transmision_fog=0.135  transmision_volum=0.819
  d=20 transmision_fog=0.018  transmision_volum=0.670
  d=30 transmision_fog=0.002  transmision_volum=0.549
  d=40 transmision_fog=0.000  transmision_volum=0.449
```

A **30 unidades de cámara, la transmisión es 0.2 %**. Todo es color de niebla. A 40, cero absoluto.

El curso usa `0.2` porque su cámara está a **5 metros** del jugador: ahí `exp(-0.2*5) = 0.37`, que da un dungeon brumoso lindo. Mi cámara cenital está a 30. La misma constante, un efecto completamente distinto.

**La regla:** `fog_density` no es un valor estético, es una **tasa por unidad de distancia**. Cambiás la distancia de cámara y la niebla se vuelve otra cosa. Si migrás el valor de un tutorial, migrás también su cámara.

En la práctica bajé a `0.012` (transmisión 70 % a 30 m) y subí `sun.light_energy` a 1.6 y `ambient_light_energy` a 0.35, porque sin niebla densa la escena quedaba lavada por el ambiente.

### La otra trampa: sin `Camera3D`, no hay 3D

Omar, al pintar tiles y dar play (00:18:47):

> «if I hit play nothing will happen... that is because I do not have a camera 3D... in order for it to play»

Obvio para quien ya lo sabe, invisible para quien empieza. **Un `Node3D` con geometría y sin `Camera3D` no dibuja nada, aunque el editor lo muestre.** Y encima: dos `Camera3D` con `current = true` se pelean; la última del árbol gana.

## El ejercicio del curso, completado

El original: pintar un piso con `Ctrl+F` (fill), rotar tiles con `S`, y exportar la `MeshLibrary`.

El mío, además:

1. `build_mesh_library.gd` — arma la librería en código y la guarda.
2. `build_level.gd` — `level.tscn` con Floor + Walls separados, `WorldEnvironment`, sol y cámara.
3. `test_mesh_library.gd` — 6 checks.
4. `test_level.gd` — 16 checks, incluidos los tres «nodos vacíos».
5. `shot.gd` — captura real (`m1_shot.png`), porque headless no dibuja.

```console
$ Godot --headless --path . --script test_level.gd
  OK   el Environment esta asignado
  OK   la camara es current
  OK   el piso tiene 144 celdas (12x12)
  OK   las paredes tienen 44 celdas (borde 12x12)
  OK   la esquina sigue siendo piso
  OK   glow apagado (el curso lo deja para Forward+)
M1_LEVEL_OK
```

### Por qué Floor y Walls son dos GridMap

El curso lo hace y lo explica recién en el módulo 11, cuando ya pintó todo mal:

> «when I start adding walls it's going to remove the floor I don't want that» (04:14:46)

**Un `GridMap` tiene UNA celda por coordenada.** Pintás una pared en `(3,1,3)` y el piso que estaba en `(3,0,3)` se pierde si las capas se solapan. La solución no es magia: son dos `GridMap` con la misma `MeshLibrary` y `cell_size`, apilados en coordenadas distintas.

Lo dejo ahora porque en el módulo 1 el curso crea **un solo** GridMap y no lo vuelve a tocar hasta el 11. Si seguís el curso al pie de la letra, vas a pintar 40 minutos de nivel y después rehacerlo.

## Lo que el módulo no enseña

- **`GridMap` está de salida.** En Godot 4.4+ se recomienda `TileMapLayer` incluso para 3D, y el equipo de Godot viene empujando reemplazos. No es urgente para el curso, pero no construyas un pipeline de niveles sobre `GridMap` sin saberlo.
- **Nada de navegación.** El curso pinta paredes que *no* van a ser evitadas por el monstruo (que persigue en línea recta). Lo vas a notar en el módulo 4.
- **Ningún `git init`.** Igual que el módulo 0.

## Preguntas

1. ¿Por qué `Make Local` es obligatorio y qué se rompe sin él?
2. Un `WorldEnvironment` sin `Environment` — ¿usa defaults o no hace nada? ¿Por qué la diferencia importa?
3. Tu cámara está a 30 m y no ves nada con `fog_density = 0.2`. ¿Qué número mirás para saber si es la niebla y qué te dice?
4. ¿Por qué el curso separa Floor y Walls en el módulo 11 y no en el 1?
5. ¿Por qué la escalera usa un `BoxShape3D` rotado en vez de la colisión del mesh?
6. ¿Qué puede tener un item de `MeshLibrary` que no puede faltarle, y qué sí puede faltarle sin error?

## Próximo bloque

**Módulo 2 — Player: cámara, movimiento y animación** (00:19:15–01:11:07). Es el módulo más largo del curso (52 min) y el que más choca con 4.7 por el `AnimationTree` / `BlendSpace.sync_mode`.

Va a ser el primero con práctica de **input real**: un personaje que se mueve y podés manejar. Ahí el test automático empieza a quedarse corto y hace falta captura o grabación.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
