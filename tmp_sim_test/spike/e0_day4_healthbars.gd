extends Control

# E0 Day 4: one 2D layer for 200 health bars and selection markers.
var camera: Camera3D
var units: Array = []
var selected: Array = []

var _frame := 0

func _process(_delta: float) -> void:
	_frame += 1
	if _frame % 2 == 0:
		queue_redraw()

func _draw() -> void:
	if camera == null:
		return
	for unit in units:
		if unit.get("state") == "dead":
			continue
		var world: Vector3 = unit.global_transform.origin + Vector3(0, 2.1, 0)
		if camera.is_position_behind(world):
			continue
		var p := camera.unproject_position(world)
		var hp := float(unit.get("hp"))
		var max_hp := maxf(1.0, float(unit.get("max_hp")))
		draw_rect(Rect2(p.x - 11.0, p.y, 22.0, 4.0), Color(0, 0, 0, 0.65))
		draw_rect(Rect2(p.x - 11.0, p.y, 22.0 * clampf(hp / max_hp, 0.0, 1.0), 4.0), Color(0.25, 0.90, 0.30, 1))
	for unit in selected:
		var feet: Vector3 = unit.global_transform.origin
		if camera.is_position_behind(feet):
			continue
		var fp := camera.unproject_position(feet)
		draw_arc(fp, 9.0, 0.0, TAU, 20, Color(1.0, 0.9, 0.2, 0.9), 1.5)
