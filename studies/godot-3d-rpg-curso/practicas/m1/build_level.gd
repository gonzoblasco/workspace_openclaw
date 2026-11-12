# Construye level.tscn: GridMap con piso y paredes + WorldEnvironment de dungeon.
# Reproduce lo del curso (m1) pero escrito, para poder verificarlo.
#
# Uso: Godot --headless --path <practica> --script build_level.gd
extends SceneTree


func _init() -> void:
	var root := Node3D.new()
	root.name = "Level"

	# --- GridMap ---------------------------------------------------------
	var grid := GridMap.new()
	grid.name = "Grid"
	grid.mesh_library = load("res://mesh_library.tres")
	grid.cell_size = Vector3(2, 2, 2)
	root.add_child(grid)
	grid.owner = root

	# --- Piso 12x12 en una capa, paredes en GridMap separado --------------
	# El curso separa floor y walls en dos GridMaps porque pintar una pared
	# encima del piso en el mismo GridMap BORRA el piso de esa celda.
	var floor_grid := GridMap.new()
	floor_grid.name = "Floor"
	floor_grid.mesh_library = grid.mesh_library
	floor_grid.cell_size = grid.cell_size
	root.add_child(floor_grid)
	floor_grid.owner = root

	var wall_grid := GridMap.new()
	wall_grid.name = "Walls"
	wall_grid.mesh_library = grid.mesh_library
	wall_grid.cell_size = grid.cell_size
	root.add_child(wall_grid)
	wall_grid.owner = root

	root.remove_child(grid)
	grid.free()

	for x in range(12):
		for z in range(12):
			floor_grid.set_cell_item(Vector3i(x, 0, z), 0)

	# Borde de paredes.
	for i in range(12):
		wall_grid.set_cell_item(Vector3i(i, 1, 0), 1)
		wall_grid.set_cell_item(Vector3i(i, 1, 11), 1)
		wall_grid.set_cell_item(Vector3i(0, 1, i), 1)
		wall_grid.set_cell_item(Vector3i(11, 1, i), 1)

	# --- WorldEnvironment -------------------------------------------------
	# Sin Environment asignado, el nodo no hace NADA (el curso lo muestra
	# con "if I hit play you will see no difference").
	var we := WorldEnvironment.new()
	we.name = "WorldEnvironment"

	var env := Environment.new()
	env.background_mode = Environment.BG_COLOR
	env.background_color = Color(100.0 / 255.0, 100.0 / 255.0, 100.0 / 255.0)
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.ambient_light_color = Color(0.55, 0.55, 0.6)
	env.ambient_light_energy = 0.35

	env.volumetric_fog_enabled = true
	env.volumetric_fog_density = 0.02
	env.fog_enabled = true
	# El curso usa 0.2, pero esa densidad esta calibrada para una camara a
	# ~5 m del jugador. Con la camara de este nivel a 30 m, exp(-0.2*30) = 0.2%
	# de transmision: no se ve NADA. La niebla se escala con la distancia.
	env.fog_density = 0.012
	env.fog_light_energy = 0.5
	env.glow_enabled = false  # el curso lo deja apagado hasta Forward+

	we.environment = env
	root.add_child(we)
	we.owner = root

	# --- Luz direccional --------------------------------------------------
	var sun := DirectionalLight3D.new()
	sun.name = "Sun"
	sun.light_energy = 1.6
	sun.rotation_degrees = Vector3(-55, -30, 0)
	sun.shadow_enabled = true
	root.add_child(sun)
	sun.owner = root

	# --- Camara -----------------------------------------------------------
	# El curso dice: "if I hit play nothing will happen... I do not have a
	# camera 3D in order to make our 3D scene work".
	var cam := Camera3D.new()
	cam.name = "Camera"
	# Mirando al centro del piso de 12x12 (centro en 12,0,12 en coords de mundo:
	# 12 celdas * 2 unidades). Antes la camara estaba DENTRO del borde de paredes.
	cam.position = Vector3(12, 26, 34)
	cam.rotation_degrees = Vector3(-42, 0, 0)
	cam.fov = 55
	cam.current = true
	root.add_child(cam)
	cam.owner = root

	var packed := PackedScene.new()
	var err := packed.pack(root)
	if err != OK:
		print("PACK_FAIL ", err)
		quit(1)
		return
	err = ResourceSaver.save(packed, "res://level.tscn")
	if err != OK:
		print("SAVE_FAIL ", err)
		quit(1)
		return

	print("LEVEL_OK floor_cells=144 walls=", wall_grid.get_used_cells().size())

	# Sin esto, Godot sale con RIDs y objetos sin liberar (8 GodotBody3D,
	# 1 Camera3D, 1 Environment...). No es un error del nivel: es que el nodo
	# raiz nunca se libero. En un --script no hay arbol que lo limpie solo.
	root.free()
	quit(0)
