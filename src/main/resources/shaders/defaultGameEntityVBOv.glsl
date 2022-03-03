#version 330 core
layout(location=0) in vec3 aPos;
layout(location=1) in vec2 aTexCoord;
layout(location=2) in float aTexID;

uniform mat4 proj;
uniform mat4 view;
uniform float uTime;

out vec3 fPos;
// TODO - consider changing to vec3
out vec2 fTexCoord;
out float fTexID;

void main(){
    gl_Position = proj * view * vec4(aPos, 1.0);
    fPos = aPos;
    fTexCoord = aTexCoord;
    fTexID = aTexID;
}