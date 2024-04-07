import pygame
import sys
from pygame import DOUBLEBUF, OPENGL

from OpenGL.GL import *


class App:
    def __init__(self) -> None:
        pygame.init()

        pygame.display.set_mode((640,480), OPENGL | DOUBLEBUF)

        self.clock = pygame.time.Clock()

        # colors are not from 0 to 255
        # but they are from 0.1 to 1.0
        glClearColor(0.1, 0.7, 0.2, 1)

        self.main_loop()

    
    def main_loop(self) -> None:
        running = True

        while running:
            # check events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            glClear(GL_COLOR_BUFFER_BIT)
            pygame.display.flip()
        
            self.clock.tick(60)
        
        self.quit()


    def quit() -> None:    
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    app = App()


