import pygame
import random
import time
import sys

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


def run_on_all_adjacent_blocks(row, col, dimension, func):
    if row != 0 and col != 0:
        func(row - 1, col - 1)
    if row != 0:
        func(row - 1, col)
    if col != 0:
        func(row, col - 1)
    if row != dimension - 1 and col != dimension - 1:
        func(row + 1, col + 1)
    if row != dimension - 1:
        func(row + 1, col)
    if col != dimension - 1:
        func(row, col + 1)
    if row != 0 and col != dimension - 1:
        func(row - 1, col + 1)
    if row != dimension - 1 and col != 0:
        func(row + 1, col - 1)

def for_each_cell(matrix, func):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            func(matrix[i][j], i, j)


class Cell:
    def __init__(self):
        self.is_bomb = False
        self.is_flagged = False
        self.is_revealed = False
        self.number = 0

    def reveal(self):
        if not self.is_bomb:
            self.is_flagged = False
        self.is_revealed = True

class Minesweeper:
    def __init__(self, dimension):
        self.dimension = dimension
        self.bombs_count = dimension * dimension // 7
        self.num_non_bomb_cells = dimension * dimension - self.bombs_count
        self.revealed_non_bomb_cells = 0
        self.won = False
        self.lost = False
        self.initialize_board()

    def initialize_board(self):
        self.board = [[Cell() for _ in range(self.dimension)] for _ in range(self.dimension)]
        bomb_locations = self.generate_bombs()
        for row, col in bomb_locations:
            cell = self.board[row][col]
            cell.is_bomb = True
            run_on_all_adjacent_blocks(row, col, self.dimension, lambda r, c: self.increment_cell_number(r, c))

    def generate_bombs(self):
        bomb_locations = set()
        while len(bomb_locations) < self.bombs_count:
            bomb = (random.randint(0, self.dimension - 1), random.randint(0, self.dimension - 1))
            bomb_locations.add(bomb)
        return bomb_locations

    def increment_cell_number(self, row, col):
        cell = self.board[row][col]
        if not cell.is_bomb:
            cell.number += 1

    def on_cell_clicked(self, row, col):
        if self.won or self.lost:
            return
        cell = self.board[row][col]
        if cell.is_bomb:
            self.handle_loss()
        else:
            self.reveal_non_bomb_cells_and_adjacent(row, col)
            self.check_win()

    def reveal_non_bomb_cells_and_adjacent(self, row, col):
        cell = self.board[row][col]
        if cell.is_revealed or cell.is_bomb:
            return
        cell.reveal()
        self.revealed_non_bomb_cells += 1
        self.check_win()
        if cell.number == 0:
            run_on_all_adjacent_blocks(row, col, self.dimension, lambda r, c: self.reveal_non_bomb_cells_and_adjacent(r, c))

    def handle_loss(self):
        self.lost = True
        for_each_cell(self.board, lambda cell, row, col: cell.reveal() if cell.is_bomb else None)

    def check_win(self):
        if self.revealed_non_bomb_cells == self.num_non_bomb_cells:
            self.won = True

    def on_cell_right_clicked(self, row, col):
        if self.won or self.lost:
            return
        cell = self.board[row][col]
        if not cell.is_revealed:
            cell.is_flagged = not cell.is_flagged
            self.check_win()

class Solver:
    def __init__(self, minesweeper):
        self.minesweeper = minesweeper

    def get_next_move(self):
        cell_to_flag = self.find_cell_to_flag()
        if cell_to_flag:
            return [False, cell_to_flag[0], cell_to_flag[1]]

        cell_to_click = self.find_cell_to_click()
        if cell_to_click:
            return [True, cell_to_click[0], cell_to_click[1]]

        dimen = self.minesweeper.dimension
        row = random.randint(0, dimen - 1)
        col = random.randint(0, dimen - 1)
        return [True, row, col]

    def find_cell_to_flag(self):
        dimen = self.minesweeper.dimension

        for row in range(dimen):
            for col in range(dimen):
                cell = self.minesweeper.board[row][col]
                if cell.is_revealed or cell.is_flagged:
                    continue  # Skip revealed or flagged cells

                num_unrevealed_around = 0
                num_flagged_around = 0

                # Check neighbors
                for i in range(row - 1, row + 2):
                    for j in range(col - 1, col + 2):
                        if 0 <= i < dimen and 0 <= j < dimen:  # Check valid indices
                            neighbor = self.minesweeper.board[i][j]
                            if neighbor.is_flagged:
                                num_flagged_around += 1

                if cell.number == num_flagged_around:
                    return [row, col]

        return None

    def find_cell_to_click(self):
        dimen = self.minesweeper.dimension

        for row in range(dimen):
            for col in range(dimen):
                cell = self.minesweeper.board[row][col]
                if cell.is_revealed or cell.is_flagged:
                    continue  # Skip revealed or flagged cells

                num_flagged = 0
                num_unrevealed = 0

                # Check neighbors
                for i in range(row - 1, row + 2):
                    for j in range(col - 1, col + 2):
                        if 0 <= i < dimen and 0 <= j < dimen:  # Check valid indices
                            neighbor = self.minesweeper.board[i][j]
                            if neighbor.is_flagged:
                                num_flagged += 1
                            elif not neighbor.is_revealed:
                                num_unrevealed += 1

                if num_flagged == cell.number and num_unrevealed > 0:
                    return [row, col]

        return None


