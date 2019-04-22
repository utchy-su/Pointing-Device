import pygame
from pygame.locals import *
import numpy as np


class Master:

    def __init__(self):
        self.screen_size = (900, 900)
        pygame.init()
        self.screen = pygame.display.set_mode(self.screen_size)
        self.screen.fill((255, 255, 255))
        pygame.display.set_caption(u"mouse configuration")


    def main(self):

        while True:

            for event in pygame.event.get():
                if event.type == QUIT:
                    quit()

            pygame.display.update()


if __name__ == '__main__':
    test = Master()
    test.main()