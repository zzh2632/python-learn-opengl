import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
from PIL import Image
from glm import *
from camera import Camera

SCR_WIDTH = 800
SCR_HEIGHT = 600

# 相机属性

camera = Camera(2.5)
lastX = 800.0 / 2.0
lastY = 600.0 / 2.0
firstMouse = True

deltaTime = 0.0
lastFrame = 0.0

lightPos = vec3(1.2, 1.0, 2.0)


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
    # 隐藏光标，并保持在屏幕中心
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
    # 注册光标回调
    glfw.set_cursor_pos_callback(window, mouse_callback)
    # 滚轮回调
    glfw.set_scroll_callback(window, scroll_callback)
    # 开启深度测试
    glEnable(GL_DEPTH_TEST)

    # -------------------------------------------------------------------
    # 顶点输入
    # -------------------------------------------------------------------

    # 定义顶点数据
    vertices = [
        -0.5, -0.5, -0.5,
        0.5, -0.5, -0.5,
        0.5, 0.5, -0.5,
        0.5, 0.5, -0.5,
        -0.5, 0.5, -0.5,
        -0.5, -0.5, -0.5,

        -0.5, -0.5, 0.5,
        0.5, -0.5, 0.5,
        0.5, 0.5, 0.5,
        0.5, 0.5, 0.5,
        -0.5, 0.5, 0.5,
        -0.5, -0.5, 0.5,

        -0.5, 0.5, 0.5,
        -0.5, 0.5, -0.5,
        -0.5, -0.5, -0.5,
        -0.5, -0.5, -0.5,
        -0.5, -0.5, 0.5,
        -0.5, 0.5, 0.5,

        0.5, 0.5, 0.5,
        0.5, 0.5, -0.5,
        0.5, -0.5, -0.5,
        0.5, -0.5, -0.5,
        0.5, -0.5, 0.5,
        0.5, 0.5, 0.5,

        -0.5, -0.5, -0.5,
        0.5, -0.5, -0.5,
        0.5, -0.5, 0.5,
        0.5, -0.5, 0.5,
        -0.5, -0.5, 0.5,
        -0.5, -0.5, -0.5,

        -0.5, 0.5, -0.5,
        0.5, 0.5, -0.5,
        0.5, 0.5, 0.5,
        0.5, 0.5, 0.5,
        -0.5, 0.5, 0.5,
        -0.5, 0.5, -0.5
    ]
    vertices = np.array(vertices, dtype=np.float32)


    # 在GPU上创建内存用于储存顶点数据，配置OpenGL如何解释这些内存，并且指定其如何发送给显卡，交给顶点着色器处理
    VBO = glGenBuffers(1)

    cubeVAO = glGenVertexArrays(1)
    glBindVertexArray(cubeVAO)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * 4, ctypes.c_void_p(0))  # position
    glEnableVertexAttribArray(0)

    # 创建灯光
    lightCubeVAO = glGenVertexArrays(1)
    glBindVertexArray(lightCubeVAO)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * 4, ctypes.c_void_p(0))  # position
    glEnableVertexAttribArray(0)

    # -------------------------------------------------------------------
    # 已经把顶点数据储存在显卡的内存中，用VBO这个顶点缓冲对象管理
    # 开始编写着色器
    # -------------------------------------------------------------------

    with open("colors.vs", "rb") as file:
        lightingVertexShaderSource = file.read()
    with open("colors.fs", "rb") as file:
        lightingFragmentShaderSource = file.read()

    lightingShader = compileProgram(compileShader(lightingVertexShaderSource, GL_VERTEX_SHADER),
                                   compileShader(lightingFragmentShaderSource, GL_FRAGMENT_SHADER))

    with open("light_cube.vs", "rb") as file:
        lightCubeVertexShaderSource = file.read()
    with open("light_cube.fs", "rb") as file:
        lightCubeFragmentShaderSource = file.read()

    lightCubeShader = compileProgram(compileShader(lightCubeVertexShaderSource, GL_VERTEX_SHADER),
                                   compileShader(lightCubeFragmentShaderSource, GL_FRAGMENT_SHADER))


    # -------------------------------------------------------------------
    # 渲染循环: 让GLFW退出前一直保持运行
    # -------------------------------------------------------------------

    while not glfw.window_should_close(window):  # 检查一次GLFW是否被要求退出
        global deltaTime, lastFrame

        currentFrame = glfw.get_time()
        deltaTime = currentFrame - lastFrame
        lastFrame = currentFrame

        processInput(window)

        # 清除颜色缓冲
        glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # 立方体
        glUseProgram(lightingShader)
        objectColorLoc = glGetUniformLocation(lightingShader, "objectColor")
        glUniform3f(objectColorLoc, 1.0, 0.5, 0.31)
        lightColorLoc = glGetUniformLocation(lightingShader, "lightColor")
        glUniform3f(lightColorLoc, 1.0, 1.0, 1.0)
        # Model
        model = mat4(1.0)
        modelLoc = glGetUniformLocation(lightingShader, "model")
        glUniformMatrix4fv(modelLoc, 1, GL_FALSE, value_ptr(model))
        # View
        view = camera.GetViewMatrix()
        viewLoc = glGetUniformLocation(lightingShader, "view")
        glUniformMatrix4fv(viewLoc, 1, GL_FALSE, value_ptr(view))
        # Projection Matrix
        projection = perspective(radians(camera.fov), SCR_WIDTH / SCR_HEIGHT, 1.0, 100.0)
        projectionLoc = glGetUniformLocation(lightingShader, "projection")
        glUniformMatrix4fv(projectionLoc, 1, GL_FALSE, value_ptr(projection))
        # 渲染
        glBindVertexArray(cubeVAO)
        glDrawArrays(GL_TRIANGLES, 0, 36)

        # 光源
        glUseProgram(lightCubeShader)
        # View
        view = camera.GetViewMatrix()
        viewLoc = glGetUniformLocation(lightCubeShader, "view")
        glUniformMatrix4fv(viewLoc, 1, GL_FALSE, value_ptr(view))
        # Projection Matrix
        projection = perspective(radians(camera.fov), SCR_WIDTH / SCR_HEIGHT, 1.0, 100.0)
        projectionLoc = glGetUniformLocation(lightCubeShader, "projection")
        glUniformMatrix4fv(projectionLoc, 1, GL_FALSE, value_ptr(projection))
        # Model
        model = mat4(1.0)
        model = translate(model, lightPos)
        model = scale(model, vec3(0.2))
        modelLoc = glGetUniformLocation(lightCubeShader, "model")
        glUniformMatrix4fv(modelLoc, 1, GL_FALSE, value_ptr(model))
        # 渲染
        glBindVertexArray(lightCubeVAO)
        glDrawArrays(GL_TRIANGLES, 0, 36)

        glfw.swap_buffers(window)  # 交换颜色缓冲
        glfw.poll_events()

    # 渲染循环结束后我们需要正确释放/删除之前的分配的所有资源
    glfw.terminate()
    return


