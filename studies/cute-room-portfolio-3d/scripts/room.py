"""Cuarto con los tres pedidos: silla gamer, cuadro, cama de Benny bajo el cuadro.

Convencion de ejes: +Y es la pared del fondo. La camara mira desde -Y hacia +Y,
o sea: ve el interior. La silla queda DE ESPALDAS a esa pared (+Y) y el respaldo
toca la pared; el cuerpo mira hacia -Y, hacia afuera del cubo.
"""
import bpy, math, mathutils, sys

def clean():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.context.scene.render.engine = 'BLENDER_EEVEE'
    w = bpy.data.worlds.new("W"); bpy.context.scene.world = w
    w.use_nodes = True
    bg = w.node_tree.nodes["Background"]
    bg.inputs[0].default_value = (0.04, 0.045, 0.06, 1)
    bg.inputs[1].default_value = 1.0

def mat(ob, color, rough=0.7, metal=0.0):
    m = bpy.data.materials.new(ob.name + "_m")
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*color, 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    ob.data.materials.append(m)
    return m

def bevel_smooth(ob, w=0.02, seg=3):
    b = ob.modifiers.new("Bevel", 'BEVEL'); b.width = w; b.segments = seg
    bpy.context.view_layer.objects.active = ob
    bpy.ops.object.shade_smooth()

def cube(name, loc, scale, rot=(0, 0, 0), color=(0.5, 0.5, 0.55), rough=0.7, bv=None):
    bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rot)
    ob = bpy.context.active_object; ob.name = name
    ob.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    mat(ob, color, rough)
    if bv: bevel_smooth(ob, *bv)
    return ob

def cyl(name, loc, r, depth, rot=(0, 0, 0), color=(0.2, 0.2, 0.22), verts=24):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=depth, location=loc,
                                        rotation=rot, vertices=verts)
    ob = bpy.context.active_object; ob.name = name
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    mat(ob, color, 0.5, 0.6)
    return ob

# ---------------- escena ----------------
clean()
W, D, H = 3.6, 2.8, 2.9          # medio ancho, medio fondo, alto
FLOOR_Y = D                      # pared del fondo en +Y

# piso
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0))
floor = bpy.context.active_object; floor.name = "piso"
floor.scale = (W + 0.6, D + 0.6, 1); bpy.ops.object.transform_apply(scale=True)
bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, 0.14)})
bpy.ops.object.mode_set(mode='OBJECT')
mat(floor, (0.30, 0.24, 0.21), 0.85); bevel_smooth(floor, 0.02, 2)

# paredes: planos extruidos con solidify (como el modulo)
def wall(name, loc, rot, sx, sy, color):
    bpy.ops.mesh.primitive_plane_add(size=1, location=loc, rotation=rot)
    w = bpy.context.active_object; w.name = name
    w.scale = (sx, sy, 1); bpy.ops.object.transform_apply(scale=True)
    s = w.modifiers.new("Solidify", 'SOLIDIFY'); s.thickness = 0.12
    b = w.modifiers.new("Bevel", 'BEVEL'); b.width = 0.05; b.segments = 3
    bpy.context.view_layer.objects.active = w; bpy.ops.object.shade_smooth()
    mat(w, color, 0.88)
    return w

WALL = (0.46, 0.40, 0.38)        # terracota apagado, mas calido que el gris
wall("pared_fondo", (0, FLOOR_Y, H / 2), (math.pi / 2, 0, 0), 2 * W, H, WALL)
wall("pared_izq", (-W, 0, H / 2), (math.pi / 2, 0, math.pi / 2), 2 * D, H, WALL)

# escritorio contra la pared del fondo, a la izquierda
DESK_X, DESK_Y = -1.35, FLOOR_Y - 0.42
cube("tabla", (DESK_X, DESK_Y, 1.02), (0.95, 0.36, 0.035), color=(0.42, 0.32, 0.26), bv=(0.01, 2))
# cuatro patas: dos en el frente, dos contra la pared. Sin las de atras se cae.
DESK_TABLE_Z = 1.02
for sx in (-1, 1):
    for sy in (-1, 1):
        cube(f"pata_{sx}_{sy}", (DESK_X + sx * 0.88, DESK_Y + sy * 0.30, DESK_TABLE_Z / 2),
             (0.028, 0.028, DESK_TABLE_Z / 2), color=(0.16, 0.16, 0.18))
# travesano entre las patas del fondo, donde apoyan
cube("travesano", (DESK_X, DESK_Y + 0.30, 0.18),
     (0.88, 0.02, 0.02), color=(0.16, 0.16, 0.18))
# monitor mirando hacia -Y (hacia afuera)
cube("monitor", (DESK_X, DESK_Y + 0.12, 1.42), (0.40, 0.025, 0.24),
     color=(0.07, 0.07, 0.09), rough=0.35, bv=(0.01, 3))
