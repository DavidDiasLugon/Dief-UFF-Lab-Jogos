import pygame
from config import *


class Chave(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)  # init so que da herança "pygame.sprite.Sprite"
        self.image = pygame.image.load("../Assets/Key/pixel-art-key/key.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 40))
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
