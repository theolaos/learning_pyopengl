#version 330 core

in vec3 framgemntColor;

out vec4 color;

void main(){
    color = vec4(framgemntColor, 1.0);
}