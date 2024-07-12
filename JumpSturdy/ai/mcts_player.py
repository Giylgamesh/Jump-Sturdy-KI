import random
import math
import time
from JumpSturdy.ai.evolved_player import EvolvedAIPlayer
from JumpSturdy.game_state.board import Board, Coordinate, Move

def reverse_move_string(move):
    positions = move.split('-')
    reversed_move = positions[1] + '-' + positions[0]
    return reversed_move

class MCTSNode:
    """
    Initialization of the move of this node, the parent node, the children of this node, 
    number of simulations won and number of simulations under this node
    """
    def __init__(self, move:Move, parent):
        self.move = move
        self.parent = parent
        self.children = {}
        self.wins = 0
        self.visits = 0
    
    """
    Add the children in this node. 
    Generates children nodes based on the available train options.
    """
    def add_children(self, children:dict) -> None:
        for child in children:
            self.children[child.move] = child

    """
    Indicates the value of the node based on the Upper Confidence bound (UCT). 
    """
    def value(self, explore: float = math.sqrt(2)):
        if self.visits == 0:
            return 0 if explore == 0 else float('inf')
        else:
            return self.wins/self.visits + explore + math.sqrt(math.log(self.parent.visits)/self.visits)

class Player:
    """Our Monte Carlo Tree Search Player class. It includes all the actions the MCTS 
    needs to play the game.
    """
    def __init__(self, color, board:Board, time, turn):
        self.color = color
        self.board = board
        self.time = time
        self.turn = turn

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

class MCTS:
    def __init__(self, player:Player):
        self.player = player
        self.copy_board = player.board.copy_board()
        self.root = MCTSNode(None, None)
        self.run_time = 0
        self.node_count = 0
        self.amount_simulation = 0


    def select(self) -> tuple:
        node = self.root
        board = self.copy_board.copy_board()

        while len(node.children) != 0:
            children = node.children.values()
            max_value = float('-inf')
            for child in children:
                value = child.value()

                if value > max_value:
                    max_value = value

            max_nodes = []
            for child in children:
                if child.value() == max_value:
                    max_nodes.append(child)

            node = random.choice(max_nodes)
            board.apply_move(node.move)

            if node.visits == 0:
                return node, board

        if self.generate(node, board):
            node = random.choice(list(node.children.values()))
            board.apply_move(node.move)
        return node, board
    
    def generate(self, parent: MCTSNode, board: Board) -> bool:
        if board.is_game_over()[0]:
            return False
        children = []
        for move in board.get_legal_moves_list(board.get_all_legal_moves(self.player.color)):
            from_square, to_square = move.split('-')
            from_coordinate = Coordinate[from_square]
            to_coordinate = Coordinate[to_square]
            converted_move = Move(self.player.color, fromm=from_coordinate, to=to_coordinate)
            child_node = MCTSNode(converted_move, parent)
            children.append(child_node)
        parent.add_children(children)
        return True

    def simulate(self, board: Board) -> int:
        turn = 0
        while not board.is_game_over()[0]:
            if turn%2==0:
                if self.player.color == "Blue":
                    move = random.choice(board.get_legal_moves_list(board.get_all_legal_moves("Blue")))
                else:
                    move = random.choice(board.get_legal_moves_list(board.get_all_legal_moves("Red")))
                from_square, to_square = move.upper().split('-')
                from_coordinate = Coordinate[from_square]
                to_coordinate = Coordinate[to_square]
                converted_move =  Move(self.player.color, fromm=from_coordinate, to=to_coordinate)
                board.apply_move(converted_move)
            else:
                if self.player.color == "Red":
                    move = random.choice(board.get_legal_moves_list(board.get_all_legal_moves("Red")))
                else:
                    move = random.choice(board.get_legal_moves_list(board.get_all_legal_moves("Blue")))
                from_square, to_square = move.upper().split('-')
                from_coordinate = Coordinate[from_square]
                to_coordinate = Coordinate[to_square]
                converted_move =  Move(self.player.color, fromm=from_coordinate, to=to_coordinate)
                board.apply_move(converted_move)
        return board.is_game_over()[1]

    def back_propagate(self, node: MCTSNode, color: str, winner: str) -> None:
        reward = 1 if winner == color else 0
        while node is not None:
            node.visits += 1
            node.wins += reward
            node = node.parent
            reward = 1 - reward

    def search(self, time_limit: int):
        start_time = time.time()

        amount_simulation = 0
        while time.time() - start_time < time_limit:
            node, board = self.select()
            outcome = self.simulate(board)
            self.back_propagate(node, self.player.color, outcome)
            amount_simulation += 1 

        run_time = time.time() - start_time
        self.run_time = run_time
        self.amount_simulation = amount_simulation

    def best_move(self):
        if self.copy_board.is_game_over()[0]:
            return -1

        max_visits = float('-inf')
        for child in self.root.children.values():
            if child.visits > max_visits:
                max_visits = child.visits
        max_nodes = []
        for child in self.root.children.values():
            if child.visits == max_visits:
                max_nodes.append(child)
        return random.choice(max_nodes).move

    def move(self, move):
        if move in self.root.children:
            self.copy_board.apply_move(move)
            self.root = self.root.children[move]
            return

        self.copy_board.apply_move(move)
        self.root = MCTSNode(None, None)

    def statistics(self) -> tuple:
        return self.amount_simulation, self.run_time

