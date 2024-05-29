import pygame
import random

# Constants
WIDTH, HEIGHT = 500, 400
ROWS, COLS = 10, 10
MINE_COUNT = 10
CELL_SIZE = WIDTH // COLS
MENU_WIDTH = 100
FPS = 30

# Colors
WHITE = (255, 255, 255)
GRAY = (192, 192, 192)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Initialize Pygame
pygame.init()
pygame.display.set_caption("Minesweeper")
screen = pygame.display.set_mode((WIDTH + MENU_WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont(None, 30)

class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        self.is_mine = False
        self.revealed = False
        self.marked = False
        self.neighbor_mines = 0

    def draw(self):
        if not self.revealed:
            pygame.draw.rect(screen, GRAY, self.rect)
            if self.marked:
                pygame.draw.rect(screen, RED, self.rect, 3)
        else:
            pygame.draw.rect(screen, WHITE, self.rect)
            if self.is_mine:
                pygame.draw.circle(screen, BLACK, self.rect.center, CELL_SIZE // 4)
            elif self.neighbor_mines > 0:
                text_surface = font.render(str(self.neighbor_mines), True, BLACK)
                text_rect = text_surface.get_rect(center=self.rect.center)
                screen.blit(text_surface, text_rect)

    def reveal(self):
        self.revealed = True

    def mark(self):
        self.marked = not self.marked

    def count_neighbor_mines(self, grid):
        if self.is_mine:
            self.neighbor_mines = -1
            return
        count = 0
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                if 0 <= self.row + dr < ROWS and 0 <= self.col + dc < COLS:
                    if grid[self.row + dr][self.col + dc].is_mine:
                        count += 1
        self.neighbor_mines = count

def create_grid():
    grid = [[Cell(row, col) for col in range(COLS)] for row in range(ROWS)]
    return grid

def place_mines(grid):
    mines_placed = 0
    while mines_placed < MINE_COUNT:
        row = random.randint(0, ROWS - 1)
        col = random.randint(0, COLS - 1)
        cell = grid[row][col]
        if not cell.is_mine:
            cell.is_mine = True
            mines_placed += 1

def reveal_empty_cells(cell, grid):
    if cell.revealed:
        return
    cell.reveal()
    if cell.neighbor_mines == 0:
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                if 0 <= cell.row + dr < ROWS and 0 <= cell.col + dc < COLS:
                    neighbor = grid[cell.row + dr][cell.col + dc]
                    reveal_empty_cells(neighbor, grid)

def reveal_mines(grid):
    for row in grid:
        for cell in row:
            if cell.is_mine:
                cell.reveal()

def draw_grid(grid):
    for row in grid:
        for cell in row:
            cell.draw()

def draw_menu():
    menu_rect = pygame.Rect(WIDTH, 0, MENU_WIDTH, HEIGHT)
    pygame.draw.rect(screen, GRAY, menu_rect)

    menu_font = pygame.font.SysFont(None, 24)
    menu_options = ["AutoPlay", "AI Move", "Reset", "Exit"]
    for i, option in enumerate(menu_options):
        text_surface = menu_font.render(option, True, BLACK)
        text_rect = text_surface.get_rect(center=(WIDTH + MENU_WIDTH // 2, 50 + i * 50))
        screen.blit(text_surface, text_rect)

def handle_menu_click(pos):
    x, y = pos
    if WIDTH <= x <= WIDTH + MENU_WIDTH:
        option_index = (y - 50) // 50
        if option_index == 0:
            board.autoplay()
        elif option_index == 1:
            board.ai_move()
        elif option_index == 2:
            board.reset(mines)
        elif option_index == 3:
            pygame.quit()

def main():
    grid = create_grid()
    place_mines(grid)
    for row in grid:
        for cell in row:
            cell.count_neighbor_mines(grid)

    running = True
    while running:
        screen.fill(BLACK)
        draw_grid(grid)
        draw_menu()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    pos = pygame.mouse.get_pos()
                    handle_menu_click(pos)

    pygame.quit()

if __name__ == "__main__":
    main()
