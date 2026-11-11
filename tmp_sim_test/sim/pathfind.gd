# Simple deterministic pathfinding using Godot's AStarGrid2D.

class_name SimPathfind extends RefCounted

var grid: AStarGrid2D

func _init(width: int = 96, height: int = 96) -> void:
    grid = AStarGrid2D.new()
    # Define the navigable region. Origin (0,0) inclusive.
    grid.region = Rect2i(0, 0, width, height)
    grid.cell_size = Vector2(1, 1)
    # Disallow diagonal movement as required.
    grid.diagonal_mode = AStarGrid2D.DIAGONAL_MODE_NEVER
    grid.update()

# Mark a cell as solid (impassable) or walkable.
func set_solid(cell: Vector2i, solid: bool = true) -> void:
    grid.set_point_solid(cell, solid)

# Compute a path from "from" to "to". Returns an Array of Vector2i.
func find_path(from: Vector2i, to: Vector2i) -> Array[Vector2i]:
    # Convert the grid's path (PackedVector2Array) to an Array of Vector2i.
    var raw_path = grid.get_point_path(from, to)
    var result: Array[Vector2i] = []
    for p in raw_path:
        # The grid uses integer coordinates; cast to Vector2i.
        result.append(Vector2i(p.x, p.y))
    return result

