import pygame
from config import *


class Bau(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)  # init so que da herança "pygame.sprite.Sprite"
        self.image = pygame.image.load("Assets/Itens/Chest/Chest1.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 40))
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
