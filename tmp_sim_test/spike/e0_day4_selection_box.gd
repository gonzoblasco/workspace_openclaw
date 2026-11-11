extends Control

# E0 Day 4: screen-space selection rectangle.
var rect: Rect2 = Rect2()
var active: bool = false

func _draw() -> void:
	if not active:
		return
	if rect.size.x < 1.0 or rect.size.y < 1.0:
		return
	draw_rect(rect, Color(0.3, 0.8, 1.0, 0.12))
	draw_rect(rect, Color(0.4, 0.9, 1.0, 0.9), false, 1.5)
