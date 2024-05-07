class MinimaxAlphaBetaAgent:
    def __init__(self):
        return
    
    def get_all_next_moves(self, state):
        moves = []
        for row in state.empty_tiles():
            for tile in row:
                moves.append(tile)
        
        return moves