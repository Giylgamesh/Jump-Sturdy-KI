import JumpSturdy.ai.JumpSturdyNode as JumpSturdyNode
import JumpSturdy.game_state.board as board


class GameTree:
    def __init__(self, board, current_player, depth):
        self.board = board
        self.current_player = current_player
        self.seed = self.build_tree(self.board, self.current_player, depth = 0)
        self.children = []

    def build_tree(self, board, depth):
        node = JumpSturdyNode.JumpSturdyNode(board, 0)
        if depth == 0 or node.is_terminal():
            return node
        
        # I dont know
        
        legal_moves = node.get_legal_moves()
        for move in legal_moves:
            new_board = node.get_state().make_move(move)
            child = self.build_tree(new_board, depth - 1)
            node.add_child(child)
        
        return node
    
    def add_child(self, child):
        self.children.append(child)
        return self.add_child

    def get_children(self):
        return self.children

    def get_state(self):
        return self.state

    def is_terminal(self):
        return len(self.children) == 0