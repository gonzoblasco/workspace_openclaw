"""Teclado estilizado pero con detalle real: perfil de tecla, fila espaciadora,
bloques de modificadores, hueco entre grupos. Low-poly: se lee por silueta."""
import bpy, math, mathutils

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene; sc.render.engine = 'BLENDER_EEVEE'
w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True
w.node_tree.nodes["Background"].inputs[0].default_value = (0.045, 0.045, 0.06, 1)
w.node_tree.nodes["Background"].inputs[1].default_value = 1.0

def mat(ob, color, rough=0.6):
    m = bpy.data.materials.new(ob.name + "_m"); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*color, 1)
    b.inputs["Roughness"].default_value = rough
    ob.data.materials.append(m); return m

def key(name, x, y, z, w=1.0, h=1.0, color=(0.62, 0.62, 0.66)):
    """Tecla con perfil: base ancha, tope mas chico (el taper de una tecla real)."""
    bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
    ob = bpy.context.active_object; ob.name = name
    ob.scale = (0.0092 * w, 0.0092 * h, 0.0032)
    bpy.ops.object.transform_apply(scale=True)
    # bisel generoso: la tecla estilizada se lee por el redondeo
    bv = ob.modifiers.new("Bevel", 'BEVEL'); bv.width = 0.0022; bv.segments = 2
    # taper: escalar la cara superior hacia adentro
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    for p in ob.data.polygons:
        if p.normal.z > 0.9: p.select = True
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.transform.resize(value=(0.82, 0.82, 1), orient_type='GLOBAL')
    bpy.ops.object.mode_set(mode='OBJECT')
    ob["rests_on"] = "carcasa"
    mat(ob, color, 0.55)
    bpy.context.view_layer.objects.active = ob; bpy.ops.object.shade_smooth()
    return ob

# ---------- carcasa del teclado ----------
BW, BD, BH = 0.44, 0.155, 0.020      # ancho, profundidad, alto
bpy.ops.mesh.primitive_cube_add(location=(0, 0, BH / 2))
case = bpy.context.active_object; case.name = "carcasa"
case.scale = (BW / 2, BD / 2, BH / 2)
bpy.ops.object.transform_apply(scale=True)
bv = case.modifiers.new("Bevel", 'BEVEL'); bv.width = 0.004; bv.segments = 3
case["rests_on"] = "floor"
mat(case, (0.16, 0.16, 0.19), 0.55)
bpy.context.view_layer.objects.active = case; bpy.ops.object.shade_smooth()

# La tecla se APOYA en la carcasa: su centro va a carcasa_top + mitad de su alto.
# KEY_HALF es la mitad del alto de la tecla (cubo de 0.0064 -> 0.0032), + el bevel
# que sobresale un pelin. Sumar TOP primero y despues un offset era el bug: hacia
# flotar las teclas 7 mm sobre el teclado.
KEY_HALF = 0.0032
# inclinacion: la fila del fondo (y+) va 1.5 mm mas alta, pero SIEMPRE apoyada
Z_BACK  = BH + KEY_HALF          # fila del fondo, apoyada sobre la carcasa
Z_FRONT = BH + KEY_HALF + 0     # mismo plano: la carcasa ya tiene el angulo

# ---------- teclas ----------
# filas: y crece hacia el fondo. 5 filas de alfanumerico + espacio + modificadores
N_COLS = 14
KEY_PITCH_X = 0.0265
KEY_PITCH_Y = 0.0255
x0 = -(N_COLS - 1) * KEY_PITCH_X / 2
rows_y = [0.042, 0.017, -0.008, -0.033]
count = 0

for ri, ry in enumerate(rows_y):
    z = Z_BACK
    # la fila del fondo (numeros) es continua; la de letras tiene el hueco del Enter
    for c in range(N_COLS):
        x = x0 + c * KEY_PITCH_X
        kw = 1.0
        # teclas de modificador: la primera y la ultima de varias filas son mas anchas
        if c == 0 and ri in (0, 1, 2): kw = 1.5
        if c == N_COLS - 1 and ri in (1, 2): kw = 1.5
        key(f"k_{ri}_{c}", x, ry, z, w=kw)
        count += 1

# fila espaciadora
SPACE_Y = -0.062
key("espaciadora", 0, SPACE_Y, Z_FRONT, w=6.4, h=1.0)
count += 1
# teclas chicas a los lados del espacio
for sx, nm in [(-1, "alt_izq"), (1, "alt_der")]:
    key(nm, sx * 0.135, SPACE_Y, Z_FRONT, w=1.4)
    count += 1
# flechas, a la derecha, un bloque aparte
for i, (dx, dy, nm) in enumerate([(0, 0.008, "arriba"), (0, -0.008, "abajo"),
                                  (-0.010, 0, "izq"), (0.010, 0, "der")]):
    key(f"flecha_{nm}", 0.175 + dx, -0.062 + dy, Z_FRONT, w=1.0)
    count += 1

