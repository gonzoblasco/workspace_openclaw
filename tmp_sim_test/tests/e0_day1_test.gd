extends SceneTree

# E0 Day 1 acceptance test: orthographic camera, 1 m tile, 1.8 m character.
func _initialize() -> void:
	var scene: Node = load("res://spike/e0_day1.tscn").instantiate()
	get_root().add_child(scene)
	process_frame.connect(_check.bind(scene), CONNECT_ONE_SHOT)

func _check(scene: Node) -> void:
	var cam := scene.get_node("Camera3D") as Camera3D
	if cam.projection != Camera3D.PROJECTION_ORTHOGONAL:
		_fail("camera projection is not orthogonal")
		return
	if not is_equal_approx(cam.size, 14.0):
		_fail("camera size != 14")
		return
	if not is_equal_approx(cam.near, 0.1):
		_fail("camera near != 0.1")
		return
	if not is_equal_approx(cam.far, 200.0):
		_fail("camera far != 200")
		return
	if not cam.rotation_degrees.is_equal_approx(Vector3(-30, 45, 0)):
		_fail("camera rotation != (-30, 45, 0)")
		return
	if cam.position.is_equal_approx(Vector3.ZERO):
		_fail("camera position is zero")
		return

	var tile := scene.get_node("TileReference") as MeshInstance3D
	var box := tile.mesh as BoxMesh
	if not box.size.is_equal_approx(Vector3(1, 1, 1)):
		_fail("tile reference is not 1x1x1")
		return

	var warrior := scene.get_node("Warrior") as Node3D
	var skeleton := warrior.get_node("CharacterArmature/Skeleton3D") as Skeleton3D
	var head_idx := skeleton.find_bone("Head")
	if head_idx == -1:
		_fail("Head bone not found")
		return
	var head_global: Vector3 = skeleton.global_transform * skeleton.get_bone_global_pose(head_idx).origin
	if absf(head_global.y - 1.64) > 0.06:
		_fail("head global Y %.3f is not ~1.64 (character is not 1.8 m tall)" % head_global.y)
		return
	if absf(warrior.position.x - 1.5) > 0.01:
		_fail("warrior is not at x=1.5")
		return

	var anim := warrior.get_node("AnimationPlayer") as AnimationPlayer
	if anim == null or not anim.has_animation("Idle"):
		_fail("AnimationPlayer missing Idle")
		return
	if anim.current_animation != "Idle" or not anim.is_playing():
		_fail("Idle is not playing")
		return

	print("DAY1_OK")
	scene.free()
	quit(0)

func _fail(message: String) -> void:
	push_error(message)
	quit(1)
