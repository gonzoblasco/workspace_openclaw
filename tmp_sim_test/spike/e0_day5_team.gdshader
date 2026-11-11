shader_type spatial;
render_mode diffuse_burley, specular_disabled;

uniform sampler2D albedo_tex : source_color, filter_linear;
uniform vec4 team_color : source_color = vec4(0.2, 0.35, 0.6, 1.0);
uniform float mix_amount : hint_range(0.0, 1.0) = 0.65;

void fragment() {
	vec3 base = texture(albedo_tex, UV).rgb;
	ALBEDO = mix(base, team_color.rgb, mix_amount);
	ROUGHNESS = 1.0;
}