class App:
    def __init__(self, main):
        self.timer = None
        self.solver_timer = None
        self.running = True
        self.main = main

    def play_game(self, dimen):
        self.reset_state()
        self.minesweeper = Minesweeper(dimen)
        self.solver = Solver(self.minesweeper)
        self.time_elapsed = 0
        self.timer = time.time()
        #self.screen = pygame.display.set_mode((dimen * 30, 650))
        pygame.display.set_caption("Minesweeper")
        self.clock = pygame.time.Clock()
        while self.running:
            for event in self.main.pygame.event.get():
                if event.type == self.main.pygame.QUIT:
                    self.main.pygame.quit()
                    running = False
                    sys.exit()
                self.handle_events()
                self.draw_board()
                self.draw_solver_button()
                self.draw_colores()
                if event.type == self.main.pygame.MOUSEBUTTONDOWN:
                        mouse = self.main.pygame.mouse.get_pos()
                        if 650 >= mouse[0] >= 550 and 40 >= mouse[1] >= 10 and not self.game_over:
                            self.auto_solve_one_move()
                        elif 650 >= mouse[0] >= 550 and 70 >= mouse[1] >= 40:
                            running = False
                            #self.main.init_game()
                            self.main.run_main()
                        elif 650 >= mouse[0] >= 550 and 90 >= mouse[1] >= 70:
                            running = False
                            self.main.__init__()
                            self.main.run_main()
                self.main.pygame.display.flip()
                self.clock.tick(30)

                if self.minesweeper.won:
                    self.on_game_won()
                    self.running = False

    def reset_state(self):
        self.timer = None
        self.solver_timer = None
        self.running = True

    def handle_events(self):
        for event in self.main.pygame.event.get():
            if event.type == self.main.pygame.QUIT:
                self.main.pygame.quit()
                sys.exit()
            elif event.type == self.main.pygame.MOUSEBUTTONDOWN:
                pos = self.main.pygame.mouse.get_pos()
                row, col = pos[1] // 30, pos[0] // 30
                if 0 <= pos[1] < 600:  # Dentro del área del tablero
                    if event.button == 1:  # Clic izquierdo
                        self.handle_click(row, col)
                    elif event.button == 3:  # Clic derecho
                        self.handle_right_click(row, col)
                elif 610 <= pos[1] <= 650 and 10 <= pos[0] <= 100:  # Dentro del área del botón
                    if event.button == 1:  # Clic izquierdo en el botón
                        self.auto_solve_game()

    def handle_click(self, row, col):
        if not (0 <= row < self.minesweeper.dimension) or not (0 <= col < self.minesweeper.dimension):
            print("Invalid input! Try again.")
            return
        self.minesweeper.on_cell_clicked(row, col)

    def handle_right_click(self, row, col):
        if not (0 <= row < self.minesweeper.dimension) or not (0 <= col < self.minesweeper.dimension):
            print("Invalid input! Try again.")
            return
        self.minesweeper.on_cell_right_clicked(row, col)

    def auto_solve_game(self):
        self.solver_timer = time.time()
        while not (self.minesweeper.won or self.minesweeper.lost):
            if time.time() - self.solver_timer >= 0.5:  # Retraso de 1 segundo (1000ms)
                self.solver_timer = time.time()
                self.auto_solve_one_move()
                self.draw_board()
                
                self.main.pygame.display.flip()  # Actualizar pantalla después de cada movimiento
            self.handle_events()

    def auto_solve_one_move(self):
        move = self.solver.get_next_move()
        if move[0]:
            self.minesweeper.on_cell_clicked(move[1], move[2])
        else:
            self.minesweeper.on_cell_right_clicked(move[1], move[2])
        self.draw_board()

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

    def draw_board(self):
        self.main.screen.blit(self.main.background, (0, 0))
        for row in range(self.minesweeper.dimension):
            for col in range(self.minesweeper.dimension):
                cell = self.minesweeper.board[row][col]
                rect = self.main.pygame.Rect(col * 30, row * 30, 30, 30)
                if cell.is_revealed:
                    if cell.is_bomb:
                        self.main.pygame.draw.rect(self.main.screen, (255, 0, 0), rect)
                    else:
                        self.main.pygame.draw.rect(self.main.screen, (200, 200, 200), rect)
                        if cell.number > 0:
                            font = self.main.pygame.font.Font(None, 24)
                            text = font.render(str(cell.number), True, (0, 0, 0))
                            self.main.screen.blit(text, (col * 30 + 10, row * 30 + 5))
                else:
                    self.main.pygame.draw.rect(self.main.screen, (100, 100, 100), rect)
                    if cell.is_flagged:
                        self.main.pygame.draw.rect(self.main.screen, (0, 0, 255), rect)
                self.main.pygame.draw.rect(self.main.screen, (0, 0, 0), rect, 1)
    
    def draw_solver_button(self):
        font = self.main.pygame.font.Font(None, 36)
        button_rect = self.main.pygame.Rect(10, 610, 90, 40)
        self.main.pygame.draw.rect(self.main.screen, (0, 0, 255), button_rect)
        text = font.render("Solver", True, (255, 255, 255))
        self.main.screen.blit(text, (20, 615))
