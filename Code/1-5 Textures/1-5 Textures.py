import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
import math
from PIL import Image


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
        # ---- 位置 - ---       ---- 颜色 - ---     - 纹理坐标 -
        0.5, 0.5, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0,  # 右上
        0.5, -0.5, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0,  # 右下
        - 0.5, -0.5, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0,  # 左下
    ]
    vertices = np.array(vertices, dtype=np.float32)
    indices = [
        0, 1, 3,  # first triangle
        1, 2, 3  # second triangle
    ]
    indices = np.array(indices, dtype=np.float32)

    # 在GPU上创建内存用于储存顶点数据，配置OpenGL如何解释这些内存，并且指定其如何发送给显卡，交给顶点着色器处理
    VAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)
    EBO = glGenBuffers(1)

    glBindVertexArray(VAO)

    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

    # -------------------------------------------------------------------
    # 已经把顶点数据储存在显卡的内存中，用VBO这个顶点缓冲对象管理
    # 开始编写着色器
    # -------------------------------------------------------------------

    with open("VertexShader", "rb") as file:
        vertexShaderSource = file.read()

    with open("FragmentShader", "rb") as  file:
        fragmentShaderSource = file.read()

    # 使用封装的 shaders 库
    shaderProgram = compileProgram(compileShader(vertexShaderSource, GL_VERTEX_SHADER),
                                   compileShader(fragmentShaderSource, GL_FRAGMENT_SHADER))

    # 用刚创建的程序对象作为它的参数，以激活这个程序对象，每个着色器调用和渲染调用都会使用这个程序对象
    glUseProgram(shaderProgram)

    # -------------------------------------------------------------------
    # 链接顶点属性
    # 我们必须手动指定输入数据的哪一个部分对应顶点着色器的哪一个顶点属性
    # -------------------------------------------------------------------
    # position attribute
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * 4, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    # color attribute
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 8 * 4, ctypes.c_void_p(12))
    glEnableVertexAttribArray(1)
    # texturecoord attribute
    glEnableVertexAttribArray(2)
    glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 8 * 4, ctypes.c_void_p(24))

    # -------------------------------------------------------------------
    # 纹理
    # -------------------------------------------------------------------
    texture = glGenTextures(1)  # 创建纹理
    glBindTexture(GL_TEXTURE_2D, texture)  # 绑定创建的纹理

    # 为当前绑定的纹理对象设置环绕、过滤方式
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    # 加载并生成纹理
    # image = Image.open("wall.jpg")
    image = Image.open("textures/cat.png")
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    img_data = image.convert("RGBA").tobytes()

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    glGenerateMipmap(GL_TEXTURE_2D)

    # -------------------------------------------------------------------
    # 渲染循环: 让GLFW退出前一直保持运行
    # -------------------------------------------------------------------

    while not glfw.window_should_close(window):  # 检查一次GLFW是否被要求退出
        processInput(window)

        # 清除颜色缓冲
        glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)
        # 记得激活着色器
        # glUseProgram(shaderProgram)

        # 绑定纹理
        glBindTexture(GL_TEXTURE_2D, texture)

        # 绘制
        glDrawArrays(GL_TRIANGLES, 0, 3)

        # glBindVertexArray(VAO)
        # glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)

        glfw.swap_buffers(window)  # 交换颜色缓冲
        glfw.poll_events()  # 检查有没有触发什么事件（比如键盘输入、鼠标移动等）、更新窗口状态，并调用对应的回调函数

    glDeleteVertexArrays(1, VAO)
    glDeleteBuffers(1, VBO)
    glDeleteBuffers(1, EBO)

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
