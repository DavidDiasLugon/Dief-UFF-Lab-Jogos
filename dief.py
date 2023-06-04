import pygame
from config import *

"""player_walk_images = [
    pygame.image.load("lateral_1.png"),
    pygame.image.load("lateral_2.png"),
    pygame.image.load("lateral_3.png"),
]
frontal = pygame.image.load("Dief_frontal.png")

subindo = [
    pygame.image.load("subindo_1.png"),
    pygame.image.load("subindo_2.png"),
    pygame.image.load("subindo_3.png"),
]

descendo = [
    pygame.image.load("descendo_1.png"),
    pygame.image.load("Dief_frontal.png"),
    pygame.image.load("descendo_2.png"),
]"""


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacles_sprites):
        super().__init__(groups)  # init so que da herança "pygame.sprite.Sprite"
        self.image = pygame.image.load(
            "Assets/Main Character/Dief_frontal.png"
        ).convert_alpha()  # ../sprites/test/player.png
        self.image = pygame.transform.scale(self.image, (54, 64))
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -20)
        self.direction = pygame.math.Vector2()
        self.speed = 8

        self.obstacle_sprites = obstacles_sprites

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0
    
    def move(self,speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        
        self.hitbox.x += self.direction.x *speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center
    
    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: #movendo pra direita
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0: #movendo pra esquerda
                        self.hitbox.left = sprite.hitbox.right
        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0: #movendo pra baixo
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0: #movendo pra cima
                        self.hitbox.top = sprite.hitbox.bottom

    def update(self):
        self.input()
        self.rect.center += self.direction * self.speed
        self.move(self.speed)
