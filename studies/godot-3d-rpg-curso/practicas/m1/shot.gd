# Captura del nivel M1 en ventana real (no headless: el renderer dummy no
# dibuja). Espera unos frames y guarda un PNG.
#
# Uso: Godot --path <practica> --script shot.gd
extends SceneTree

var frames := 0
var frames_target := 20


func _initialize() -> void:
	var lvl := (load("res://level.tscn") as PackedScene).instantiate()
	root.add_child(lvl)


func _process(delta: float) -> bool:
	frames += 1
	if frames < frames_target:
		return false
	var img := root.get_texture().get_image()
	img.save_png("res://m1_shot.png")
	print("SHOT_OK ", img.get_width(), "x", img.get_height())
	quit(0)
	return true
