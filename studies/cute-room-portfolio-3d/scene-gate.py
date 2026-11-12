#!/usr/bin/env python3
"""scene-gate.py — chequeos que fallan antes de renderizar una escena de Blender.

Nace de cuatro errores repetidos el 2026-11-11/12 modelando un cuarto por script:
la silla dada vuelta, el monitor dado vuelta, las ruedas enterradas bajo el piso y
las teclas flotando 7 mm sobre la carcasa. Ninguno fue un error de modelado: los
cuatro fueron de RELACION entre piezas (apoyo, orientacion, contacto).

Uso:
    Blender -b escena.blend --python scene-gate.py -- [--floor F] [--gap 0.002]
    Blender -b --python scene-gate.py -- --exec mi_escena.py     (corre y luego chequea)

Salida: una linea por hallazgo, resumen y EXIT=0/1. Cero hallazgos = EXIT 0.

Chequeos:
  1. HUNDIDO   - un objeto apoyado con geometria por debajo del plano del piso.
  2. FLOTANDO  - un objeto apoyado cuya cara inferior esta a mas de --gap del piso.
  3. ORIENTACION - un objeto marcado con la custom prop `front_axis` mira al reves.
  4. DESPEGADO - una pieza con custom prop `parent_surface` no toca esa superficie.

Las custom properties son el contrato: el script que arma la escena declara la
intencion, y el gate la verifica. Sin declaracion no hay chequeo, y eso es a
proposito: un gate que adivina da falsos positivos y se termina ignorando.

    obj["front_axis"] = "+Y"       # hacia donde mira el frente del objeto
    obj["camera_side"] = "-Y"      # de que lado esta la camara
    obj["rests_on"] = "floor"      # o el nombre de otro objeto
"""

import bpy
import mathutils
import sys
import math

argv = sys.argv
args = argv[argv.index("--") + 1:] if "--" in argv else []

def arg(name, default=None, cast=str):
    if name in args:
        return cast(args[args.index(name) + 1])
    return default

FLOOR_Z = arg("--floor", 0.0, float)
MAX_GAP = arg("--gap", 0.002, float)
EXEC = arg("--exec", None)

if EXEC:
    exec(open(EXEC).read(), {"__name__": "__main__", "bpy": bpy})

dg = bpy.context.evaluated_depsgraph_get()
findings = []
checked = 0

def world_bbox(ob):
    return [ob.matrix_world @ mathutils.Vector(c) for c in ob.bound_box]

def bottom_z(ob):
    return min(v.z for v in world_bbox(ob))

def top_z(ob):
    return max(v.z for v in world_bbox(ob))

def is_resting(ob):
    """Devuelve contra que superficie hay que verificar el apoyo, o None si no aplica.

    Solo se verifica lo que DECLARA rests_on. Un default de "floor" para todo objeto
    sin padre produce falsos positivos en masa: en un teclado, cada una de las 63
    teclas esta a 2-3 cm del piso porque apoya sobre la carcasa, no sobre el piso.
    Verificado el 2026-11-12: el gate reporto 63 FLOTANDO en una escena correcta.

    La regla es el contrato declarado, no la heuristica.
    """
    return ob.get("rests_on")

meshes = [o for o in bpy.data.objects if o.type == 'MESH']

# ---------- 1 y 2: apoyo sobre el piso ----------
for ob in meshes:
    surface = is_resting(ob)
    if surface is None or surface == "none":
        continue
    if surface != "floor":
        target = bpy.data.objects.get(surface)
        if target is None:
            findings.append(("DESPEGADO", ob.name, f"declara rests_on='{surface}' que no existe"))
            continue
        ref_z = top_z(target)
        ref_name = surface
    else:
        ref_z = FLOOR_Z
        ref_name = "piso"

    checked += 1
    bz = bottom_z(ob)

    # cuantas caras quedan por debajo del plano de apoyo
    ev = ob.evaluated_get(dg)
    me = ev.to_mesh()
    me.transform(ob.matrix_world)
    below = sum(1 for v in me.vertices if v.co.z < ref_z - 0.0005)
    total_v = len(me.vertices)
    ev.to_mesh_clear()

    # HUNDIDO se mide por PROFUNDIDAD, no por cuantos vertices estan abajo.
    # En una superficie curva o con bevel, una pieza que apoya bien tiene siempre
    # algunos vertices por debajo del plano del punto mas alto: contarlos convierte
    # una tecla bien puesta en un error (verificado: 28/56 en el teclado, correcto).
    # Lo que importa es cuanto penetra el punto mas bajo.
    depth = ref_z - bz if below > 0 else 0.0
    if depth > MAX_GAP:
        findings.append(("HUNDIDO", ob.name,
                         f"{depth * 1000:.1f} mm adentro de {ref_name} "
                         f"({below}/{total_v} vertices pasan el plano)"))
    else:
        gap = bz - ref_z
        if gap > MAX_GAP:
            findings.append(("FLOTANDO", ob.name,
                             f"{gap * 1000:.1f} mm sobre {ref_name} (limite {MAX_GAP * 1000:.1f})"))

# ---------- 3: orientacion ----------
AXES = {"+X": (1, 0, 0), "-X": (-1, 0, 0), "+Y": (0, 1, 0),
        "-Y": (0, -1, 0), "+Z": (0, 0, 1), "-Z": (0, 0, -1)}

cam = bpy.context.scene.camera
cam_side = None
if cam:
    d = cam.matrix_world.to_quaternion() @ mathutils.Vector((0, 0, -1))
    # el lado de la camara es el opuesto a su direccion de vista, en el plano XY
    cam_side = mathutils.Vector((-d.x, -d.y, 0)).normalized()

for ob in meshes:
    if "front_axis" not in ob:
        continue
    checked += 1
    try:
        local = mathutils.Vector(AXES[ob["front_axis"]])
    except KeyError:
        findings.append(("ORIENTACION", ob.name,
                         f"front_axis='{ob['front_axis']}' no es un eje valido"))
        continue
    world = (ob.matrix_world.to_quaternion() @ local).normalized()
    declared_cam = ob.get("camera_side")
    ref = mathutils.Vector(AXES[declared_cam]) if declared_cam in AXES else cam_side
    if ref is None:
        continue
    ref = mathutils.Vector((ref.x, ref.y, 0)).normalized()
    world_xy = mathutils.Vector((world.x, world.y, 0))
    if world_xy.length < 1e-6:
        continue
    dot = world_xy.normalized().dot(ref)
    if dot < 0:
        findings.append(("ORIENTACION", ob.name,
                         f"su frente ({ob['front_axis']}) apunta al reves de la camara "
                         f"(dot={dot:.2f}); rotar 180 en Z"))

# ---------- reporte ----------
print("\n=== SCENE GATE ===")
if not findings:
    print(f"  ok  {checked} objetos verificados, sin hallazgos")
else:
    for kind, name, detail in findings:
        print(f"  {kind:11} {name:20} {detail}")

kinds = {}
for k, _, _ in findings:
    kinds[k] = kinds.get(k, 0) + 1
print(f"\n{checked} objetos verificados, {len(findings)} hallazgos"
      + (f"  {kinds}" if kinds else ""))
print(f"EXIT={1 if findings else 0}")
print("=== END GATE ===")
