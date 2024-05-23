
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
        
        
        ########################################################
        
def alpha_beta_search(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over() != "Game not over":
        return evaluate_board(board)  # Bewertungsfunktion für die aktuelle Brettstellung

    if maximizing_player:
        value = float('-inf')
        for move in board.get_legal_moves_list():  # Alle möglichen Züge
            board.apply_move(move)
            value = max(value, alpha_beta_search(board, depth - 1, alpha, beta, False))
            board.undo_move()  # Zug rückgängig machen
            alpha = max(alpha, value)
            if alpha >= beta:
                break  # Beta-Cutoff
        return value
    else:  # Minimizing player
        value = float('inf')
        for move in board.get_legal_moves_list():
            board.apply_move(move)
            value = min(value, alpha_beta_search(board, depth - 1, alpha, beta, True))
            board.undo_move()
            beta = min(beta, value)
            if alpha >= beta:
                break  # Alpha-Cutoff
        return value


def find_best_move(board, max_depth):
    best_move = None
    for depth in range(max_depth + 1):
        best_move = alpha_beta_search(board, depth, float('-inf'), float('inf'), True)
        # ... (Potenziell hier den besten Zug speichern)
    return best_move 


#########################################

    def alphabeta(self, alpha: float, beta, max_player: bool, depth: int, max_depth:int):
        if depth == 0 or self.board.is_game_over() != "Game not over":
            return self.get_score()
    
        # parse move_categories
        #selected_categories = self.board.parse_move_categories(self.board.move_categories, self.board.move_categories_dict)
        # get legal moves
        #selected_legal_moves = board.get_legal_moves(selected_categories, turn)
        # select random move
        #next_move = board.select_random_move(selected_legal_moves)
        #self.board.selected_categories = 
        #self.board.selected_legal_moves = self.board.get_legal_moves(selected_categories, turn)
        #legal_moves_list = self.board.get_legal_moves
        
        #------ hash------
        board_hash = hash(state)  # Eindeutige Darstellung des Zustands
        if board_hash in transposition_table:
            trans_table_entry = transpositional_table[board_hash]
            if trans_table_entry["depth"] >= depth:
                return trans_table_entry[board_hash]
        #-----------------
        
        legal_moves_list = []
    
        if max_player: #if its our turn
            alphabeta_move = None
            alphabeta_value = float('-inf')
            # get children of game-tree
            
            #for move in self.board.get_legal_moves_list(["Singles", "Doubles"], "Blue").values():
            
            #generate list/dictionairy of legal moves to chose from
            for move in self.board.get_all_legal_moves(self.board, self.color):
                #chose the next move from list
                next_move = move
                # apply move
                from_square, to_square = next_move.upper().split('-')
                from_coordinate = Coordinate[from_square]
                to_coordinate = Coordinate[to_square]
                move = Move(player=turn.color, fromm=from_coordinate, to=to_coordinate)
                response = board.apply_move(move)
                # self.board.undo_move()
                # move one depth further and set max_player to false
                value = self.get_score()
                
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
