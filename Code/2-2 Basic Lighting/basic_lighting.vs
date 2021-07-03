#version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aNormal;

out vec3 Normal;
out vec3 FragPos;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main()
{
    // 获取世界空间下的片段位置
    FragPos = vec3(model * vec4(aPos, 1.0));
    Normal = aNormal;
    gl_Position = projection * view * model * vec4(aPos, 1.0);
}