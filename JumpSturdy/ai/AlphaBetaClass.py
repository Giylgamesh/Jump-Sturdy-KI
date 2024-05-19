import GameTree
import game_state.board
import JumpSturdy.ai.JumpSturdyNode as JumpSturdyNode

class AlphaBeta:
    def __init__(self, evaluate):
        # function, that sets value to a node
        self.evaluate = evaluate

    # search method for a game tree. Node will be the bitboard of the current state 
    # Depth is how far we are in the game tree
    def search(self, node, depth):
        # we use strings instead of very big numbers for alpas and betas initial value
        alpha = float("-inf")
        beta = float("inf")
        return self.alphabeta(node, depth, alpha, beta, True)

    # Recursive function for alpha-beta pruning.
    def alphabeta(self, node, depth, alpha, beta, is_maximizing):
        """
        Args:
            node: Current node/Birboard in Game Tree
            depth: current depth in Game tree
            alpha: best value for max player so far
            beta: best value for min player so far
            is_maximizing: if True, than max playrs turn 
        Returns:
            score of best move for current Player
        """

        # Base case: Terminal node (leaf node) or maximum depth reached
        # is_terminal returns boolean. is_terminal = 1, node is terminal
        # if node is terminal, we propagate values upwards 
        if depth == 0 or self.is_terminal(node):
            return self.evaluate(node)

        if is_maximizing:
        # max player find the move with the highest score
            best_score = float('-inf')
            for child in get_children(node):
                score = self.alphabeta(child, depth - 1, alpha, beta, False)
                best_score = max(best_score, score)
                alpha = max(alpha, best_score)
                # beta cut off, if min player would propagate lower value, than max has alpha value 
                if beta <= alpha:
                    break 
            return best_score

        else:
        # min player find the move with the lowest score
            best_score = float('inf')
            for child in GameTree.get_children(node):
                score = self.alphabeta(child, depth - 1, alpha, beta, True)
                best_score = min(best_score, score)
                beta = min(beta, best_score) 
                # alpha cut off
                if alpha >= beta:
                    break
            return best_score


    def is_terminal(self, node):
        return node.check_temrinal()
    
       
        # creates a list of children for current node
    def get_children(self, node):
        children = []
        possible_moves = node.generate_moves(node)
        for move in possible_moves:
            child = node.aply_move(node, move)
            children.append(child)
        return children

# Example call
root_node = ...  # Initialize your game state representation
depth = 3  # Desired search depth
alphabeta = AlphaBeta(evaluate)
best_score = alphabeta.search(root_node, depth)
print(f"Best score for maximizing player: {best_score}")
