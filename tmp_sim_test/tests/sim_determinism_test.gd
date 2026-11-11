extends SceneTree
var SimState = preload("res://sim/sim_state.gd")

func _init():
    var seed = 42
    var width = 96
    var height = 96
    var state1 = SimState.new(seed, width, height)
    var state2 = SimState.new(seed, width, height)
    # Add identical entities.
    var e1a = state1.add_entity(1, Vector2i(1, 1))
    var e2a = state1.add_entity(2, Vector2i(2, 2))
    var e1b = state2.add_entity(1, Vector2i(1, 1))
    var e2b = state2.add_entity(2, Vector2i(2, 2))
    # Same target positions.
    var target1 = Vector2i(10, 10)
    var target2 = Vector2i(20, 20)
    state1.enqueue_move(e1a, target1, 1)
    state1.enqueue_move(e2a, target2, 1)
    state2.enqueue_move(e1b, target1, 1)
    state2.enqueue_move(e2b, target2, 1)
    var steps = 10000
    for i in range(steps):
        state1.step()
        state2.step()
    var hash1 = state1.hash_state()
    var hash2 = state2.hash_state()
    if hash1 != hash2:
        push_error("Determinism hash mismatch: %s vs %s" % [hash1, hash2])
        quit(1)
        return
    print("DETERMINISM_OK hash=%s ticks=%d" % [hash1, steps])
    quit()

