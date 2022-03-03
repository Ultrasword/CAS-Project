#version 120
in vec3 fPos;
in vec2 fTexCoord;
in float fTexID;

uniform sampler2D tex[9];
uniform float uTime;

void main() {
    gl_FragColor = texture(tex[int(fTexID)], fTexCoord);
    if(gl_FragColor.a == 0) discard;
}
