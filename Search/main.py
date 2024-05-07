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
    """
    Returns the winner of the game, if there is one.
    """
    return terminal(board)
    #raise NotImplementedError

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    for i in range(len(board)):
        if (board[i][0] == board[i][1] == board[i][2] != E) or (board[0][i] == board[1][i] == board[2][i] != E):
            return True

    if (board[0][0] == board[1][1] == board[2][2] != E) or (board[2][0] == board[1][1] == board[0][2] != E):
        return True

    #return not any(col == None for row in board for col in row)
    return not any (E in row for row in board)
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


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return utility(board)

    if player(board) == X:
        value = -float('inf')
        copy_board = [row[:] for row in board]
        for action in actions(copy_board):
            value = max(value, minimax(result(copy_board, action)))

    else:
        value = float('inf')
        copy_board = [row[:] for row in board]
        for action in actions(copy_board):
            value = min(value, minimax(result(copy_board, action)))

    return value

    #raise NotImplementedError

def games(board):
    game = []
    if not terminal(board):
        for action in actions(board):
            copy_board = [row[:] for row in board]
            game.append((minimax(result(copy_board, action)), action))
        return min(game, key=lambda x: x[0])

def minimax2(board):
    """
    Returns the optimal action for the current player on the board.

    'X' Player is trying to maximise the score, 'O' Player is trying to minimise it
    """

    global actions_explored
    actions_explored = 0

    def max_player(board, best_min = 20):
      """ Helper function to maximise score for 'X' player.
          Uses alpha-beta pruning to reduce the state space explored.
          best_min is the best result
      """

      global actions_explored

      # If the game is over, return board value
      if terminal(board):
        return (utility(board), None)

      # Else pick the action giving the max value when min_player plays optimally
      value = -10
      best_action = None


      # Get set of actions and then select a random one until list is empty:
      action_set = actions(board)

      while len(action_set) > 0:
        action = random.choice(tuple(action_set))
        action_set.remove(action)

        # A-B Pruning skips calls to min_player if lower result already found:
        if best_min <= value:
          break

        actions_explored += 1
        min_player_result = min_player(result(board, action), value)
        if min_player_result[0] > value:
          best_action = action
          value = min_player_result[0]

      return (value, best_action)


    def min_player(board, best_max = -2):
      """ Helper function to minimise score for 'O' player """

      global actions_explored

      # If the game is over, return board value
      if terminal(board):
        return (utility(board), None)

      # Else pick the action giving the min value when max_player plays optimally
      value = 10
      best_action = None

      # Get set of actions and then select a random one until list is empty:
      action_set = actions(board)

      while len(action_set) > 0:
        action = random.choice(tuple(action_set))
        action_set.remove(action)

        # A-B Pruning skips calls to max_player if higher result already found:
        if best_max >= value:
          break

        actions_explored += 1
        max_player_result = max_player(result(board, action), value)
        if max_player_result[0] < value:
          best_action = action
          value = max_player_result[0]

      return (value, best_action)


    # If the board is terminal, return None:
    if terminal(board):
      return None
    if player(board) == 'X':
      print('AI is exploring possible actions...')
      best_move = max_player(board)[1]
      print('Actions explored by AI: ', actions_explored)
      return best_move
    else:
      print('AI is exploring possible actions...')
      best_move = min_player(board)[1]
      print('Actions explored by AI: ', actions_explored)
      return best_move

def miniTem(board):
   copy = [row[:] for row in board]
   i, j = minimax2(copy)
   return (i, j)
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

while not terminal(s0):
    print_board(s0)
    if player(s0) == X:
        x = int(input('i: '))
        y = int(input('j: '))
        s0[x][y] = X
    else:
        i, j = miniTem(s0)
        s0[i][j] = O