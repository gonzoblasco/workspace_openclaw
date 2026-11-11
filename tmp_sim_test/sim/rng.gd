# Deterministic random number generator using xorshift32.
# No reliance on Godot's global RNG.

class_name SimRNG extends RefCounted

# Internal 32‑bit state.
var state: int = 0

func _init(seed_value: int = 1) -> void:
    # Ensure state stays within 32‑bit unsigned range.
    state = seed_value & 0xFFFFFFFF
    if state == 0:
        state = 0x9E3779B9

# Xorshift32 algorithm (32‑bit unsigned integers).
func next_u32() -> int:
    # Perform bitwise operations with masking to emulate 32‑bit overflow.
    state ^= (state << 13) & 0xFFFFFFFF
    state ^= (state >> 17) & 0xFFFFFFFF
    state ^= (state << 5) & 0xFFFFFFFF
    state = state & 0xFFFFFFFF
    return state

# Return a float in the range [0, 1).
func next_float() -> float:
    # Divide by the maximum 32‑bit value (2^32‑1).
    return float(next_u32()) / 4294967296.0

# Return an integer in [0, max_exclusive).
func next_int(max_exclusive: int) -> int:
    if max_exclusive <= 0:
        push_error("SimRNG.next_int called with non‑positive max_exclusive: %d" % max_exclusive)
        return 0
    return int(next_u32() % max_exclusive)

# Get / set the internal state for serialization.
func get_state() -> int:
    return state

func set_state(value: int) -> void:
    state = value & 0xFFFFFFFF

