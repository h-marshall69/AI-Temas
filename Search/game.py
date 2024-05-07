import pygame
import math
import random
import sys

# Constantes
FONT = 'couriernew'
WIDTH, HEIGHT = 300, 300
LINE_COLOR = (0, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SQUARE_SIZE = WIDTH // 3

X = 'X'
O = 'O'
E = None

def initial_state():
    return [[E for _ in range(3)] for _ in range(3)]

class Gato:
    def __init__(self, board = initial_state(), game_over = False, quit = False, albedo = False):
        self.pygame = pygame
        self.pygame.init()
        self.screen = pygame.display.set_mode((650, 650))
        self.pygame.display.set_caption("Abadeer")
        #self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.board = board
        #self.board = [[X, O, E], [O, E, X], [X, O, E]]
        self.current_player = X

        #controller
        self.game_over = game_over
        self.quit = quit
        self.albedo = albedo

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

    def draw_win_state(self, player):
        self.screen.fill((255, 255, 215))
        mouse = self.pygame.mouse.get_pos()
        font = self.pygame.font.SysFont(FONT, 40, bold=True)
        introText = font.render("Wineer is {} !!!".format(player), True, BLACK)
        self.screen.blit(introText, (90, 50))
        if 250 + 100 >= mouse[0] >= 250 and 150 + 50 >= mouse[1] >= 150:
            font = self.pygame.font.SysFont(FONT, 40, bold=True)
            introText = font.render("Menu", True, BLACK)
            self.screen.blit(introText, (250, 140))
            font = self.pygame.font.SysFont(FONT, 30)
            introText = font.render("Exit", True, BLACK)
            self.screen.blit(introText, (250, 190))
        elif 250 + 100 >= mouse[0] >= 250 and 190 + 50 >= mouse[1] >= 190:
            font = self.pygame.font.SysFont(FONT, 30)
            introText = font.render("Menu", True, BLACK)
            self.screen.blit(introText, (250, 150))
            font = self.pygame.font.SysFont(FONT, 40, bold=True)
            introText = font.render("Exit", True, BLACK)
            self.screen.blit(introText, (250, 190))
        else:
            font = self.pygame.font.SysFont(FONT, 30)
            introText = font.render("Menu", True, BLACK)
            self.screen.blit(introText, (250, 150))
            introText = font.render("Exit", True, BLACK)
            self.screen.blit(introText, (250, 190))

    def terminal(self, board):
        """
        Returns True if game is over, False otherwise.
        """
        for i in range(len(board)):
            if (board[i][0] == board[i][1] == board[i][2] != E) or (board[0][i] == board[1][i] == board[2][i] != E):
                return True

        if (board[0][0] == board[1][1] == board[2][2] != E) or (board[2][0] == board[1][1] == board[0][2] != E):
            return True

        return not any (E in row for row in board)
        #raise NotImplementedError

    def draw_lines(self):
        pygame.draw.line(self.screen, BLACK, [215, 0], [215, 650], 5)
        pygame.draw.line(self.screen, BLACK, [430, 0], [430, 650], 5)
        pygame.draw.line(self.screen, BLACK, [0, 215], [650, 215], 5)
        pygame.draw.line(self.screen, BLACK, [0, 430], [650, 430], 5)

    def draw_symbols(self):
        for row in range(3):
            for col in range(3):
                if self.board[row][col] != E:
                    font = pygame.font.Font(None, 200)
                    text = font.render(self.board[row][col], True, LINE_COLOR)
                    text_rect = text.get_rect(center=(col * 215 + 215 // 2, 
                                                      row * 215 + 215 // 2))
                    self.screen.blit(text, text_rect)

    def actions(self, board):
        """
        Returns set of all possible actions (i, j) available on the board.
        """
        action = []

        for i, row in enumerate(board):
            for j, col in enumerate(row):
                if col == E:
                    action.append((i, j))

        return action
    
    def player(self, board):
        """
        Returns player who has the next turn on a board.
        """
        count_X = 0
        count_O = 0

        for i in board:
            for j in i:
                if j == X:
                    count_X += 1
                if j == O:
                    count_O += 1

        if count_O < count_X:
            return 'O'

        return 'X'

    def result(self, board, action):
        """
        Returns the board that results from making move (i, j) on the board.
        """
        current = self.player(board)

        i, j = action

        board[i][j] = current
        return board


    def check_winner(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != E:
                return self.board[i][0]
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != E:
                return self.board[0][i]
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != E:
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != E:
            return self.board[0][2]
        return None


    def check_draw(self):
        for row in self.board:
            if E in row:
                return False
        return True

    def utility(self, board):
        """
        Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
        """
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != E: #row
                return 1 if self.board[i][0] == X else -1
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != E: #col
                return -1 if self.board[0][i] == O else 1
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != E: #diagonal principal
            return 1 if self.board[1][1] == X else -1
        if self.board[2][0] == self.board[1][1] == self.board[0][2] != E: #diagonal secundaria
            return -1 if self.board[1][1] == O else 1
        
        return 0
    #albedo
    def minimax(self, board, depth, alpha, beta, maximizing_player):
        if self.terminal(board) or depth == 0:
            return self.utility(board)

        #if maximizing_player:
        if maximizing_player:
            value = -float('inf')
            for action in self.actions(board):
                value = max(value, self.minimax(self.result(board, action), depth - 1, alpha, beta, False))
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value
        else:
            value = float('inf')
            for action in self.actions(board):
                value = min(value, self.minimax(self.result(board, action), depth - 1, alpha, beta, True))
                beta = min(beta, value)
                if beta <= alpha:
                    break
            return value
    #albedo
    def best_move(self):
        best_score = -float('inf')
        best_move = None
        alpha = -float('inf')
        beta = float('inf')
        for action in self.actions(self.board):
            copy_board = [row[:] for row in self.board]
            score = self.minimax(self.result(copy_board, action), depth=100, alpha=alpha, beta=beta, maximizing_player=False)
            if score > best_score:
                best_score = score
                best_move = action
            alpha = min(alpha, best_score)
        return best_move
    #madeline
    def minimax_mad(self, board):
        """
        Returns the optimal action for the current player on the board.
        """
        if self.terminal(board):
            return self.utility(board)

        if self.player(board) == X:
            value = -float('inf')
            copy_board = [row[:] for row in board]
            for action in self.actions(board):
                value = max(value, self.minimax_mad(self.result(copy_board, action)))

        else:
            value = float('inf')
            copy_board = [row[:] for row in board]
            for action in self.actions(board):
                
                value = min(value, self.minimax_mad(self.result(copy_board, action)))

        return value

        #raise NotImplementedError
    #madeline
    def best_move_mad(self, board):
        game = []
        if not self.terminal(board):
            for action in self.actions(board):
                copy_board = [row[:] for row in board]
                game.append((self.minimax_mad(self.result(copy_board, action)), action))
            return min(game, key=lambda x: x[0])
        
   
    #naomi
    def minimax_nao(self, board):
        global actions_explored
        actions_explored = 0

        def max_player(self, board, best_min = 20):
            """ Helper function to maximise score for 'X' player.
            Uses alpha-beta pruning to reduce the state space explored.
            best_min is the best result
            """

            global actions_explored

            # If the game is over, return board value
            if self.terminal(board):
                return (self.utility(board), None)

            # Else pick the action giving the max value when min_player plays optimally
            value = -10
            best_action = None


            # Get set of actions and then select a random one until list is empty:
            action_set = self.actions(board)

            while len(action_set) > 0:
                action = random.choice(tuple(action_set))
                action_set.remove(action)

                # A-B Pruning skips calls to min_player if lower result already found:
                if best_min <= value:
                    break

                actions_explored += 1
                min_player_result = self.min_player(self.result(board, action), value)
                if min_player_result[0] > value:
                    best_action = action
                    value = min_player_result[0]

            return (value, best_action)


        def min_player(self, board, best_max = -20):
            """ Helper function to minimise score for 'O' player """

            global actions_explored

            # If the game is over, return board value
            if self.terminal(board):
                return (self.utility(board), None)

            # Else pick the action giving the min value when max_player plays optimally
            value = 10
            best_action = None

            # Get set of actions and then select a random one until list is empty:
            action_set = self.actions(board)

            while len(action_set) > 0:
                action = random.choice(tuple(action_set))
                action_set.remove(action)

                # A-B Pruning skips calls to max_player if higher result already found:
                if best_max >= value:
                    break

                actions_explored += 1
                max_player_result = self.max_player(self.result(board, action), value)
                if max_player_result[0] < value:
                    best_action = action
                    value = max_player_result[0]

            return (value, best_action)


        # If the board is terminal, return None:
        if self.terminal(board):
            return None
        if self.player(board) == 'X':
            print('AI is exploring possible actions...')
            best_move = self.max_player(board)[1]
            print('Actions explored by AI: ', actions_explored)
            return best_move
        else:
            print('AI is exploring possible actions...')
            best_move = self.min_player(board)[1]
            print('Actions explored by AI: ', actions_explored)
            return best_move

    def best_move_nao(self, board):
        copy = [row[:] for row in board]
        i, j = self.minimax_nao(copy)
        return (i, j)
    
    #   CONTROLLER
    def run(self):
        intro = True
        while intro:
            for event in self.pygame.event.get():
                if event.type == self.pygame.QUIT:
                    intro = False
                    pygame.quit()
                    sys.exit()
                    break

                if event.type == self.pygame.MOUSEBUTTONDOWN:
                    mouse = self.pygame.mouse.get_pos()
                    if 250 + 200 >= mouse[0] >= 250 and 150 + 50 >= mouse[1] >= 150:
                        intro = False
                        self.screen.fill((255, 255, 255))
                        self.run_game() 
                    if 250 + 200 >= mouse[0] >= 250 and 190 + 50 >= mouse[1] >= 190:
                        intro = False
                        self.screen.fill((255, 255, 255))
                        self.albedo = True
                        self.run_game()

            self.draw_menu()
            self.pygame.display.update()

    def run_game(self):
        self.draw_lines()
        while not self.game_over or self.quit:
            for event in self.pygame.event.get():
                if event.type == self.pygame.QUIT:
                    self.quit = True
                    pygame.quit()
                    sys.exit()

                if event.type == self.pygame.MOUSEBUTTONDOWN:
                    if self.albedo:
                        #self.move_albedo()
                        #self.madeline()
                        self.naomi()
                    else:
                        self.move()
            self.draw_symbols()
            self.pygame.display.update()

        if self.game_over:
            self.screen.fill((255, 255, 215))
            self.run_end_game()

    def run_end_game(self):
        player = "No one"
        end_game = True
        while end_game:
            for event in self.pygame.event.get():
                if event.type == self.pygame.QUIT:
                    end_game = False
                    pygame.quit()
                    sys.exit()
                    break

                if event.type == self.pygame.MOUSEBUTTONDOWN:
                    mouse = self.pygame.mouse.get_pos()
                    if 250 + 200 >= mouse[0] >= 250 and 150 + 50 >= mouse[1] >= 150:
                        end_game = False
                        self.screen.fill((255, 255, 215))
                        self.__init__(initial_state(), False, False, False)
                        self.run() 
                    if 250 + 200 >= mouse[0] >= 250 and 190 + 50 >= mouse[1] >= 190:
                        end_game = False
                        pygame.quit()
                        sys.exit()
                        break

            self.draw_win_state(player)
            self.pygame.display.update()

    def move(self):
        mouse = self.pygame.mouse.get_pos()
        clicked_row = mouse[1] // 215
        clicked_col = mouse[0] // 215
        if not self.game_over and self.board[clicked_row][clicked_col] == E:
            self.board[clicked_row][clicked_col] = self.current_player
            winner = self.check_winner()
            if winner:
                self.game_over = True
            elif self.check_draw():
                self.game_over = True
            else:
                self.current_player = O if self.current_player == X else X

    def move_albedo(self):
        mouse = self.pygame.mouse.get_pos()
        clicked_row = mouse[1] // 215
        clicked_col = mouse[0] // 215
        if not self.game_over and self.board[clicked_row][clicked_col] == E:
            self.board[clicked_row][clicked_col] = self.current_player
            winner = self.check_winner()
            if winner:
                self.game_over = True
            elif self.check_draw():
                self.game_over = True
            else:
                i, j = self.best_move()
                self.board[i][j] = O

    def madeline(self):
        mouse = self.pygame.mouse.get_pos()
        clicked_row = mouse[1] // 215
        clicked_col = mouse[0] // 215
        if not self.game_over and self.board[clicked_row][clicked_col] == E:
            self.board[clicked_row][clicked_col] = self.current_player
            winner = self.check_winner()
            if winner:
                self.game_over = True
            elif self.check_draw():
                self.game_over = True
            else:
                i, j = self.best_move_mad(self.board)[1]
                self.board[i][j] = O

    def naomi(self):
        mouse = self.pygame.mouse.get_pos()
        clicked_row = mouse[1] // 215
        clicked_col = mouse[0] // 215
        if not self.game_over and self.board[clicked_row][clicked_col] == E:
            self.board[clicked_row][clicked_col] = self.current_player
            winner = self.check_winner()
            if winner:
                self.game_over = True
            elif self.check_draw():
                self.game_over = True
            else:
                i, j = self.best_move_nao(self.board)
                self.board[i][j] = O

if __name__ == "__main__":
    game = Gato()
    game.run()
