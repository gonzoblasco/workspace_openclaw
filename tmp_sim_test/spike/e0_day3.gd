extends Node3D

# Controller for the minimal select‑move‑attack loop.

var selected: Node3D = null
@onready var selection_ring: MeshInstance3D = $SelectionRing

func _ready() -> void:
    # Ensure the selection ring starts hidden, then auto-select Player for the initial capture.
    selection_ring.visible = false
    # Auto-select the Player unit so that the selection ring is visible in the screenshot.
    selected = $Player
    selection_ring.global_transform.origin = $Player.global_transform.origin + Vector3(0, 0.02, 0)
    selection_ring.visible = true

func pick_at(world_pos: Vector3) -> bool:
    # Find the nearest unit (Player or Enemy) within 1.0 m.
    var candidates := [ $Player, $Enemy ]
    var nearest: Node3D = null
    var nearest_dist: float = INF
    for unit in candidates:
        var d: float = unit.global_transform.origin.distance_to(world_pos)
        if d <= 1.0 and d < nearest_dist:
            nearest = unit
            nearest_dist = d
    if nearest:
        selected = nearest
        selection_ring.global_transform.origin = nearest.global_transform.origin + Vector3(0, 0.02, 0)
        selection_ring.visible = true
        return true
    else:
        selected = null
        selection_ring.visible = false
        return false

func command_at(world_pos: Vector3) -> void:
    if selected == null:
        return
    # Determine if an enemy of the selected unit is within 1.0 m of the target point.
    var enemy_candidate: Node3D = null
    for unit in [ $Player, $Enemy ]:
        if unit != selected and unit.team != selected.team:
            var d: float = unit.global_transform.origin.distance_to(world_pos)
            if d <= 1.0:
                enemy_candidate = unit
                break
    if enemy_candidate:
        selected.order_attack(enemy_candidate)
    else:
        selected.order_move(world_pos)

func _unhandled_input(event) -> void:
    if not event is InputEventMouseButton:
        return
    if not event.pressed:
        return
    var cam: Camera3D = $Camera3D
    var from: Vector3 = cam.project_ray_origin(event.position)
    var to: Vector3 = from + cam.project_ray_normal(event.position) * 1000.0
    var plane: Plane = Plane(Vector3.UP, 0.0)
    var intersect: Vector3 = plane.intersects_ray(from, to)
    if event.button_index == MOUSE_BUTTON_LEFT:
        pick_at(intersect)
    elif event.button_index == MOUSE_BUTTON_RIGHT:
        command_at(intersect)

func _process(_delta: float) -> void:
    # Keep the selection ring positioned on the selected unit.
    if selected:
        selection_ring.global_transform.origin = selected.global_transform.origin + Vector3(0, 0.02, 0)
    # Visibility already handled in pick_at/command_at.
    pass

