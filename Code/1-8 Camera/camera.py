from glm import *


class Camera:
    def __init__(self, movementSpeed):
        self.cameraPos = vec3(0.0, 0.0, 3.0)
        self.cameraFront = vec3(0.0, 0.0, -1.0)
        self.cameraUp = vec3(0.0, 1.0, 0.0)
        self.movementSpeed = movementSpeed
        self.sensitivity = 0.1
        self.yaw = -90
        self.pitch = 0.0
        self.fov = 45.0

    def ProcessMouseMovement(self, xoffset, yoffset, constrainPitch = True):
        xoffset *= self.sensitivity
        yoffset *= self.sensitivity
        self.yaw += xoffset
        self.pitch += yoffset
        if constrainPitch:
            if self.pitch > 89.0:
                self.pitch = 89.0
            if self.pitch < -89.0:
                self.pitch = -89.0
        self.updateCameraVectors()

    def updateCameraVectors(self):
        front = vec3()
        front.x = cos(radians(self.yaw)) * cos(radians(self.pitch))
        front.y = sin(radians(self.pitch))
        front.z = sin(radians(self.yaw)) * cos(radians(self.pitch))
        self.cameraFront = normalize(front)