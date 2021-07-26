from glm import *
import numpy as np
from OpenGL.GL import *


class Vertex:
    def __int__(self):
        # 使用 glm: to_list 将 vec()转换为list
        self.Position = vec3(0.0)
        self.Normal = vec3(0.0)
        self.TexCoords = vec2(0.0)


class Texture:
    def __int__(self):
        self.id = 0
        self.type = ""


class Mesh:
    def __init__(self, vertices, indices, textures):
        self.vertices = np.array(vertices, dtype=np.float32)  # vertices为int列表
        self.indices = np.array(indices, dtype=np.uint32)  # int列表
        self.textures = textures  # Texture对象列表
        self.VAO = None
        self.VBO = None
        self.EBO = None
        self.setupMesh()

    def Draw(self, shader):
        # 绘制。期间为shader指定uniform
        diffuseNr = 1
        specularNr = 1
        normalNr = 1
        heightNr = 1
        for i in range(len(self.textures)):
            # active proper texture unit before binding
            glActiveTexture(GL_TEXTURE0 + i)
            # retrieve texture number (the N in diffuse_textureN)
            number = 0
            name = self.textures[i].type
            if name == "texture_diffuse":
                diffuseNr += 1
                number = str(diffuseNr)
            elif name == "texture_specular":
                specularNr += 1
                number = str(specularNr)
            elif name == "texture_normal":
                normalNr += 1
                number = str(normalNr)
            elif name == "texture_height":
                heightNr += 1
                number = str(heightNr)
            # now set the sampler to the correct texture unit
            glUniform1i(glGetUniformLocation(shader, name + number), i)
            # and finally bind the texture
            glBindTexture(GL_TEXTURE_2D, self.textures[i].id)
        # draw mesh
        glBindVertexArray(self.VAO)
        glDrawElements(GL_TRIANGLES, self.indices.size, GL_UNSIGNED_INT, 0)
        glBindVertexArray(0)
        # always good practice to set everything back to defaults once configured.
        glActiveTexture(GL_TEXTURE0)

    def setupMesh(self):
        # 初始化缓冲
        VAO = glGenVertexArrays(1)
        VBO = glGenBuffers(1)
        EBO = glGenBuffers(1)

        glBindVertexArray(VAO)
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices.nbytes * self.indices, GL_STATIC_DRAW)

        # vertex positions
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * 4, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        # vertex normals
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 8 * 4, ctypes.c_void_p(3 * 4))
        glEnableVertexAttribArray(1)
        # vertex texturecoords
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 8 * 4, ctypes.c_void_p(6 * 4))

        glBindVertexArray(0)
