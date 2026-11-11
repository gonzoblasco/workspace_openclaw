extends SceneTree

# E0 Day 4 performance acceptance: same criteria as Day 2, full scene.
const CSV_PATH := "res://docs/captures/e0-day4_metrics.csv"
const MAX_P95_MS := 16.7
const MAX_P99_MS := 16.7
const MAX_OVER33_RATIO := 0.001

func _initialize() -> void:
	var f := FileAccess.open(CSV_PATH, FileAccess.READ)
	if f == null:
		_fail("missing %s; run the --benchmark scene first" % CSV_PATH)
		return
	var header := f.get_csv_line()
	if header.size() < 5:
		_fail("bad CSV header")
		return
	var times: Array[float] = []
	var units := 0
	while not f.eof_reached():
		var row := f.get_csv_line()
		if row.size() < 5:
			continue
		times.append(float(row[2]))
		units = int(row[4])
	f.close()

	if units != 200:
		_fail("units=%d, expected 200" % units)
		return
	if times.size() < 1000:
		_fail("only %d frames sampled" % times.size())
		return

	var sorted := times.duplicate()
	sorted.sort()
	var n := sorted.size()
	var p95: float = sorted[clampi(int(round((n - 1) * 0.95)), 0, n - 1)]
	var p99: float = sorted[clampi(int(round((n - 1) * 0.99)), 0, n - 1)]
	var worst: float = sorted[n - 1]
	var over33 := 0
	for t in times:
		if t > 33.0:
			over33 += 1
	var ratio := float(over33) / float(n)

	if p95 > MAX_P95_MS:
		_fail("p95 %.3f ms > %.1f" % [p95, MAX_P99_MS])
		return
	if p99 > MAX_P99_MS:
		_fail("p99 %.3f ms > %.1f" % [p99, MAX_P99_MS])
		return
	if ratio > MAX_OVER33_RATIO:
		_fail("%d/%d frames > 33 ms (%.4f > %.4f)" % [over33, n, ratio, MAX_OVER33_RATIO])
		return

	print("DAY4_OK frames=%d p95_ms=%.3f p99_ms=%.3f max_ms=%.3f over33=%d (%.4f%%)" % [n, p95, p99, worst, over33, ratio * 100.0])
	quit(0)

func _fail(message: String) -> void:
	push_error(message)
	quit(1)
