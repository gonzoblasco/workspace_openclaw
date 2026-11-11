# Fixed-rate simulation clock. Pure accumulator, no special cases.
class_name SimClock extends RefCounted

const TICK_RATE: int = 30
const TICK_DT: float = 1.0 / float(TICK_RATE)
const MAX_DELTA: float = 0.25

var accumulator: float = 0.0
var max_ticks_per_advance: int = 5

func advance(delta: float) -> int:
	# Clamp long frames so a stall does not produce a burst of simulation.
	accumulator += minf(delta, MAX_DELTA)
	var ticks := 0
	while accumulator >= TICK_DT - 1e-9 and ticks < max_ticks_per_advance:
		accumulator -= TICK_DT
		ticks += 1
	return ticks

func reset() -> void:
	accumulator = 0.0
