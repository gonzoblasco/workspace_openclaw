# Prueba la hipotesis: con fog_density 0.2 a 30 unidades de camara no se ve nada.
extends SceneTree
func _initialize() -> void:
	var lvl := (load("res://level.tscn") as PackedScene).instantiate()
	root.add_child(lvl)
	var env: Environment = (lvl.get_node("WorldEnvironment") as WorldEnvironment).environment
	print("fog_density=", env.fog_density, " volumetric=", env.volumetric_fog_density)
	# Visibilidad a distancia d con FogExp: exp(-density*d)
	for d in [10, 20, 30, 40]:
		print("  d=", d, " transmision_fog=", "%.3f" % exp(-env.fog_density * d),
			" transmision_volum=", "%.3f" % exp(-env.volumetric_fog_density * d))
	quit(0)
