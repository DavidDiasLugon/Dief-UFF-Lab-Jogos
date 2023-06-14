import pygame
from config import *


class Chave(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)  # init so que da herança "pygame.sprite.Sprite"
        self.image = pygame.image.load("Assets/Itens/Key/key.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 40))
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, -10)
        self.animation_speed = 0.15
        self.status = "white_sprites"
        self.frame_index = 0
        self.import_player_assets()
    
    def import_player_assets(self):
        sprite_path = "Assets/Itens/Key"
        self.animations = {"white_sprites":[]}
        self.animations["white_sprites"] = import_folder("Assets/Itens/Key/white_sprites")
        '''for animation in self.animations.keys():
            full_path = sprite_path + animation
            self.animations[animation] = import_folder(full_path)'''
        print(self.animations)
    
    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        
        self.image = animation[int(self.frame_index)]
        self.image = pygame.transform.scale(self.image, (30, 40))
    
    def update(self):
        self.animate()
