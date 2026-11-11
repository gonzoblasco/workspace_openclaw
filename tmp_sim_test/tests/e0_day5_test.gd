extends SceneTree

# E0 Day 5 acceptance: visual composition, palette shader, outline and shadows.
func _initialize() -> void:
	var scene: Node = load("res://spike/e0_day5.tscn").instantiate()
	get_root().add_child(scene)
	process_frame.connect(_check.bind(scene), CONNECT_ONE_SHOT)

func _check(scene: Node) -> void:
	var cam := scene.get_node("Camera3D") as Camera3D
	if cam.projection != Camera3D.PROJECTION_ORTHOGONAL or not is_equal_approx(cam.size, 11.0):
		_fail("camera is not orthographic size 11")
		return
	var light := scene.get_node("DirectionalLight3D") as DirectionalLight3D
	if not light.shadow_enabled:
		_fail("directional light has no shadows")
		return
	if scene.get_node("Trees").get_child_count() != 3:
		_fail("trees != 3")
		return
	if scene.get_node("Rocks").get_child_count() != 2:
		_fail("rocks != 2")
		return
	if scene.get_node("Walls").get_child_count() != 2:
		_fail("walls != 2")
		return
	var units := scene.get_node("Units").get_children()
	if units.size() != 14:
		_fail("units=%d, expected 14" % units.size())
		return
	var rect := scene.get_node("PaletteLayer/ColorRect") as ColorRect
	var mat := rect.material as ShaderMaterial
	if mat == null:
		_fail("palette layer has no ShaderMaterial")
		return
	var palette = mat.get_shader_parameter("palette")
	if palette == null or palette.size() != 16:
		_fail("palette uniform missing or size != 16")
		return
	# The outline is applied at runtime as material_overlay on every mesh.
	var outlined := 0
	for mi in scene.find_children("*", "MeshInstance3D", true, false):
		if mi.material_overlay != null:
			outlined += 1
	if outlined == 0:
		_fail("no mesh has an outline overlay")
		return
	print("DAY5_OK units=14 meshes_outlined=%d palette=16" % outlined)
	scene.free()
	quit(0)

func _fail(message: String) -> void:
	push_error(message)
	quit(1)
