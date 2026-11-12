"""Escena con errores REALES y medibles. Cada uno falla contra una regla distinta."""
import bpy, mathutils
bpy.ops.wm.read_factory_settings(use_empty=True)

bpy.ops.mesh.primitive_plane_add(size=6, location=(0,0,0))
floor = bpy.context.active_object; floor.name = "piso"
floor["rests_on"] = "none"

# 1. HUNDIDO: cubo de 1 m centrado en -0.1 -> 10 cm bajo el piso
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -0.1))
ob = bpy.context.active_object; ob.name = "hundido"
ob["rests_on"] = "floor"          # declara: apoya en el piso (y atraviesa)

# 2. FLOTANDO: cubo de 1 m centrado en 0.6 -> base a 10 cm del piso
bpy.ops.mesh.primitive_cube_add(size=1, location=(2, 0, 0.6))
ob = bpy.context.active_object; ob.name = "flotando"
ob["rests_on"] = "floor"          # declara: apoya en el piso (y queda 10 cm arriba)

# 3. ORIENTACION INVERTIDA: declara frente +Y y la camara esta en -Y
bpy.ops.mesh.primitive_cube_add(size=0.4, location=(-2, 0, 0.2))
ob = bpy.context.active_object; ob.name = "dado_vuelta"
ob["front_axis"] = "+Y"          # su frente apunta al fondo, lejos de la camara

# 4. OK: apoyado, y su frente -Y si mira a la camara
bpy.ops.mesh.primitive_cube_add(size=1, location=(5, 0, 0.5))
good = bpy.context.active_object; good.name = "ok_apoyado"
good["front_axis"] = "-Y"
good["rests_on"] = "floor"

cd = bpy.data.cameras.new("C"); cam = bpy.data.objects.new("C", cd)
bpy.context.scene.collection.objects.link(cam); bpy.context.scene.camera = cam
cam.location = (1.5, -9, 4)
d = mathutils.Vector((1.5, 0, 0.5)) - mathutils.Vector(cam.location)
cam.rotation_euler = d.to_track_quat('-Z','Y').to_euler()
print("TEST READY")
