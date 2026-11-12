# Prueba de M1: el nivel tiene lo que el modulo promete.
# Verifica las tres trampas que el curso menciona de pasada:
#   1. WorldEnvironment sin Environment no hace nada.
#   2. Sin Camera3D el 3D no se ve.
#   3. Piso y paredes en GridMaps separados (si van juntos, la pared borra el piso).
extends SceneTree

var fails: int = 0


func check(cond: bool, label: String) -> void:
	if cond:
		print("  OK   ", label)
	else:
		print("  FAIL ", label)
		fails += 1


func _init() -> void:
	var ok := _run()
	print("M1_LEVEL_OK" if ok else "M1_LEVEL_FAIL")
	quit(0 if ok else 1)


func _run() -> bool:
	var packed := load("res://level.tscn") as PackedScene
	check(packed != null, "level.tscn carga")
	if packed == null:
		return false

	var lvl := packed.instantiate()
	check(lvl != null, "level.tscn instancia")
	if lvl == null:
		return false

	# 1. WorldEnvironment CON environment.
	var we := lvl.get_node_or_null("WorldEnvironment") as WorldEnvironment
	check(we != null, "hay WorldEnvironment")
	check(we != null and we.environment != null, "el Environment esta asignado")

	# 2. Camera3D current.
	var cam := lvl.get_node_or_null("Camera") as Camera3D
	check(cam != null, "hay Camera3D")
	check(cam != null and cam.current, "la camara es current")

	# 3. Dos GridMaps con la misma libreria.
	var fl := lvl.get_node_or_null("Floor") as GridMap
	var wl := lvl.get_node_or_null("Walls") as GridMap
	check(fl != null, "hay GridMap Floor")
	check(wl != null, "hay GridMap Walls")
	check(fl != null and wl != null and fl.mesh_library == wl.mesh_library,
		"Floor y Walls comparten la misma MeshLibrary")

	# 4. El piso tiene 144 celdas y las paredes no lo pisaron.
	var floor_cells := fl.get_used_cells().size() if fl != null else 0
	check(floor_cells == 144, "el piso tiene 144 celdas (12x12)")
	var wall_cells := wl.get_used_cells().size() if wl != null else 0
	check(wall_cells == 44, "las paredes tienen 44 celdas (borde 12x12)")

	# 5. Una celda de pared NO es una celda de piso en el GridMap de piso:
	#    por eso estan separados. Si estuvieran juntos, esto seria el mismo nodo.
	var corner := Vector3i(0, 0, 0)
	check(fl != null and fl.get_cell_item(corner) == 0, "la esquina sigue siendo piso")
	check(wl != null and wl.get_cell_item(Vector3i(0, 1, 0)) == 1, "la esquina tiene pared arriba")

	# 6. Niebla volumetrica prendida (lo que el curso configura).
	var env := we.environment if we != null else null
	check(env != null and env.volumetric_fog_enabled, "niebla volumetrica encendida")
	check(env != null and env.volumetric_fog_density > 0.0, "densidad de niebla > 0")
	check(env != null and not env.glow_enabled, "glow apagado (el curso lo deja para Forward+)")

	lvl.free()
	return fails == 0
