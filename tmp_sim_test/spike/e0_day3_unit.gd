extends Node3D

# Unit script handling movement, attack, health, and health bar.

@export var team: int = 0
var hp: int = 100
var max_hp: int = 100
var speed: float = 2.5
var state: String = "idle" # idle, move, attack, dead
var target_pos: Vector3 = Vector3.ZERO
var target: Node3D = null
var _attack_cooldown: float = 0.0

func _ready() -> void:
    # Register in a global group for easy lookup.
    add_to_group("units")
    # Ensure a health bar exists (optional).
    if not has_node("HealthBar"):
        _create_health_bar()

func order_move(pos: Vector3) -> void:
    state = "move"
    target_pos = pos
    var anim: AnimationPlayer = $AnimationPlayer
    if anim and anim.has_animation("Walk"):
        anim.play("Walk")

func order_attack(enemy: Node3D) -> void:
    if enemy == null:
        return
    state = "attack"
    target = enemy
    _attack_cooldown = 0.0
    var anim: AnimationPlayer = $AnimationPlayer
    if anim and anim.has_animation("Sword_Attack"):
        anim.play("Sword_Attack")

func step(delta: float) -> void:
    if state == "dead":
        return
    if state == "move":
        _process_move(delta)
    elif state == "attack":
        _process_attack(delta)

func _process_move(delta: float) -> void:
    var current: Vector3 = global_transform.origin
    var dir: Vector3 = target_pos - current
    var distance: float = dir.length()
    if distance <= 0.1:
        global_transform.origin = target_pos
        state = "idle"
        var anim: AnimationPlayer = $AnimationPlayer
        if anim:
            anim.stop()
        return
    var move_dist: float = speed * delta
    if move_dist >= distance:
        global_transform.origin = target_pos
    else:
        global_transform.origin = current + dir.normalized() * move_dist
    if target_pos != global_transform.origin:
        look_at(target_pos, Vector3.UP)

func _process_attack(delta: float) -> void:
    if not is_instance_valid(target):
        state = "idle"
        return
    var current: Vector3 = global_transform.origin
    var enemy_pos: Vector3 = target.global_transform.origin
    var dir: Vector3 = enemy_pos - current
    var distance: float = dir.length()
    if distance > 1.2:
        # Chase the enemy.
        var move_dist: float = speed * delta
        if move_dist >= distance:
            global_transform.origin = enemy_pos
        else:
            global_transform.origin = current + dir.normalized() * move_dist
        look_at(enemy_pos, Vector3.UP)
        var chase_anim: AnimationPlayer = $AnimationPlayer
        if chase_anim and chase_anim.current_animation != "Walk":
            chase_anim.play("Walk")
        return
    # Within attack range.
    if enemy_pos != global_transform.origin:
        look_at(enemy_pos, Vector3.UP)
    _attack_cooldown -= delta
    if _attack_cooldown <= 0.0:
        # Apply damage.
        if target.has_method("take_damage"):
            target.take_damage(10)
        _attack_cooldown = 1.0
        var anim: AnimationPlayer = $AnimationPlayer
        if anim and anim.has_animation("Sword_Attack"):
            anim.play("Sword_Attack")

func take_damage(amount: int) -> void:
    hp = max(hp - amount, 0)
    _update_health_bar()
    if hp <= 0:
        state = "dead"
        var anim: AnimationPlayer = $AnimationPlayer
        if anim and anim.has_animation("Death"):
            anim.play("Death")

func _update_health_bar() -> void:
    if not has_node("HealthBar"):
        return
    var bar: MeshInstance3D = $HealthBar as MeshInstance3D
    var ratio: float = float(hp) / float(max_hp)
    # The bar's original scale.x = 1.0, adjust proportionally.
    var s: Vector3 = bar.scale
    s.x = clamp(ratio, 0.0, 1.0)
    bar.scale = s

func _create_health_bar() -> void:
    # Simple quad mesh health bar above the unit.
    var bar := MeshInstance3D.new()
    var quad := QuadMesh.new()
    quad.size = Vector2(1.0, 0.12)
    bar.mesh = quad
    var mat := StandardMaterial3D.new()
    mat.albedo_color = Color(0, 1, 0, 1)
    mat.billboard_mode = BaseMaterial3D.BILLBOARD_ENABLED
    mat.no_depth_test = true
    bar.material_override = mat
    bar.name = "HealthBar"
    # Position the bar above the 1.8 m head.
    bar.position = Vector3(0, 2.8, 0)
    add_child(bar)

