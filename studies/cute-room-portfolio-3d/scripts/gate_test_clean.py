import bpy, mathutils
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.mesh.primitive_plane_add(size=6, location=(0,0,0))
bpy.context.active_object.name = "piso"
bpy.context.active_object["rests_on"] = "none"
for i, (x, sz) in enumerate([(0,1), (2,0.5), (4,0.8)]):
    bpy.ops.mesh.primitive_cube_add(size=sz, location=(x, 0, sz/2))   # apoyado exacto
    o = bpy.context.active_object; o.name = f"caja{i}"
    o["front_axis"] = "-Y"
cd = bpy.data.cameras.new("C"); cam = bpy.data.objects.new("C", cd)
bpy.context.scene.collection.objects.link(cam); bpy.context.scene.camera = cam
cam.location = (2, -9, 3)
d = mathutils.Vector((2,0,0.5)) - mathutils.Vector(cam.location)
cam.rotation_euler = d.to_track_quat('-Z','Y').to_euler()
