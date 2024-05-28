import pygame
import sys
from Assets.button import Button
import logicape

pygame.init()

PANTALLA = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/images/Background.png")
FG = pygame.image.load("assets/images/FON.jpg")


def get_font(size):
    return pygame.font.Font("assets/images/font.ttf", size)

def play():
    textbox1_text = "" 
    textbox1_active = False
 
    textbox2_text = "" 
    textbox2_active = True 

    textbox3_text = "" 
    textbox3_active = False 

    PERSONAJES = ""
    SOLUCIONES = ""

    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        PANTALLA.blit(FG, (0, 0))

        '''
        PLAY_TEXT = get_font(25)render("Bienvenido", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(350, 60))
        PANTALLA.blit(PLAY_TEXT, PLAY_RECT)
        '''

        # Labels
        LABEL1_TEXT = get_font(20).render("Casas: \n Grifindor \n Ravenclaw", True, "White")
        LABEL1_RECT = LABEL1_TEXT.get_rect(topleft=(10, 70))
        PANTALLA.blit(LABEL1_TEXT, LABEL1_RECT)

        
        LABEL2_TEXT = get_font(20).render("PERSONAJES: " + PERSONAJES, True ,"White")
        LABEL2_RECT = LABEL2_TEXT.get_rect(topleft=(30, 125))
        PANTALLA.blit(LABEL2_TEXT, LABEL2_RECT)

        LABEL3_TEXT = get_font(10).render("j" + SOLUCIONES, True ,"White")
        LABEL3_RECT = LABEL3_TEXT.get_rect(topleft=(10,550))
        PANTALLA.blit(LABEL3_TEXT, LABEL3_RECT)



        # Text boxes
        TEXTBOX1_RECT = pygame.Rect(20, 300, 300, 50)
        pygame.draw.rect(PANTALLA, "White", TEXTBOX1_RECT, 2)
        
        TEXTBOX2_RECT = pygame.Rect(340, 300, 300, 50)
        pygame.draw.rect(PANTALLA, "White", TEXTBOX2_RECT, 2)

        TEXTBOX3_RECT = pygame.Rect(150, 420, 300, 50)
        pygame.draw.rect(PANTALLA, "White", TEXTBOX3_RECT, 2)


        textbox1_surface = get_font(20).render(textbox1_text, True, "White")
        PANTALLA.blit(textbox1_surface, (TEXTBOX1_RECT.x + 5, TEXTBOX1_RECT.y + 5))

        textbox2_surface = get_font(20).render(textbox2_text, True, "White")
        PANTALLA.blit(textbox2_surface, (TEXTBOX2_RECT.x + 5, TEXTBOX2_RECT.y + 5))


        textbox3_surface = get_font(20).render(textbox3_text, True, "White")
        PANTALLA.blit(textbox3_surface, (TEXTBOX3_RECT.x + 5, TEXTBOX3_RECT.y + 5))

        # Buttons
        PLAY_BACK = Button(image=None, pos=(1200, 680),text_input="BACK", font=get_font(38), base_color="White", hovering_color="Red")
        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(PANTALLA)

        or1 = Button(image=None, pos=(170, 270),
                         text_input="or 1", font=get_font(30), base_color="White", hovering_color="Blue")
        or1.changeColor(PLAY_MOUSE_POS)
        or1.update(PANTALLA)

        or2 = Button(image=None, pos=(410, 270),
                         text_input="or 2", font=get_font(30), base_color="White", hovering_color="Blue")
        or2.changeColor(PLAY_MOUSE_POS)
        or2.update(PANTALLA)

        or3 = Button(image=None, pos=(275, 400),
                         text_input="not", font=get_font(30), base_color="White", hovering_color="Blue")
        or3.changeColor(PLAY_MOUSE_POS)
        or3.update(PANTALLA)
        
        iniciar = Button(image=None, pos=(600, 20),
                         text_input="iniciar", font=get_font(24), base_color="White", hovering_color="Green")
        iniciar.changeColor(PLAY_MOUSE_POS)
        iniciar.update(PANTALLA)

        piensaa = Button(image=None, pos=(1100, 100),
                     text_input="PIENSA", font=get_font(34), base_color="White", hovering_color="Green")
        piensaa.changeColor(PLAY_MOUSE_POS)
        piensaa.update(PANTALLA)
        

        enviar = Button(image=None, pos=(275, 500),
                     text_input="enviar", font=get_font(24), base_color="White", hovering_color="Green")
        enviar.changeColor(PLAY_MOUSE_POS)
        enviar.update(PANTALLA)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

                if or1.checkForInput(PLAY_MOUSE_POS):
                    textbox2_active = False
                    textbox3_active = False
                    textbox1_active = True

                if or2.checkForInput(PLAY_MOUSE_POS):
                    textbox1_active = False
                    textbox3_active = False
                    textbox2_active = True

                if or3.checkForInput(PLAY_MOUSE_POS):
                    textbox1_active = False
                    textbox2_active = False
                    textbox3_active = True

                if iniciar.checkForInput(PLAY_MOUSE_POS):
                    PERSONAJES = logicape.escribir_personas()

                if piensaa.checkForInput(PLAY_MOUSE_POS):
                    SOLUCIONES = logicape.cheroka()

                if enviar.checkForInput(PLAY_MOUSE_POS):
                    if textbox3_text != "":
                        logicape.negar(textbox3_text)
                        textbox3_text = ""


            if textbox1_active:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        textbox1_text = textbox1_text[:-1]
                    else:
                        textbox1_text += event.unicode

            if textbox2_active:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        textbox2_text = textbox2_text[:-1]
                    else:
                        textbox2_text += event.unicode

            if textbox3_active:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        textbox3_text = textbox3_text[:-1]
                    else:
                        textbox3_text += event.unicode

        pygame.display.update()

def main_menu():
    while True:
        PANTALLA.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", False, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/images/Play Rect.png"), pos=(640, 250),
                             text_input="PLAY", font=get_font(80), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/images/Options Rect.png"), pos=(640, 400),
                                text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/images/Quit Rect.png"), pos=(640, 550),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        PANTALLA.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(PANTALLA)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def run_game_casas():
    
    main_menu()
