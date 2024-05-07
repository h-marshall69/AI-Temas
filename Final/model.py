import pygame
import sys

from mine import Mine
from color import Color
from gato import Gato
from house import House

# Colores
BLANCO = (255, 255, 255)
BLACK = (0, 0, 0)
COLOR_FONDO = (30, 144, 255)
FONT = 'couriernew'

# Dimensiones de la pantalla
WIDTH, HEIGHT = 650, 650

# Dimensiones y posición de los cuadrados
CUADRADO_SIZE = 100
CUADRADO_MARGIN = 20
NUM_CUADRADOS = 6

class Ventana:
    def __init__(self):
        self.pygame = pygame
        self.pygame.init()
        self.screen = self.pygame.display.set_mode((WIDTH, HEIGHT))
        self.font = self.pygame.font.SysFont(FONT, 40, bold=True)

    def dibujar_cuadrados(self):
        self.pygame.draw.rect(self.screen, BLACK, (100, 100, 100, 100))
        self.pygame.draw.rect(self.screen, BLACK, (220, 100, 100, 100))
        self.pygame.draw.rect(self.screen, BLACK, (340, 100, 100, 100))
        self.pygame.draw.rect(self.screen, BLACK, (100, 220, 100, 100))

    def run_model(self):
        running = True
        while running:
            for event in self.pygame.event.get():
                if event.type == pygame.QUIT:
                    self.pygame.quit()
                    running = False
                    sys.exit()
                if event.type == self.pygame.MOUSEBUTTONDOWN:
                    mouse = self.pygame.mouse.get_pos()
                    if 200 >= mouse[0] >= 100 and 200 >= mouse[1] >= 100:
                        running = False
                        self.mine = Mine(self)
                        self.mine.run_game()
                    elif 320 >= mouse[0] >= 220 and 200 >= mouse[1] >= 100:
                        running = False
                        self.mine = Color(self)
                        self.mine.run_game()
                    elif 440 >= mouse[0] >= 340 and 200 >= mouse[1] >= 100:
                        running = False
                        self.mine = House(self)
                        self.mine.run_game()
                    elif 200 >= mouse[0] >= 100 and 320 >= mouse[1] >= 220:
                        running = False
                        self.mine = Gato(self)
                        self.mine.run_game()

            self.screen.fill(COLOR_FONDO)
            self.dibujar_cuadrados()
            self.pygame.display.flip()

if __name__ == "__main__":
    ventana = Ventana()
    ventana.run_model()