print(f"\n=== TECLADO ===")
print(f"teclas: {count}")

# ---------- inclinacion: rotar el grupo entero, no cada tecla ----------
# Un teclado real tiene la fila del fondo ~6 grados mas alta. La tecla y la carcasa
# giran juntas, asi ninguna tecla se despega: es una rotacion rigida del conjunto.
#
# GOTCHA: bpy.ops.transform.rotate NO hace nada en modo headless (-b): no hay area
# 3D en el contexto y el operador retorna sin error pero sin efecto. Verificado el
# 2026-11-12: la carcasa seguia plana (sup=0.0200) despues de llamarlo. Rotar por
# matrix_world es lo unico que funciona sin UI.
TILT = math.radians(6.0)
PIVOT = mathutils.Vector((0, -BD / 2, 0.0))
R = mathutils.Matrix.Rotation(TILT, 4, 'X')
T = mathutils.Matrix.Translation(-PIVOT)
Tinv = mathutils.Matrix.Translation(PIVOT)
M = Tinv @ R @ T
board = [o for o in bpy.data.objects
         if o.name.startswith(("k_", "espaciadora", "alt", "flecha", "carcasa"))]
for ob in board:
    ob.matrix_world = M @ ob.matrix_world

# ---------- medicion: caras de una tecla y del teclado ----------
dg = bpy.context.evaluated_depsgraph_get()
one = bpy.data.objects["k_0_0"].evaluated_get(dg)
me = one.to_mesh(); faces_one = len(me.polygons); one.to_mesh_clear()
total = sum(len(o.evaluated_get(dg).to_mesh().polygons)
            for o in bpy.data.objects if o.name.startswith(("k_", "espaciadora", "alt", "flecha")))
print(f"caras por tecla: {faces_one}")
print(f"caras totales de teclas: {total}")
print(f"carcasa: {len(case.evaluated_get(dg).to_mesh().polygons)}")

# ---------- render ----------
TABLE_Z = 1.00
for loc, e in [((0.5, -0.9, 1.9), 90), ((-0.6, -0.5, 1.7), 40)]:
    ld = bpy.data.lights.new("L", 'AREA'); ld.energy = e; ld.size = 1.6
    lo = bpy.data.objects.new("L", ld); sc.collection.objects.link(lo); lo.location = loc
    d = mathutils.Vector((0, 0, 1)) - mathutils.Vector(loc)
    lo.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()

cd = bpy.data.cameras.new("C"); cd.lens = 90
cam = bpy.data.objects.new("C", cd); sc.collection.objects.link(cam); sc.camera = cam
cam.location = (0.18, -0.42, 0.32)
d = mathutils.Vector((0, 0, 0.02)) - mathutils.Vector(cam.location)
cam.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
sc.render.resolution_x, sc.render.resolution_y = 1400, 950
sc.render.filepath = "/tmp/quadlab/m3b_teclado.png"
bpy.ops.render.render(write_still=True)
print("M3B OK")

print("\n=== CONTACTO TECLA / CARCASA (local de la carcasa) ===")
dg2 = bpy.context.evaluated_depsgraph_get()
CASE = bpy.data.objects["carcasa"]
case_ev = CASE.evaluated_get(dg2)
case_me = case_ev.to_mesh()          # malla ya evaluada, en espacio LOCAL del objeto
inv = CASE.matrix_world.inverted()   # mundo -> local de la carcasa
for nm in ("k_0_0", "k_2_0", "espaciadora", "flecha_abajo"):
    ob = bpy.data.objects.get(nm)
    if not ob: continue
    # centro de la tecla en mundo, pasado a local de la carcasa
    c = ob.matrix_world @ mathutils.Vector(ob.bound_box[0])
    cw = sum((ob.matrix_world @ mathutils.Vector(b) for b in ob.bound_box),
             mathutils.Vector()) / 8
    cl = inv @ cw
    zmin_w = min((ob.matrix_world @ mathutils.Vector(b)).z for b in ob.bound_box)
    hit, loc, nrm, idx = case_ev.ray_cast(
        mathutils.Vector((cl.x, cl.y, cl.z + 1.0)), mathutils.Vector((0, 0, -1)))
    if hit:
        surf_world = (CASE.matrix_world @ loc).z
        print(f"  {nm:14} zmin={zmin_w:.4f}  sup={surf_world:.4f}  GAP={zmin_w - surf_world:+.5f}")
    else:
        print(f"  {nm:14} zmin={zmin_w:.4f}  SUP=NO HIT (la tecla no esta sobre la carcasa)")
case_ev.to_mesh_clear()
print("=== END CONTACTO ===")
