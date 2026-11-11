extends SceneTree

# Acceptance test for E0 Day 3 minimal select‑move‑attack loop.

func _initialize() -> void:
    var scene: Node = load("res://spike/e0_day3.tscn").instantiate()
    get_root().add_child(scene)
    # Run checks after the first frame.
    process_frame.connect(_check.bind(scene), CONNECT_ONE_SHOT)

func _check(scene: Node) -> void:
    # 1. Verify essential nodes exist.
    var house := scene.get_node("House")
    var tree := scene.get_node("Tree")
    var player := scene.get_node("Player") as Node3D
    var enemy := scene.get_node("Enemy") as Node3D
    if not house or not tree or not player or not enemy:
        _fail("Missing House, Tree, Player, or Enemy node")
        return

    # 2. Verify scales.
    if not is_equal_approx(house.scale.x, 4.0):
        _fail("House scale not ≈4")
        return
    if not is_equal_approx(tree.scale.x, 4.5):
        _fail("Tree scale not ≈4.5")
        return

    # 3. Verify Player head height ≈1.64 m.
    var skeleton: Skeleton3D = player.get_node("CharacterArmature/Skeleton3D") as Skeleton3D
    var head_idx: int = skeleton.find_bone("Head")
    if head_idx == -1:
        _fail("Head bone not found on Player")
        return
    var head_global: Vector3 = skeleton.global_transform * skeleton.get_bone_global_pose(head_idx).origin
    if absf(head_global.y - 1.64) > 0.06:
        _fail("head global Y %.3f is not ~1.64" % head_global.y)
        return

    # 4. Test selection ring via pick_at.
    var controller := scene as Node3D
    var pick_ok: bool = controller.pick_at(player.global_transform.origin)
    if not pick_ok:
        _fail("pick_at on player returned false")
        return
    var ring: MeshInstance3D = controller.get_node("SelectionRing") as MeshInstance3D
    if not ring.visible:
        _fail("Selection ring not visible after pick")
        return

    # 5. Test move command and actual displacement.
    var target_move := Vector3(1, 0, 3)
    var start_pos := player.global_transform.origin
    controller.command_at(target_move)
    if player.state != "move":
        _fail("Player state not 'move' after command_at")
        return
    for i in 4:
        player.step(0.5)
    var dist := player.global_transform.origin.distance_to(target_move)
    if dist > 0.1:
        _fail("Player did not reach the move target (dist=%.2f)" % dist)
        return
    if player.global_transform.origin.distance_to(start_pos) < 0.5:
        _fail("Player did not move from its start position")
        return
    if player.state != "idle":
        _fail("Player state not 'idle' after arriving")
        return
    # 6. Test attack command.
    controller.command_at(enemy.global_transform.origin)
    if player.state != "attack":
        _fail("Player state not 'attack' after attack command")
        return
    # Place player within attack range (≈1 m).
    var enemy_pos := enemy.global_transform.origin
    player.global_transform.origin = enemy_pos + Vector3(1, 0, 0)
    # Run several attack steps.
    for i in 12:
        player.step(0.1)
    if enemy.hp >= 100:
        _fail("Enemy hp not reduced after attack (hp=%d)" % enemy.hp)
        return

    # 7. Test death.
    enemy.take_damage(100)
    if enemy.state != "dead":
        _fail("Enemy not dead after lethal damage (state=%s)" % enemy.state)
        return

    print("DAY3_OK")
    scene.free()
    quit(0)

func _fail(message: String) -> void:
    push_error(message)
    quit(1)

