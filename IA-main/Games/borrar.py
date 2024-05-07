import pygame
import random
import sys
import os

# Inicializar Pygame
pygame.init()

# Definir colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)

# Configurar la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Buscaminas")

# Tamaño de la cuadrícula

CELL_SIZE = 40

# Constantes
FONT = 'couriernew'

class Mine:
    def __init__(self):
        self.pygame = pygame
        self.pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.font = pygame.font.SysFont(FONT, 40, bold=True)
        self.pygame.display.set_caption("Abadeer Games")
        self.image1 = pygame.image.load(os.path.join('images', 'mine.png')).convert_alpha()
        self.image1 = pygame.transform.scale(self.image1, (100, 100))

        self.ROWS = 10
        self.COLS = 10
        self.mines = 15
        self.large = CELL_SIZE * 10
        self.grid = [[0 for _ in range(self.COLS)] for _ in range(self.ROWS)]
        self.game_over = False

        self.init_game()

    def init_game(self):
        

        #Coloca las minas
        mine_positions = random.sample([(row, col) for row in range(self.ROWS) for col in range(self.COLS)], self.mines)
        for pos in mine_positions:
            self.grid[pos[0]][pos[1]] = -1

        # Cuenta la cantidad de minas vecinas
        for row in range(self.ROWS):
            for col in range(self.COLS):
                if self.grid[row][col] == -1:  # Si es una mina, no es necesario contar vecinos
                    continue
                contador = 0
                for dr in [-1, 0, 1]:  # Desplazamiento vertical
                    for dc in [-1, 0, 1]:  # Desplazamiento horizontal
                        if dr == 0 and dc == 0:  # Ignorar la propia celda
                            continue
                        r, c = row + dr, col + dc
                        if 0 <= r < self.ROWS and 0 <= c < self.COLS and self.grid[r][c] == -1:
                            contador += 1
                self.grid[row][col] = contador
                    
    def draw_grid(self):
        for row in range(self.ROWS):
            for col in range(self.COLS):
                cell_rect = self.pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if self.grid[row][col] == 10: #minas
                    self.pygame.draw.rect(self.screen, BLACK, cell_rect)
                elif self.grid[row][col] < 10:  # Celda vacía
                    self.pygame.draw.rect(self.screen, GRAY, cell_rect)
        for row in range(self.ROWS + 1):
            self.pygame.draw.line(self.screen, BLACK, (0, row * CELL_SIZE), (self.large, row * CELL_SIZE), 2)
            self.pygame.draw.line(self.screen, BLACK, (row * CELL_SIZE, 0), (row * CELL_SIZE, self.large), 2)

    def reveal_mines(self):
        for row in range(self.ROWS):
            for col in range(self.COLS):
                if grid[row][col] == -1:
                    self.pygame.draw.rect(screen, RED, (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def reveal_empty_cell(self, row, col):
        

    def run_game(self):
        running = True
        while not self.game_over or running:
            for event in self.pygame.event.get():
                if event.type == self.pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                    break

                if event.type == self.pygame.MOUSEBUTTONDOWN:
                    mouse = self.pygame.mouse.get_pos()
                    if 500 >= mouse[0] >= 0 and 500 >= mouse[1] >= 0:
                        click_row = mouse[1] // CELL_SIZE
                        click_col = mouse[0] // CELL_SIZE
                        if self.grid[click_row][click_col] == -1:
                            self.reveal_mines()
                            self.game_over = True
                            running = False
                        elif self.grid[click_row][click_col] == 0:
                            self.reveal_empty_cell(click_row, click_col)
                        else:
                            self.grid[click_row][click_col] += 10
                        #running = False
                        self.screen.fill((255, 255, 255))
                        #self.run_mine_sweeper()
                        #self.mine = Mine(0, self.gui)
                        #self.mine.run_mine_sweeper()

            #self.gui.draw_menu()
            #self.draw_state()
            self.draw_grid()
            self.pygame.display.update()

if __name__ == "__main__":
    mine = Mine()
    mine.run_game()