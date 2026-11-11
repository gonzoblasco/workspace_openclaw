extends SceneTree
var SimCommands = preload("res://sim/commands.gd")

func _init():
    var cmds = SimCommands.new()
    # Enqueue three commands for tick 5.
    cmds.enqueue({"type": "move", "entity_id": 1, "target": Vector2i(5,5)}, 5)
    cmds.enqueue({"type": "move", "entity_id": 2, "target": Vector2i(6,6)}, 5)
    cmds.enqueue({"type": "move", "entity_id": 3, "target": Vector2i(7,7)}, 5)
    # Enqueue a future command for tick 6.
    cmds.enqueue({"type": "move", "entity_id": 4, "target": Vector2i(8,8)}, 6)
    var drained = cmds.drain(5)
    if drained.size() != 3:
        push_error("Expected 3 commands at tick 5, got %d" % drained.size())
        quit(1)
        return
    if drained[0]["entity_id"] != 1 or drained[1]["entity_id"] != 2 or drained[2]["entity_id"] != 3:
        push_error("Commands out of insertion order")
        quit(1)
        return
    if cmds.size() != 1:
        push_error("Future command was not retained in queue")
        quit(1)
        return
    print("COMMANDS_OK")
    quit()

