extends Node3D

# E0 Day 4 unit: wander, move, health. No 3D health bar; the 2D overlay draws it.

@export var team: int = 0
var hp: int = 100
var max_hp: int = 100
var speed: float = 2.0
var state: String = "wander" # wander, move, dead
var base_pos: Vector3 = Vector3.ZERO
var target_pos: Vector3 = Vector3.ZERO
var phase: float = 0.0
var _attack_cd: float = 0.0

func _ready() -> void:
	base_pos = global_position
	_play("Walk")

func order_move(pos: Vector3) -> void:
	state = "move"
	target_pos = pos
	_play("Walk")

func step(delta: float) -> void:
	if state == "dead":
		return
	if state == "wander":
		phase += delta * 0.7
		global_position = base_pos + Vector3(cos(phase) * 0.35, 0.0, sin(phase) * 0.35)
		var facing := base_pos + Vector3(-sin(phase), 0.0, cos(phase)) * 0.5
		_look(facing)
		return
	if state == "move":
		var dir := target_pos - global_position
		dir.y = 0.0
		var distance := dir.length()
		if distance <= 0.15:
			global_position = target_pos
			base_pos = target_pos
			state = "wander"
			phase = 0.0
			return
		var step_len := speed * delta
		global_position += dir.normalized() * minf(step_len, distance)
		_look(target_pos)

func take_damage(amount: int) -> void:
	hp = maxi(hp - amount, 0)
	if hp == 0:
		state = "dead"
		_play("Death")

func _play(anim_name: String) -> void:
	var anim := get_node_or_null("AnimationPlayer") as AnimationPlayer
	if anim and anim.has_animation(anim_name) and anim.current_animation != anim_name:
		anim.play(anim_name)

func _look(target: Vector3) -> void:
	var flat := Vector3(target.x, global_position.y, target.z)
	if flat.distance_to(global_position) > 0.01:
		look_at(flat, Vector3.UP)

func _process(delta: float) -> void:
	step(delta)
