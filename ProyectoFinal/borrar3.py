import pygame
import random
import time
import sys

class MinesweeperAI:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.moves_made = set()
        self.mines = set()
        self.board = [['.' for _ in range(width)] for _ in range(height)]

    def mine_sweeper_solver(self, row, col):
        if self.board[row][col] == '*':
            self.board[row][col] = 'B'
            return True

        if self.board[row][col] != '.':
            return False

        self.board[row][col] = 'F'
        for (i, j) in self.valid_moves(row, col):
            if self.mine_sweeper_solver(i, j):
                self.board[i][j] = '*'
        return False

    def valid_moves(self, row, col):
        moves = []

        for m in [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]:
            if 0 <= m[0] < len(self.board) and 0 <= m[1] < len(self.board[0]):
                moves.append(m)

        return moves

    def make_safe_move(self):
        for r in range(self.height):
            for c in range(self.width):
                if self.board[r][c] == 'F' and (r, c) not in self.moves_made:
                    return (r, c)
        return None

    def make_random_move(self):
        import random
        choices = [(r, c) for r in range(self.height) for c in range(self.width)
                   if self.board[r][c] == '.' and (r, c) not in self.moves_made]
        if choices:
            return random.choice(choices)
        return None


class MinesweeperBoard:
    def __init__(self, height, width, mines):
        self.height = height
        self.width = width
        self.dimension = mines
        self.board = [['.' for _ in range(width)] for _ in range(height)]
        self.place_random_mines(mines)

    def print_board(self):
        for row in self.board:
            print(" ".join(row))
        print()

    def count_nearby_mines(self, cell):
        row, col = cell
        count = 0
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if (r, c) != cell and 0 <= r < self.height and 0 <= c < self.width:
                    if self.board[r][c] == '*':
                        count += 1
        return count

    def place_random_mines(self, num_mines):
        mines_placed = 0
        while mines_placed < num_mines:
            row = random.randint(0, self.height - 1)
            col = random.randint(0, self.width - 1)
            if self.board[row][col] != '*':
                self.board[row][col] = '*'
                mines_placed += 1

    def calculate_numbers(self):
        for row in range(self.height):
            for col in range(self.width):
                if self.board[row][col] == '.':
                    count = self.count_nearby_mines((row, col))
                    if count > 0:
                        self.board[row][col] = str(count)

    def get_neighbors(self, cell):
        row, col = cell
        neighbors = []
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                if 0 <= row + dr < self.height and 0 <= col + dc < self.width:
                    if (dr, dc) != (0, 0):
                        neighbors.append((row + dr, col + dc))
        return neighbors
    def play(self):
        ai = MinesweeperAI(self.height, self.width)
        ai.board = [row[:] for row in self.board]  # Clone the board
        while True:
            move = ai.make_safe_move()
            if move is None:
                move = ai.make_random_move()
            if move is None:
                break
            row, col = move
            if self.board[row][col] == '*':
                print(f"Game Over! Hit a mine at {(row, col)}")
                return
            count = self.count_nearby_mines(move)
            ai.moves_made.add(move)
            ai.board[row][col] = str(count)
            ai.mine_sweeper_solver(row, col)
        print("AI has solved the board successfully!")
        self.board = ai.board

    def autoplay(self):
        ai = MinesweeperAI(self.height, self.width)
        ai.board = [row[:] for row in self.board]
        while True:
            move = ai.make_safe_move()
            if move is None:
                move = ai.make_random_move()
            if move is None:
                break
            row, col = move
            if self.board[row][col] == '*':
                print(f"Game Over! Hit a mine at {(row, col)}")
                return
            count = self.count_nearby_mines(move)
            ai.moves_made.add(move)
            ai.board[row][col] = str(count)
            ai.mine_sweeper_solver(row, col)
        print("AI has solved the board successfully!")
        self.board = ai.board

    def ai_move(self):
        ai = MinesweeperAI(self.height, self.width)
        ai.board = [row[:] for row in self.board]
        move = ai.make_safe_move()
        if move is None:
            move = ai.make_random_move()
        if move is None:
            print("No moves available!")
            return
        row, col = move
        if self.board[row][col] == '*':
            print(f"Game Over! Hit a mine at {(row, col)}")
            return
        count = self.count_nearby_mines(move)
        ai.moves_made.add(move)
        ai.board[row][col] = str(count)
        self.board = ai.board
        print(f"AI moved to {(row, col)}")

    def reset(self, mines):
        self.mines = set(mines)
        self.board = [['.' for _ in range(self.width)] for _ in range(self.height)]
        for (r, c) in mines:
            self.board[r][c] = '*'

class App:
    def __init__(self):
        self.timer = None
        self.solver_timer = None
        self.running = True

    def play_game(self, dimen):
        self.minesweeper = MinesweeperBoard(dimen)
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
        pass

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

def main():
    height = 5
    width = 5
    mines = [(0, 1), (1, 3), (2, 2), (4, 0)]
    num_mines = len(mines)
    board = MinesweeperBoard(height, width, num_mines)

    while True:
        print("1. AutoPlay")
        print("2. AI move")
        print("3. Reset")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            board.autoplay()
            board.print_board()
        elif choice == "2":
            board.ai_move()
            board.print_board()
        elif choice == "3":
            board.reset(mines)
            board.print_board()
        elif choice == "4":
            break
        else:
            print("Invalid choice! Please try again.")


if __name__ == "__main__":
    main()