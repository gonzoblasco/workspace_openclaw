extends Node3D

# E0 Day 4: 200 units, box selection, 2D health bars, fog shader, minimap.
# Benchmark mode: pass `-- --benchmark` on the command line.

const UNIT_SCENE: PackedScene = preload("res://assets/quaternius/rpg-characters/Warrior.gltf")
const UNIT_SCRIPT: Script = preload("res://spike/e0_day4_unit.gd")
const PLAYER_COUNT := 100
const ENEMY_COUNT := 100
const COLS := 10
const SPACING := 2.0
const FLOOR_SIZE := 40.0
const FOG_SIZE := 48
const MINIMAP_SIZE := 96
const FOG_INTERVAL := 0.5
const MINIMAP_INTERVAL := 0.5
const BENCH_WARMUP := 10.0
const BENCH_SAMPLE := 60.0
const CSV_PATH := "res://docs/captures/e0-day4_metrics.csv"

var units: Array[Node3D] = []
var selected: Array[Node3D] = []

var _fog_image: Image
var _fog_texture: ImageTexture
var _minimap_image: Image
var _minimap_texture: ImageTexture
var _timer_fog := 0.0
var _timer_minimap := 0.0
var _dragging := false
var _drag_start := Vector2.ZERO
var _drag_end := Vector2.ZERO

var _bench := false
var _bench_short := false
var _warmup := BENCH_WARMUP
var _sample_len := BENCH_SAMPLE
var _no_shadows := false
var _no_bars := false
var _no_fog := false
var _no_minimap := false
var _bench_elapsed := 0.0
var _bench_sample := 0.0
var _last_us := 0
var _finished := false
var _frame_ms: PackedFloat32Array = []
var _draw_calls: PackedInt32Array = []

@onready var camera: Camera3D = $Camera3D
@onready var floor_mi: MeshInstance3D = $Floor
@onready var healthbars: Control = $UI/HealthBars
@onready var selection_box: Control = $UI/SelectionBox
@onready var minimap: TextureRect = $UI/Minimap

func _ready() -> void:
	_bench = OS.get_cmdline_user_args().has("--benchmark")
	_bench_short = OS.get_cmdline_user_args().has("--bench-short")
	_no_shadows = OS.get_cmdline_user_args().has("--no-shadows")
	_no_bars = OS.get_cmdline_user_args().has("--no-bars")
	_no_fog = OS.get_cmdline_user_args().has("--no-fog")
	_no_minimap = OS.get_cmdline_user_args().has("--no-minimap")
	if _bench_short:
		_warmup = 3.0
		_sample_len = 10.0
	if _no_shadows:
		($DirectionalLight3D as DirectionalLight3D).shadow_enabled = false
	if _no_bars:
		healthbars.visible = false
		healthbars.set_process(false)
	_spawn_units()
	_init_fog()
	_init_minimap()
	healthbars.set("camera", camera)
	healthbars.set("units", units)
	healthbars.set("selected", selected)
	_update_fog()
	_update_minimap()
	_select_initial_units()
	if _bench:
		if DisplayServer.get_name() == "headless":
			push_error("benchmark requires a real renderer")
			get_tree().quit(1)
			return
		DisplayServer.window_set_vsync_mode(DisplayServer.VSYNC_DISABLED)
		Engine.max_fps = 0
		print("DAY4_WINDOW=", DisplayServer.window_get_size(), " adapter=", RenderingServer.get_video_adapter_name())
		_last_us = Time.get_ticks_usec()

func _spawn_units() -> void:
	var root := $Units
	for i in PLAYER_COUNT:
		_spawn_unit(root, i, 0, Vector3(-20.0 + (i % COLS) * SPACING, 0.0, -9.0 + (i / COLS) * SPACING))
	for i in ENEMY_COUNT:
		_spawn_unit(root, i + PLAYER_COUNT, 1, Vector3(2.0 + (i % COLS) * SPACING, 0.0, -9.0 + (i / COLS) * SPACING))

func _spawn_unit(root: Node3D, index: int, team: int, pos: Vector3) -> void:
	var unit: Node3D = UNIT_SCENE.instantiate()
	unit.scale = Vector3(0.78, 0.78, 0.78)
	unit.position = pos
	unit.set_script(UNIT_SCRIPT)
	unit.set("team", team)
	unit.set("phase", float(index) * 0.37)
	root.add_child(unit)
	units.append(unit)

