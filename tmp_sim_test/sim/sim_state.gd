# Global deterministic simulation state.

class_name SimState extends RefCounted

const SCHEMA_VERSION: int = 1

# Explicitly preload dependent classes to ensure they are known at compile time.
var SimRNGClass = preload("res://sim/rng.gd")
var SimPathfindClass = preload("res://sim/pathfind.gd")
var SimCommandsClass = preload("res://sim/commands.gd")
var SimEntityClass = preload("res://sim/sim_entity.gd")

var tick: int = 0
var next_id: int = 1
var rng
var pathfinder
var commands
var entities = []

func _init(seed_value: int = 1, width: int = 96, height: int = 96) -> void:
    rng = SimRNGClass.new(seed_value)
    pathfinder = SimPathfindClass.new(width, height)
    commands = SimCommandsClass.new()
    entities = []

func add_entity(team: int, cell: Vector2i) -> int:
    var e = SimEntityClass.new()
    e.id = next_id
    e.team = team
    e.cell = cell
    e.hp = 100
    # The SimEntity class provides sensible defaults for path, path_index, and move_cooldown.
    entities.append(e)
    next_id += 1
    return e.id

func get_entity_by_id(entity_id: int):
    for e in entities:
        if e.id == entity_id:
            return e
    return null

func enqueue_move(entity_id: int, target: Vector2i, delay_ticks: int = 1) -> void:
    var cmd = {"type": "move", "entity_id": entity_id, "target": target}
    commands.enqueue(cmd, tick + delay_ticks)

func step() -> void:
    tick += 1
    # Process pending commands for the new tick.
    var pending = commands.drain(tick)
    for cmd in pending:
        if cmd.get("type", "") == "move":
            var eid = cmd["entity_id"]
            var target = cmd["target"]
            var ent = get_entity_by_id(eid)
            if ent != null:
                ent.target = target
                var path = pathfinder.find_path(ent.cell, target)
                if path.size() > 0:
                    # If the first cell in the path is the current position, skip it.
                    var start_idx = 0
                    if path[0] == ent.cell:
                        start_idx = 1
                    ent.path = path
                    ent.path_index = start_idx
                else:
                    ent.path.clear()
                    ent.path_index = 0
    # Update movement for each entity in stable order.
    for ent in entities:
        # Cool‑down handling.
        if ent.move_cooldown > 0:
            ent.move_cooldown -= 1
        # Move if ready and there is a remaining path.
        if ent.move_cooldown == 0 and ent.path.size() > 0 and ent.path_index < ent.path.size():
            ent.cell = ent.path[ent.path_index]
            ent.path_index += 1
            ent.move_cooldown = 2  # Next move after two more ticks (total 3).
        # Clear completed path.
        if ent.path.size() > 0 and ent.path_index >= ent.path.size():
            ent.path.clear()
            ent.path_index = 0
            ent.move_cooldown = 0

func to_dict() -> Dictionary:
    var result: Dictionary = {
        "schema_version": SCHEMA_VERSION,
        "tick": tick,
        "next_id": next_id,
        "rng_state": rng.get_state(),
        "entities": []
    }
    # Ensure deterministic ordering by sorting entities by id.
    for e in entities:
        result["entities"].append(e.to_dict())
    return result

# Sorting is not required because entities are stored in insertion order, which is deterministic.

func from_dict(data: Dictionary) -> void:
    tick = data.get("tick", 0)
    next_id = data.get("next_id", 1)
    var rng_state = data.get("rng_state", 1)
    rng = SimRNGClass.new()
    rng.set_state(rng_state)
    # Re‑create pathfinder with default size (96×96) – sufficient for tests.
    pathfinder = SimPathfindClass.new()
    commands = SimCommandsClass.new()
    entities.clear()
    var ents = data.get("entities", [])
    for d in ents:
        var e = SimEntityClass.new()
        e.id = int(d.get("id", 0))
        e.team = int(d.get("team", 0))
        e.cell = Vector2i(int(d.get("cell_x", 0)), int(d.get("cell_y", 0)))
        e.hp = int(d.get("hp", 100))
        e.target = Vector2i(int(d.get("target_x", -1)), int(d.get("target_y", -1)))
        for p in d.get("path", []):
            e.path.append(Vector2i(int(p[0]), int(p[1])))
        e.path_index = int(d.get("path_index", 0))
        e.move_cooldown = int(d.get("move_cooldown", 0))
        entities.append(e)

func hash_state() -> String:
    # Build a canonical string.
    var sb = ""
    sb += str(SCHEMA_VERSION) + "|"
    sb += str(tick) + "|"
    sb += str(rng.get_state()) + "|"
    for e in entities:
        sb += str(e.id) + "," + str(e.team) + "," + str(e.cell.x) + "," + str(e.cell.y) + "," + str(e.hp)
        sb += "," + str(e.target.x) + "," + str(e.target.y) + "," + str(e.path_index) + "," + str(e.move_cooldown) + ","
        for p in e.path:
            sb += str(p.x) + ":" + str(p.y) + "."
        sb += ";"
    var ctx = HashingContext.new()
    ctx.start(HashingContext.HASH_SHA256)
    ctx.update(sb.to_utf8_buffer())
    var hash_bytes = ctx.finish()
    return hash_bytes.hex_encode()

