# ADOPCIÓN — Creative Web Development with Three.js and Blender

**Fecha:** 2026-11-11 · **Curso:** 05:39:21 · Andrew Woan / freeCodeCamp

**Pregunta:** ¿qué hacemos hoy mal en el workspace que este curso arregla?

## Veredicto

**Sí se adopta, con un artefacto:** `glb-budget.py`, un gate de presupuesto de assets 3D (tris, MB, clips de animación) que corre sobre un `.gltf`/`.glb`.

Por qué este y no otro: el curso tiene un módulo entero dedicado a **lo que se borra antes de exportar** («Preparing to export: checking normals, deleting faces, etc.», 02:18:52). Ese módulo existe porque un modelo que se ve bien en Blender puede ser basura en el browser: cubos apilados con geometría oculta, modificadores sin aplicar, caras que nunca se ven. La frase que lo justifica está en el Módulo 3 y no es estética: «the issue with overlapping geometry is that we're pretty much wasting information» (00:23:35).

En el workspace hay un proyecto 3D real con assets ya descargados que **nunca pasaron por una medición**: `projects/reinos-de-la-frontera/assets/`. Y hay un caso concreto donde el curso habría servido: `Warrior.gltf` pesa **2,89 MB con 5.402 tris** — el 83 % del peso es una textura PNG embebida de 693 KB más otra de 169 KB, sobre 1,6 MB de buffer en base64. Nadie lo había medido antes de hoy.

## Tabla

| Idea del curso (con t=) | Qué hacemos hoy | Artefacto verificable |
|---|---|---|
| Antes de exportar: aplicar modificadores, unir piezas por concepto, borrar caras que nunca se ven (02:18:52) | `assets/CREDITS.md` registra licencia y URL de cada asset, pero **ningún asset pasa por un chequeo de peso** antes de entrar al proyecto. `Warrior.gltf` entró a 2,89 MB y nadie lo miró | **`glb-budget.py`** — lee el glTF/GLB, calcula tris/verts/meshes/MB/clips y falla (exit 1) si pasa los presupuestos. Corrido abajo |
| La geometría solapada es información desperdiciada porque el browser es débil comparado con Blender (00:23:14, 00:23:35) | No hay regla escrita sobre tamaño de asset en ningún HANDOFF ni DECISIONS | **Mismo artefacto**, columna de tris. El presupuesto por defecto (20k tris, 5 MB, 20 clips) queda arriba de lo que hoy hay, así que no bloquea el trabajo: frena lo que venga |
| Exportar solo lo seleccionado con `Y up` y verificar en `threejs.org/editor` antes de escribir código (02:27:47, 02:30:43) | `reinos-de-la-frontera` no exporta desde Blender: los assets son de terceros ya hechos | **Candidato, no escrito.** No aplica hasta que el proyecto modele algo propio. Un chequeo de orientación solo tiene sentido cuando hay un paso de exportación que controlamos |
| Instancing (`Alt`+`D`) vs duplicado (`Shift`+`D`) para repeticiones (01:40:40) | Godot maneja instancing en el motor, no en el asset | **Sin adopción.** Es una técnica de Blender; el runtime de `reinos` usa `MultiMeshInstance3D`, que ya lo resuelve |
| El método para leer código ajeno: copiarlo a un archivo nuevo, comentar lo que se entiende, marcar lo que no (05:00:09) | Se lee código ajeno, pero sin un procedimiento escrito | **Candidato, no escrito.** Lo cubre en parte `delegation-result-verification` y la regla de verificar antes de confirmar. Un artefacto acá sería una plantilla de comentarios, y todavía no hay un caso donde el método actual haya fallado |

## El artefacto, corrido contra los assets reales del repo

```bash
$ python3 studies/creative-web-threejs-blender/glb-budget.py \
    projects/reinos-de-la-frontera/assets/quaternius/rpg-characters/Warrior.gltf
archivo   Warrior.gltf
tamano      2.89 MB  (payload embebido 2.41 MB)
geometria    5846 verts /    5402 tris / 5 meshes / 2 mats
anim      13 clips
ok
EXIT=0

$ python3 studies/creative-web-threejs-blender/glb-budget.py \
    projects/reinos-de-la-frontera/assets/quaternius/rts/Resource_Tree1.gltf
archivo   Resource_Tree1.gltf
tamano      0.02 MB  (payload embebido 0.01 MB)
geometria     296 verts /     552 tris / 1 meshes / 2 mats
anim      0 clips
ok
EXIT=0

$ python3 studies/creative-web-threejs-blender/glb-budget.py \
    projects/reinos-de-la-frontera/assets/quaternius/rts/Rock.gltf
archivo   Rock.gltf
tamano      0.01 MB  (payload embebido 0.01 MB)
geometria     196 verts /     162 tris / 1 meshes / 1 mats
anim      0 clips
ok
EXIT=0
```

**Qué prueba esto:** los cuatro assets de `reinos-de-la-frontera` pasan con los defaults (20k tris / 5 MB / 20 clips). El gate no encontró un bug — encontró que el presupuesto nunca había sido explícito. `Warrior.gltf` está a 2,89 MB con 5.402 tris: el margen lo da la textura, no la malla.

Y prueba que **muerde** cuando el presupuesto se aprieta, que es el uso real (un asset de fondo no necesita lo mismo que un personaje de primer plano):

```bash
$ python3 studies/creative-web-threejs-blender/glb-budget.py \
    projects/reinos-de-la-frontera/assets/quaternius/rpg-characters/Warrior.gltf \
    --mb 1 --tris 3000
archivo   Warrior.gltf
tamano      2.89 MB  (payload embebido 2.41 MB)
geometria    5846 verts /    5402 tris / 5 meshes / 2 mats
anim      13 clips
FAIL     tris 5402 > 3000; tamano 2.89 MB > 1.0 MB
EXIT=1

$ python3 studies/creative-web-threejs-blender/glb-budget.py /tmp/nope.glb
ERROR /tmp/nope.glb: [Errno 2] No such file or directory: '/tmp/nope.glb'
EXIT=2
```

Un archivo ilegible sale **2**, no 1: el script distingue «no pasa el presupuesto» de «no lo pude leer». Un gate que devuelve el mismo código para las dos cosas se ignora a la semana.

## Lo que el curso no cubre

- **Compresión real.** El curso no habla de Draco, meshopt, KTX2 ni de reducir texturas. El gate mide, no optimiza. Si mañana un asset falla, la salida es «comprimí o simplificá», y el procedimiento no está en el curso.
- **Bundling.** El video usa CDN y archivos planos a propósito: «for beginners, using a CDN is probably more understandable and less overwhelming» (02:38:02). Un proyecto con Vite/TypeScript no aprende acá cómo se integra `three` al build.
- **El paso de Blender a Godot.** Todo lo de los Módulos 3-7 es Blender→GLB→Three.js. `reinos-de-la-frontera` usa `.gltf` en Godot, con su propio importador. Lo que sí transfiere es el criterio (borrar lo invisible, unir por concepto, origen correcto), no los atajos.
- **Nada de accesibilidad ni de `prefers-reduced-motion`.** Para un portfolio 3D, es justo lo que falta: el curso no menciona qué pasa si el usuario tiene movimiento reducido o no puede usar mouse.

## Dónde quedó

- Script: `studies/creative-web-threejs-blender/glb-budget.py`
- Uso: `python3 studies/creative-web-threejs-blender/glb-budget.py <asset>.gltf [--tris N --mb N --anims N]`
- No se creó skill: por la regla del workspace, la skill se escribe recién cuando el artefacto sobrevivió a un uso real. Hoy tiene una corrida.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
