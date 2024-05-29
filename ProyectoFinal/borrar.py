import pygame
import random
import time
import sys

# Funciones utilitarias
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

def to_mmss(sec_num):
    hours = sec_num // 3600
    minutes = (sec_num - (hours * 3600)) // 60
    seconds = sec_num - (hours * 3600) - (minutes * 60)

    if minutes < 10:
        minutes = "0" + str(minutes)
    if seconds < 10:
        seconds = "0" + str(seconds)
    return f"{minutes}:{seconds}"

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
        self.num_bombs = dimension * dimension // 7
        self.won = False
        self.lost = False
        self.initialize_board()

    def initialize_board(self):
        self.board = [[Cell() for _ in range(self.dimension)] for _ in range(self.dimension)]
        bombs = self.generate_bombs()
        for bomb in bombs:
            self.board[bomb[0]][bomb[1]].is_bomb = True
            run_on_all_adjacent_blocks(bomb[0], bomb[1], self.dimension, lambda row, col: self.increment_cell_number(row, col))
    

    def generate_bombs(self):
        bomb_locations = []
        while len(bomb_locations) < self.num_bombs:
            bomb = [random.randint(0, self.dimension - 1), random.randint(0, self.dimension - 1)]
            if bomb not in bomb_locations:
                bomb_locations.append(bomb)
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
        if cell.number == 0:
            run_on_all_adjacent_blocks(row, col, self.dimension, lambda new_row, new_col: self.reveal_non_bomb_cells_and_adjacent(new_row, new_col))

    def handle_loss(self):
        self.lost = True
        for_each_cell(self.board, lambda cell, row, col: cell.reveal() if cell.is_bomb else None)

    def check_win(self):
        self.won = all(cell.is_revealed or (cell.is_flagged and cell.is_bomb) for row in self.board for cell in row)

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
        row_to_flag = None
        col_to_flag = None

        def check_cell(cell, row, col):
            nonlocal row_to_flag, col_to_flag
            if cell.is_revealed or cell.is_flagged or row_to_flag is not None:
                return

            def check_neighbor(neighbor_row, neighbor_col):
                neighbor = self.minesweeper.board[neighbor_row][neighbor_col]
                if neighbor.is_revealed and neighbor.number > 0:
                    num_unrevealed_around_neighbor = 0
                    num_flagged_around_neighbor = 0

                    def count_unrevealed_and_flagged(i, j):
                        neighbor_of_neighbor = self.minesweeper.board[i][j]
                        nonlocal num_unrevealed_around_neighbor, num_flagged_around_neighbor
                        if not neighbor_of_neighbor.is_revealed:
                            if neighbor_of_neighbor.is_flagged:
                                num_flagged_around_neighbor += 1
                            else:
                                num_unrevealed_around_neighbor += 1

                    run_on_all_adjacent_blocks(neighbor_row, neighbor_col, dimen, count_unrevealed_and_flagged)

                    if num_unrevealed_around_neighbor == neighbor.number - num_flagged_around_neighbor:
                        row_to_flag = row
                        col_to_flag = col

            run_on_all_adjacent_blocks(row, col, dimen, check_neighbor)

        for_each_cell(self.minesweeper.board, check_cell)

        if row_to_flag is not None:
            return [row_to_flag, col_to_flag]
        return None

    def find_cell_to_click(self):
        dimen = self.minesweeper.dimension
        row_to_click = None
        col_to_click = None

        def check_cell(cell, row, col):
            nonlocal row_to_click, col_to_click
            if cell.is_revealed or cell.is_flagged or row_to_click is not None:
                return

            def check_neighbor(neighbor_row, neighbor_col):
                neighbor = self.minesweeper.board[neighbor_row][neighbor_col]
                if neighbor.is_revealed:
                    num_flagged = 0
                    num_unrevealed = 0

                    def count_flagged_and_unrevealed(i, j):
                        neighbor_of_neighbor = self.minesweeper.board[i][j]
                        nonlocal num_flagged, num_unrevealed
                        if not neighbor_of_neighbor.is_revealed:
                            if neighbor_of_neighbor.is_flagged:
                                num_flagged += 1
                            else:
                                num_unrevealed += 1

                    run_on_all_adjacent_blocks(neighbor_row, neighbor_col, dimen, count_flagged_and_unrevealed)

                    if num_flagged == neighbor.number and num_unrevealed > 0:
                        row_to_click = row
                        col_to_click = col

            run_on_all_adjacent_blocks(row, col, dimen, check_neighbor)

        for_each_cell(self.minesweeper.board, check_cell)

        if row_to_click is not None:
            return [row_to_click, col_to_click]
        return None


