import pygame
from config import *
from os import kill



class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacles_sprites, chave_sprite, destroy_key, bau_sprite, destroy_bau):
        super().__init__(groups)  # init so que da herança "pygame.sprite.Sprite"
        self.image = pygame.image.load(
            "Assets/Main Character/Dief_frontal.png"
        ).convert_alpha() 
        self.image = pygame.transform.scale(self.image, (54, 64))
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -20)

        self.Import_player_assets()
        self.status = 'down'
        self.frame_index = 0
        self.animation_speed = 0.15
        self.orientacao = 0

        self.direction = pygame.math.Vector2()
        self.speed = 5

        self.obstacle_sprites = obstacles_sprites

        self.chave_sprite = chave_sprite
        self.destroy_key = destroy_key
        self.tem_chave = False

        self.bau_sprite = bau_sprite
        self.destroy_bau = destroy_bau

    def Import_player_assets(self):
        character_path = "Assets/Main Character/"
        self.animations = {'up':[],
                           'up_idle':[],
                           'lado':[],
                           'lado_idle':[],
                           'down':[],
                           'down_idle':[]}
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)
        print(self.animations)

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.status = 'up'
            self.orientacao = 0
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.status = 'down'
            self.orientacao = 0
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = 'lado'
            self.orientacao = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = 'lado'
            self.orientacao = 0
        else:
            self.direction.x = 0
    
    def get_status(self):
        #idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status:
                self.status = self.status + '_idle'

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
            for sprite in self.chave_sprite:
                if sprite.hitbox.colliderect(self.hitbox):
                    self.destroy_key()
                    self.tem_chave = True

            for sprite in self.bau_sprite:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.tem_chave:
                        self.destroy_bau()
                        self.tem_chave = False
                    else:
                        if self.direction.x > 0: #movendo pra direita
                            self.hitbox.right = sprite.hitbox.left
                        if self.direction.x < 0: #movendo pra esquerda
                            self.hitbox.left = sprite.hitbox.right

            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: #movendo pra direita
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0: #movendo pra esquerda
                        self.hitbox.left = sprite.hitbox.right
        if direction == 'vertical':
            for sprite in self.chave_sprite:
                if sprite.hitbox.colliderect(self.hitbox):
                    self.destroy_key()
                    self.tem_chave = True

            for sprite in self.bau_sprite:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.tem_chave:
                        self.destroy_bau()
                        self.tem_chave = False
                    else:
                        if self.direction.y > 0: #movendo pra baixo
                            self.hitbox.bottom = sprite.hitbox.top
                        if self.direction.y < 0: #movendo pra cima
                            self.hitbox.top = sprite.hitbox.bottom

            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0: #movendo pra baixo
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0: #movendo pra cima
                        self.hitbox.top = sprite.hitbox.bottom

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        
        self.image = animation[int(self.frame_index)]
        self.image = pygame.transform.scale(self.image, (54, 64))
        if self.orientacao == 1:
            self.image = pygame.transform.flip(self.image,True,False)
        self.rect = self.image.get_rect(center = self.hitbox.center)

    def update(self):
        self.input()
        self.rect.center += self.direction * self.speed
        self.get_status()
        self.animate()
        self.move(self.speed)