func _init_fog() -> void:
	_fog_image = Image.create(FOG_SIZE, FOG_SIZE, false, Image.FORMAT_RGBA8)
	_fog_image.fill(Color(0, 0, 0, 1))
	_fog_texture = ImageTexture.create_from_image(_fog_image)
	var mat := floor_mi.material_override as ShaderMaterial
	if mat:
		mat.set_shader_parameter("fog_mask", _fog_texture)

func _init_minimap() -> void:
	_minimap_image = Image.create(MINIMAP_SIZE, MINIMAP_SIZE, false, Image.FORMAT_RGBA8)
	_minimap_image.fill(Color(0.05, 0.06, 0.07, 1))
	_minimap_texture = ImageTexture.create_from_image(_minimap_image)
	minimap.texture = _minimap_texture

func _process(delta: float) -> void:
	_timer_fog += delta
	_timer_minimap += delta
	if not _no_fog and _timer_fog >= FOG_INTERVAL:
		_update_fog()
		_timer_fog = 0.0
	if not _no_minimap and _timer_minimap >= MINIMAP_INTERVAL:
		_update_minimap()
		_timer_minimap = 0.0
	if _bench and not _finished:
		_benchmark_tick()

func _benchmark_tick() -> void:
	var now := Time.get_ticks_usec()
	var frame_ms := float(now - _last_us) / 1000.0
	_last_us = now
	_bench_elapsed += frame_ms / 1000.0
	if _bench_elapsed < _warmup:
		return
	_frame_ms.append(frame_ms)
	_draw_calls.append(RenderingServer.get_rendering_info(RenderingServer.RENDERING_INFO_TOTAL_DRAW_CALLS_IN_FRAME))
	_bench_sample += frame_ms / 1000.0
	if _bench_sample >= _sample_len:
		_finish_benchmark()

func _finish_benchmark() -> void:
	_finished = true
	var sorted := _frame_ms.duplicate()
	sorted.sort()
	var n := sorted.size()
	if n == 0:
		push_error("benchmark collected no frames")
		get_tree().quit(1)
		return
	var p50: float = sorted[clampi(int(round((n - 1) * 0.50)), 0, n - 1)]
	var p95: float = sorted[clampi(int(round((n - 1) * 0.95)), 0, n - 1)]
	var p99: float = sorted[clampi(int(round((n - 1) * 0.99)), 0, n - 1)]
	var worst: float = sorted[n - 1]
	var over33 := 0
	for t in _frame_ms:
		if t > 33.0:
			over33 += 1
	var ratio := float(over33) / float(n)
	var draw_avg := 0.0
	for d in _draw_calls:
		draw_avg += float(d)
	draw_avg /= maxf(1.0, float(_draw_calls.size()))

	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path("res://docs/captures"))
	var f := FileAccess.open(CSV_PATH, FileAccess.WRITE)
	if f:
		f.store_line("frame,time_s,frame_ms,draw_calls,units")
		for i in n:
			f.store_line("%d,%.4f,%.4f,%d,%d" % [i, float(i) * _sample_len / float(n), _frame_ms[i], _draw_calls[i], units.size()])
		f.close()

	var verdict := "PASS" if p95 <= 16.7 and p99 <= 16.7 and ratio <= 0.001 else "FAIL"
	print("DAY4_SUMMARY units=%d frames=%d p50_ms=%.3f p95_ms=%.3f p99_ms=%.3f max_ms=%.3f over33=%d (%.4f%%) draw_calls_avg=%.1f verdict=%s" % [units.size(), n, p50, p95, p99, worst, over33, ratio * 100.0, draw_avg, verdict])
	get_tree().quit(0)

# --- Selection and commands ---

func _select_initial_units() -> void:
	selected.clear()
	for unit in units:
		if unit.get("team") == 0:
			selected.append(unit)
			if selected.size() == 12:
				break
	healthbars.queue_redraw()

func _select_all_player_units() -> void:
	selected.clear()
	for unit in units:
		if unit.get("team") == 0:
			selected.append(unit)
	healthbars.queue_redraw()

func select_in_rect(rect: Rect2) -> void:
	selected.clear()
	for unit in units:
		if unit.get("team") != 0:
			continue
		var world := unit.global_transform.origin + Vector3(0, 0.9, 0)
		if camera.is_position_behind(world):
			continue
		if rect.has_point(camera.unproject_position(world)):
			selected.append(unit)
	healthbars.queue_redraw()

func pick_at(world_pos: Vector3) -> bool:
	var nearest: Node3D = null
	var best := 1.0
	for unit in units:
		if unit.get("team") != 0:
			continue
		var d := unit.global_transform.origin.distance_to(world_pos)
		if d < best:
			best = d
			nearest = unit
	selected.clear()
	if nearest:
		selected.append(nearest)
	healthbars.queue_redraw()
	return nearest != null

