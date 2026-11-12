# Construye mesh_library.tres como lo hace el curso a mano, pero en codigo.
# El curso pide: escena 3D -> mesh -> Make Local -> Create Collision Shape ->
# StaticBody3D > CollisionShape3D en ese orden -> Export as MeshLibrary.
# Aca se arma el mismo arbol y se guarda como recurso.
#
# Uso:
#   Godot --headless --path <practica> --script build_mesh_library.gd
extends SceneTree

const OUT := "res://mesh_library.tres"
const CELL := 2.0


func _init() -> void:
	var lib := MeshLibrary.new()

	# Item 0: piso. Box de 2x0.2x2, con su collision box.
	lib.create_item(0)
	lib.set_item_name(0, "floor")
	lib.set_item_mesh(0, _box_mesh(Vector3(CELL, 0.2, CELL), Vector3.ZERO, Color(0.34, 0.33, 0.31)))
	lib.set_item_shapes(0, [_box_shape(Vector3(CELL, 0.2, CELL))])

	# Item 1: pared. Box de 2x2x0.2, corrido media celda para arriba.
	lib.create_item(1)
	lib.set_item_name(1, "wall")
	lib.set_item_mesh(1, _box_mesh(Vector3(CELL, 2.0, 0.2), Vector3(0, 1.0, 0), Color(0.46, 0.42, 0.38)))
	lib.set_item_shapes(1, [_box_shape(Vector3(CELL, 2.0, 0.2), Vector3(0, 1.0, 0))])

	# Item 2: escalera. Caja inclinada (el curso hace a mano el box rotado
	# porque los escalones no colisionan bien con el CapsuleShape del player).
	lib.create_item(2)
	lib.set_item_name(2, "stairs")
	lib.set_item_mesh(2, _box_mesh(Vector3(CELL, 0.3, CELL * 1.4), Vector3(0, 0.5, 0), Color(0.40, 0.38, 0.36)))
	lib.set_item_shapes(2, [_box_shape(Vector3(CELL, 0.3, CELL * 1.4), Vector3(0, 0.5, 0))])

	var err := ResourceSaver.save(lib, OUT)
	if err != OK:
		print("SAVE_FAIL err=", err)
		quit(1)
		return

	print("BUILD_OK items=", lib.get_item_list())
	quit(0)


func _box_mesh(size: Vector3, offset: Vector3 = Vector3.ZERO, tint: Color = Color.WHITE) -> Mesh:
	var m := BoxMesh.new()
	m.size = size
	# Un material por item: sin material propio, todos comparten el default
	# blanco y el GridMap se ve como un bloque gris informe.
	var mat := StandardMaterial3D.new()
	mat.albedo_color = tint
	mat.roughness = 0.85
	m.material = mat
	return m


func _box_shape(size: Vector3, offset: Vector3 = Vector3.ZERO) -> Shape3D:
	var s := BoxShape3D.new()
	s.size = size
	return s
