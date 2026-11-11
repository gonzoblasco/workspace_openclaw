# Stable command queue for deterministic simulation.

class_name SimCommands extends RefCounted

var _seq_counter: int = 0
var _queue: Array[Dictionary] = []

# Enqueue a command dictionary to be applied at the given tick.
func enqueue(cmd: Dictionary, apply_tick: int) -> void:
    var entry = cmd.duplicate()
    entry["apply_tick"] = apply_tick
    entry["seq"] = _seq_counter
    _seq_counter += 1
    _queue.append(entry)

# Return all commands whose apply_tick <= the supplied tick, in insertion order.
func drain(apply_tick: int) -> Array[Dictionary]:
    var ready: Array[Dictionary] = []
    var remaining: Array[Dictionary] = []
    for entry in _queue:
        if entry["apply_tick"] <= apply_tick:
            ready.append(entry)
        else:
            remaining.append(entry)
    _queue = remaining
    # The ready list preserves the order they were added because _queue was ordered.
    return ready

func size() -> int:
    return _queue.size()

