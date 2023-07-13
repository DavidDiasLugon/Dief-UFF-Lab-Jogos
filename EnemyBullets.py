import math
import pygame
from AtackCheck import check_atack


class EnemyBullets(pygame.sprite.Sprite):
        def __init__(self, x, y, player_x, player_y, groups, obstacles_sprites):
            super().__init__(groups)
            self.x = x
            self.y = y
            self.player_x = player_x
            self.player_y = player_y
            self.speed = 20
            self.angle = math.atan2(y - player_y, x - player_x)
            self.x_vel = math.cos(self.angle) * self.speed
            self.y_vel = math.sin(self.angle) * self.speed
            self.image = pygame.image.load("Assets/aim/mira_2.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (20, 20))
            self.rect = self.image.get_rect(topleft=(x, y))
            self.hitbox = self.rect.inflate(10, 10)
            self.player_pos = player_x, player_y
            self.direction = pygame.math.Vector2()
            self.obstacle_sprites = obstacles_sprites
            self.contador = 10
            self.status = 0
        
        '''def __getattribute__(self, self.status):
            self.self.status'''

        def get_player_distance_direction(self, player):
            enemy_vec = pygame.math.Vector2(self.rect.center)
            player_vec = player
            distance = (player_vec - enemy_vec).magnitude()

            if distance > 0:
                direction = (player_vec - enemy_vec).normalize()
            else:
                direction = pygame.math.Vector2()
            
            return(distance, direction)

        def move(self, speed, player):
            self.direction = self.get_player_distance_direction(player)[1]

            if self.direction.magnitude() != 0:
                self.direction = self.direction.normalize()
            
            self.hitbox.x += self.direction.x * speed
            self.collision('horizontal')
            self.hitbox.y += self.direction.y * speed
            self.collision('vertical')
            self.rect.center = self.hitbox.center

        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            if self.rect.colliderect(self.player_x, self.player_y, 40, 30):
                self.kill()
                self.status = "attack"
                check_atack(1,0)
                return self.status
            else:
                self.status = 'danone'
                return self.status

        def return_status(self):
            return self.status

        def collision(self, direction):
            if direction == 'horizontal':
                for sprite in self.obstacle_sprites:
                    if sprite.hitbox.colliderect(self.hitbox):
                        if self.direction.x > 0:
                            self.hitbox.right = sprite.hitbox.left
                            self.kill()
                        if self.direction.x < 0:
                            self.hitbox.left = sprite.hitbox.right
                            self.kill()
            
            if direction == 'vertical':
                for sprite in self.obstacle_sprites:
                    if sprite.hitbox.colliderect(self.hitbox):
                        if self.direction.y > 0:
                            self.hitbox.bottom = sprite.hitbox.top
                            self.kill()
                        if self.direction.y < 0:
                            self.hitbox.top = sprite.hitbox.bottom
                            self.kill()
        
        def update(self):
            self.move(self.speed, self.player_pos)
            self.contador -= 1
            if self.contador == 0:
                self.kill()