# 用户改变窗口的大小的时候，视口也应该被调整
def framebuffer_size_callback(window, width, height):
    glViewport(0, 0, width, height)


def mouse_callback(window, xpos, ypos):
    global firstMouse, yaw, pitch, lastX, lastY

    if firstMouse:
        lastX = xpos
        lastY = ypos
        firstMouse = False

    xoffset = xpos - lastX
    yoffset = lastY - ypos

    lastX = xpos
    lastY = ypos

    camera.ProcessMouseMovement(xoffset, yoffset)








def scroll_callback(window, xoffset, yoffset):
    global fov
    fov -= yoffset
    if fov < 1.0:
        fov = 1.0
    if fov > 45.0:
        fov = 45.0


def processInput(window):
    global deltaTime
    cameraSpeed = camera.movementSpeed * deltaTime

    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
        glfw.set_window_should_close(window, GL_TRUE)
    if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
        camera.cameraPos += cameraSpeed * camera.cameraFront
    if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
        camera.cameraPos -= cameraSpeed * camera.cameraFront
    if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
        camera.cameraPos -= normalize(cross(camera.cameraFront, camera.cameraUp)) * cameraSpeed
    if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
        camera.cameraPos += normalize(cross(camera.cameraFront, camera.cameraUp)) * cameraSpeed


if __name__ == '__main__':
    main()
