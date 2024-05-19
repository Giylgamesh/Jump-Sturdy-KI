
    def alphabeta(self, alpha: float, beta, max_player: bool, depth: int, max_depth:int):
        if depth == 0 or self.is_game_over() != "Game not over":
            return self.get_score()


        if max_player: #if its our turn
            value = -float('inf')
            # get children of game-tree
            for move in self.get_legal_moves(["Singles", "Doubles"], "Blue").values():
                # move one depth further and set max_player to false
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
                if beta >= alpha:
                    break  
            return value
    
    ##########################################
    
    def alphabeta(self, alpha: float, beta, max_player: bool, depth: int, max_depth:int):
        if depth == 0 or self.board.is_game_over() != "Game not over":
            return self.get_score()
        
        if max_player: #if its our turn
            alphabeta_move = None
            alphabeta_value = float('-inf')
            # get children of game-tree
            
            for move in self.board.get_legal_moves_list(["Singles", "Doubles"], "Blue").values():
                # move one depth further and set max_player to false
                value = move.alphabeta(self, alpha, beta, False, depth + 1, max_depth)
                if value > alphabeta_value:
                    alphabeta_value = value
                    alphabeta_move = move
                alpha = max(alpha, alphabeta_value) 
                # beta cutof because beta value is too low to continue searching
                if alpha >= beta:
                    break  
            return alphabeta_value, alphabeta_move
        else:
            alphabeta_move = None
            alphabeta_value = float('inf')
            # get children of game-tree
            for move in self.board.get_legal_moves(["Singles", "Doubles"], "Blue").values():
                # move one depth further and set max_player to false
                value = move.alphabeta(self, alpha, beta, True, depth + 1, max_depth)
                if value > alphabeta_value:
                    alphabeta_value = value
                    alphabeta_move = move
                alpha = min(beta, alphabeta_value) 
                # alpha cutof 
                if beta >= alpha:
                    break  
            return alphabeta_value, alphabeta_move