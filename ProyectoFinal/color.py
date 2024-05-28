import pygame
import random
import sys
import os
from logic import *
# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLOR_FONDO = (30, 144, 255)
FONT = 'couriernew'
# Definir colores
ROJO = (255, 0, 0)
AMARILLO = (255, 255, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Dimensiones de la pantalla
WIDTH, HEIGHT = 650, 650

# Dimensiones y posición de los cuadrados
CUADRADO_SIZE = 100
CUADRADO_MARGIN = 20
NUM_CUADRADOS = 6

# Clase para el botón de selección de colores
class BotonColor:
    def __init__(self, color, x, y):
        self.color = color
        self.radius = 20
        self.x = x
        self.y = y

    def dibujar(self, pantalla):
        pygame.draw.circle(pantalla, self.color, (self.x, self.y), self.radius)

class Color:
    def __init__(self, main):
        
        self.main = main
        self.main.pygame.display.set_caption("Mastermind")
        self.COLOR_BASE = ['R', 'Y', 'G', 'B']
        

    def init_game(self):
        self.botones_colores = [
            BotonColor(ROJO, 50, 50),  # Modificar las coordenadas para colocarlos en la parte superior
            BotonColor(AMARILLO, 100, 50),
            BotonColor(VERDE, 150, 50),
            BotonColor(AZUL, 200, 50)
        ]

        #self.codigo = [random.choice([ROJO, AMARILLO, VERDE, AZUL]) for _ in range(4)]
        self.COLOR_FINAL = ['Y', 'B', 'R', 'G']
        self.intentos = []
        self.intentos_realizados = 0
        self.INTENTOS_MAXIMOS = 10
        self.knowledge = And()
        self.color_ar = ["_" for _ in range(len(self.COLOR_BASE))]
        self.combinacion = []
        self.game_over = False

        self.symbols = {f"{color}{i}" for color in self.COLOR_BASE for i in range(len(self.COLOR_BASE))}


    def draw_menu(self):
        #self.main.screen.fill(COLOR_FONDO)
        self.main.screen.blit(self.main.background, (0, 0))

        font = self.main.pygame.font.Font(self.main.FONT, 100)
        introText = font.render("COLOR", True, 'white')
        self.main.screen.blit(introText, (100, 100))

        rect = self.main.pygame.Rect(20, 300, 300, 50)
        self.main.pygame.draw.rect(self.main.screen, 'white', rect, 2)

        mouse = self.main.pygame.mouse.get_pos()
        if 190 >= mouse[0] >= 90 and 90 >= mouse[1] >= 50:
            font = self.main.pygame.font.SysFont(self.main.FONT, 80, bold=True)
            introText = font.render("Back->", True, BLACK)
            self.main.screen.blit(introText, (85, 45))
            font = self.main.pygame.font.SysFont(self.main.FONT, 70, bold=True)
            introText = font.render("Play->", True, BLACK)
            self.main.screen.blit(introText, (90, 100))
        elif 190 >= mouse[0] >= 90 and 140 >= mouse[1] >= 100:
            font = self.main.pygame.font.SysFont(self.main.FONT, 70, bold=True)
            introText = font.render("Back->", True, BLACK)
            self.main.screen.blit(introText, (90, 50))
            font = self.main.pygame.font.SysFont(self.main.FONT, 80, bold=True)
            introText = font.render("Play->", True, BLACK)
            self.main.screen.blit(introText, (85, 95))
        else:
            font = self.main.pygame.font.SysFont(self.main.FONT, 70, bold=True)
            introText = font.render("Back->", True, BLACK)
            self.main.screen.blit(introText, (90, 50))
            introText = font.render("Play->", True, BLACK)
            self.main.screen.blit(introText, (90, 100))

    def run_menu(self):
        running = True
        while running:
            for event in self.main.pygame.event.get():
                if event.type == self.main.pygame.QUIT:
                    self.main.pygame.quit()
                    running = False
                    sys.exit()
                if event.type == self.main.pygame.MOUSEBUTTONDOWN:
                    mouse = self.main.pygame.mouse.get_pos()
                    if 190 >= mouse[0] >= 90 and 90 >= mouse[1] >= 50:
                        self.main.__init__()
                        self.main.run_main()
                    elif 190 >= mouse[0] >= 90 and 140 >= mouse[1] >= 100:
                        #running = False
                        self.init_game()
                        self.run_game_easy()

            self.main.screen.fill(COLOR_FONDO)
            self.draw_menu()
            self.main.pygame.display.flip()

    def draw_colores(self):
        mouse = self.main.pygame.mouse.get_pos()
        if 650 >= mouse[0] >= 550 and 40 >= mouse[1] >= 10:
            font = self.main.pygame.font.SysFont(FONT, 35, bold=True)
            introText = font.render("IA", True, BLACK)
            self.main.screen.blit(introText, (525, 5))
            font = self.main.pygame.font.SysFont(FONT, 30, bold=True)
            introText = font.render("Menu->", True, BLACK)
            self.main.screen.blit(introText, (530, 40))
            introText = font.render("Exit->", True, BLACK)
            self.main.screen.blit(introText, (530, 70))
        elif 650 >= mouse[0] >= 550 and 70 >= mouse[1] >= 40:
            font = self.main.pygame.font.SysFont(FONT, 30, bold=True)
            introText = font.render("IA", True, BLACK)
            self.main.screen.blit(introText, (530, 10))
            font = self.main.pygame.font.SysFont(FONT, 35, bold=True)
            introText = font.render("Menu->", True, BLACK)
            self.main.screen.blit(introText, (525, 35))
            font = self.main.pygame.font.SysFont(FONT, 30, bold=True)
            introText = font.render("Exit->", True, BLACK)
            self.main.screen.blit(introText, (530, 70))
        elif 650 >= mouse[0] >= 550 and 90 >= mouse[1] >= 70:
            font = self.main.pygame.font.SysFont(FONT, 30, bold=True)
            introText = font.render("IA", True, BLACK)
            self.main.screen.blit(introText, (530, 10))
            introText = font.render("Menu->", True, BLACK)
            self.main.screen.blit(introText, (530, 40))
            font = self.main.pygame.font.SysFont(FONT, 35, bold=True)
            introText = font.render("Exit->", True, BLACK)
            self.main.screen.blit(introText, (525, 65))
        else:
            font = self.main.pygame.font.SysFont(FONT, 30, bold=True)
            introText = font.render("IA", True, BLACK)
            self.main.screen.blit(introText, (530, 10))
            introText = font.render("Menu->", True, BLACK)
            self.main.screen.blit(introText, (530, 40))
            introText = font.render("Exit->", True, BLACK)
            self.main.screen.blit(introText, (530, 70))

        for boton in self.botones_colores:
            boton.dibujar(self.main.screen)

        for idx, combinacion in enumerate(self.intentos):
            for i, color in enumerate(combinacion):
                if color == 'Y':
                    self.main.pygame.draw.circle(self.main.screen, AMARILLO, (50 + i * 50, (100 + idx * 50)), 20)
                if color == 'R':
                    self.main.pygame.draw.circle(self.main.screen, ROJO, (50 + i * 50, (100 + idx * 50)), 20)
                if color == 'G':
                    self.main.pygame.draw.circle(self.main.screen, VERDE, (50 + i * 50, (100 + idx * 50)), 20)
                if color == 'B':
                    self.main.pygame.draw.circle(self.main.screen, AZUL, (50 + i * 50, (100 + idx * 50)), 20)

            font = self.main.pygame.font.Font(None, 24)  # Fuente para el número
            texto = font.render(str(self.verificar_intentos(combinacion)), True, NEGRO)
            texto_rect = texto.get_rect(midleft=(250, (100 + idx * 50)))
            self.main.screen.blit(texto, texto_rect)

        for i, color in enumerate(self.COLOR_FINAL):
            if color == "Y":
                self.main.pygame.draw.circle(self.main.screen, AMARILLO, (300 + i * 50, 50), 20)
            if color == "R":
                self.main.pygame.draw.circle(self.main.screen, ROJO, (300 + i * 50, 50), 20)
            if color == "G":
                self.main.pygame.draw.circle(self.main.screen, VERDE, (300 + i * 50, 50), 20)
            if color == "B":
                self.main.pygame.draw.circle(self.main.screen, AZUL, (300 + i * 50, 50), 20)

    def verificar_intentos(self, combinacion):
        pociciones = 0

        for i, color in enumerate(combinacion):
            if color == self.COLOR_FINAL[i]:
                pociciones += 1

        return pociciones

    def update_knowledge(self, combinacion):
        ten = set()
        if self.verificar_intentos(combinacion) > 0:
            
            for i, color in enumerate(combinacion):
                if color == self.COLOR_FINAL[i]:
                    self.knowledge.add(Symbol(f"{color}{i}"))
                else:
                    self.knowledge.add(Not(Symbol(f"{color}{i}")))
                    ten.add(f"{color}{i}")

        else:
            for i, color in enumerate(combinacion):
                if color != self.COLOR_FINAL[i]:
                    self.knowledge.add(Not(Symbol(f"{color}{i}")))
                    ten.add(f"{color}{i}")
        
        updated_symbols = self.symbols - ten
        return updated_symbols

    def run_game_easy(self):
        running = True
        while running:
            for event in self.main.pygame.event.get():
                if event.type == self.main.pygame.QUIT:
                    self.main.pygame.quit()
                    running = False
                    sys.exit()
                if event.type == self.main.pygame.MOUSEBUTTONDOWN:
                    mouse = self.main.pygame.mouse.get_pos()
                    if 650 >= mouse[0] >= 550 and 40 >= mouse[1] >= 10 and not self.game_over:
                        self.move()
                    elif 650 >= mouse[0] >= 550 and 70 >= mouse[1] >= 40:
                        running = False
                        self.init_game()
                        self.run_menu()
                    elif 650 >= mouse[0] >= 550 and 90 >= mouse[1] >= 70:
                        running = False
                        self.main.__init__()
                        self.main.run_main()

            self.main.screen.fill(COLOR_FONDO)
            self.draw_colores()
            self.main.pygame.display.flip()

    def move(self):
        #if self.intentos_realizados< self.INTENTOS_MAXIMOS and not self.game_over:
        if not self.game_over:
            #random2 = random_color(color_ar)
            random2 = self.random_color1()
            self.intentos.append(random2)
            self.symbols = self.update_knowledge(random2)
            if self.color_ar != self.COLOR_FINAL:
                print(self.intentos_realizados,    "         ==============")
                for symbol in self.symbols:
                    if model_check(self.knowledge, Symbol(symbol)):
                        if self.color_ar[int(symbol[1])] == '_':
                            self.color_ar[int(symbol[1])] = symbol[0]
                        print(f"True: {symbol}")
                    else:
                        print(f"False: {symbol}")
                self.intentos_realizados += 1
            if self.color_ar == self.COLOR_FINAL:
                self.game_over = True
                self.intentos.append(self.color_ar)
    
            print(self.color_ar)

    def random_color1(self):
        return random.sample(self.COLOR_BASE, k=4)
