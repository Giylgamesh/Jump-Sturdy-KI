import Nodes_JumpSturdy
import game_state.board

class GameTree:
    def __init__(self, board, current_player, depth):
        self.board = board
        self.current_player = current_player
        self.seed = self.build_tree(self.board, self.current_player, depth = 0)
        self.children = []

    def build_tree(self, board, current_player, depth):
        node = Nodes_JumpSturdy(board, current_player, 0)
        for moves in legal_moves_array:
            child = node.
    
    def add_child(self, child):
        self.children.append(child)

    def get_children(self):
        return self.children

    def get_state(self):
        return self.state

    def is_terminal(self):
        return len(self.children) == 0