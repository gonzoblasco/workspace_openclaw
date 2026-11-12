# ADOPCIÓN — Create a Cute Room Portfolio with Blender, Three.js, JavaScript

**Fecha:** 2026-11-11 · **Curso:** 8:42:31 · Andrew Woan · freeCodeCamp.org
**Fuente:** https://www.youtube.com/watch?v=tdsQwuyS6DQ

**Pregunta:** ¿qué hacemos hoy mal en el workspace que este curso arregla?

## Veredicto

**Sí se adopta, con un artefacto:** `web-asset-gate.py`, un presupuesto de carga para cualquier asset 3D que salga a web.

Por qué este y no el modelado o el procedural: el resto del curso enseña una habilidad que hoy no tenemos en producción, y las clases de Blender ya están cubiertas por [`../creative-web-threejs-blender/`](../creative-web-threejs-blender/) para Three.js. El único momento donde este curso dice algo que **hoy hacemos mal sin saberlo** es la medición de compresión: el autor compara el mismo modelo antes y después de Draco, «it's only 1 megabyte compared to our original one which is 12 megabytes» (6:46:02), y separa ese paso del export de Blender a propósito, porque hacerlo dentro de Blender «has been removed» (6:45:32). Es decir: el peso no se mira una vez al exportar, se mide y se verifica aparte.

En el workspace hay un proyecto que **va a** servir assets 3D por web (`projects/reinos-de-la-frontera`, Godot con export web en el roadmap) y que ya tiene 7,6 MB de `.gltf` + texturas de terceros. Hoy nadie mira ese peso: se descargó lo que se encontró y se commiteó el `CREDITS.md`. Es exactamente el error que el curso documenta.

## Tabla