class App:
    def __init__(self):
        self.timer = None
        self.solver_timer = None
        self.running = True

    def play_game(self, dimen):
        self.reset_state()
        self.minesweeper = Minesweeper(dimen)
        self.solver = Solver(self.minesweeper)
        self.time_elapsed = 0
        self.timer = time.time()
        pygame.init()
        self.screen = pygame.display.set_mode((dimen * 30, 650))
        pygame.display.set_caption("Minesweeper")
        self.clock = pygame.time.Clock()
        while self.running:
            self.handle_events()
            self.draw_board()
            self.draw_solver_button()
            pygame.display.flip()
            self.clock.tick(30)

            if self.minesweeper.won:
                self.on_game_won()
                self.running = False

    def reset_state(self):
        self.timer = None
        self.solver_timer = None
        self.running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = pos[1] // 30, pos[0] // 30
                if 0 <= pos[1] < 600:  # Dentro del área del tablero
                    if event.button == 1:  # Clic izquierdo
                        self.minesweeper.on_cell_clicked(row, col)
                    elif event.button == 3:  # Clic derecho
                        self.minesweeper.on_cell_right_clicked(row, col)
                elif 610 <= pos[1] <= 650 and 10 <= pos[0] <= 100:  # Dentro del área del botón
                    if event.button == 1:  # Clic izquierdo en el botón
                        self.auto_solve_game()

    def auto_solve_game(self):
        while not (self.minesweeper.won or self.minesweeper.lost):
            self.auto_solve_one_move()

    def auto_solve_one_move(self):
        move = self.solver.get_next_move()
        if move[0]:
            self.minesweeper.on_cell_clicked(move[1], move[2])
        else:
            self.minesweeper.on_cell_right_clicked(move[1], move[2])
        self.draw_board()
        pygame.display.flip()


    def draw_board(self):
        self.screen.fill((255, 255, 255))
        for row in range(self.minesweeper.dimension):
            for col in range(self.minesweeper.dimension):
                cell = self.minesweeper.board[row][col]
                rect = pygame.Rect(col * 30, row * 30, 30, 30)
                if cell.is_revealed:
                    if cell.is_bomb:
                        pygame.draw.rect(self.screen, (255, 0, 0), rect)
                    else:
                        pygame.draw.rect(self.screen, (200, 200, 200), rect)
                        if cell.number > 0:
                            font = pygame.font.Font(None, 24)
                            text = font.render(str(cell.number), True, (0, 0, 0))
                            self.screen.blit(text, (col * 30 + 10, row * 30 + 5))
                else:
                    pygame.draw.rect(self.screen, (100, 100, 100), rect)
                    if cell.is_flagged:
                        pygame.draw.rect(self.screen, (0, 0, 255), rect)
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)

    def draw_solver_button(self):
        font = pygame.font.Font(None, 36)
        button_rect = pygame.Rect(10, 610, 90, 40)
        pygame.draw.rect(self.screen, (0, 0, 255), button_rect)
        text = font.render("Solver", True, (255, 255, 255))
        self.screen.blit(text, (20, 615))

# Inicializar el juego con una dimensión dada
dimension = 10
app = App()
app.play_game(dimension)
