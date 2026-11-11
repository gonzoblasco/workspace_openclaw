extends Node3D

# E0 Day 2 benchmark: 200 animated Warrior instances, real renderer.
# Measures frame time with vsync off and Engine.max_fps = 0.
# Warm-up 10 s, sample 60 s, writes docs/captures/e0-day2_metrics.csv.

const UNIT_SCENE: PackedScene = preload("res://assets/quaternius/rpg-characters/Warrior.gltf")
const UNIT_COUNT := 200
const COLS := 20
const SPACING := 1.2
const WARMUP_SEC := 10.0
const SAMPLE_SEC := 60.0
const CSV_PATH := "res://docs/captures/e0-day2_metrics.csv"

var _units: Array[Node3D] = []
var _bases: Array[Vector3] = []
var _frame_ms: PackedFloat32Array = []
var _draw_calls: PackedInt32Array = []
var _elapsed := 0.0
var _sample_elapsed := 0.0
var _last_us := 0
var _finished := false

func _ready() -> void:
	if DisplayServer.get_name() == "headless":
		push_error("DAY2 requires a real renderer; --headless uses the dummy driver")
		get_tree().quit(1)
		return
	if DisplayServer.window_get_size().x < 3440 or DisplayServer.window_get_size().y < 1440:
		DisplayServer.window_set_size(Vector2i(3440, 1440))
	DisplayServer.window_set_vsync_mode(DisplayServer.VSYNC_DISABLED)
	Engine.max_fps = 0
	print("DAY2_WINDOW=", DisplayServer.window_get_size(), " adapter=", RenderingServer.get_video_adapter_name())
	_spawn_units()
	_last_us = Time.get_ticks_usec()

func _spawn_units() -> void:
	for i in UNIT_COUNT:
		var unit: Node3D = UNIT_SCENE.instantiate()
		unit.scale = Vector3(0.78, 0.78, 0.78)
		var col := i % COLS
		var row := i / COLS
		var base := Vector3((col - COLS / 2.0 + 0.5) * SPACING, 0.0, (row - 5.0 + 0.5) * SPACING)
		unit.position = base
		add_child(unit)
		var anim := unit.get_node("AnimationPlayer") as AnimationPlayer
		anim.play("Walk")
		anim.speed_scale = 1.0 + float(i % 7) * 0.03
		_units.append(unit)
		_bases.append(base)

func _process(_delta: float) -> void:
	if _finished:
		return
	var now := Time.get_ticks_usec()
	var frame_ms := float(now - _last_us) / 1000.0
	_last_us = now
	_elapsed += frame_ms / 1000.0

	_move_units(_elapsed)

	if _elapsed >= WARMUP_SEC:
		_frame_ms.append(frame_ms)
		_draw_calls.append(RenderingServer.get_rendering_info(RenderingServer.RENDERING_INFO_TOTAL_DRAW_CALLS_IN_FRAME))
		_sample_elapsed += frame_ms / 1000.0
		if _sample_elapsed >= SAMPLE_SEC:
			_finish()

func _move_units(t: float) -> void:
	for i in _units.size():
		var phase := t * 0.6 + float(i) * 0.37
		_units[i].position = _bases[i] + Vector3(cos(phase) * 0.35, 0.0, sin(phase) * 0.35)

func _finish() -> void:
	_finished = true
	var sorted := _frame_ms.duplicate()
	sorted.sort()
	var n := sorted.size()
	var p50 := sorted[clampi(int(round((n - 1) * 0.50)), 0, n - 1)]
	var p95 := sorted[clampi(int(round((n - 1) * 0.95)), 0, n - 1)]
	var p99 := sorted[clampi(int(round((n - 1) * 0.99)), 0, n - 1)]
	var worst := sorted[n - 1]
	var draw_avg := 0.0
	for d in _draw_calls:
		draw_avg += float(d)
	draw_avg /= maxf(1.0, float(_draw_calls.size()))

	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path("res://docs/captures"))
	var f := FileAccess.open(CSV_PATH, FileAccess.WRITE)
	if f:
		f.store_line("frame,time_s,frame_ms,draw_calls,units")
		for i in n:
			f.store_line("%d,%.4f,%.4f,%d,%d" % [i, float(i) * SAMPLE_SEC / float(n), _frame_ms[i], _draw_calls[i], UNIT_COUNT])
		f.close()

	var over33 := 0
	for t in _frame_ms:
		if t > 33.0:
			over33 += 1
	var over33_ratio := float(over33) / float(n)
	var verdict := "PASS" if p95 <= 16.7 and p99 <= 16.7 and over33_ratio <= 0.001 else "FAIL"
	print("DAY2_SUMMARY units=%d frames=%d p50_ms=%.3f p95_ms=%.3f p99_ms=%.3f max_ms=%.3f over33=%d (%.4f%%) draw_calls_avg=%.1f verdict=%s" % [UNIT_COUNT, n, p50, p95, p99, worst, over33, over33_ratio * 100.0, draw_avg, verdict])
	get_tree().quit(0)