| Idea del curso (con t=) | Qué hacemos hoy | Artefacto verificable |
|---|---|---|
| El peso se mide **después** de comprimir, no se asume: 12 MB → 1 MB con Draco («it's only 1 megabyte compared to our original one which is 12 megabytes», 6:46:02) | `projects/reinos-de-la-frontera/assets/` pesa 3,7 MB de `Warrior.gltf` duplicado más 677 KB de textura, y nunca se midió comprimido ni se eligió un techo | **`web-asset-gate.py`** — mide gzip por modelo, lado mayor de textura y formato; falla (exit 1) si un asset se pasa del presupuesto. Corrido abajo |
| Las texturas se convierten a WebP porque el ratio calidad/peso es mejor «because WEBP is optimized for the» (6:46:30) | Las texturas del proyecto son PNG de 677 KB; en el repo no hay paso de conversión ni de verificación | **Candidato, no escrito.** El gate ya marca el formato; un paso de conversión a WebP con `cwebp` es trabajo de build, no de gate. Se deja listado |
| Se hornea la luz porque el ray tracing «would really really hurt the performance on the browser» (5:02:08) | Godot corre el render en el engine, no en Three.js: no hay bake de lighting que hacer en el flujo actual | **Sin adopción.** El trade-off del curso (estático = horneado) no aplica a un engine con su propio pipeline. Vale como criterio cuando se exporte a web |
| UV unwrap para empaquetado: «rectangles and squares will pack better than some sort of distorted shape» (5:34:07) | El proyecto usa assets de terceros (Quaternius), no modelamos props propios para web | **Sin adopción todavía.** El día que haya un prop propio, la regla ya está escrita acá |
| El raycaster filtra a los clickeables por nombre para no recorrer 200 mallas | Nuestro 3D es Godot con `pick_at` por física, no raycaster de Three.js | **Sin adopción.** El problema (recorrer toda la escena por evento) no existe en el flujo actual |

## El artefacto, corrido contra el repo

Presupuesto propuesto para un proyecto que sirve web: **2 MB gzip por modelo**, **2048 px de lado mayor** por textura (es lo que el curso usa después de hornear y comprimir).

```bash
$ python3 studies/cute-room-portfolio-3d/web-asset-gate.py \
    projects/reinos-de-la-frontera/assets --max-glb 2.0 --max-tex 2048
ok     1.25 MB gz  projects/reinos-de-la-frontera/assets/quaternius/_download/Warrior.gltf
ok     1.25 MB gz  projects/reinos-de-la-frontera/assets/quaternius/rpg-characters/Warrior.gltf
ok     0.01 MB gz  projects/reinos-de-la-frontera/assets/quaternius/rts/Houses_FirstAge_1_Level1.gltf
ok     0.01 MB gz  projects/reinos-de-la-frontera/assets/quaternius/rts/Resource_Tree1.gltf
ok     0.01 MB gz  projects/reinos-de-la-frontera/assets/quaternius/rts/Rock.gltf
ok     0.01 MB gz  projects/reinos-de-la-frontera/assets/quaternius/rts/Wall_FirstAge.gltf
ok   512x512      165 KB  projects/reinos-de-la-frontera/assets/quaternius/_download/Warrior_Warrior_Sword_Texture.png
ok   1024x1024      677 KB  projects/reinos-de-la-frontera/assets/quaternius/_download/Warrior_Warrior_Texture.png
ok   512x512      165 KB  projects/reinos-de-la-frontera/assets/quaternius/rpg-characters/Warrior_Warrior_Sword_Texture.png
ok   1024x1024      677 KB  projects/reinos-de-la-frontera/assets/quaternius/rpg-characters/Warrior_Warrior_Texture.png

10 assets medidos, 0 fallas
EXIT=0
```

Con el presupuesto de un portfolio (un objeto estrella por página, no una escena) el gate **falla**, que es lo que tenía que demostrar. Este es el mismo comando con un techo más ajustado:

```bash
$ python3 studies/cute-room-portfolio-3d/web-asset-gate.py \
    projects/reinos-de-la-frontera/assets --max-glb 1.0 --max-tex 768
FAIL    1.25 MB gz  projects/reinos-de-la-frontera/assets/quaternius/_download/Warrior.gltf
FAIL    1.25 MB gz  projects/reinos-de-la-frontera/assets/quaternius/rpg-characters/Warrior.gltf
ok     0.01 MB gz  projects/reinos-de-la-frontera/assets/quaternius/rts/Houses_FirstAge_1_Level1.gltf
ok     0.01 MB gz  projects/reinos-de-la-frontera/assets/quaternius/rts/Resource_Tree1.gltf
ok     0.01 MB gz  projects/reinos-de-la-frontera/assets/quaternius/rts/Rock.gltf
ok     0.01 MB gz  projects/reinos-de-la-frontera/assets/quaternius/rts/Wall_FirstAge.gltf
ok   512x512      165 KB  projects/reinos-de-la-frontera/assets/quaternius/_download/Warrior_Warrior_Sword_Texture.png
FAIL  1024x1024      677 KB  projects/reinos-de-la-frontera/assets/quaternius/_download/Warrior_Warrior_Texture.png
ok   512x512      165 KB  projects/reinos-de-la-frontera/assets/quaternius/rpg-characters/Warrior_Warrior_Sword_Texture.png
FAIL  1024x1024      677 KB  projects/reinos-de-la-frontera/assets/quaternius/rpg-characters/Warrior_Warrior_Texture.png

10 assets medidos, 4 fallas
EXIT=1
```

**Verificado que el test falla de verdad**: el mismo binario da exit 0 con el presupuesto del engine y exit 1 con el de portfolio. Un gate que nunca falló no pasó ninguna prueba — esta es la lección del 2026-11-11 que ya estaba registrada en el daily de `reinos-de-la-frontera`.

**Hallazgo que el gate sacó solo:** `_download/` es una copia exacta de `rpg-characters/`. Los 1,25 MB gzip del `Warrior.gltf` están **duplicados**, igual que los 677 KB de textura. El presupuesto no es "cuánto pesa un archivo", es cuánto pesa **el paquete**; el gate mide por archivo y por eso no lo marca. El duplicado se resuelve quitando la carpeta de descarga, no comprimiendo más.

## Lo que este curso deja para más adelante

- **Paso de build que convierte PNG → WebP** y vuelve a correr el gate. Hoy no hay pipeline web en el proyecto, así que no hay dónde colgarlo.
- **Presupuesto por escena, no por archivo.** El gate mide archivo; un portfolio real pesa la suma. Se puede agregar un `--total` el día que exista una escena armada.
- **Regla del `_download/`.** Un asset descargado y su copia de trabajo no van los dos en el repo. Es una regla de repo, no de este gate: `CREDITS.md` ya documenta la procedencia, no hace falta conservar dos binarios.

## Por qué el resto del curso no cambia el workspace

- **El modelado en Blender** es habilidad, no proceso: no hay nada que "hacer mal" hoy salvo no saber modelar.
- **El material procedural** es igual: no tenemos escena propia con materiales en producción.
- **El bake** depende de un engine con su propio pipeline (Godot), y la regla del video es para Three.js.
- **El raycaster y los modales** son Three.js puro; no hay un proyecto con Three.js en el workspace. Si se construye uno, el módulo 12 del outline es el que se relee.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->

---

# Cierre del estudio práctico — 2026-11-12

Después de la clase, el estudio pasó a práctica real: construir el cuarto por script y
enseñarlo con renders. Se completaron **módulo 1** (vocabulario, con render antes/después
de subdividir) y **módulo 2** (bloqueo, pared con solidify, decisión de escena abierta).
El módulo 3 (props) quedó a medias a propósito.

## El artefacto que sí se ganó el lugar: `scene-gate.py`

**No es el que estaba planeado.** Se descubrió construyendo: en una sola sesión se
cometieron **seis errores del mismo tipo** — silla dada vuelta, monitor dado vuelta,
ruedas enterradas bajo el piso, teclas flotando 7 mm, piezas de mouse despegadas, y
teclas hundidas 12 mm dentro de la carcasa. Ninguno fue modelado. Todos fueron
**relación entre piezas**.

| Error real (fecha) | Qué falló | Qué chequea el gate |
|---|---|---|
| Ruedas a z=0.04, piso de 0.14 | objeto bajo el plano de apoyo | `HUNDIDO` por profundidad |
| Teclas 7 mm sobre la carcasa | objeto flotando | `FLOTANDO` por gap |
| Silla y monitor girados 180° | orientación | `ORIENTACION` vía `front_axis` |
| Mouse con piezas en el aire | pieza sin contacto | `DESPEGADO` vía `rests_on` |

**Contrato:** el script declara `rests_on` y `front_axis`; el gate verifica. Sin
declaración no hay chequeo — y eso es deliberado: un gate que adivina da falsos
positivos y se termina ignorando.

### Probado en las dos direcciones

```
$ Blender -b --python scene-gate.py -- --exec scripts/gate_test_broken.py
  FLOTANDO    flotando             100.0 mm sobre piso (limite 2.0)
  HUNDIDO     hundido              600.0 mm adentro de piso
  ORIENTACION dado_vuelta          su frente (+Y) apunta al reves de la camara (dot=-1.00)
5 objetos verificados, 3 hallazgos   EXIT=1

$ Blender -b --python scene-gate.py -- --exec scripts/gate_test_clean.py
3 objetos verificados, 0 hallazgos   EXIT=0
```

### El hallazgo que justifica todo el ejercicio

Corrido sobre el teclado real, el gate reportó:

```
HUNDIDO  k_3_8  12.5 mm adentro de carcasa (56/56 vertices pasan el plano)
64 objetos verificados, 63 hallazgos  {'HUNDIDO': 63}
```

Yo había medido esas mismas teclas con raycast y había dicho «GAP −0.0009, está bien».
**Las dos mediciones eran del mismo objeto y decían cosas distintas.** El raycast
comparaba un punto; el gate cuenta los 56 vértices. Las teclas estaban 12 mm adentro.
El render no lo mostraba porque la carcasa es curva y el hueco quedaba oculto por el bevel.

Lección: **una medición puntual no valida un apoyo.** Hay que medir la pieza entera
contra la superficie entera.

### Ajustes al gate que salieron de probarlo

1. **Default `rests_on="floor"` eliminado.** En el teclado dio 63 FLOTANDO falsos
   (las teclas apoyan en la carcasa, no en el piso). Pasó a ser contrato explícito.
2. **HUNDIDO por profundidad, no por conteo de vértices.** Contar vértices bajo un
   plano marca error en cualquier superficie curva con una pieza bien puesta.

Un gate que grita cuando todo está bien es un gate que se ignora.

## Gotchas de Blender headless (no están en el video)

- **`bpy.ops.transform.rotate` no hace nada en `-b`.** No hay área 3D en el contexto:
  el operador retorna sin error y sin efecto. Verificado 2026-11-12 (la carcasa seguía
  plana después de llamarlo). Hay que rotar por `matrix_world`.
- **`bpy.ops.*` en general es frágil headless.** Los operadores que dependen de
  selección/contexto necesitan `view_layer.objects.active` + `select_set` explícitos.
- **`BLENDER_EEVEE_NEXT` no existe en 5.3**: el enum es `BLENDER_EEVEE`.
- **`World.use_nodes` está deprecado** en 5.3 (se remueve en 6.0); funciona igual.

## Estado del cuarto (no terminado)

| Pieza | Estado |
|---|---|
| Distribución de la escena | ✅ escritorio, silla en ángulo, cuadro, cama de Benny |
| Pared abierta en L, piso con bevel | ✅ |
| Teclado | ⚠️ forma correcta (taper, espaciador, flechas, inclinado), **12 mm hundido — el gate lo marca** |
| Mouse | ❌ dos intentos fallidos, forma todavía no legible |
| Monitor | ⚠️ caja con panel, sin bisel ni detalle |
| Silla | ⚠️ bloques, sin detalle |

**Deuda declarada:** el teclado se hunde y el mouse no está resuelto. Ambos se detectan
con el gate y se retoman cuando haya tiempo.
