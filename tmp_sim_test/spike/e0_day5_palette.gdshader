shader_type canvas_item;
render_mode unshaded;

uniform sampler2D screen_tex : hint_screen_texture, filter_linear;
uniform vec3 palette[16];

void fragment() {
	vec3 c = texture(screen_tex, SCREEN_UV).rgb;
	float best = 1e9;
	vec3 q = palette[0];
	for (int i = 0; i < 16; i++) {
		float d = distance(c, palette[i]);
		if (d < best) {
			best = d;
			q = palette[i];
		}
	}
	COLOR = vec4(q, 1.0);
}
