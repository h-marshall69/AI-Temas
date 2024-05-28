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
        self.image1 = pygame.image.load(os.path.join('Assets/images', 'mine.png')).convert_alpha()
        self.image1 = pygame.transform.scale(self.image1, (100, 100))

        self.ROWS = 10
        self.COLS = 10
        self.mines = 15
        self.large = CELL_SIZE * 10
        self.grid = [[0 for _ in range(self.COLS)] for _ in range(self.ROWS)]
        self.game_over = False

        self.init_game()

    def init_game(self):
        # Coloca las minas
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

        # Contador para las minas restantes
        self.remaining_mines = self.mines

        # Cargar sonidos
        self.click_sound = pygame.mixer.Sound(os.path.join('Assets/sounds', 'click.wav'))
        #self.mine_sound = pygame.mixer.Sound(os.path.join('sounds', 'mine.wav'))
        self.mine_sound = pygame.mixer.Sound(os.path.join('Assets/sounds', 'lose_minesweeper.wav'))
        self.win_sound = pygame.mixer.Sound(os.path.join('Assets/sounds', 'win.wav'))

    def draw_grid(self):
        for row in range(self.ROWS):
            for col in range(self.COLS):
                cell_rect = self.pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if self.grid[row][col] == -11:  # minas
                    self.pygame.draw.rect(self.screen, BLACK, cell_rect)
                elif self.grid[row][col] < 10:  # Celda vacía
                    self.pygame.draw.rect(self.screen, GRAY, cell_rect)
                else:  # Número de minas vecinas
                    self.pygame.draw.rect(self.screen, GRAY, cell_rect)
                    text_surface = self.font.render(str(self.grid[row][col] % 10), True, BLACK)
                    text_rect = text_surface.get_rect(center=cell_rect.center)
                    self.screen.blit(text_surface, text_rect)

        for row in range(self.ROWS + 1):
            self.pygame.draw.line(self.screen, BLACK, (0, row * CELL_SIZE), (self.large, row * CELL_SIZE), 2)
            self.pygame.draw.line(self.screen, BLACK, (row * CELL_SIZE, 0), (row * CELL_SIZE, self.large), 2)

    def reveal_mines(self):
        for row in range(self.ROWS):
            for col in range(self.COLS):
                if self.grid[row][col] == -1:
                    self.grid[row][col] = -11

    def reveal_empty_cell(self, row, col):
        if 0 <= row < self.ROWS and 0 <= col < self.COLS and self.grid[row][col] < 10:
            self.grid[row][col] += 10
            if self.grid[row][col] == 10:  # Si es una celda vacía, continuar revelando recursivamente
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        self.reveal_empty_cell(row + dr, col + dc)

    def update_remaining_mines(self):
        remaining_text = self.font.render(f'Remaining Mines: {self.remaining_mines}', True, BLACK)
        self.screen.blit(remaining_text, (WIDTH - 200, 20))

    def show_message(self, message):
        message_surface = self.font.render(message, True, RED)
        message_rect = message_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(message_surface, message_rect)

    def play_sound(self, sound):
        pygame.mixer.Sound.play(sound)

    def run_game(self):
        self.start_game()  # Llama a la función start_game() en lugar de run_game()

    def start_game(self):  # Aquí cambiamos el nombre de la función
        running = True
        while running:
            self.screen.fill(WHITE)
            self.update_remaining_mines()
            self.draw_grid()
            for event in self.pygame.event.get():
                if event.type == self.pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == self.pygame.MOUSEBUTTONDOWN and not self.game_over:
                    mouse = self.pygame.mouse.get_pos()
                    if 500 >= mouse[0] >= 0 and 500 >= mouse[1] >= 0:
                        click_row = mouse[1] // CELL_SIZE
                        click_col = mouse[0] // CELL_SIZE
                        if self.grid[click_row][click_col] == -1:
                            self.reveal_mines()
                            self.play_sound(self.mine_sound)
                            self.show_message("Game Over! Click to play again.")
                            self.game_over = True
                        elif self.grid[click_row][click_col] == 0:
                            self.reveal_empty_cell(click_row, click_col)
                            self.play_sound(self.click_sound)
                        else:
                            self.grid[click_row][click_col] += 10
                            self.play_sound(self.click_sound)
                        self.remaining_mines -= 1
                elif event.type == self.pygame.KEYDOWN and self.game_over:
                    if event.key == pygame.K_RETURN:
                        self.__init__()  # Reiniciar el juego al presionar Enter

            if self.remaining_mines == 0 and not self.game_over:
                self.show_message("You Win! Click to play again.")
                self.play_sound(self.win_sound)
                self.game_over = True

            self.pygame.display.update()


def run_game_busca_minas():
    mine = Mine()
    mine.run_game()