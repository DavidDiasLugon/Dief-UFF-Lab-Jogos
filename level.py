import pygame
from config import *
from tile import *
from dief import Player
from cavaleiro import Cavaleiro
from chave import Chave
from bau import *
from os import kill
import math
from EnemyBullets import *
from AtackCheck import check_atack


class Level:
    def __init__(self, map):
        # "superficie" a ser exibida
        self.display_surface = pygame.display.get_surface()
        # grupos de sprite
        self.visible_sprites = YSortCameraGroup()  # pygame.sprite.Group()
        self.obstacles_sprites = pygame.sprite.Group()
        self.chave_sprite = pygame.sprite.Group()
        self.chave = None
        self.bau_sprite = pygame.sprite.Group()
        self.bau = None
        self.bau_pos = []
        self.bullet = 0
        self.atacou = 0
        self.mapa = map

        # sprite setup
        self.create_map()

    def create_map(self):
        if self.mapa == 0:
            self.mapa = WORLD_MAP
        elif self.mapa == 1:
            self.mapa = WORLD_MAP2
        elif self.mapa == 2:
            self.mapa = WORLD_MAP3
        for row_index, row in enumerate(self.mapa):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                Y = row_index * TILESIZE
                if col == "x":
                    Tile((x, Y), [self.visible_sprites, self.obstacles_sprites])
                '''if col == "y":
                    x = x * 3
                    Y = Y * 3
                    Tile2((x, Y), [self.visible_sprites, self.obstacles_sprites])
                if col == "z":
                    x = x * 3
                    Y = Y * 3
                    Tile3((x, Y), [self.visible_sprites, self.obstacles_sprites])'''
                if col == "p":
                    self.player = Player((x, Y), [self.visible_sprites],self.obstacles_sprites,self.chave_sprite,self.destroy_key,self.bau_sprite, self.destroy_bau)
                if col == "c":
                    self.cavaleiro = Cavaleiro((x,Y),[self.visible_sprites], self.obstacles_sprites, self.tiro_inimigo, self.fim_de_jogo)
                if col == "k":
                    self.chave = Chave((x,Y),[self.visible_sprites,self.chave_sprite])
                if col == "b":
                    self.bau = Bau((x,Y),[self.visible_sprites,self.bau_sprite])
                    self.bau_pos_x = x
                    self.bau_pos_y = Y

    def fim_de_jogo(self):
        self.cavaleiro.has_collide_player = True

    def tiro_inimigo(self, x, y, player_x, player_y, criararquivo):
        '''b_list = []
        b_list.append(EnemyBullets(x, y, player_x, player_y, [self.visible_sprites], self.obstacles_sprites))
        if len(b_list) > 5:
            b_list.pop(-1)'''
        self.bullet = EnemyBullets(x, y, player_x, player_y, [self.visible_sprites], self.obstacles_sprites, criararquivo)


    def destroy_bau(self):
        self.bau.kill()
        Bau_aberto((self.bau_pos_x, self.bau_pos_y),[self.visible_sprites,self.bau_sprite])

    def destroy_key(self):
        if self.chave:
            self.chave.kill()
        self.chave = None

    def run(self):
        # Atualiza e desenha o jogo
        self.visible_sprites.custom_draw(self.player)  # draw(self.display_surface)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        # General setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # Criando o chão
        self.floor_surf = pygame.image.load('Assets/Enviroment/tile_fixed.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))

    def custom_draw(self, player):
        # Fazendo o recorte
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # Desenhando o chão
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf,floor_offset_pos)

        #for sprite in self.sprites():
        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            #self.display_surface.blit(pygame.transform.scale(sprite.image,(100,120)), offset_pos)
            self.display_surface.blit(sprite.image, offset_pos)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, "sprite_type") and sprite.sprite_type == "enemy"]
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
