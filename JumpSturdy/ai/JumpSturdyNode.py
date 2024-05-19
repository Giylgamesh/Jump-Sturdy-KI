from game_state import board

# all nodes in our Game Tree will be classes with their own values but the same attributes
# this makes it easier for us to adjust something later in th e process
class JumpSturdyNode:

    def __init__(self, board, current_player, parent=None):
        self.board = board
        self.current_player = current_player
        self.parent = parent
        self.is_terminal = self.check_terminal()

    # here we check if the node is terminal (a leaf). The node is terminal if
    # the game has ended in that node. The possibilities are, that one
    # of the players has reached the end of the board, or killed all 
    # pieces of the enemy
    def check_terminal(self):
        # checks if is_game_over() method returns the "Game not over" message. If True, we negate message to be False
        # indicating, that node is NOT terminal. Our is_game_over() method is implemented in such a way, that it's easier to
        # do it like this, because the "game over" message also includes other information that i dont want to catch individually.
        game_over = self.is_game_over()
        return game_over != "Game not over" 

    
    def _get_children_from_piece(self, row, col):
        # Generates child nodes for a specific piece location.
        
        children = []
        new_board = self.board.copy()  # Create a copy to avoid modifying the original board [NOT DONE YET 18.05.2024] 
        new_board.move
        new_board[row][col] = None  # Remove the current piece from the new board
        children.append(JumpSturdyNode(new_board, self.get_opponent_color(), self))  # Single-square move placeholder
        # Returns: A list of JumpSturdyNode instances representing valid child nodes from this piece.   
        return children

    def get_opponent_color(self):
        if self.current_player == "BLUE":
            return "RED"
        else:
            return "BLUE"
