extends SceneTree
var SimClock = preload("res://sim/clock.gd")

func _init():
	# One second fed as 30 small steps == exactly 30 ticks.
	var clock = SimClock.new()
	var total = 0
	for i in range(SimClock.TICK_RATE):
		total += clock.advance(1.0 / float(SimClock.TICK_RATE))
	if total != SimClock.TICK_RATE:
		_fail("30 small advances expected %d got %d" % [SimClock.TICK_RATE, total])
		return
	if clock.accumulator >= SimClock.TICK_DT:
		_fail("accumulator should be below one tick, got %f" % clock.accumulator)
		return

	# A long frame is clamped to max_ticks_per_advance, not simulated in full.
	var big = SimClock.new()
	var ticks = big.advance(1.0)
	if ticks != 5:
		_fail("advance(1.0) should clamp to 5, got %d" % ticks)
		return
	var huge = SimClock.new()
	if huge.advance(10.0) != 5:
		_fail("advance(10.0) should clamp to 5")
		return
	print("CLOCK_OK")
	quit()

func _fail(message: String) -> void:
	push_error(message)
	quit(1)
