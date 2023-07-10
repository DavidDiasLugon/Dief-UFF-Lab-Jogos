from PPlay.window import *
from PPlay.mouse import *
from PPlay.sprite import *


def menu_inic():
    # Reconhecimento do mouse e teclado
    janela = Window(800, 640)
    mouse = Window.get_mouse()
    
    background = Sprite("Assets/Menu/background.png",1)

    # Criação dos sprites dos botões 
    botão_jogar = Sprite("Assets/Menu/jogar.png", 1)
    botão_dificuldade = Sprite("Assets/Menu/opções.png", 1)
    botão_sair = Sprite("Assets/Menu/sair.png", 1)

    # Posiciona os botões 
    botão_jogar.set_position((janela.width/2)-(botão_jogar.width/2) + 250,(janela.height/2 )-(botão_jogar.height/2 + 60))
    botão_dificuldade.set_position((janela.width/2)-(botão_dificuldade.width/2) + 250,(janela.height/2 )-(botão_dificuldade.height/2))
    botão_sair.set_position((janela.width/2)-(botão_sair.width/2) + 250,(janela.height/2 )-(botão_sair.height/2 - 60))
        
    while True:
        for event in pygame.event.get():
            pygame.mixer.init()
            pygame.mixer.music.load('Soundtrack/magical_theme.flac')
            pygame.mixer.music.play(-1) # Loop infinito da música
            pygame.mixer.music.set_volume(0.25) # Ajusta o volume da música 

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        
        if (mouse.is_over_object(botão_jogar) and mouse.is_button_pressed(1)):
            return True
        elif (mouse.is_over_object(botão_dificuldade) and mouse.is_button_pressed(1)):
            return False
        elif (mouse.is_over_object(botão_sair) and mouse.is_button_pressed(1)):
            pygame.quit()
            sys.exit()

        background.draw()
        botão_jogar.draw()
        botão_dificuldade.draw()
        botão_sair.draw()
        janela.update()