cube("monitor_pie", (DESK_X, DESK_Y + 0.14, 1.12), (0.10, 0.08, 0.06), color=(0.10, 0.10, 0.12))

# teclado y mouse: sobre la tabla, frente al monitor, del lado de quien se sienta
KB_Y = DESK_Y - 0.16
cube("teclado", (DESK_X, KB_Y, DESK_TABLE_Z + 0.055), (0.34, 0.12, 0.018),
     color=(0.11, 0.11, 0.13), rough=0.6, bv=(0.006, 2))
# filas de teclas: solo relieve, no 104 cubitos
for row in range(4):
    cube(f"teclas_{row}", (DESK_X, KB_Y - 0.075 + row * 0.05, DESK_TABLE_Z + 0.072),
         (0.315, 0.019, 0.004), color=(0.19, 0.19, 0.22), rough=0.7, bv=(0.002, 1))
# mouse a la derecha del teclado
bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(DESK_X + 0.52, KB_Y - 0.02, DESK_TABLE_Z + 0.075))
mouse = bpy.context.active_object; mouse.name = "mouse"
mouse.scale = (0.045, 0.065, 0.028)
bpy.ops.object.transform_apply(scale=True)
mat(mouse, (0.11, 0.11, 0.13), 0.5); bevel_smooth(mouse, 0.004, 2)

# ---------------- silla gamer ----------------
# La silla MIRA al fondo (+Y), al monitor. Respaldo del lado del cuarto (-Y).
# "Alguien acaba de levantarse": corrida hacia atras y girada ~25 grados.
SEAT_Z = 0.75                   # +50% a pedido: comparado visualmente con la mesa (1.02), 0.50 quedaba bajo
SEAT = (0.055, 0.055, 0.16)
ROJO = (0.42, 0.06, 0.06)
CHAIR_ROT = math.radians(24)
CX, CY = DESK_X + 0.62, FLOOR_Y - 1.62

# todo se construye en local y despues se rota alrededor de la columna
def place(lx, ly, lz, sx, sy, sz, name, color, rot_x=0.0, bv=(0.01, 2), rough=0.45):
    """Punto local de la silla -> mundo, con las dos rotaciones aplicadas por separado.

    El error anterior: pasar rot=(rot_x, 0, CHAIR_ROT) al operador escala por los
    ejes del objeto y el resultado sale estirado (0.6 x 0.41 en vez de 0.58 x 0.10).
    Se construye con la escala, se aplica scale, y despues se rotan los euler.
    """
    wx = CX + lx * math.cos(CHAIR_ROT) - ly * math.sin(CHAIR_ROT)
    wy = CY + lx * math.sin(CHAIR_ROT) + ly * math.cos(CHAIR_ROT)
    bpy.ops.mesh.primitive_cube_add(location=(wx, wy, lz))
    ob = bpy.context.active_object; ob.name = name
    ob.scale = (sx, sy, sz)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    ob.rotation_euler = (rot_x, 0, CHAIR_ROT)
    mat(ob, color, rough)
    if bv: bevel_smooth(ob, *bv)
    return ob

# asiento a 0.50: la columna arranca abajo del asiento
place(0, 0, SEAT_Z, 0.30, 0.28, 0.06, "asiento", SEAT, bv=(0.025, 3))
# respaldo: 0.30 del centro del asiento hacia el respaldo (-Y local)
place(0, -0.27, SEAT_Z + 0.42, 0.29, 0.05, 0.35, "respaldo", SEAT,
      rot_x=math.radians(-10), bv=(0.025, 3))
place(0, -0.297, SEAT_Z + 0.42, 0.055, 0.02, 0.30, "franja_respaldo", ROJO,
      rot_x=math.radians(-10), bv=(0.006, 2), rough=0.4)
for sx in (-1, 1):
    place(sx * 0.29, 0.02, SEAT_Z + 0.29, 0.03, 0.25, 0.035, f"apoya_{sx}", SEAT)
    place(sx * 0.335, -0.02, SEAT_Z + 0.29, 0.05, 0.19, 0.02, f"brazo_{sx}", SEAT, rough=0.5)

# columna: del piso al asiento, con un tramo de gas
FLOOR_TOP = 0.14               # el piso tiene 14 cm de espesor: nada de la silla va por debajo
col_h = SEAT_Z - FLOOR_TOP - 0.06
cyl("columna", (CX, CY, FLOOR_TOP + 0.06 + col_h / 2), 0.05, col_h,
    color=(0.14, 0.14, 0.16))
