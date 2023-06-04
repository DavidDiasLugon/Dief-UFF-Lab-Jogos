import pygame
from pygame.locals import *
import sys
import math
import random
from config import *

pygame.init()

display = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

player_walk_images = [
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
]


class Player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.animation_count_horizontal = 0
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def main(self, display):
        if self.animation_count_horizontal + 1 >= 12:
            self.animation_count_horizontal = 0
        self.animation_count_horizontal += 1

        if self.moving_left:
            display.blit(
                pygame.transform.scale(
                    player_walk_images[self.animation_count_horizontal // 4], (42, 52)
                ),
                (self.x, self.y),
            )
        elif self.moving_right:
            display.blit(
                pygame.transform.scale(
                    pygame.transform.flip(
                        player_walk_images[self.animation_count_horizontal // 4],
                        True,
                        False,
                    ),
                    (42, 52),
                ),
                (self.x, self.y),
            )
        elif self.moving_up:
            display.blit(
                pygame.transform.scale(
                    subindo[self.animation_count_horizontal // 4], (42, 52)
                ),
                (self.x, self.y),
            )
        elif self.moving_down:
            display.blit(
                pygame.transform.scale(
                    descendo[self.animation_count_horizontal // 4], (42, 52)
                ),
                (self.x, self.y),
            )
        else:
            display.blit(
                pygame.transform.scale(frontal, (42, 52)),
                (self.x, self.y),
            )
        self.moving_right = False
        self.moving_left = False
        self.moving_down = False
        self.moving_up = False


class PlayerBullet:
    def __init__(self, x, y, mouse_x, mouse_y):
        self.x = x
        self.y = y
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        self.speed = 15
        self.angle = math.atan2(y - mouse_y, x - mouse_x)
        self.x_vel = math.cos(self.angle) * self.speed
        self.y_vel = math.sin(self.angle) * self.speed

    def main(self, display):
        self.x -= int(self.x_vel)
        self.y -= int(self.y_vel)

        pygame.draw.circle(display, (0, 0, 0), (self.x, self.y), 5)


class KnightEnemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y  # CONTINUAR DAQUI
        self.animation_images_right = [
            pygame.image.load("knighRight1.png"),
            pygame.image.load("knightRight2.png"),
            pygame.image.load("knightRight3.png"),
            pygame.image.load("knightRight4.png"),
            pygame.image.load("knightRight5.png"),
            pygame.image.load("knightRight6.png"),
            pygame.image.load("knightRight7.png"),
            pygame.image.load("knightRight8.png"),
        ]
        self.animation_count = 0
        self.reset_offset = 0
        self.offset_x = random.randrange(-150, 150)
        self.offset_y = random.randrange(-150, 150)

    def main(self, display):
        if self.animation_count + 1 == 32:
            self.animation_count = 0
        self.animation_count += 1

        if self.reset_offset == 0:
            self.offset_x = random.randrange(-150, 150)
            self.offset_y = random.randrange(-150, 150)
            self.reset_offset = random.randrange(120, 150)
        else:
            self.reset_offset -= 1

        if player.x + self.offset_x > self.x - display_scroll[0]:
            self.x += 1
        elif player.x + self.offset_x < self.x - display_scroll[0]:
            self.x -= 1

        if player.y + self.offset_y > self.y - display_scroll[1]:
            self.y += 1
        elif player.y + self.offset_y < self.y - display_scroll[1]:
            self.y -= 1

        display.blit(
            pygame.transform.scale(
                self.animation_images_right[self.animation_count // 4], (52, 52)
            ),
            (self.x - display_scroll[0], self.y - display_scroll[1]),
        )


player = Player(640, 360, 32, 32)

player_bullets = []

enemies = [KnightEnemy(400, 300)]

display_scroll = [0, 0]

while True:
    display.fill((24, 164, 86))

    mouse_x, mouse_y = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                player_bullets.append(
                    PlayerBullet(player.x, player.y, mouse_x, mouse_y)
                )

    keys = pygame.key.get_pressed()

    pygame.draw.rect(
        display,
        (255, 255, 255),
        (100 - display_scroll[0], 100 - display_scroll[1], 16, 16),
    )

    if keys[pygame.K_a]:
        display_scroll[0] -= 5
        player.moving_left = True

        for bullet in player_bullets:
            bullet.x += 5
    if keys[pygame.K_d]:
        display_scroll[0] += 5
        player.moving_right = True

        for bullet in player_bullets:
            bullet.x -= 5
    if keys[pygame.K_w]:
        display_scroll[1] -= 5
        player.moving_up = True

        for bullet in player_bullets:
            bullet.y += 5
    if keys[pygame.K_s]:
        display_scroll[1] += 5
        player.moving_down = True

        for bullet in player_bullets:
            bullet.y -= 5

    player.main(display)

    for bullet in player_bullets:
        bullet.main(display)

    for enemy in enemies:
        enemy.main(display)

    clock.tick(60)
    pygame.display.update()
