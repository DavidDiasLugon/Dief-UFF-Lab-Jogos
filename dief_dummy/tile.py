import pygame
from config import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)  # init so que da herança "pygame.sprite.Sprite"
        self.image = pygame.image.load("../sprites/test/rock5.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
    

