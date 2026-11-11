extends Node3D

# E0 Day 5: visual pass. Palette + depth outline post-process, warm light,
# and a small composition for the final spike capture.

const UNIT_SCENE: PackedScene = preload("res://assets/quaternius/rpg-characters/Warrior.gltf")
const TEAM_SHADER: Shader = preload("res://spike/e0_day5_team.gdshader")
const PALETTE := [
	Vector3(0.07, 0.06, 0.05), # ink
	Vector3(0.16, 0.14, 0.12), # dark
	Vector3(0.30, 0.28, 0.24), # stone dark
	Vector3(0.48, 0.45, 0.39), # stone light
	Vector3(0.30, 0.20, 0.13), # wood dark
	Vector3(0.55, 0.34, 0.20), # wood light
	Vector3(0.64, 0.30, 0.18), # roof terracotta
	Vector3(0.22, 0.32, 0.15), # grass dark
	Vector3(0.36, 0.48, 0.22), # grass light
	Vector3(0.55, 0.42, 0.28), # dirt
	Vector3(0.82, 0.64, 0.44), # skin
	Vector3(0.24, 0.35, 0.43), # cloth blue
	Vector3(0.60, 0.62, 0.64), # metal
	Vector3(0.78, 0.64, 0.16), # gold
	Vector3(0.46, 0.18, 0.18), # crimson
	Vector3(0.85, 0.82, 0.74), # off-white
]

@onready var palette_rect: ColorRect = $PaletteLayer/ColorRect

func _ready() -> void:
	var mat := palette_rect.material as ShaderMaterial
	if mat:
		mat.set_shader_parameter("palette", PALETTE)
	_spawn_units()
	_apply_outline(self)

func _apply_outline(node: Node) -> void:
	var outline := StandardMaterial3D.new()
	outline.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	outline.albedo_color = Color(0.06, 0.05, 0.04)
	outline.cull_mode = BaseMaterial3D.CULL_FRONT
	outline.grow = true
	outline.grow_amount = 0.02
	for child in node.get_children():
		if child is MeshInstance3D:
			(child as MeshInstance3D).material_overlay = outline
		_apply_outline(child)

func _spawn_units() -> void:
	var positions := [
		Vector3(-1.2, 0, 2.2), Vector3(-0.2, 0, 3.0), Vector3(0.8, 0, 2.4),
		Vector3(-1.0, 0, 4.0), Vector3(0.2, 0, 4.4), Vector3(1.2, 0, 3.8),
		Vector3(2.2, 0, 3.0), Vector3(2.0, 0, 4.6),
		Vector3(4.6, 0, -0.6), Vector3(5.4, 0, 0.2), Vector3(4.2, 0, 0.8),
		Vector3(5.8, 0, 1.4), Vector3(6.4, 0, -0.2), Vector3(3.8, 0, -1.4),
	]
	for i in positions.size():
		var unit: Node3D = UNIT_SCENE.instantiate()
		unit.scale = Vector3(0.78, 0.78, 0.78)
		unit.position = positions[i]
		unit.rotation_degrees = Vector3(0, 180.0 if i < 8 else 0.0, 0)
		$Units.add_child(unit)
		var team_color := Color(0.18, 0.32, 0.62) if i < 8 else Color(0.62, 0.16, 0.12)
		_tint_team(unit, team_color)
		var anim := unit.get_node("AnimationPlayer") as AnimationPlayer
		if anim and anim.has_animation("Idle"):
			anim.play("Idle")

func _tint_team(unit: Node3D, color: Color) -> void:
	for mesh_name in ["Warrior_Body", "ShoulderPad_L", "ShoulderPad_R"]:
		var mi := unit.find_child(mesh_name, true, false) as MeshInstance3D
		if mi == null:
			continue
		var base := mi.get_active_material(0) as StandardMaterial3D
		if base == null:
			continue
		var mat := ShaderMaterial.new()
		mat.shader = TEAM_SHADER
		mat.set_shader_parameter("albedo_tex", base.albedo_texture)
		mat.set_shader_parameter("team_color", color)
		mat.set_shader_parameter("mix_amount", 0.65)
		mi.material_override = mat
