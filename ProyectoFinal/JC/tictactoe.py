import pygame
import sys
import math
import random

def run_game_tictactoe():
    # Inicializar Pygame
    pygame.init()

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)

    WIDTH, HEIGHT = 800, 800
    LINE_WIDTH = 15
    ROWS, COLS = 3, 3
    SQUARE_SIZE = WIDTH // COLS

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("tres en raya")

    INITIAL_STATE = [['' for _ in range(3)] for _ in range(3)]

    # Jugadores
    PLAYER_X = 'X'
    PLAYER_O = 'O'

    # Función para verificar si hay ganador
    def check_winner(S, symbol):
        # Verificar filas y columnas
        for i in range(3):
            if all([S[i][j] == symbol for j in range(3)]) or \
               all([S[j][i] == symbol for j in range(3)]):
                return True

        # Verificar diagonales
        if all([S[i][i] == symbol for i in range(3)]) or \
           all([S[i][2 - i] == symbol for i in range(3)]):
            return True

        return False

    # Función para obtener acciones posibles
    def ACTIONS(S):
        possible_actions = []
        for i in range(3):
            for j in range(3):
                if S[i][j] == '':
                    possible_actions.append((i, j))
        return possible_actions

    # Función para obtener el estado resultante después de una acción
    def RESULT(S, A, symbol):
        new_S = [row[:] for row in S]
        row, col = A
        new_S[row][col] = symbol
        return new_S

    # Función para calcular la utilidad de un estado
    def utility(S):
        if check_winner(S, PLAYER_X):
            return 1
        elif check_winner(S, PLAYER_O):
            return -1
        else:
            return 0

    # Algoritmo MINIMAX
    def minimax(S, player_turn, depth):
        if terminal(S) or depth == 0:
            return utility(S), None

        if player_turn == PLAYER_X:
            v = -math.inf
            optimal_move = None
            for action in ACTIONS(S):
                min_val, _ = minimax(RESULT(S, action, PLAYER_X), PLAYER_O, depth - 1)
                if min_val > v:
                    v = min_val
                    optimal_move = action
            return v, optimal_move

        else:  # player_turn == PLAYER_O
            v = math.inf
            optimal_move = None
            for action in ACTIONS(S):
                max_val, _ = minimax(RESULT(S, action, PLAYER_O), PLAYER_X, depth - 1)
                if max_val < v:
                    v = max_val
                    optimal_move = action
            return v, optimal_move

    # Función para determinar el jugador actual
    def current_player(S, selected_symbol):
        if selected_symbol == PLAYER_X:
            return PLAYER_X if sum(row.count(PLAYER_X) for row in S) <= sum(row.count(PLAYER_O) for row in S) else PLAYER_O
        else:
            return PLAYER_X if sum(row.count(PLAYER_X) for row in S) < sum(row.count(PLAYER_O) for row in S) else PLAYER_O

    # Función para verificar si el estado es terminal
    def terminal(S):
        if check_winner(S, PLAYER_X) or check_winner(S, PLAYER_O) or all(S[i][j] != '' for i in range(3) for j in range(3)):
            return True
        else:
            return False

    # Función para dibujar el tablero
    def draw_board():
        for i in range(1, ROWS):
            pygame.draw.line(screen, WHITE, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE), LINE_WIDTH)
            pygame.draw.line(screen, WHITE, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

    # Función para dibujar el símbolo (X o O)
    def draw_symbol(row, col, symbol):
        centerX = col * SQUARE_SIZE + SQUARE_SIZE // 2
        centerY = row * SQUARE_SIZE + SQUARE_SIZE // 2

        if symbol == 'X':
            pygame.draw.line(screen, BLUE, (centerX - SQUARE_SIZE // 4, centerY - SQUARE_SIZE // 4),
                             (centerX + SQUARE_SIZE // 4, centerY + SQUARE_SIZE // 4), 10)
            pygame.draw.line(screen, BLUE, (centerX + SQUARE_SIZE // 4, centerY - SQUARE_SIZE // 4),
                             (centerX - SQUARE_SIZE // 4, centerY + SQUARE_SIZE // 4), 10)
        else:
            pygame.draw.circle(screen, RED, (centerX, centerY), SQUARE_SIZE // 4, 10)

    def handle_click(row, col, player):
        if vs_ia_mode:  # Si estás jugando contra la IA
            if S[row][col] == '':
                S[row][col] = player
                draw_board()  # Dibujamos el tablero nuevamente después de actualizarlo
                for row in range(3):
                    for col in range(3):
                        if S[row][col] != '':
                            draw_symbol(row, col, S[row][col])
                if check_winner(S, player):
                    show_message(f'¡{player} ha ganado!')
                elif all(S[i][j] != '' for i in range(3) for j in range(3)):
                    show_message('Empate')
                else:
                    next_player = current_player(S, selected_symbol)
                    if next_player != selected_symbol:
                        minimax_move(S, next_player)
                pygame.display.update()
        else:  # Si estás jugando contra otro jugador humano
            if S[row][col] == '':  # Verificar si la casilla está vacía
                S[row][col] = player
                draw_board()  # Dibujamos el tablero nuevamente después de actualizarlo
                for row in range(3):
                    for col in range(3):
                        if S[row][col] != '':
                            draw_symbol(row, col, S[row][col])
                if check_winner(S, player):
                    show_message(f'¡{player} ha ganado!')
                elif all(S[i][j] != '' for i in range(3) for j in range(3)):
                    show_message('Empate')
                pygame.display.update()

            
    def minimax_move(S, player):
        _, best_move = minimax(S, player, 6)  # Profundidad ajustada a 3
        if best_move:
            handle_click(best_move[0], best_move[1], player)
        else:
            random_move = random.choice(ACTIONS(S))  # Movimiento aleatorio si no hay mejor opción
            handle_click(random_move[0], random_move[1], player)

    def show_message(message):
        font = pygame.font.SysFont(None, 50)
        text = font.render(message, True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))

        # Ajustar el tamaño del fondo semitransparente
        background_width = text_rect.width + 40  # Más ancho
        background_height = text_rect.height + 100  # Más alto

        # Crear una superficie para el fondo semitransparente
        background = pygame.Surface((background_width, background_height), pygame.SRCALPHA)

        # Ajustar el nivel de transparencia del color de relleno
        background.fill((0, 0, 0, 250))  # Relleno negro semitransparente más oscuro

        # Dibujar el fondo detrás del texto
        screen.blit(background, (text_rect.left - 20, text_rect.top - 20))

        screen.blit(text, text_rect)

        # Mostrar botones
        button_new_game = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 30, 300, 50)
        button_exit = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 100, 300, 50)

        pygame.draw.rect(screen, WHITE, button_new_game)
        pygame.draw.rect(screen, WHITE, button_exit)

        text_new_game = font.render("Jugar de nuevo", True, BLACK)
        text_exit = font.render("Salir", True, BLACK)

        screen.blit(text_new_game, (button_new_game.x + 40, button_new_game.y + 10))
        screen.blit(text_exit, (button_exit.x + 120, button_exit.y + 10))

        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos

                    if button_new_game.collidepoint(mouse_pos):
                        reset_game()
                        screen.fill(BLACK)  # Limpiar la pantalla para la nueva partida
                        draw_board()  # Volver a dibujar el tablero
                        pygame.display.update()
                        return
                    elif button_exit.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()


    # Función para esperar a que se presione una tecla
    def wait_for_key():
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        reset_game()
                        return
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                    else:
                        return

    # Función para reiniciar el juego
    def reset_game():
        global S
        S = [['' for _ in range(3)] for _ in range(3)]
        
    def select_player_screen():
        screen.fill(BLACK)
        font = pygame.font.SysFont(None, 50)
        text = font.render("Selecciona tu símbolo:", True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        screen.blit(text, text_rect)

        button_x = pygame.Rect(150, 300, 100, 50)
        button_o = pygame.Rect(350, 300, 100, 50)
        button_random = pygame.Rect(250, 400, 100, 50)

        pygame.draw.rect(screen, WHITE, button_x)
        pygame.draw.rect(screen, WHITE, button_o)
        pygame.draw.rect(screen, WHITE, button_random)

        text_x = font.render("X", True, BLACK)
        text_o = font.render("O", True, BLACK)
        text_random = font.render("?", True, BLACK)

        screen.blit(text_x, (button_x.x + 40, button_x.y + 10))
        screen.blit(text_o, (button_o.x + 40, button_o.y + 10))
        screen.blit(text_random, (button_random.x + 40, button_random.y + 10))

        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos

                    if button_x.collidepoint(mouse_pos):
                        return PLAYER_X
                    elif button_o.collidepoint(mouse_pos):
                        return PLAYER_O
                    elif button_random.collidepoint(mouse_pos):
                        return PLAYER_X

    def select_options_screen():
        screen.fill(BLACK)
        font = pygame.font.SysFont(None, 50)
        text = font.render("Selecciona una opción:", True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        screen.blit(text, text_rect)

        button_new_game = pygame.Rect(150, 300, 300, 50)
        button_exit = pygame.Rect(150, 400, 300, 50)

        pygame.draw.rect(screen, WHITE, button_new_game)
        pygame.draw.rect(screen, WHITE, button_exit)

        text_new_game = font.render("Nuevo Juego", True, BLACK)
        text_exit = font.render("Salir", True, BLACK)

        screen.blit(text_new_game, (button_new_game.x + 40, button_new_game.y + 10))
        screen.blit(text_exit, (button_exit.x + 120, button_exit.y + 10))

        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos

                    if button_new_game.collidepoint(mouse_pos):
                        return True  # Indica que se seleccionó Nuevo Juego
                    elif button_exit.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()

    def select_mode_screen():
        screen.fill(BLACK)
        font = pygame.font.SysFont(None, 50)
        text = font.render("Selecciona el modo de juego:", True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        screen.blit(text, text_rect)

        button_vs_ia = pygame.Rect(150, 300, 300, 50)
        button_vs_player = pygame.Rect(150, 400, 300, 50)

        pygame.draw.rect(screen, WHITE, button_vs_ia)
        pygame.draw.rect(screen, WHITE, button_vs_player)

        text_vs_ia = font.render("vs IA", True, BLACK)
        text_vs_player = font.render("vs Jugador", True, BLACK)

        screen.blit(text_vs_ia, (button_vs_ia.x + 120, button_vs_ia.y + 10))
        screen.blit(text_vs_player, (button_vs_player.x + 60, button_vs_player.y + 10))

        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos

                    if button_vs_ia.collidepoint(mouse_pos):
                        return True  # Indica que se seleccionó vs IA
                    elif button_vs_player.collidepoint(mouse_pos):
                        return False  # Indica que se seleccionó vs Jugador

    # Estado inicial del tablero
    S = [['' for _ in range(3)] for _ in range(3)]

    # Mostrar la pantalla de opciones
    if select_options_screen():  # Si se seleccionó Nuevo Juego
        # Mostrar la pantalla de selección de modo
        vs_ia_mode = select_mode_screen()
        # Mostrar la pantalla de selección de jugador
        selected_symbol = select_player_screen()

        # Determinar quién empieza la partida
        current_symbol = current_player(S, selected_symbol)

        # Dibujar el tablero vacío antes de entrar en el bucle principal
        screen.fill(BLACK)
        draw_board()
        pygame.display.update()

    # Bucle principal del juego
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()
                clicked_row = mouseY // SQUARE_SIZE
                clicked_col = mouseX // SQUARE_SIZE
                
                handle_click(clicked_row, clicked_col, current_symbol)
                current_symbol = current_player(S, selected_symbol)  # Cambiar al siguiente jugador si es necesario







    else:
        pygame.quit()
        sys.exit()
