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

    # 定义顶点数据
    vertices = [
        -0.5, -0.5, 0.0,
        0.5, -0.5, 0.0,
        0.0, 0.5, 0.0
    ]
    vertices = np.array(vertices, dtype=np.float32)

    # 在GPU上创建内存用于储存顶点数据，配置OpenGL如何解释这些内存，并且指定其如何发送给显卡，交给顶点着色器处理
    # 通过顶点缓冲对象(Vertex Buffer Objects, VBO)管理内存，它会在GPU内存（通常被称为显存）中储存大量顶点
    VBO = glGenBuffers(1)  # 生成一个VBO对象，指定缓冲ID
    # 把新创建的缓冲绑定到顶点缓冲GL_ARRAY_BUFFER目标上
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    # 把之前定义的顶点数据复制到缓冲的内存中
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

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

    # # 创建顶点着色器
    # vertexShader = glCreateShader(GL_VERTEX_SHADER)
    # # 把这个着色器源码附加到着色器对象上
    # glShaderSource(vertexShader, 1, vertexShaderSource, None)
    # glCompileShader(vertexShader)  # 编译

    fragmentShaderSource = """
    #version 330 core
    out vec4 FragColor;
    void main()
    {
    FragColor = vec4(1.0f, 0.5f, 0.2f, 1.0f);
    }
    """

    # # 创建片段着色器
    # fragmentShader = glCreateShader(GL_FRAGMENT_SHADER)
    # # 把这个着色器源码附加到着色器对象上
    # glShaderSource(fragmentShader, 1, fragmentShaderSource, None)
    # glCompileShader(fragmentShader)  # 编译

    # 链接
    # shaderProgram = glCreateProgram()   # 创建程序对象
    # glAttachShader(shaderProgram, vertexShader)
    # glAttachShader(shaderProgram, fragmentShader)
    # glLinkProgram(shaderProgram)

    # 使用封装的 shaders 库
    shaderProgram = compileProgram(compileShader(vertexShaderSource, GL_VERTEX_SHADER),
                            compileShader(fragmentShaderSource, GL_FRAGMENT_SHADER))

    # 用刚创建的程序对象作为它的参数，以激活这个程序对象，每个着色器调用和渲染调用都会使用这个程序对象
    glUseProgram(shaderProgram)

    # 删除着色器对象
    # glDeleteShader(vertexShader)
    # glDeleteShader(fragmentShader)

    # -------------------------------------------------------------------
    # 链接顶点属性
    # 我们必须手动指定输入数据的哪一个部分对应顶点着色器的哪一个顶点属性
    # -------------------------------------------------------------------

    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3*4, ctypes.c_void_p(0))
    # 以顶点属性位置值作为参数，启用顶点属性
    glEnableVertexAttribArray(0)

    # -------------------------------------------------------------------
    # 渲染循环: 让GLFW退出前一直保持运行
    # -------------------------------------------------------------------

    while not glfw.window_should_close(window):  # 检查一次GLFW是否被要求退出
        processInput(window)

        glfw.swap_buffers(window)  # 交换颜色缓冲
        glfw.poll_events()  # 检查有没有触发什么事件（比如键盘输入、鼠标移动等）、更新窗口状态，并调用对应的回调函数
        glDrawArrays(GL_TRIANGLES, 0, 3)

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
