import pygame
from model import Model
import sys
import os
# Constantes
FONT = 'couriernew'
WIDTH, HEIGHT = 800, 650
LINE_COLOR = (0, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)

# Tamaño de la cuadrícula
ROWS, COLS = 10, 10
CELL_SIZE = 40

X = 'X'
O = 'O'
E = None

class GuiView:
    def __init__(self):
        self.pygame = pygame
        self.pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.font = pygame.font.SysFont(FONT, 40, bold=True)
        self.pygame.display.set_caption("Abadeer Games")
        self.image1 = pygame.image.load(os.path.join('images', 'mine.png')).convert_alpha()
        self.image1 = pygame.transform.scale(self.image1, (100, 100))

    def draw_menu(self):
        self.screen.fill((255, 255, 215))
        mouse = self.pygame.mouse.get_pos()
        font = self.pygame.font.SysFont(FONT, 40, bold=True)
        introText = font.render("Gato:", True, BLACK)
        self.screen.blit(introText, (90, 50))
        if 250 + 200 >= mouse[0] >= 250 and 150 + 50 >= mouse[1] >= 150:
            font = self.pygame.font.SysFont(FONT, 40, bold=True)
            introText = font.render("vs Player", True, BLACK)
            self.screen.blit(introText, (235, 145))
            font = self.pygame.font.SysFont(FONT, 30)
            introText = font.render("vs Computer", True, BLACK)
            self.screen.blit(introText, (250, 195))
        elif 250 + 200 >= mouse[0] >= 250 and 190 + 50 >= mouse[1] >= 190:
            font = self.pygame.font.SysFont(FONT, 30)
            introText = font.render("vs Player", True, BLACK)
            self.screen.blit(introText, (250, 150))
            font = self.pygame.font.SysFont(FONT, 40, bold=True)
            introText = font.render("vs Computer", True, BLACK)
            self.screen.blit(introText, (210, 190))
        else:
            font = self.pygame.font.SysFont(FONT, 30)
            introText = font.render("vs Player", True, BLACK)
            self.screen.blit(introText, (250, 150))
            introText = font.render("vs Computer", True, BLACK)
            self.screen.blit(introText, (250, 190))

    def draw_state(self):
        self.screen.fill((BLACK))
        margin = 20
        spacing = 10

        cell_width = (WIDTH - margin * 2 - spacing * 2) // 3
        cell_height = (HEIGHT - margin * 2 - spacing * 2) // 2

        x, y = 100, 100
        mouse = self.pygame.mouse.get_pos()
        if 200 >= mouse[0] >= 100 and 200 >= mouse[1] >= 100:
            self.image1 = pygame.transform.scale(self.image1, (150, 150))
            self.screen.blit(self.image1, (x - 25, y - 25))
            #self.screen.blit(self.image1, (x + cell_width + spacing, y))
            #self.screen.blit(self.image1, (x + (cell_width + spacing) * 2, y))

            #self.screen.blit(self.image1, (x, y + cell_height + spacing))
            #self.screen.blit(self.image1, (x + cell_width + spacing, y + cell_height + spacing))
            #self.screen.blit(self.image1, (x + (cell_width + spacing) * 2, y + cell_height + spacing))

        else:
            self.image1 = pygame.transform.scale(self.image1, (100, 100))
            self.screen.blit(self.image1, (x, y))
            #self.screen.blit(self.image1, (x + cell_width + spacing, y))
            #self.screen.blit(self.image1, (x + (cell_width + spacing) * 2, y))

            #self.screen.blit(self.image1, (x, y + cell_height + spacing))
            #self.screen.blit(self.image1, (x + cell_width + spacing, y + cell_height + spacing))
            #self.screen.blit(self.image1, (x + (cell_width + spacing) * 2, y + cell_height + spacing))

