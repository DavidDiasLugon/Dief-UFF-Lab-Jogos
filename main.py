import pygame, sys
from config import *
from level import Level
from dief import *
from PPlay import *
import pygame
from pygame.locals import *
from pygame import mixer
from random import randint


class Game:
    def __init__(self):
        # Setup geral
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Dief")
        self.clock = pygame.time.Clock()
        self.level = Level()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            color = (0, 0, 0)
            self.screen.fill(color)
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)
            

if __name__ == "__main__":
    game = Game()
    game.run()
