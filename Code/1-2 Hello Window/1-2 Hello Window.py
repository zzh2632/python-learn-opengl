import glfw
from OpenGL import GL


def main():
    # 实例化GLFW窗口
    glfw.init()

    # 配置GLFW
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)  # 主版本号
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)  # 次版本号
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE) # 核心模式

    # 创建一个窗口对象，这个窗口对象存放了所有和窗口相关的数据
    window = glfw.create_window(800, 600, "LearnOpenGL", None, None)
    glfw.set_window_pos(window, 400, 200)
    glfw.make_context_current(window)

    # OpenGL渲染窗口的尺寸大小：视口
    width, height = glfw.get_framebuffer_size(window)
    GL.glViewport(0, 0, width, height)
    # 注册:每当窗口调整大小的时候调用
    glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)

    # 渲染循环: 让GLFW退出前一直保持运行
    while not glfw.window_should_close(window):  # 检查一次GLFW是否被要求退出
        processInput(window)

        glfw.swap_buffers(window)   # 交换颜色缓冲
        glfw.poll_events()  # 检查有没有触发什么事件（比如键盘输入、鼠标移动等）、更新窗口状态，并调用对应的回调函数

    # 渲染循环结束后我们需要正确释放/删除之前的分配的所有资源
    glfw.terminate()
    return


# 用户改变窗口的大小的时候，视口也应该被调整
def framebuffer_size_callback(window, width, height):
    GL.glViewport(0, 0, width, height)


def processInput(window):
    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
        glfw.set_window_should_close(window, GL.GL_TRUE)


if __name__ == '__main__':
    main()
