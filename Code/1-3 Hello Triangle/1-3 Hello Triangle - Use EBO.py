import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np


def main():
    # 实例化GLFW窗口
    glfw.init()

    # 配置GLFW
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)  # 主版本号
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)  # 次版本号
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_COMPAT_PROFILE)  # 核心模式

    # 创建一个窗口对象，这个窗口对象存放了所有和窗口相关的数据
    window = glfw.create_window(800, 600, "LearnOpenGL", None, None)
    glfw.set_window_pos(window, 400, 200)
    glfw.make_context_current(window)

    # OpenGL渲染窗口的尺寸大小：视口
    width, height = glfw.get_framebuffer_size(window)
    glViewport(0, 0, width, height)
    # 注册:每当窗口调整大小的时候调用
    glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)

    # -------------------------------------------------------------------
    # 顶点输入
    # -------------------------------------------------------------------

    # 定义顶点数据：两个三角形
    vertices = [
        0.5,  0.5, 0.0,
        0.5, -0.5, 0.0,
        -0.5, -0.5, 0.0,
        -0.5, 0.5, 0.0,
    ]
    vertices = np.array(vertices, dtype=np.float32)

    indices = [
        0, 1, 3,
        1, 2, 3
    ]
    indices = np.array(indices, dtype=np.uint32)

    # 在GPU上创建内存用于储存顶点数据，配置OpenGL如何解释这些内存，并且指定其如何发送给显卡，交给顶点着色器处理

    VAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)
    EBO = glGenBuffers(1)

    # 1 绑定VAO，用于存储后续顶点属性指针的配置
    glBindVertexArray(VAO)

    # 2 绑定VBO，把之前定义的顶点数据复制到VBO
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    # 3 将顶点索引数据复制到索引缓冲
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

    # -------------------------------------------------------------------
    # 已经把顶点数据储存在显卡的内存中，用VBO这个顶点缓冲对象管理
    # 开始编写着色器
    # -------------------------------------------------------------------

    vertexShaderSource = """
    #version 330 core
    layout (location = 0) in vec3 aPos;
    void main()
    {
       gl_Position = vec4(aPos.x, aPos.y, aPos.z, 1.0);
    }
    """

    fragmentShaderSource = """
    #version 330 core
    out vec4 FragColor;
    void main()
    {
    FragColor = vec4(1.0f, 0.5f, 0.2f, 1.0f);
    }
    """

    # 在此使用封装的 shaders 库
    shaderProgram = compileProgram(compileShader(vertexShaderSource, GL_VERTEX_SHADER),
                                   compileShader(fragmentShaderSource, GL_FRAGMENT_SHADER))



    # -------------------------------------------------------------------
    # 链接顶点属性
    # 我们必须手动指定输入数据的哪一个部分对应顶点着色器的哪一个顶点属性
    # -------------------------------------------------------------------

    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * 4, ctypes.c_void_p(0))
    # 以顶点属性位置值作为参数，启用顶点属性
    glEnableVertexAttribArray(0)

    # -------------------------------------------------------------------
    # 渲染循环: 让GLFW退出前一直保持运行
    # -------------------------------------------------------------------

    while not glfw.window_should_close(window):  # 检查一次GLFW是否被要求退出
        processInput(window)

        glUseProgram(shaderProgram)
        glBindVertexArray(VAO)  # 多个VAO时在此进行绑定切换
        glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)
        glfw.swap_buffers(window)  # 交换颜色缓冲
        glfw.poll_events()  # 检查有没有触发什么事件（比如键盘输入、鼠标移动等）、更新窗口状态，并调用对应的回调函数

    # 渲染循环结束后我们需要正确释放/删除之前的分配的所有资源
    glfw.terminate()
    return


# 用户改变窗口的大小的时候，视口也应该被调整
def framebuffer_size_callback(window, width, height):
    glViewport(0, 0, width, height)


def processInput(window):
    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
        glfw.set_window_should_close(window, GL_TRUE)


if __name__ == '__main__':
    main()
