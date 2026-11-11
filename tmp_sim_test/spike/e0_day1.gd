extends Node3D

# E0 Day 1: presentation-only scene. No gameplay logic.
func _ready() -> void:
	var anim: AnimationPlayer = $Warrior/AnimationPlayer
	if anim and anim.has_animation("Idle"):
		anim.play("Idle")
