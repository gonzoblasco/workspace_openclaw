extends SceneTree

func _initialize() -> void:
    var scene = load("res://main.tscn").instantiate()
    # Camera checks
    var cam = scene.get_node("Camera") as Camera3D
    if cam.projection != Camera3D.PROJECTION_ORTHOGONAL:
        push_error("Camera projection is not orthogonal")
        quit(1)
    if not is_equal_approx(cam.size, 14.0):
        push_error("Camera size not approx 14.0")
        quit(1)
    if not cam.rotation_degrees.is_equal_approx(Vector3(-30, 45, 0)):
        push_error("Camera rotation_degrees incorrect")
        quit(1)
    if cam.position == Vector3.ZERO:
        push_error("Camera position is zero")
        quit(1)
    # Floor mesh size
    var floor = scene.get_node("Floor") as MeshInstance3D
    var plane = floor.mesh as PlaneMesh
    if plane.size != Vector2(20, 20):
        push_error("Floor mesh size incorrect")
        quit(1)
    # Box mesh size
    var box = scene.get_node("Box") as MeshInstance3D
    var box_mesh = box.mesh as BoxMesh
    if box_mesh.size != Vector3(1, 1, 1):
        push_error("Box mesh size incorrect")
        quit(1)
    # Capsule mesh dimensions
    var capsule = scene.get_node("Capsule") as MeshInstance3D
    var cap_mesh = capsule.mesh as CapsuleMesh
    if not is_equal_approx(cap_mesh.height, 1.8) or not is_equal_approx(cap_mesh.radius, 0.3):
        push_error("Capsule mesh dimensions incorrect")
        quit(1)
    # Label text
    var label = scene.get_node("UI/Label") as Label
    if label.text == "":
        push_error("Label text is empty")
        quit(1)
    # All checks passed
    print("SCAFFOLD_OK")
    # Cleanup
    scene.free()
    quit(0)
