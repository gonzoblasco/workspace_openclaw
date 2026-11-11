extends SceneTree
var SimState = preload("res://sim/sim_state.gd")

func _init():
    var state = SimState.new(42, 96, 96)
    var e1 = state.add_entity(1, Vector2i(3, 4))
    var e2 = state.add_entity(2, Vector2i(5, 6))
    # Enqueue some movement commands.
    state.enqueue_move(e1, Vector2i(10, 10), 1)
    state.enqueue_move(e2, Vector2i(11, 11), 2)
    # Run a few ticks.
    for i in range(5):
        state.step()
    var dict = state.to_dict()
    var hash_before = state.hash_state()
    # Re‑create from dict.
    var new_state = SimState.new()
    new_state.from_dict(dict)
    var dict2 = new_state.to_dict()
    var hash_after = new_state.hash_state()
    if dict != dict2:
        push_error("State round‑trip dict mismatch")
        quit(1)
        return
    if hash_before != hash_after:
        push_error("Hash mismatch after round‑trip")
        quit(1)
        return
    if dict.get("schema_version", 0) != SimState.SCHEMA_VERSION:
        push_error("Incorrect schema version")
        quit(1)
        return
    # Verify hash changes when tick advances.
    state.step()
    var hash_changed = state.hash_state()
    if hash_changed == hash_before:
        push_error("Hash did not change after tick advance")
        quit(1)
        return
    print("STATE_OK")
    quit()

