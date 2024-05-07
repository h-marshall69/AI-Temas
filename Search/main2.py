import math

X = "X"
O = "O"
E = None

current_player = X

def initial_state():
    return [[E for _ in range(3)] for _ in range(3)]

def actions(board):
    action = []

    for i, row in enumerate(board):
        for j, col in enumerate(row):
            if col == E:
                action.append([i, j])
    
    return action

def result(board, action):
    global current_player
    if current_player == X:
        current_player = O

    i, j = action

    board[i][j] = current_player

    return board

def winer(board):
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] != E:
            return True
        if board[i][0] == board[i][1] == board[i][2] != E:
            return True
    if board[0][0] == board[1][1] == board[2][2] != E:
        return True
    if board[2][0] == board[1][1] == board[0][2] != E:
        return True
    return False

def draw(board):
    for row in board:
        if E in row:
            return False
    return True

def terminal(board):
    return True if (winer(board) or draw(board)) else False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != E: #row
            return 1 if board[i][0] == X else -1

        if board[0][i] == board[1][i] == board[2][i] != E: #col
            return -1 if board[0][i] == O else 1

    if board[0][0] == board[1][1] == board[2][2] != E: #diagonal principal
        return 1 if board[1][1] == X else -1

    if board[2][0] == board[1][1] == board[0][2] != E: #diagonal secundaria
        return -1 if board[1][1] == O else 1

    return 0



def player(board):
    count_X = 0
    count_O = 0
    for row in board:
        count_X += row.count(X)
        count_O += row.count(O)

    return O if count_O < count_X else X



def minimax(board):
    copy_board = [row[:] for row in board]
    if terminal(board):
        return utility(board)

    if player(board) == X:
        value = -float('inf')
        for action in actions(board):

            value = max(value, minimax(result(copy_board, action)))

    else:
        value = float('inf')
        for action in actions(copy_board):
            value = min(value, minimax(result(copy_board, action)))

    return value

    #raise NotImplementedError

def games(board):
    game = []
    if not terminal(board):
        if player(board) == X:
            for action in actions(board):
                copy_board = [row[:] for row in board]
                game.append((minimax(result(copy_board, action)), action))

            #max_state = max(game, key=lambda x: x[0])[0]
            #game_max = [tupla for tupla in game if tupla[0] == max_state]
            #return random.choice(game_max)
            return max(game, key=lambda x: x[0])
        else:
            for action in actions(board):
                copy_board = [row[:] for row in board]
                game.append((minimax(result(copy_board, action)), action))

            #min_state = min(game, key=lambda x: x[0])[0]
            #game_min = [tupla for tupla in game if tupla[0] == min_state]
            #return random.choice(game_min)
            return min(game, key=lambda x: x[0])

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

s1 = [
    [X, O, X],
    [O, X, O],
    [O, X, E]
]

while not terminal(s0):
    print_board(s0)
    if player(s0) == X:
        x = int(input('i: '))
        y = int(input('j: '))
        s0[x][y] = X
    else:
        i, j = games(s0)[1]
        s0[i][j] = O