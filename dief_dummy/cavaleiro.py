import pygame
from config import *


class Cavaleiro(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)  # init so que da herança "pygame.sprite.Sprite"
        self.image = pygame.image.load("knight_left.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (75, 72))
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
    