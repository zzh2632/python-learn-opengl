import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
from PIL import Image
from glm import *
from camera import Camera
from TextureLoader import load_texture

SCR_WIDTH = 800
SCR_HEIGHT = 600

# 相机属性

camera = Camera(2.5)
lastX = 800.0 / 2.0
lastY = 600.0 / 2.0
firstMouse = True

deltaTime = 0.0
lastFrame = 0.0


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
    # 开启模板缓冲
    glDepthFunc(GL_LESS)
    glEnable(GL_STENCIL_TEST)
    glStencilFunc(GL_NOTEQUAL, 1, 0xFF)
    glStencilOp(GL_KEEP, GL_KEEP, GL_REPLACE)

    # -------------------------------------------------------------------
    # 顶点输入
    # -------------------------------------------------------------------

    # 定义顶点数据
    cubeVertices = [
        -0.5, -0.5, -0.5, 0.0, 0.0,
        0.5, -0.5, -0.5, 1.0, 0.0,
        0.5, 0.5, -0.5, 1.0, 1.0,
        0.5, 0.5, -0.5, 1.0, 1.0,
        -0.5, 0.5, -0.5, 0.0, 1.0,
        -0.5, -0.5, -0.5, 0.0, 0.0,

        -0.5, -0.5, 0.5, 0.0, 0.0,
        0.5, -0.5, 0.5, 1.0, 0.0,
        0.5, 0.5, 0.5, 1.0, 1.0,
        0.5, 0.5, 0.5, 1.0, 1.0,
        -0.5, 0.5, 0.5, 0.0, 1.0,
        -0.5, -0.5, 0.5, 0.0, 0.0,

        -0.5, 0.5, 0.5, 1.0, 0.0,
        -0.5, 0.5, -0.5, 1.0, 1.0,
        -0.5, -0.5, -0.5, 0.0, 1.0,
        -0.5, -0.5, -0.5, 0.0, 1.0,
        -0.5, -0.5, 0.5, 0.0, 0.0,
        -0.5, 0.5, 0.5, 1.0, 0.0,

        0.5, 0.5, 0.5, 1.0, 0.0,
        0.5, 0.5, -0.5, 1.0, 1.0,
        0.5, -0.5, -0.5, 0.0, 1.0,
        0.5, -0.5, -0.5, 0.0, 1.0,
        0.5, -0.5, 0.5, 0.0, 0.0,
        0.5, 0.5, 0.5, 1.0, 0.0,

        -0.5, -0.5, -0.5, 0.0, 1.0,
        0.5, -0.5, -0.5, 1.0, 1.0,
        0.5, -0.5, 0.5, 1.0, 0.0,
        0.5, -0.5, 0.5, 1.0, 0.0,
        -0.5, -0.5, 0.5, 0.0, 0.0,
        -0.5, -0.5, -0.5, 0.0, 1.0,

        -0.5, 0.5, -0.5, 0.0, 1.0,
        0.5, 0.5, -0.5, 1.0, 1.0,
        0.5, 0.5, 0.5, 1.0, 0.0,
        0.5, 0.5, 0.5, 1.0, 0.0,
        -0.5, 0.5, 0.5, 0.0, 0.0,
        -0.5, 0.5, -0.5, 0.0, 1.0
    ]
    cubeVertices = np.array(cubeVertices, dtype=np.float32)

    planeVertices = [
        5.0, -0.5, 5.0, 2.0, 0.0,
        -5.0, -0.5, 5.0, 0.0, 0.0,
        -5.0, -0.5, -5.0, 0.0, 2.0,
        5.0, -0.5, 5.0, 2.0, 0.0,
        -5.0, -0.5, -5.0, 0.0, 2.0,
        5.0, -0.5, -5.0, 2.0, 2.0
    ]
    planeVertices = np.array(planeVertices, dtype=np.float32)


    # 在GPU上创建内存用于储存顶点数据，配置OpenGL如何解释这些内存，并且指定其如何发送给显卡，交给顶点着色器处理
    cubeVAO = glGenVertexArrays(1)
    cubeVBO = glGenBuffers(1)
    glBindVertexArray(cubeVAO)
    glBindBuffer(GL_ARRAY_BUFFER, cubeVBO)
    glBufferData(GL_ARRAY_BUFFER, cubeVertices.nbytes, cubeVertices, GL_STATIC_DRAW)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 5 * 4, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 5 * 4, ctypes.c_void_p(3 * 4))
    glEnableVertexAttribArray(1)
    glBindVertexArray(0)

    planeVAO = glGenVertexArrays(1)
    planeVBO = glGenBuffers(1)
    glBindVertexArray(planeVAO)
    glBindBuffer(GL_ARRAY_BUFFER, planeVBO)
    glBufferData(GL_ARRAY_BUFFER, planeVertices.nbytes, planeVertices, GL_STATIC_DRAW)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 5 * 4, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 5 * 4, ctypes.c_void_p(3 * 4))
    glEnableVertexAttribArray(1)
    glBindVertexArray(0)

    # -------------------------------------------------------------------
    # 已经把顶点数据储存在显卡的内存中，用VBO这个顶点缓冲对象管理
    # 开始编写着色器
    # -------------------------------------------------------------------

    with open("VertexShader", "rb") as file:
        vertexShaderSource = file.read()

    with open("FragmentShader", "rb") as file:
        fragmentShaderSource = file.read()

    # 使用封装的 shaders 库
    shaderProgram = compileProgram(compileShader(vertexShaderSource, GL_VERTEX_SHADER),
                                   compileShader(fragmentShaderSource, GL_FRAGMENT_SHADER))

    with open("VertexShader", "rb") as file:
        vertexShaderSource = file.read()

    with open("shaderSingleColor", "rb") as file:
        stencil_single_color = file.read()

    # 使用封装的 shaders 库
    shaderSingleColor = compileProgram(compileShader(vertexShaderSource, GL_VERTEX_SHADER),
                                   compileShader(stencil_single_color, GL_FRAGMENT_SHADER))

    # -------------------------------------------------------------------
    # 纹理
    # -------------------------------------------------------------------

    cubeTexture = load_texture("textures/container.jpg")
    floorTexture = load_texture("textures/awesomeface.png")

    glUseProgram(shaderProgram)
    # 获取采样器统一变量在着色器中的位置，并为其赋值，指定其相应的纹理单元
    glUniform1i(glGetUniformLocation(shaderProgram, "texture1"), 0)

    # -------------------------------------------------------------------
    # 渲染循环: 让GLFW退出前一直保持运行
    # -------------------------------------------------------------------

    while not glfw.window_should_close(window):  # 检查一次GLFW是否被要求退出
        global deltaTime, lastFrame

        currentFrame = glfw.get_time()
        deltaTime = currentFrame - lastFrame
        lastFrame = currentFrame

        processInput(window)

        # 渲染
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT)

        glUseProgram(shaderSingleColor)
        model = mat4(1.0)
        view = camera.GetViewMatrix()
        projection = perspective(radians(camera.fov), SCR_WIDTH / SCR_HEIGHT, 1.0, 100.0)
        glUniformMatrix4fv(glGetUniformLocation(shaderSingleColor, "view"), 1, GL_FALSE, value_ptr(view))
        glUniformMatrix4fv(glGetUniformLocation(shaderSingleColor, "projection"), 1, GL_FALSE, value_ptr(projection))

        glUseProgram(shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(shaderProgram, "view"), 1, GL_FALSE, value_ptr(view))
        glUniformMatrix4fv(glGetUniformLocation(shaderProgram, "projection"), 1, GL_FALSE, value_ptr(projection))

        # draw floor as normal, but don't write the floor to the stencil buffer, we only care about the containers.
        # We set its mask to 0x00 to not write to the stencil buffer.
        glStencilMask(0x00)

        # floor
        glBindVertexArray(planeVAO)
        glBindTexture(GL_TEXTURE_2D, floorTexture)
        glUniformMatrix4fv(glGetUniformLocation(shaderProgram, "model"), 1, GL_FALSE, value_ptr(mat4(1.0)))
        glDrawArrays(GL_TRIANGLES, 0, 6)
        glBindVertexArray(0)

        # 1st. render pass, draw objects as normal, writing to the stencil buffer
        glStencilFunc(GL_ALWAYS, 1, 0xFF)
        glStencilMask(0xFF)

        # cubes
        model = mat4(1.0)
        glBindVertexArray(cubeVAO)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, cubeTexture)
        model = translate(model, vec3(-1.0, 0.0, -1.0))
        glUniformMatrix4fv(glGetUniformLocation(shaderProgram, "model"), 1, GL_FALSE, value_ptr(model))
        glDrawArrays(GL_TRIANGLES, 0, 36)
        model = mat4(1.0)
        model = translate(model, vec3(2.0, 0.0, 0.0))
        glUniformMatrix4fv(glGetUniformLocation(shaderProgram, "model"), 1, GL_FALSE, value_ptr(model))
        glDrawArrays(GL_TRIANGLES, 0, 36)

        # 2nd. render pass: now draw slightly scaled versions of the objects, this time disabling stencil writing.
        # Because the stencil buffer is now filled with several 1s. The parts of the buffer that are 1 are not drawn, thus only drawing
        # the objects' size differences, making it look like borders.
        glStencilFunc(GL_NOTEQUAL, 1, 0xFF)
        glStencilMask(0x00)
        glDisable(GL_DEPTH_TEST)
        glUseProgram(shaderSingleColor)
        objet_scale = 1.1
        # cubes
        glBindVertexArray(cubeVAO)
        glBindTexture(GL_TEXTURE_2D, cubeTexture)
        model = mat4(1.0)
        model = translate(model, vec3(-1.0, 0.0, -1.0))
        model = scale(model, vec3(objet_scale, objet_scale, objet_scale))
        glUniformMatrix4fv(glGetUniformLocation(shaderSingleColor, "model"), 1, GL_FALSE, value_ptr(model))
        glDrawArrays(GL_TRIANGLES, 0, 36)
        model = mat4(1.0)
        model = translate(model, vec3(2.0, 0.0, 0.0))
        model = scale(model, vec3(objet_scale, objet_scale, objet_scale))
        glUniformMatrix4fv(glGetUniformLocation(shaderProgram, "model"), 1, GL_FALSE, value_ptr(model))
        glDrawArrays(GL_TRIANGLES, 0, 36)
        glBindVertexArray(0)
        glStencilMask(0xFF)
        glStencilFunc(GL_ALWAYS, 0, 0xFF)
        glEnable(GL_DEPTH_TEST)

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
    camera.fov -= yoffset
    if camera.fov < 1.0:
        fov = 1.0
    if camera.fov > 45.0:
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
