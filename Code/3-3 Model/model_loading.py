import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from glm import *
from camera import Camera
from ObjLoader import ObjLoader
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

    # 加载模型
    indices, vertices = ObjLoader.load_model("backpack/backpack.obj")

    # 在GPU上创建内存用于储存顶点数据，配置OpenGL如何解释这些内存，并且指定其如何发送给显卡，交给顶点着色器处理
    VBO = glGenBuffers(1)

    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * 4, ctypes.c_void_p(0))  # position
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 8 * 4, ctypes.c_void_p(3 * 4))  # normal
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 8 * 4, ctypes.c_void_p(5 * 4))  # texcoord
    glEnableVertexAttribArray(2)

    # -------------------------------------------------------------------
    # 已经把顶点数据储存在显卡的内存中，用VBO这个顶点缓冲对象管理
    # 开始编写着色器
    # -------------------------------------------------------------------

    with open("model_loading.vs", "rb") as file:
        lightingVertexShaderSource = file.read()
    with open("model_loading.fs", "rb") as file:
        lightingFragmentShaderSource = file.read()

    lightingShader = compileProgram(compileShader(lightingVertexShaderSource, GL_VERTEX_SHADER),
                                    compileShader(lightingFragmentShaderSource, GL_FRAGMENT_SHADER))

    # 加载纹理
    load_texture("backpack/diffuse.jpg")
    # glUseProgram(lightingShader)
    # glUniform1i(glGetUniformLocation(lightingShader, "texture_diffuse1"), 0)

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

        glUseProgram(lightingShader)

        # Model
        model = mat4(1.0)
        glUniformMatrix4fv(glGetUniformLocation(lightingShader, "model"), 1, GL_FALSE, value_ptr(model))
        # View
        view = camera.GetViewMatrix()
        glUniformMatrix4fv(glGetUniformLocation(lightingShader, "view"), 1, GL_FALSE, value_ptr(view))
        # Projection Matrix
        projection = perspective(radians(camera.fov), SCR_WIDTH / SCR_HEIGHT, 1.0, 100.0)
        glUniformMatrix4fv(glGetUniformLocation(lightingShader, "projection"), 1, GL_FALSE, value_ptr(projection))

        # 渲染
        glBindVertexArray(VAO)
        glDrawArrays(GL_TRIANGLES, 0, len(indices))


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


if __name__ == '__main__':
    main()
