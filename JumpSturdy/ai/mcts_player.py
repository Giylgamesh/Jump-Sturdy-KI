import random
import math
import time
from collections import deque
from JumpSturdy.game_state.board import Board, Coordinate, Move

def reverse_move_string(move):
    positions = move.split('-')
    reversed_move = positions[1] + '-' + positions[0]
    return reversed_move

class MCTSNode:
    def __init__(self, color, board: Board, parent=None):
        self.board = board
        self.parent = parent
        self.children = []
        self.wins = 0
        self.visits = 0
        self.color = color

    def is_fully_expanded(self):
        return len(self.children) == len(list(self.board.get_legal_moves_list(self.board.get_all_legal_moves(self.color))))

    def best_child(self, exploration_weight=1.41):
        choices_weights = [
            (child.wins / child.visits) + exploration_weight * math.sqrt((2 * math.log(self.visits) / child.visits))
            for child in self.children
        ]
        return self.children[choices_weights.index(max(choices_weights))]

    def expand(self):
        if self.is_fully_expanded():
            return None
        legal_moves = self.board.get_legal_moves_list(self.board.get_all_legal_moves(self.color))
        for move in legal_moves:
            if not any(child.board == self.board for child in self.children):
                new_board = self.board.copy_board()
                from_square, to_square = move.upper().split('-')
                from_coordinate = Coordinate[from_square]
                to_coordinate = Coordinate[to_square]
                move_class = Move(self.color, fromm=from_coordinate, to=to_coordinate)
                new_board.apply_move(move_class)
                new_node = MCTSNode(new_board, parent=self)
                self.children.append(new_node)
                return new_node

    def backpropagate(self, result):
        self.visits += 1
        self.wins += result
        if self.parent:
            self.parent.backpropagate(result)

class MCTSPlayer:
    """Our Monte Carlo Tree Search Player class. It includes all the actions the AI Player 
    needs to play the game.
    """
    def __init__(self, color, board:Board, time, turn):
        # Initialize AI components
        self.color = color
        self.board = board
        self.time = time
        self.turn = turn

    def simulate(self):
        last_position = ""
        copy_board = self.board.copy_board()
        color = self.color
        while not copy_board.is_game_over()[0]:
            random_move = random.choice(copy_board.get_legal_moves_list(copy_board.get_all_legal_moves(color)))
            if random_move != last_position:
                from_square, to_square = random_move.upper().split('-')
                from_coordinate = Coordinate[from_square]
                to_coordinate = Coordinate[to_square]
                move = Move(color, fromm=from_coordinate, to=to_coordinate)
                copy_board.apply_move(move)
                last_position = reverse_move_string(random_move)
                if color == "Blue":
                    color = "Red"
                else:
                    color = "Blue"
                copy_board.print_board()
        if copy_board.is_game_over()[1] == self.color:
            return 1
        else:
            return 0


    def get_random_move(self):
        """
        Generates a random move for the player

        Returns:
            Move: "move" object representing the randomly generated move
        """
        posible_moves = self.board.get_legal_moves_list(self.board.get_legal_moves(self.board.get_legal_moves(
            {'singles_left_empty': True, 'singles_front_empty': True, 'singles_right_empty': True,
                'singles_kill_left_singles': True, 'singles_kill_left_doubles': True, 'singles_kill_right_singles': True,
                'singles_kill_right_doubles': True, 'singles_upgrade_left': True, 'singles_upgrade_front': True,
                'singles_upgrade_right': True, 'doubles_l_l_f_empty': True, 'doubles_f_f_l_empty': True,
                'doubles_f_f_r_empty': True, 'doubles_r_r_f_empty': True, 'doubles_kill_l_l_f_singles': True,
                'doubles_kill_l_l_f_doubles': True, 'doubles_kill_f_f_l_singles': True, 'doubles_kill_f_f_l_doubles': True,
                'doubles_kill_f_f_r_singles': True, 'doubles_kill_f_f_r_doubles': True, 'doubles_kill_r_r_f_singles': True,
                'doubles_kill_r_r_f_doubles': True, 'doubles_l_l_f_singles': True, 'doubles_f_f_l_singles': True,
                'doubles_f_f_r_singles': True, 'doubles_r_r_f_singles': True}, self.color), self.color))
        random_index = random.randrange(0, len(posible_moves), 1)
        move = posible_moves[random_index]
        return move
    
    def mcts(self, simulations=1000):
        root = MCTSNode(self.color, self.board)
        for _ in range(simulations):
            node = root
            # Selection
            while node.is_fully_expanded() and node.children:
                node = node.best_child()
            # Expansion
            new_node = node.expand()
            if new_node is None:
                new_node = node
            # Simulation
            result = self.simulate()
            # Backpropagation
            new_node.backpropagate(result)
        return root.best_child(exploration_weight=0).board.lastMove

def main():
    """
    This is the main method that sets up the game board and players, 
    and then simulates a game between two AI players. Here we give the board a FEN-String to generate the initial board state.
    This allows us to start the game from any state (e.g. Game-start, early-game, mid-game, late-game)
    """
    board = Board()
    board.initialize()
    aiplayer = MCTSPlayer("Blue",board,12000,0)
    print(aiplayer.simulate())
    print(aiplayer.mcts(1000))

if __name__ == "__main__":
    main()
