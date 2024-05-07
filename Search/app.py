"""
Tic Tac Toe Player
"""

import random

import math

X = "X"
O = "O"
E = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[E, E, E],
            [E, E, E],
            [E, E, E]]


def player(board):
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

    #return 'A'
    #raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    action = []

    for i, row in enumerate(board):
      for j, col in enumerate(row):
        if col == E:
          action.append((i, j))

    return action
    #raise NotImplementedError

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    current = player(board)

    i, j = action

    board[i][j] = current

    return board
    #raise NotImplementedError

def winner(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != E:  # Check rows
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != E:  # Check columns
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != E:  # Check diagonal
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != E:  # Check diagonal
        return board[0][2]
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    for i in range(len(board)):
        if (board[i][0] == board[i][1] == board[i][2] != E) or (board[0][i] == board[1][i] == board[2][i] != E):
            return True

    if (board[0][0] == board[1][1] == board[2][2] != E) or (board[2][0] == board[1][1] == board[0][2] != E):
        return True

    return not any(col == None for row in board for col in row)
    #raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    for i in range(len(board)):
        if board[i][0] == board[i][1] == board[i][2] != E: #row
            return 1 if board[i][0] == X else -1

        if board[0][i] == board[1][i] == board[2][i] != E: #col
            return -1 if board[0][i] == O else 1

    if board[0][0] == board[1][1] == board[2][2] != E: #diagonal principal
        return 1 if board[1][1] == X else -1

    if board[2][0] == board[1][1] == board[0][2] != E: #diagonal secundaria
        return -1 if board[1][1] == O else 1

    return 0
    #raise NotImplementedError


def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or terminal(board):
        return utility(board)

    if maximizing_player:
        value = -float('inf')
        copy_board = [row[:] for row in board]
        for action in actions(board):
            value = max(value, minimax(result(copy_board, action), depth - 1, alpha, beta, False))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value
    else:
        value = float('inf')
        copy_board = [row[:] for row in board]
        for action in actions(board):
            value = min(value, minimax(result(copy_board, action), depth - 1, alpha, beta, True))
            beta = min(beta, value)
            if beta <= alpha:
                break
        return value

def best_move(board):
    best_score = -float('inf')
    best_move = None
    alpha = -float('inf')
    beta = float('inf')

    for action in actions(board):
        copy_board = [row[:] for row in board]  # Make a copy of the board for each action
        score = minimax(result(copy_board, action), depth=100, alpha=alpha, beta=beta, maximizing_player=False)
        if score > best_score:
            best_score = score
            best_move = action
        alpha = min(alpha, best_score)

    return best_move


def print_board(board):
    for row in board:
        for col in row:
            if col == X:
                print('X', end=' ')
            if col == O:
                print('O',end=' ')
            if col == E:
                print('E', end=' ')
        print()

s0 = initial_state()


s0 = initial_state()

while True:
    print_board(s0)
    if player(s0) == X:  # Jugador humano
        x = int(input('i: '))
        y = int(input('j: '))
        if s0[x][y] is E:
            s0[x][y] = X
        else:
            continue
    else:  # Jugador de IA
        i, j = best_move(s0)
        s0[i][j] = O

    if terminal(s0):
        print_board(s0)
        winner_name = winner(s0)
        if winner_name:
            print(f'¡El jugador {winner_name} ha ganado!')
        else:
            print('¡Empate!')
        break



