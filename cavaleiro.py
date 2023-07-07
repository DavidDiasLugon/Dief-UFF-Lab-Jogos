import pygame
from config import *


class Cavaleiro(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)  # init so que da herança "pygame.sprite.Sprite"
        self.image = pygame.image.load("Assets/Enemies/knight_left.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.sprite_type = "enemy"
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -15)

        self.initial_pos = pos

        self.Import_enemy_assets()
        self.animation_speed = 0.15
        self.lado = "esquerda"

        self.notice_radius = 190
        self.atack_radius = 120

        self.direction = pygame.math.Vector2()
        self.speed = 3
        self.orientacao = -1
        self.pace_count = 0
        self.turn_after = 400

        self.obstacle_sprites = obstacle_sprites

        self.frame_index = 0
        self.status = 'idle'
        self.place_holder = 'idle'
        #self.image = self.animations[self.status][self.frame_index]

    def Import_enemy_assets(self):
        character_path = "Assets/Enemies/"
        self.animations = {'idle':[]}
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)
        print(self.animations)

    def get_player_distance_direction(self, player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()

        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()

        return(distance, direction)

    def get_status(self, player):
        distance = self.get_player_distance_direction(player)[0]

        if distance <= self.atack_radius:
            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'idle'

    def actions(self, player):
        if self.status == 'move':
            self.direction = pygame.math.Vector2()
            #self.direction = self.get_player_distance_direction(player)[1]
        elif self.status == 'attack':
            pass
        elif self.status == 'idle':
            if self.orientacao == -1:
                self.lado = "esquerda"
            else:
                self.lado = "direita"
            if self.orientacao == 0:
                self.orientacao = -1

            self.pace_count +=1
            self.hitbox.x += self.orientacao

            if self.pace_count >= self.turn_after:
                self.orientacao *= -1
                self.pace_count = 0
    
    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
            
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center


    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0 or self.orientacao > -1:
                        if self.status == 'move':
                            self.hitbox.right = sprite.hitbox.left
                        elif self.status == 'idle':
                            self.orientacao = 0
                            self.pace_count = 0
                    if self.direction.x < 0 or self.orientacao == -1:
                        if self.status == 'move':
                            self.hitbox.left = sprite.hitbox.right
                        elif self.status == 'idle':
                            self.orientacao = 1
                            self.pace_count = 0
        
        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def animate(self):
        animation = self.animations[self.place_holder]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        
        self.image = animation[int(self.frame_index)]
        self.image = pygame.transform.scale(self.image, (64,64))
        if self.lado == "esquerda":
            self.image = pygame.transform.flip(self.image,True,False)
        self.rect = self.image.get_rect(center = self.hitbox.center)

    def update(self):
        self.move(self.speed)


    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)
        self.animate()
