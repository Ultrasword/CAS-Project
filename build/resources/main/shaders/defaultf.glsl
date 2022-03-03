#version 330 core
in vec3 fPos;
in vec4 fCol;
in vec2 fTexCoords;
in float fTexID;

uniform sampler2D tex[9];
uniform float uTime;

void main() {
    gl_FragColor = texture(tex[int(fTexID)], fTexCoords);
    if(gl_FragColor.a == 0) discard;
}