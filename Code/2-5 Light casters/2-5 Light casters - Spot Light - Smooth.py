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

    # 定义顶点数据：位置，法向量
    vertices = [
        # positions # normals # texturecoords
        - 0.5, -0.5, -0.5, 0.0, 0.0, -1.0, 0.0, 0.0,
        0.5, -0.5, -0.5, 0.0, 0.0, -1.0, 1.0, 0.0,
        0.5, 0.5, -0.5, 0.0, 0.0, -1.0, 1.0, 1.0,
        0.5, 0.5, -0.5, 0.0, 0.0, -1.0, 1.0, 1.0,
        -0.5, 0.5, -0.5, 0.0, 0.0, -1.0, 0.0, 1.0,
        -0.5, -0.5, -0.5, 0.0, 0.0, -1.0, 0.0, 0.0,

        -0.5, -0.5, 0.5, 0.0, 0.0, 1.0, 0.0, 0.0,
        0.5, -0.5, 0.5, 0.0, 0.0, 1.0, 1.0, 0.0,
        0.5, 0.5, 0.5, 0.0, 0.0, 1.0, 1.0, 1.0,
        0.5, 0.5, 0.5, 0.0, 0.0, 1.0, 1.0, 1.0,
        -0.5, 0.5, 0.5, 0.0, 0.0, 1.0, 0.0, 1.0,
        -0.5, -0.5, 0.5, 0.0, 0.0, 1.0, 0.0, 0.0,

        -0.5, 0.5, 0.5, -1.0, 0.0, 0.0, 1.0, 0.0,
        -0.5, 0.5, -0.5, -1.0, 0.0, 0.0, 1.0, 1.0,
        -0.5, -0.5, -0.5, -1.0, 0.0, 0.0, 0.0, 1.0,
        -0.5, -0.5, -0.5, -1.0, 0.0, 0.0, 0.0, 1.0,
        -0.5, -0.5, 0.5, -1.0, 0.0, 0.0, 0.0, 0.0,
        -0.5, 0.5, 0.5, -1.0, 0.0, 0.0, 1.0, 0.0,

        0.5, 0.5, 0.5, 1.0, 0.0, 0.0, 1.0, 0.0,
        0.5, 0.5, -0.5, 1.0, 0.0, 0.0, 1.0, 1.0,
        0.5, -0.5, -0.5, 1.0, 0.0, 0.0, 0.0, 1.0,
        0.5, -0.5, -0.5, 1.0, 0.0, 0.0, 0.0, 1.0,
        0.5, -0.5, 0.5, 1.0, 0.0, 0.0, 0.0, 0.0,
        0.5, 0.5, 0.5, 1.0, 0.0, 0.0, 1.0, 0.0,

        -0.5, -0.5, -0.5, 0.0, -1.0, 0.0, 0.0, 1.0,
        0.5, -0.5, -0.5, 0.0, -1.0, 0.0, 1.0, 1.0,
        0.5, -0.5, 0.5, 0.0, -1.0, 0.0, 1.0, 0.0,
        0.5, -0.5, 0.5, 0.0, -1.0, 0.0, 1.0, 0.0,
        -0.5, -0.5, 0.5, 0.0, -1.0, 0.0, 0.0, 0.0,
        -0.5, -0.5, -0.5, 0.0, -1.0, 0.0, 0.0, 1.0,

        -0.5, 0.5, -0.5, 0.0, 1.0, 0.0, 0.0, 1.0,
        0.5, 0.5, -0.5, 0.0, 1.0, 0.0, 1.0, 1.0,
        0.5, 0.5, 0.5, 0.0, 1.0, 0.0, 1.0, 0.0,
        0.5, 0.5, 0.5, 0.0, 1.0, 0.0, 1.0, 0.0,
        -0.5, 0.5, 0.5, 0.0, 1.0, 0.0, 0.0, 0.0,
        -0.5, 0.5, -0.5, 0.0, 1.0, 0.0, 0.0, 1.0
    ]
    vertices = np.array(vertices, dtype=np.float32)

    cubePositions = [
        vec3(0.0, 0.0, 0.0),
        vec3(2.0, 5.0, -15.0),
        vec3(-1.5, -2.2, -2.5),
        vec3(-3.8, -2.0, -12.3),
        vec3(2.4, -0.4, -3.5),
        vec3(-1.7, 3.0, -7.5),
        vec3(1.3, -2.0, -2.5),
        vec3(1.5, 2.0, -2.5),
        vec3(1.5, 0.2, -1.5),
        vec3(-1.3, 1.0, -1.5)
    ]

    # 在GPU上创建内存用于储存顶点数据，配置OpenGL如何解释这些内存，并且指定其如何发送给显卡，交给顶点着色器处理
    VBO = glGenBuffers(1)

    cubeVAO = glGenVertexArrays(1)
    glBindVertexArray(cubeVAO)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * 4, ctypes.c_void_p(0))  # position
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 8 * 4, ctypes.c_void_p(3 * 4))  # position
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 8 * 4, ctypes.c_void_p(6 * 4))  # position
    glEnableVertexAttribArray(2)

    # 创建灯光
    lightCubeVAO = glGenVertexArrays(1)
    glBindVertexArray(lightCubeVAO)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * 4, ctypes.c_void_p(0))  # position
    glEnableVertexAttribArray(0)

    # -------------------------------------------------------------------
    # 已经把顶点数据储存在显卡的内存中，用VBO这个顶点缓冲对象管理
    # 开始编写着色器
    # -------------------------------------------------------------------

    with open("lightcasters.vs", "rb") as file:
        lightingVertexShaderSource = file.read()
    with open("lightcasters-spotlight-smooth.fs", "rb") as file:
        lightingFragmentShaderSource = file.read()

    lightingShader = compileProgram(compileShader(lightingVertexShaderSource, GL_VERTEX_SHADER),
                                    compileShader(lightingFragmentShaderSource, GL_FRAGMENT_SHADER))

    with open("light_cube.vs", "rb") as file:
        lightCubeVertexShaderSource = file.read()
    with open("light_cube.fs", "rb") as file:
        lightCubeFragmentShaderSource = file.read()

    lightCubeShader = compileProgram(compileShader(lightCubeVertexShaderSource, GL_VERTEX_SHADER),
                                     compileShader(lightCubeFragmentShaderSource, GL_FRAGMENT_SHADER))

    # 加载纹理
    texture1 = loadTexture("textures/container2.png")
    texture2 = loadTexture("textures/container2_specular.png")
    glUseProgram(lightingShader)
    glUniform1i(glGetUniformLocation(lightingShader, "material.diffuse"), 0)  # 指定纹理单元
    glUniform1i(glGetUniformLocation(lightingShader, "material.specular"), 1)

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
        glUniform3fv(glGetUniformLocation(lightingShader, "light.position"), 1, value_ptr(lightPos))
        glUniform3fv(glGetUniformLocation(lightingShader, "viewPos"), 1, value_ptr(camera.cameraPos))
        # 传入材质

        # 传入光照信息
        glUniform3f(glGetUniformLocation(lightingShader, "light.ambient"), 0.2, 0.2, 0.2)
        glUniform3f(glGetUniformLocation(lightingShader, "light.diffuse"), 0.5, 0.5, 0.5)
        glUniform3f(glGetUniformLocation(lightingShader, "light.specular"), 1.0, 1.0, 1.0)
        glUniform1f(glGetUniformLocation(lightingShader, "light.constant"), 1.0)
        glUniform1f(glGetUniformLocation(lightingShader, "light.linear"), 0.09)
        glUniform1f(glGetUniformLocation(lightingShader, "light.quadratic"), 0.032)
        glUniform1f(glGetUniformLocation(lightingShader, "material.shininess"), 32.0)
        glUniform3fv(glGetUniformLocation(lightingShader, "light.position"), 1, value_ptr(camera.cameraPos))
        glUniform3fv(glGetUniformLocation(lightingShader, "light.direction"), 1, value_ptr(camera.cameraFront))
        glUniform1f(glGetUniformLocation(lightingShader, "light.cutOff"), cos(radians(12.5)))
        glUniform1f(glGetUniformLocation(lightingShader, "light.outerCutOff"), cos(radians(17.5)))


        # Model
        model = mat4(1.0)
        glUniformMatrix4fv(glGetUniformLocation(lightingShader, "model"), 1, GL_FALSE, value_ptr(model))
        # View
        view = camera.GetViewMatrix()
        glUniformMatrix4fv(glGetUniformLocation(lightingShader, "view"), 1, GL_FALSE, value_ptr(view))
        # Projection Matrix
        projection = perspective(radians(camera.fov), SCR_WIDTH / SCR_HEIGHT, 1.0, 100.0)
        glUniformMatrix4fv(glGetUniformLocation(lightingShader, "projection"), 1, GL_FALSE, value_ptr(projection))

        # 激活纹理单元
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, texture1)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, texture2)

        # 渲染
        glBindVertexArray(cubeVAO)


        for i in range(10):
            model = mat4(1.0)
            model = translate(model, cubePositions[i])
            angle = 20.0 * i
            model = rotate(model, glfw.get_time() * radians(angle), vec3(1.0, 0.3, 0.5))
            modelLoc = glGetUniformLocation(lightingShader, "model")
            glUniformMatrix4fv(modelLoc, 1, GL_FALSE, value_ptr(model))
            glDrawArrays(GL_TRIANGLES, 0, 36)

        # 光源
        glUseProgram(lightCubeShader)
        glUniformMatrix4fv(glGetUniformLocation(lightCubeShader, "view"), 1, GL_FALSE, value_ptr(view))
        glUniformMatrix4fv(glGetUniformLocation(lightCubeShader, "projection"), 1, GL_FALSE, value_ptr(projection))
        model = mat4(1.0)
        model = translate(model, lightPos)
        model = scale(model, vec3(0.2))
        glUniformMatrix4fv(glGetUniformLocation(lightCubeShader, "model"), 1, GL_FALSE, value_ptr(model))
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
    camera.fov -= yoffset
    if camera.fov < 1.0:
        camera.fov = 1.0
    if camera.fov > 45.0:
        camera.fov = 45.0


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

def loadTexture(path):
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    # 为当前绑定的纹理对象设置环绕、过滤方式
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    # 加载并生成纹理
    image = Image.open(path)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    data = image.convert("RGB").tobytes()
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, data)
    glGenerateMipmap(GL_TEXTURE_2D)
    return texture


if __name__ == '__main__':
    main()
