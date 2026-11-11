# Representation of an entity in the deterministic simulation.
class_name SimEntity extends RefCounted

var id: int = 0
var team: int = 0
var cell: Vector2i = Vector2i()
var hp: int = 100
# Last ordered destination. (-1,-1) means no order.
var target: Vector2i = Vector2i(-1, -1)
var path: Array[Vector2i] = []
var path_index: int = 0
var move_cooldown: int = 0

func to_dict() -> Dictionary:
	var path_data: Array = []
	for p in path:
		path_data.append([p.x, p.y])
	return {
		"id": id,
		"team": team,
		"cell_x": cell.x,
		"cell_y": cell.y,
		"hp": hp,
		"target_x": target.x,
		"target_y": target.y,
		"path": path_data,
		"path_index": path_index,
		"move_cooldown": move_cooldown,
	}

