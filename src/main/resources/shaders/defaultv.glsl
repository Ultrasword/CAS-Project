#version 330 core
layout(location=0) in vec3 aPos;
layout(location=1) in vec4 aCol;
layout(location=2) in vec2 aTexCoords;
layout(location=3) in float aTexID;

uniform mat4 proj;
uniform mat4 view;
uniform float uTime;

out vec3 fPos;
out vec4 fCol;
out vec2 fTexCoords;
out float fTexID;

void main() {
    gl_Position = proj * view * vec4(aPos, 1.0);
    fPos = aPos;
    fTexCoords = aTexCoords;
    fTexID = aTexID;
}
