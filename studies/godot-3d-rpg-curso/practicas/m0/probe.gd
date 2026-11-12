# M0 - sonda: que version corre el proyecto, y que rompe respecto de 4.3
extends SceneTree

func _init() -> void:
    print("engine_version=", Engine.get_version_info().string)
    print("major=", Engine.get_version_info().major, " minor=", Engine.get_version_info().minor)
    # Defaults que cambiaron entre 4.3 y 4.7 (doc oficial de migracion)
    print("stretch_mode=", ProjectSettings.get_setting("display/window/stretch/mode"))
    print("stretch_aspect=", ProjectSettings.get_setting("display/window/stretch/aspect"))
    print("sky_roughness_layers=", ProjectSettings.get_setting("rendering/reflections/sky_reflections/roughness_layers"))
    print("physics_3d=", ProjectSettings.get_setting("physics/3d/physics_engine"))
    quit(0)
