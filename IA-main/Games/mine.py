import pygame
import random

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

class Mine:
    def __init__(self, nivel, gui):
        self.COLS = 0
        self.ROWS = 0
        self.gui = gui
        self.quit = False
        self.game_over = False
        self.large = 0
        if nivel == 0:
            self.COLS = 10
            self.ROWS = 10
            self.mines = 10
            self.large = CELL_SIZE * 10
        elif nivel == 1:
            self.COLS = 15
            self.ROWS = 15
            self.mines = 15
            self.large = CELL_SIZE * 15
        else:
            self.COLS = 20
            self.ROWS = 20
            self.mines = 20
            self.large = CELL_SIZE * 20
        self.grid = [[0 for _ in range(self.COLS)] for _ in range(self.ROWS)]

        self.init_game()

        
    def init_game(self):
        # Colocar minas aleatoriamente
        mine_positions = random.sample([(row, col) for row in range(self.ROWS) for col in range(self.COLS)], self.mines)
        for pos in mine_positions:
            self.grid[pos[0]][pos[1]] = -1
        
        

    def draw_grid(self):
        for row in range(self.ROWS):
            for col in range(self.COLS):
                cell_rect = self.gui.pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if self.grid[row][col] == -1: #minas
                    self.gui.pygame.draw.rect(self.gui.screen, BLACK, cell_rect)
                elif self.grid[row][col] == 0:  # Celda vacía
                    self.gui.pygame.draw.rect(self.gui.screen, GRAY, cell_rect)
                else:  # Número de minas vecinas
                    self.gui.pygame.draw.rect(self.gui.screen, GRAY, cell_rect)
                    text_surface = self.gui.font.render(str(self.grid[row][col]), True, BLACK)
                    text_rect = text_surface.get_rect(center=cell_rect.center)
                    self.gui.screen.blit(text_surface, text_rect)
        for row in range(self.ROWS + 1):
            self.gui.pygame.draw.line(self.gui.screen, BLACK, (0, row * CELL_SIZE), (self.large, row * CELL_SIZE), 2)
            self.gui.pygame.draw.line(self.gui.screen, BLACK, (row * CELL_SIZE, 0), (row * CELL_SIZE, self.large), 2)

    def run_mine_sweeper(self):
        self.draw_grid()
        while not self.game_over or self.quit:
            for event in self.gui.pygame.event.get():
                if event.type == self.gui.pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    break
                if event.type == self.gui.pygame.MOUSEBUTTONDOWN:
                    self.move()
            self.draw_grid()
            self.gui.pygame.display.update()

    def move(self):
        mouse = self.gui.pygame.mouse.get_pos()
        clicked_row = mouse[1] // CELL_SIZE
        clicked_col = mouse[0] // CELL_SIZE
        #print(clicked_row, " ", clicked_col)
        #if not self.game_over and self.grid[clicked_row][clicked_col] == 0:
            #self.grid[clicked_row][clicked_col] = -1