def main():
    """
    This is the main method that sets up the game board and players, 
    and then simulates a game between two AI players. Here we give the board a FEN-String to generate the initial board state.
    This allows us to start the game from any state (e.g. Game-start, early-game, mid-game, late-game)
    """
    board = Board()
    board.initialize()
    player = Player("Blue", board, 120000,0)
    mcts = MCTS(player)
    evolvedAIPlayer = EvolvedAIPlayer("Red",board,120000,0,{'bias': 1, 'friendly_singles_value': 0.7341041163830963, 'friendly_doubles_value': 2.274233660960818, 'friendly_material_score': 1.5026103652388332, 'enemy_singles_value': -0.7291608705251027, 'enemy_doubles_value': -2.265430977891856, 'enemy_material_score': -1.5074077330290985, 'friendly_most_advanced_singles': 0.748247621491522, 'friendly_most_advanced_doubles': 1.515407356131302, 'enemy_most_advanced_singles': -1.510285668824605, 'enemy_most_advanced_doubles': -1.50961031645031, 'friendly_advancement_of_singles': 3.7785644200333097, 'friendly_advancement_of_doubles': 3.728760057392521, 'enemy_advancement_of_singles': -1.4892627538963819, 'enemy_advancement_of_doubles': -1.5077596634911712, 'control_of_center': 1.488164124061923, 'control_of_edges': 1.4856870496218675, 'friendly_single_in_edges': 2.2544290664740716, 'friendly_double_in_edges': 0.7380353065066093, 'friendly_single_in_center': 1.504606566797584, 'friendly_double_in_center': 1.506622449400612, 'enemy_single_in_edges': -2.2586791963463746, 'enemy_double_in_edges': -0.7524670320911624, 'enemy_single_in_center': -1.49559265658973, 'enemy_double_in_center': -0.7445612570569379, 'friendly_double_in_back_corner': -0.7563267575338303, 'friendly_doubles_in_line': 2.9624074414727244, 'friendly_single_double_in_line': 3.7508566377756627, 'friendly_singles_in_line': 0.7524614046343802, 'friendly_piece_is_last': 14.910873615920098, 'friendly_density': 2.2578436465288503, 'friendly_mobility': 0.7504994504492232, 'enemy_density': -0.7497067955526692, 'enemy_mobility': -2.2321338830066946, 'friendly_single_under_attack': -2.9762775175952796, 'friendly_double_under_attack': -2.9890296486546855})

    while not board.is_game_over()[0]:
        print("Current board:")
        board.print_board()

        evolved_move = evolvedAIPlayer.get_best_move_through_time()

        from_square, to_square = evolved_move.upper().split('-')
        from_coordinate = Coordinate[from_square]
        to_coordinate = Coordinate[to_square]
        move = Move(evolvedAIPlayer.color, fromm=from_coordinate, to=to_coordinate)
        board.apply_move(move)
        mcts.move(move)

        board.print_board()

        if board.is_game_over()[1]=="Red":
            print("Red Player won!")
            break

        print("Thinking...")

        mcts.search(5)
        amount_simulation, run_time = mcts.statistics()
        print("Statistics: ", amount_simulation, "rollouts in", run_time, "seconds")
        move = mcts.best_move()

        print("MCTS chose move: ", move)

        board.apply_move(move)
        mcts.move(move)

        if board.is_game_over()[1]=="Blue":
            print("Blue won!")
            break


if __name__ == "__main__":
    main()
