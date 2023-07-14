import pygame, sys
from config import *
from level import Level
from dief import *
from cavaleiro import *
from PPlay import *
from random import randint
from menu import menu_inic
import os
 

class Game:
    def __init__(self):
        # setup geral
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Dief")
        self.clock = pygame.time.Clock()
        self.menu = False
        self.quit_game = False
        self.qual_mapa = 0
        self.level = Level(self.qual_mapa)

    def run(self):
        return_to_menu = False
        cont = 0
        while True:
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        dir = 'txts/'
                        for i in os.listdir(dir):
                            os.remove(os.path.join(dir, i))
                        pygame.quit()
                        sys.exit()
                color = (0, 0, 0)
                self.screen.fill(color)
                if self.level == 0:
                    self.level = Level(self.qual_mapa)
                self.level.run()
                pygame.display.update()
                self.clock.tick(FPS)

                if self.level.cavaleiro.has_collided_player():
                    return_to_menu = True
                    self.level = 0
                    dir = 'txts/'
                    for i in os.listdir(dir):
                        os.remove(os.path.join(dir, i))
                    break

                if self.level.player.has_opened_chest():
                    '''if self.qual_mapa == 2:
                        self.qual_mapa = 0
                    else:
                        self.qual_mapa += 1'''
                    cont += 1
                    if cont > 65:
                        return_to_menu = True
                        if self.qual_mapa == 2:
                            self.qual_mapa = 0
                        else:
                            self.qual_mapa += 1
                        self.level = 0
                        dir = 'txts/'
                        for i in os.listdir(dir):
                            os.remove(os.path.join(dir, i))
                        break
            
            if return_to_menu:
                menu_result = menu_inic()
                if not menu_result:
                    pygame.quit()
                    sys.exit()


if __name__ == "__main__":
    menu_result = menu_inic()
    if menu_result:
        game = Game()
        game.run()