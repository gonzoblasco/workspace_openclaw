shader_type spatial;
render_mode cull_back, diffuse_burley, specular_disabled;

uniform sampler2D fog_mask : filter_linear, repeat_disable;
uniform vec4 base_color : source_color = vec4(0.30, 0.34, 0.27, 1.0);

void fragment() {
	float explored = texture(fog_mask, UV).r;
	ALBEDO = mix(vec3(0.035, 0.040, 0.050), base_color.rgb, explored);
	ROUGHNESS = 1.0;
}
