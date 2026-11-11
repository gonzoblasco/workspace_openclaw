extends SceneTree

# E0 Day 4 acceptance: 200 units, box selection, fog mask, minimap, UI overlays.
func _initialize() -> void:
	var scene: Node = load("res://spike/e0_day4.tscn").instantiate()
	get_root().add_child(scene)
	process_frame.connect(_check.bind(scene), CONNECT_ONE_SHOT)

func _check(scene: Node) -> void:
	var units := scene.get_node("Units").get_children()
	if units.size() != 200:
		_fail("units=%d, expected 200" % units.size())
		return
	if scene.get_node("Houses").get_child_count() != 4:
		_fail("houses != 4")
		return
	if scene.get_node("Trees").get_child_count() != 6:
		_fail("trees != 6")
		return

	var selected: Array = scene.get("selected")
	if selected.size() != 12:
		_fail("initial selection=%d, expected 12" % selected.size())
		return
	for unit in selected:
		if unit.get("team") != 0:
			_fail("selected a non-player unit")
			return

	scene.call("_select_all_player_units")
	selected = scene.get("selected")
	if selected.size() != 100:
		_fail("select_all=%d, expected 100" % selected.size())
		return

	# A rect covering the whole possible projection must select exactly the 100 player units.
	scene.select_in_rect(Rect2(-10000, -10000, 20000, 20000))
	selected = scene.get("selected")
	if selected.size() != 100:
		_fail("rect selection=%d, expected 100" % selected.size())
		return

	# Fog must have explored (bright) and unexplored (dark) texels.
	scene.call("_update_fog")
	var fog: Image = scene.get("_fog_image")
	var bright := 0
	var dark := 0
	for y in fog.get_height():
		for x in fog.get_width():
			var r := fog.get_pixel(x, y).r
			if r > 0.5:
				bright += 1
			elif r < 0.1:
				dark += 1
	if bright == 0:
		_fail("fog mask has no explored texels")
		return
	if dark == 0:
		_fail("fog mask has no unexplored texels")
		return

	# Minimap must contain at least one non-background pixel.
	scene.call("_update_minimap")
	var mm: Image = scene.get("_minimap_image")
	var colored := 0
	for y in mm.get_height():
		for x in mm.get_width():
			var c := mm.get_pixel(x, y)
			if absf(c.r - 0.05) > 0.01 or absf(c.g - 0.06) > 0.01:
				colored += 1
	if colored == 0:
		_fail("minimap has no drawn pixels")
		return

	for path in ["UI/HealthBars", "UI/SelectionBox", "UI/Minimap"]:
		if not scene.has_node(path):
			_fail("missing UI node %s" % path)
			return

	print("DAY4_OK units=200 selected=100 fog_bright=%d fog_dark=%d minimap_px=%d" % [bright, dark, colored])
	scene.free()
	quit(0)

func _fail(message: String) -> void:
	push_error(message)
	quit(1)
