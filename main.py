import pygame
import sys
from pygame import DOUBLEBUF, OPENGL
import numpy as np
import ctypes
import os
os.environ["SDL_VIDEO_X11_FORCE_EGL"] = "1"

from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader


class App:
    def __init__(self) -> None:
        pygame.init()

        pygame.display.set_mode((640,480), OPENGL | DOUBLEBUF)

        self.clock = pygame.time.Clock()

        # colors are not from 0 to 255
        # but they are from 0.1 to 1.0
        glClearColor(0.1, 0.1, 0.2, 1)
        self.shader = self.create_shaders(
            os.path.join('shaders','vertex.vert'),
            os.path.join('shaders','fragment.frag')
        )
        # it is safer to first declare the shader before the meshes
        glUseProgram(self.shader)

        self.triangle = Triangle()

        self.main_loop()

    
    def create_shaders(self, vertex_filepath: str, fragment_filepath: str) -> None:
        vertex_shader: str = ''
        fragment_shader: str = ''

        with open(vertex_filepath, 'r') as f:
            vertex_shader = f.readlines()

        with open(fragment_filepath, 'r') as f:
            fragment_shader = f.readlines()

        shader = compileProgram(
            compileShader(vertex_shader, GL_VERTEX_SHADER),
            compileShader(fragment_shader, GL_FRAGMENT_SHADER)
        )

        return shader
    
    def main_loop(self) -> None:
        running = True

        while running:
            # check events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            glClear(GL_COLOR_BUFFER_BIT)

            glUseProgram(self.shader)
            glBindVertexArray(self.triangle.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.triangle.vertex_count)

            pygame.display.flip()
        
            self.clock.tick(60)
        
        self.quit()


    def quit(self) -> None: 
        self.triangle.destroy()
        glDeleteProgram(self.shader)   
        pygame.quit()
        sys.exit()


class Triangle:
    def __init__(self) -> None:
        self.vertices = (
            -0.5, -0.5, 0.0, 1.0, 0.0, 0.0, # x, y, z, r, g, b
             0.5, -0.5, 0.0, 0.0, 1.0, 0.0, # x, y, z, r, g, b
             0.0,  0.5, 0.0, 0.0, 0.0, 1.0  # x, y, z, r, g, b
        )

        # usual graphical problems with the float32
        self.vertices = np.array(self.vertices, dtype=np.float32)

        self.vertex_count = 3

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))


    def destroy(self) -> None:

        glDeleteVertexArrays(1, (self.vao,))
        glDeleteBuffers(1,(self.vbo,))


if __name__ == '__main__':
    app = App()


