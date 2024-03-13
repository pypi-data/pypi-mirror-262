#version 460 core
layout (location = 0) in vec3 aVertex;
layout (location = 1) in vec3 aColor;

out vec3 ourColor;

uniform mat4 mvp;

void main()
{
    gl_Position = mvp * vec4(aVertex, 1.0);
    ourColor = aColor;
}