# base tipo estrella con SEIS ruedas
LEGS, LEG_R = 6, 0.27
for i in range(LEGS):
    a = math.radians(i * 360 / LEGS)
    # la pata va del centro hacia afuera, en local y rotada con la silla
    mid = LEG_R * 0.55
    place(math.cos(a) * mid, math.sin(a) * mid, FLOOR_TOP + 0.035,
          LEG_R * 0.55, 0.022, 0.022, f"pata_{i}", (0.14, 0.14, 0.16),
          bv=(0.008, 2), rough=0.5)
    # la rotacion de la pata tiene que ser radial: se corrige despues
    ob = bpy.data.objects[f"pata_{i}"]
    ob.rotation_euler.z = a + CHAIR_ROT
    # rueda en la punta
    wx = CX + math.cos(a) * LEG_R * math.cos(CHAIR_ROT) - math.sin(a) * LEG_R * math.sin(CHAIR_ROT)
    wy = CY + math.cos(a) * LEG_R * math.sin(CHAIR_ROT) + math.sin(a) * LEG_R * math.cos(CHAIR_ROT)
    cyl(f"rueda_{i}", (wx, wy, FLOOR_TOP + 0.028), 0.033, 0.024, rot=(math.pi / 2, 0, a),
        color=(0.05, 0.05, 0.06), verts=16)

# ---------------- cuadro en la pared del fondo ----------------
PX, PZ = 0.85, 1.72
cube("cuadro_marco", (PX, FLOOR_Y - 0.075, PZ), (0.52, 0.012, 0.38),
     color=(0.22, 0.16, 0.10), bv=(0.004, 2))
cube("cuadro_lienzo", (PX, FLOOR_Y - 0.083, PZ), (0.465, 0.006, 0.325),
     color=(0.55, 0.62, 0.52), rough=0.95)
# una franja de color adentro, para que no sea un rectangulo vacio
cube("cuadro_detalle", (PX + 0.07, FLOOR_Y - 0.088, PZ - 0.05), (0.16, 0.003, 0.12),
     color=(0.72, 0.45, 0.30), rough=0.95)

# ---------------- cama de Benny, bajo el cuadro ----------------
BX, BY = PX, FLOOR_Y - 0.46
bpy.ops.mesh.primitive_cylinder_add(radius=0.44, depth=0.15, location=(BX, BY, 0.075),
                                    vertices=40)
bed = bpy.context.active_object; bed.name = "cama_benny"
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
mat(bed, (0.30, 0.36, 0.50), 0.9); bevel_smooth(bed, 0.03, 3)
# almohadon interior, mas claro
bpy.ops.mesh.primitive_cylinder_add(radius=0.33, depth=0.07, location=(BX, BY, 0.088),
                                    vertices=40)
pad = bpy.context.active_object; pad.name = "almohadon"
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
mat(pad, (0.62, 0.66, 0.76), 0.95); bevel_smooth(pad, 0.025, 3)

# ---------------- camara y luces ----------------
for loc, e, col in [((2.4, -4.2, 2.6), 500, (1.0, 0.92, 0.82)),
                    ((-2.2, -1.0, 2.2), 180, (0.75, 0.82, 1.0))]:
    ld = bpy.data.lights.new("L", 'AREA'); ld.energy = e; ld.size = 3.0; ld.color = col
    lo = bpy.data.objects.new("L", ld); bpy.context.scene.collection.objects.link(lo)
    lo.location = loc
    d = mathutils.Vector((0, 0.5, 1.0)) - mathutils.Vector(loc)
    lo.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()

def shoot(name, loc, look, lens=48, res=(1400, 900)):
    cd = bpy.data.cameras.new("C"); cd.lens = lens
    cam = bpy.data.objects.new("C", cd); bpy.context.scene.collection.objects.link(cam)
    cam.location = loc
    d = mathutils.Vector(look) - mathutils.Vector(loc)
    cam.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    bpy.context.scene.camera = cam
    s = bpy.context.scene; s.render.resolution_x, s.render.resolution_y = res
    s.render.filepath = f"/tmp/quadlab/{name}.png"
    bpy.ops.render.render(write_still=True)
    bpy.data.objects.remove(cam, do_unlink=True)

shoot("v2_frontal", (0.3, -4.7, 2.9), (0.1, 1.2, 1.25), lens=42)
shoot("v2_detalle_silla", (-0.55, -2.7, 1.75), (-1.35, 1.5, 0.85), lens=58)
shoot("v2_detalle_benny", (0.75, -2.4, 1.35), (0.85, 2.5, 0.75), lens=55)
print("V2 OK")

# --- probe: donde esta todo lo de la silla ---
print("\n=== PROBE SILLA ===")
for ob in sorted(bpy.data.objects, key=lambda o: o.name):
    if any(k in ob.name for k in ("rueda", "pata_", "columna", "asiento", "respaldo")):
        print(f"{ob.name:20} loc=({ob.location.x:6.2f},{ob.location.y:6.2f},{ob.location.z:6.2f})  dim={tuple(round(v,3) for v in ob.dimensions)}")
print("PISO z:", [ (o.name, tuple(round(v,3) for v in o.dimensions)) for o in bpy.data.objects if o.name=="piso"])
print("=== END PROBE ===")
