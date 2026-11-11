extends SceneTree

func _init():
    var dir = DirAccess.open("res://sim")
    if dir == null:
        push_error("Cannot open sim directory for purity test")
        quit(1)
        return
    var bad = false
    var patterns = ["extends Node", "extends Node3D", "SceneTree", "get_tree(", "Input.", "AudioServer"]
    while true:
        var file_name = dir.get_next()
        if file_name == "":
            break
        if not file_name.ends_with(".gd"):
            continue
        var path = "res://sim/" + file_name
        var file = FileAccess.open(path, FileAccess.READ)
        if file == null:
            push_error("Cannot read file " + path)
            quit(1)
            return
        var content = file.get_as_text()
        file.close()
        for p in patterns:
            if content.find(p) != -1:
                push_error("Purity violation in " + file_name + ": " + p)
                bad = true
    if bad:
        quit(1)
        return
    print("PURITY_OK")
    quit()

