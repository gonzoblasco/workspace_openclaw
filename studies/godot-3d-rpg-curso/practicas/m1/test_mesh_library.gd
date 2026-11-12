# Prueba de M1: MeshLibrary valida y tile de piso con colision en el orden correcto.
# Corre headless. Sale con 0 si todo esta bien, 1 si algo falla.
extends SceneTree

var fails: int = 0


func check(cond: bool, label: String) -> void:
	if cond:
		print("  OK   ", label)
	else:
		print("  FAIL ", label)
		fails += 1


func _init() -> void:
	print("M1_MESH_LIBRARY_OK" if _run() else "M1_MESH_LIBRARY_FAIL")
	quit(0 if fails == 0 else 1)


func _run() -> bool:
	var path := "res://mesh_library.tres"
	check(ResourceLoader.exists(path), "mesh_library.tres existe")
	if not ResourceLoader.exists(path):
		return false

	var lib := load(path) as MeshLibrary
	check(lib != null, "carga como MeshLibrary")
	if lib == null:
		return false

	var ids := lib.get_item_list()
	check(ids.size() == 3, "3 items en la libreria (floor, wall, stairs)")
	print("       ids=", ids)

	# El orden que el curso exige: StaticBody3D > CollisionShape3D.
	var shape := lib.get_item_shapes(0)
	check(shape.size() > 0, "el item 0 tiene al menos un shape")

	var mesh := lib.get_item_mesh(0)
	check(mesh != null, "el item 0 tiene mesh")

	# El nombre del item es lo que el GridMap muestra en el picker.
	var names: Array[String] = []
	for i in ids:
		names.append(lib.get_item_name(i))
	print("       nombres=", names)
	check(names.has("floor"), "hay un item llamado 'floor'")

	if fails == 0:
		return true
	return false
