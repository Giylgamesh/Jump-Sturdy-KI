from game_state.board import Board

# depth is an index that will be increased with each recursion, if we choose to recurse
# max_depth will determine how often the recursion will happen
def alphabeta(self, alpha, beta, max_player, depth, max_depth):
    #if depth == 0 or self.is_game_over() != "Game not over":
    game_over = self.is_game_over()
    if game_over or depth == 0:
        return self.get_score()

    if max_player:
        value = -float('inf')
        # get children of game-tree
        for move in self.get_legal_moves(["Singles", "Doubles"], "Blue").values():
            value = max(value, move.alphabeta(alpha, beta, False, depth + 1, max_depth))
            alpha = max(alpha, value)
            # beta cutof because beta value is too low to continue searching
            if alpha >= beta:
                break  
        return value
    else:
        value = float('inf')
        for move in self.get_legal_moves(["Singles", "Doubles"], "Red").values():
            value = min(value, move.alphabeta(alpha, beta, True, depth + 1, max_depth))
            beta = min(beta, value)
            # alpha cutoff
            if beta <= alpha:
                break  
        return value
    
    #------- how to call this method:
    # board = Board() 
    # result_alphabeta = board.alphabeta(float('-inf'), float('inf'), True, 0, 3)
    # ----------max_depth = 3 in this case
    