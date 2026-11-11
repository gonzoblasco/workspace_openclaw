extends SceneTree
var SimPathfind = preload("res://sim/pathfind.gd")
var SimState = preload("res://sim/sim_state.gd")

func _init():
    var pf = SimPathfind.new(96, 96)
    # Place a solid obstacle at (5,5).
    pf.set_solid(Vector2i(5, 5), true)
    var start = Vector2i(1, 1)
    var target = Vector2i(10, 10)
    var path = pf.find_path(start, target)
    if path.size() == 0:
        push_error("Pathfinder returned empty path")
        quit(1)
        return
    for cell in path:
        if cell == Vector2i(5, 5):
            push_error("Path includes solid cell (5,5)")
            quit(1)
            return
    # Create a SimState and move two entities to the target.
    var state = SimState.new(1, 96, 96)
    var e1 = state.add_entity(1, Vector2i(1, 1))
    var e2 = state.add_entity(2, Vector2i(2, 2))
    state.enqueue_move(e1, target, 1)
    state.enqueue_move(e2, target, 1)
    var max_steps = 5000
    for i in range(max_steps):
        state.step()
        var pos1 = state.get_entity_by_id(e1).cell
        var pos2 = state.get_entity_by_id(e2).cell
        if pos1 == target and pos2 == target:
            break
    if state.get_entity_by_id(e1).cell != target or state.get_entity_by_id(e2).cell != target:
        push_error("Entities did not reach target after steps")
        quit(1)
        return
    print("PATHFIND_OK")
    quit()