func command_at(world_pos: Vector3) -> void:
	if selected.is_empty():
		return
	var n := selected.size()
	var cols := int(ceil(sqrt(float(n))))
	var rows := int(ceil(float(n) / float(cols)))
	for i in n:
		var off := Vector3(
			(float(i % cols) - float(cols - 1) / 2.0) * 0.9,
			0.0,
			(float(i / cols) - float(rows - 1) / 2.0) * 0.9
		)
		selected[i].call("order_move", world_pos + off)

func _ground_point(screen_pos: Vector2) -> Variant:
	var from := camera.project_ray_origin(screen_pos)
	var dir := camera.project_ray_normal(screen_pos)
	var hit = Plane(Vector3.UP, 0.0).intersects_ray(from, dir)
	return hit

func _unhandled_input(event) -> void:
	if event is InputEventMouseButton:
		if event.button_index == MOUSE_BUTTON_LEFT:
			if event.pressed:
				_dragging = true
				_drag_start = event.position
				_drag_end = event.position
				_update_selection_box()
			else:
				if _dragging:
					_dragging = false
					var rect := Rect2(_drag_start, _drag_end - _drag_start).abs()
					selection_box.set("active", false)
					selection_box.queue_redraw()
					if rect.size.length() < 6.0:
						var hit = _ground_point(event.position)
						if hit != null:
							pick_at(hit)
					else:
						select_in_rect(rect)
		elif event.button_index == MOUSE_BUTTON_RIGHT and event.pressed:
			var hit = _ground_point(event.position)
			if hit != null:
				command_at(hit)
	elif event is InputEventMouseMotion and _dragging:
		_drag_end = event.position
		_update_selection_box()

func _update_selection_box() -> void:
	selection_box.set("active", true)
	selection_box.set("rect", Rect2(_drag_start, _drag_end - _drag_start).abs())
	selection_box.queue_redraw()

# --- Fog and minimap ---

func _update_fog() -> void:
	for unit in units:
		if unit.get("team") == 0:
			_reveal(unit.global_transform.origin.x, unit.global_transform.origin.z, 6.0)
	_fog_texture.update(_fog_image)

func _reveal(world_x: float, world_z: float, radius: float) -> void:
	var cx := int((world_x + FLOOR_SIZE / 2.0) / FLOOR_SIZE * float(FOG_SIZE - 1))
	var cz := int((world_z + FLOOR_SIZE / 2.0) / FLOOR_SIZE * float(FOG_SIZE - 1))
	var r := int(radius / FLOOR_SIZE * float(FOG_SIZE - 1)) + 1
	for y in range(maxi(0, cz - r), mini(FOG_SIZE, cz + r + 1)):
		for x in range(maxi(0, cx - r), mini(FOG_SIZE, cx + r + 1)):
			if Vector2(float(x - cx), float(y - cz)).length() <= float(r):
				_fog_image.set_pixel(x, y, Color(1, 1, 1, 1))

func _update_minimap() -> void:
	_minimap_image.fill(Color(0.05, 0.06, 0.07, 1))
	for unit in units:
		var color := Color(0.25, 0.95, 0.35, 1) if unit.get("team") == 0 else Color(0.95, 0.25, 0.25, 1)
		_draw_dot(unit.global_transform.origin, color, 1)
	for house in $Houses.get_children():
		_draw_dot(house.global_transform.origin, Color(0.85, 0.85, 0.85, 1), 2)
	for tree in $Trees.get_children():
		_draw_dot(tree.global_transform.origin, Color(0.20, 0.60, 0.25, 1), 1)
	_minimap_texture.update(_minimap_image)

func _draw_dot(world: Vector3, color: Color, half: int) -> void:
	var px := int(clampf((world.x + FLOOR_SIZE / 2.0) / FLOOR_SIZE * float(MINIMAP_SIZE - 1), 0, MINIMAP_SIZE - 1))
	var pz := int(clampf((world.z + FLOOR_SIZE / 2.0) / FLOOR_SIZE * float(MINIMAP_SIZE - 1), 0, MINIMAP_SIZE - 1))
	for y in range(maxi(0, pz - half), mini(MINIMAP_SIZE, pz + half + 1)):
		for x in range(maxi(0, px - half), mini(MINIMAP_SIZE, px + half + 1)):
			_minimap_image.set_pixel(x, y, color)
