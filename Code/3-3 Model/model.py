# todo: pyassimp.load(.obj)->crash
from pyassimp import *


class Model:
    def __int__(self, path):
        self.meshes = []
        self.dictionary = ""  # 用于加载贴图
        self.loadModel(path)

    def loadModel(self, path):
        # 加载model为assimp scene对象
        scene = load(path, processing=postprocess.aiProcess_Triangulate | postprocess.aiProcess_FlipUVs)

        if not scene or scene.root
        if (!scene | | scene->mFlags & AI_SCENE_FLAGS_INCOMPLETE | | !scene->mRootNode)
            {
                cout << "ERROR::ASSIMP::" <<
            import.GetErrorString() << endl;
            return;
            }
            directory = path.substr(0, path.find_last_of('/'));

            processNode(scene->mRootNode, scene);

        def processNode(self, node, scene):

        def processNode(self, mesh, scene):
            return meshes

        def loadMaterialTextures(self, mat, type, typeName):
            return textures

        def Draw(self, shader):
            for mesh in self.meshes:
                meshes[i].Draw(shader)
