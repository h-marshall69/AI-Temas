import pygame
import sys

from mine import Mine
from color import Color
from gato import Gato
from house import House
import casas
FONT = 'couriernew'
# Dimensiones y posición de los cuadrados
CUADRADO_SIZE = 100
CUADRADO_MARGIN = 20
NUM_CUADRADOS = 6

class Ventana:
    def __init__(self):
        self.pygame = pygame
        self.pygame.init()
        
        #size
        self.WIDTH = 700
        self.HEIGHT = 1100

        #color
        self.BLACK = (0, 0, 0)
        self.WHITE  = (255, 255, 255)
        self.GRAY = (200, 200, 200)
        self.RED = (255, 0, 0)
        
        #view
        self.screen = self.pygame.display.set_mode((self.HEIGHT, self.WIDTH))
        self.background = self.pygame.image.load("assets/images/Background.png")
        #pygame.font.Font("assets/images/font.ttf", size)
        self.font = self.pygame.font.Font("assets/images/font.ttf", 40)
        #self.font = self.pygame.font.SysFont(FONT, 40, bold=True)
        self.pygame.display.set_caption("Abadeer Games")

    def dibujar_cuadrados(self):
        self.pygame.draw.rect(self.screen, self.BLACK, (100, 100, 100, 100))
        self.pygame.draw.rect(self.screen, self.BLACK, (220, 100, 100, 100))
        self.pygame.draw.rect(self.screen, self.BLACK, (340, 100, 100, 100))
        self.pygame.draw.rect(self.screen, self.BLACK, (100, 220, 100, 100))

    def run_main(self):
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
                        #running = False
                        self.color = Color(self)
                        self.color.run_menu()
                        
                    elif 320 >= mouse[0] >= 220 and 200 >= mouse[1] >= 100:
                        #running = False
                        #self.mine = Mine(self)
                        #self.mine.run_game()
                        self.screen = self.pygame.display.set_mode((1280, 720))
                        casas.run_game_casas()
                    elif 440 >= mouse[0] >= 340 and 200 >= mouse[1] >= 100:
                        #running = False
                        self.house = House(self)
                        self.house.run_game()
                    elif 200 >= mouse[0] >= 100 and 320 >= mouse[1] >= 220:
                        #running = False
                        self.gato = Gato(self)
                        self.gato.run_game()

            #self.screen.fill(self.GRAY)
            self.screen.blit(self.background, (0, 0))
            self.dibujar_cuadrados()
            self.pygame.display.flip()

if __name__ == "__main__":
    ventana = Ventana()
    ventana.run_main()