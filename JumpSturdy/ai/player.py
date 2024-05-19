import os
import random
import math
import time
from JumpSturdy.game_state.board import Board, Move, Coordinate

def value_iteration(blue_player, red_player, board, learning_rate=0.1, discount_factor=0.95):
    blue_player.weights = normalize_weights(blue_player.weights)
    total_i = 0
    total_e = 0
    N = 100

    for j in range(N):
        history, reward = simulate_game(board, blue_player, red_player)

        # Update weights based on the outcome
        next_value = 0
        # history[-1:-10:-2]
        # Iterating over the relevant history excluding the final game state
        for state, features, action, heuristic, player in history[-1:]:
            current_value = reward + discount_factor * next_value
            heuristic_error = current_value - heuristic
            print(f"heuristic error {heuristic_error}")
            total_e += heuristic_error

            # Update each feature weight based on the heuristic error
            for feature, value in features.items():
                print(f"feature {feature}, weight {value[0]}, contribution {value[1]}")
                if value[1] != 0:
                    gradient = value[1] / heuristic if heuristic != 0 else 1000000000
                    print(f"gradient {gradient}")

                    feature_error = gradient * heuristic_error
                    feature_good = value[1] + feature_error
                    print(f"feature error {feature_error}")
                    print(f"feature good {feature_good}")

                    weight_opt1 = 1 * feature_good * value[0] / value[1]
                    print(f"optimal weight {weight_opt1}")

                    blue_player.weights[feature] += (learning_rate * feature_error * value[0]) / value[1]
                    print(f"new weight {blue_player.weights[feature]}")
                    print()

            # Check if error got better
            new_heuristic, _ = blue_player.get_score()
            new_heuristic_error = current_value - new_heuristic
            print(f"new heuristic error {new_heuristic_error}")
            improvement = abs(heuristic_error) - abs(new_heuristic_error)
            print(f"improvement {improvement}")
            total_i += improvement
            print("------------")

            # Set new value for next iteration
            next_value = current_value

        blue_player.weights = normalize_weights(blue_player.weights)
    print(f"total {total_i}")
    print(f"avg: {total_e / N}")

    # Return updated weights at the end
    return blue_player.weights


def simulate_game(board, friendly_player, enemy_player):
    i = 0
    history = []  # To store state, action, reward
    friendly_player.weights = normalize_weights(friendly_player.weights)
    board.reset()

    while True:
        # Alternate turns between players
        turn = friendly_player if i % 2 == 0 else enemy_player
        i += 1

        # Get move
        next_move = turn.get_random_move()
        from_square, to_square = next_move.upper().split('-')
        from_coordinate = Coordinate[from_square]
        to_coordinate = Coordinate[to_square]
        next_move = Move(player=turn.color, fromm=from_coordinate, to=to_coordinate)

        # Print for debugging
        # board.print_board()
        # print(f"{turn.color} moves {from_square}-{to_square}")

        # Get heuristic value
        heuristic, features = friendly_player.get_score()

        # Store the state, action, reward tuple
        state = board.get_state()
        history.append((state, features, next_move, heuristic, turn))

        # Apply Move
        board.apply_move(next_move)

        # Check game status
        game_over = board.is_game_over()

        # Break if game is over
        if game_over != "Game not over":
            # Print for debugging
            # board.print_board()
            print(game_over)

            reward = 100 if "Blue wins" in game_over else 0

            # Get heuristic value
            heuristic, features = friendly_player.get_score()
            # Store the state, action, reward tuple
            state = board.get_state()
            history.append((state, features, next_move, heuristic, turn))

            # Reset board
            # board.reset()
            break

    return history, reward


def most_advanced_pieces(bitboard, friendly):
    """Find the row with the most advanced pieces (closest to the enemy side) in a single integer bitboard and count the '1's in it."""
    score = 0
    most_advanced_row = None

    # Find the row with the most advanced pieces
    if friendly:
        for row in range(7, -1, -1):
            if '1' in bitboard[row * 8:(row + 1) * 8]:
                most_advanced_row = row
                break
    else:
        for row in range(8):
            if '1' in bitboard[row * 8:(row + 1) * 8]:
                most_advanced_row = row
                break

    # Count the '1's in the most advanced row if it exists
    if most_advanced_row is not None:
        count = bitboard[most_advanced_row * 8:(most_advanced_row + 1) * 8].count('1')

        if friendly:
            score = count * (100 * (0.5 ** (7 - most_advanced_row)))
        else:
            score = count * (100 * (0.5 ** most_advanced_row))

    return score


def advancement_of_pieces(bitboard, friendly):
    """Calculate the total advancement score for all pieces on the bitboard."""
    total_advancement = 0

    if friendly:
        for i in range(64):
            if bitboard[i] == '1':
                row = i // 8
                total_advancement += 100 * (0.5 ** (7 - row))
    else:
        for i in range(64):
            if bitboard[i] == '1':
                row = i // 8
                total_advancement += 100 * (0.5 ** (row))

    return total_advancement


def piece_density(singles_binary, doubles_binary):
    """Calculate the piece density of the board."""
    positions = []
    total_distance = 0

    # Combine singles and doubles for total piece positions
    combined_binary = bin(int(singles_binary, 2) | int(doubles_binary, 2))[2:].zfill(64)

    for idx, value in enumerate(combined_binary):
        if value == '1':
            x, y = idx % 8, idx // 8  # Convert linear index to 2D coordinates
            positions.append((x, y))

    # Calculate the sum of distances between each pair of pieces
    for i in range(len(positions)):
        for j in range(i + 1, len(positions)):
            x1, y1 = positions[i]
            x2, y2 = positions[j]
            distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            total_distance += distance

    avg_distance = total_distance / len(positions)

    return avg_distance


def control_of_indices(weights, blue_singles_binary, blue_doubles_binary, red_singles_binary, red_doubles_binary,
                       center_indices):
    blue_singles_control = sum(
        weights["friendly_singles_value"] for idx in center_indices if blue_singles_binary[idx] == '1')
    blue_doubles_control = sum(
        weights["friendly_doubles_value"] for idx in center_indices if blue_doubles_binary[idx] == '1')
    red_singles_control = sum(
        weights["enemy_singles_value"] for idx in center_indices if red_singles_binary[idx] == '1')
    red_doubles_control = sum(
        weights["enemy_doubles_value"] for idx in center_indices if red_doubles_binary[idx] == '1')

    return blue_singles_control + blue_doubles_control + red_singles_control + red_doubles_control


def piece_on_indices(weights, friendly_type_binary, indices, type, friendly):
    # Initialize the control score
    edge_control_score = 0

    if any(friendly_type_binary[idx] == '1' for idx in indices):
        if friendly:
            edge_control_score = weights[f"friendly_{type}_value"]
        else:
            edge_control_score = weights[f"enemy_{type}_value"] * -1

    return edge_control_score


def piece_in_front(weights, first_bitboard, type1, second_bitboard, type2):
    """Check if the second bitboard has a piece in front of the first bitboard."""
    for i in range(56):
        if first_bitboard[i] == '1' and second_bitboard[i + 8] == '1':
            return weights[f"friendly_{type1}_value"] + weights[f"friendly_{type2}_value"]
    return 0

def piece_is_last(weights, friendly_sinlges, friendly_doubles, enemy_sinlges, enemy_doubles):
    # Find the furthest front/back friendly/enemy piece
    most_advanced_single_row = 0
    most_advanced_double_row = 0
    less_advanced_single_row = 8
    less_advanced_double_row = 8

    for row in range(7, -1, -1):
        if '1' in friendly_sinlges[row * 8:(row + 1) * 8]:
            most_advanced_single_row = row
            type = "singles"
            break
    for row in range(7, -1, -1):
        if '1' in friendly_doubles[row * 8:(row + 1) * 8]:
            most_advanced_double_row = row
            type = "doubles"
            break
    for row in range(7, -1, -1):
        if '1' in enemy_sinlges[row * 8:(row + 1) * 8]:
            less_advanced_single_row = row
            break
    for row in range(7, -1, -1):
        if '1' in enemy_doubles[row * 8:(row + 1) * 8]:
            less_advanced_double_row = row
            break

    friend = max(most_advanced_single_row, most_advanced_double_row)
    enemy = min(less_advanced_single_row, less_advanced_double_row)

    # Check if any friendly piece is beyond the furthest enemy piece
    if friend > enemy:
            return weights[f"friendly_{type}_value"] + friend
    return 0


def normalize_weights(weights):
    return weights
    total = sum(weights.values())
    if total != 0:
        normalized_weights = {k: v / total for k, v in weights.items()}
    else:
        normalized_weights = weights
    return normalized_weights


class AIPlayer:
    def __init__(self, color, board):
        # Initialize AI components
        self.color = color
        self.board = board

        self.weights = {
            "bias": 1,
            "friendly_singles_value": 1,
            "friendly_doubles_value": 3,
            "friendly_material_score": 1,
            "enemy_singles_value": -1,
            "enemy_doubles_value": -3,
            "enemy_material_score": -1,

            "friendly_most_advanced_singles": 1,
            "friendly_most_advanced_doubles": 1,
            "enemy_most_advanced_singles": -3,
            "enemy_most_advanced_doubles": -3,
            "friendly_advancement_of_singles": 1,
            "friendly_advancement_of_doubles": 1,
            "enemy_advancement_of_singles": -2,
            "enemy_advancement_of_doubles": -1,

            "control_of_center": 1,
            "control_of_edges": 3,

            "friendly_single_in_edges": 3,
            "friendly_double_in_edges": 1,
            "friendly_single_in_center": 2,
            "friendly_double_in_center": 1,
            "enemy_single_in_edges": -3,
            "enemy_double_in_edges": -2,
            "enemy_single_in_center": -2,
            "enemy_double_in_center": -2,

            "friendly_double_in_back_corner": -1,
            "friendly_doubles_in_line": 1,
            "friendly_single_double_in_line": 1,
            "friendly_singles_in_line": 1,
            "friendly_piece_is_last": 7,

            "friendly_density": 1,
            "friendly_mobility": 1,
            "enemy_density": -1,
            "enemy_mobility": -4
        }

    def get_random_move(self):
        posible_moves = self.board.get_legal_moves_list(self.board.get_legal_moves({'singles_left_empty': True,
                                                                                    'singles_front_empty': True,
                                                                                    'singles_right_empty': True,
                                                                                    'singles_kill_left_singles': True,
                                                                                    'singles_kill_left_doubles': True,
                                                                                    'singles_kill_right_singles': True,
                                                                                    'singles_kill_right_doubles': True,
                                                                                    'singles_upgrade_left': True,
                                                                                    'singles_upgrade_front': True,
                                                                                    'singles_upgrade_right': True,
                                                                                    'doubles_l_l_f_empty': True,
                                                                                    'doubles_f_f_l_empty': True,
                                                                                    'doubles_f_f_r_empty': True,
                                                                                    'doubles_r_r_f_empty': True,
                                                                                    'doubles_kill_l_l_f_singles': True,
                                                                                    'doubles_kill_l_l_f_doubles': True,
                                                                                    'doubles_kill_f_f_l_singles': True,
                                                                                    'doubles_kill_f_f_l_doubles': True,
                                                                                    'doubles_kill_f_f_r_singles': True,
                                                                                    'doubles_kill_f_f_r_doubles': True,
                                                                                    'doubles_kill_r_r_f_singles': True,
                                                                                    'doubles_kill_r_r_f_doubles': True,
                                                                                    'doubles_l_l_f_singles': True,
                                                                                    'doubles_f_f_l_singles': True,
                                                                                    'doubles_f_f_r_singles': True,
                                                                                    'doubles_r_r_f_singles': True
                                                                                    }, self.color))
        random_index = random.randrange(0, len(posible_moves), 1)
        return posible_moves[random_index]

    def get_score(self):
        game_over = self.board.is_game_over()
        if game_over != "Game Over":
            if f"{self.color} wins" in game_over:
                return 1000
            elif "Red wins" in game_over:
                return - 1000

        blue_singles_binary = bin(self.board.BLUE_SINGLES)[2:].zfill(64)
        blue_doubles_binary = bin(self.board.BLUE_DOUBLES)[2:].zfill(64)
        red_singles_binary = bin(self.board.RED_SINGLES)[2:].zfill(64)
        red_doubles_binary = bin(self.board.RED_DOUBLES)[2:].zfill(64)
        edges_indices = [8, 16, 24, 32, 40, 48, 15, 23, 31, 39, 47, 55]
        center_indices = [18, 19, 20, 21, 26, 27, 28, 29, 34, 35, 36, 37, 42, 43, 44, 45]
        corner_indices = [1, 6]

        # Material score
        friendly_singles_value = self.weights["friendly_singles_value"] * bin(self.board.BLUE_SINGLES).count('1')
        friendly_doubles_value = self.weights["friendly_doubles_value"] * bin(self.board.BLUE_DOUBLES).count('1')
        friendly_material_score = self.weights["friendly_material_score"] * (
                friendly_singles_value + friendly_doubles_value)
        enemy_singles_value = self.weights["enemy_singles_value"] * bin(self.board.RED_SINGLES).count('1')
        enemy_doubles_value = self.weights["enemy_doubles_value"] * bin(self.board.RED_DOUBLES).count('1')
        enemy_material_score = self.weights["enemy_material_score"] * (enemy_singles_value + enemy_doubles_value)

        # Advanced pieces
        friendly_most_advanced_singles = self.weights['friendly_most_advanced_singles'] * most_advanced_pieces(
            blue_singles_binary, True)
        friendly_most_advanced_doubles = self.weights['friendly_most_advanced_doubles'] * most_advanced_pieces(
            blue_doubles_binary, True)
        enemy_most_advanced_singles = self.weights['enemy_most_advanced_singles'] * most_advanced_pieces(
            red_singles_binary, False)
        enemy_most_advanced_doubles = self.weights['enemy_most_advanced_doubles'] * most_advanced_pieces(
            red_doubles_binary, False)

        friendly_advancement_of_singles = self.weights["friendly_advancement_of_singles"] * advancement_of_pieces(
            blue_singles_binary, friendly=True)
        friendly_advancement_of_doubles = self.weights["friendly_advancement_of_doubles"] * advancement_of_pieces(
            blue_doubles_binary, friendly=True)
        enemy_advancement_of_singles = self.weights["enemy_advancement_of_singles"] * advancement_of_pieces(
            red_singles_binary, friendly=False)
        enemy_advancement_of_doubles = self.weights["enemy_advancement_of_doubles"] * advancement_of_pieces(
            red_doubles_binary, friendly=False)

        # Control over the board
        control_of_center = self.weights["control_of_center"] * control_of_indices(self.weights, blue_singles_binary,
                                                                                   blue_doubles_binary,
                                                                                   red_singles_binary,
                                                                                   red_doubles_binary,
                                                                                   center_indices)
        control_of_edges = self.weights["control_of_edges"] * control_of_indices(self.weights, blue_singles_binary,
                                                                                 blue_doubles_binary,
                                                                                 red_singles_binary,
                                                                                 red_doubles_binary,
                                                                                 edges_indices)
        friendly_density = self.weights["friendly_density"] * piece_density(blue_singles_binary, blue_doubles_binary)
        friendly_mobility = self.weights["friendly_mobility"] * len(
            self.board.get_legal_moves_list(self.board.get_all_legal_moves(self.color)))
        enemy_density = self.weights["enemy_density"] * piece_density(red_singles_binary, red_doubles_binary)
        if self.color == "Blue":
            enemy_mobility = self.weights["enemy_mobility"] * len(
                self.board.get_legal_moves_list(self.board.get_all_legal_moves("Red")))
        else:
            enemy_mobility = self.weights["enemy_mobility"] * len(
                self.board.get_legal_moves_list(self.board.get_all_legal_moves("Blue")))

        # Strategic positions
        friendly_single_in_edges = self.weights["friendly_single_in_edges"] * piece_on_indices(self.weights,
                                                                                               blue_singles_binary,
                                                                                               edges_indices, "singles",
                                                                                               True)
        enemy_single_in_edges = self.weights["enemy_single_in_edges"] * piece_on_indices(self.weights,
                                                                                         red_singles_binary,
                                                                                         edges_indices, "singles",
                                                                                         False)
        friendly_double_in_edges = self.weights["friendly_double_in_edges"] * piece_on_indices(self.weights,
                                                                                               blue_doubles_binary,
                                                                                               edges_indices, "doubles",
                                                                                               True)
        enemy_double_in_edges = self.weights["enemy_double_in_edges"] * piece_on_indices(self.weights,
                                                                                         red_doubles_binary,
                                                                                         edges_indices, "doubles",
                                                                                         False)
        friendly_single_in_center = self.weights["friendly_single_in_center"] * piece_on_indices(self.weights,
                                                                                                 blue_singles_binary,
                                                                                                 center_indices,
                                                                                                 "singles", True)
        enemy_single_in_center = self.weights["enemy_single_in_center"] * piece_on_indices(self.weights,
                                                                                           red_singles_binary,
                                                                                           center_indices, "singles",
                                                                                           False)

        friendly_double_in_center = self.weights["friendly_double_in_center"] * piece_on_indices(self.weights,
                                                                                                 blue_doubles_binary,
                                                                                                 center_indices,
                                                                                                 "doubles", True)
        enemy_double_in_center = self.weights["enemy_double_in_center"] * piece_on_indices(self.weights,
                                                                                           red_doubles_binary,
                                                                                           center_indices, "doubles",
                                                                                           False)

        # Other cases
        friendly_double_in_back_corner = self.weights["friendly_double_in_back_corner"] * piece_on_indices(self.weights,
                                                                                                           blue_doubles_binary,
                                                                                                           corner_indices,
                                                                                                           "doubles",
                                                                                                           True)
        friendly_doubles_in_line = self.weights["friendly_doubles_in_line"] * piece_in_front(self.weights,
                                                                                             blue_doubles_binary,
                                                                                             "doubles",
                                                                                             blue_doubles_binary,
                                                                                             "doubles")
        friendly_single_double_in_line = self.weights["friendly_single_double_in_line"] * piece_in_front(self.weights,
                                                                                                         blue_singles_binary,
                                                                                                         "singles",
                                                                                                         blue_doubles_binary,
                                                                                                         "doubles")
        friendly_singles_in_line = self.weights["friendly_singles_in_line"] * piece_in_front(self.weights,
                                                                                             blue_singles_binary,
                                                                                             "singles",
                                                                                             blue_singles_binary,
                                                                                             "singles")
        friendly_piece_is_last = self.weights["friendly_piece_is_last"] * piece_is_last(self.weights,
                                                                                        blue_singles_binary,
                                                                                        blue_doubles_binary,
                                                                                        red_singles_binary,
                                                                                        red_doubles_binary)

        bias = self.weights["bias"] * 0

        total_score = (bias +
                       friendly_singles_value +
                       friendly_doubles_value +
                       friendly_material_score +
                       enemy_singles_value +
                       enemy_doubles_value +
                       enemy_material_score +
                       friendly_most_advanced_singles +
                       friendly_most_advanced_doubles +
                       enemy_most_advanced_singles +
                       enemy_most_advanced_doubles +
                       friendly_advancement_of_singles +
                       friendly_advancement_of_doubles +
                       enemy_advancement_of_singles +
                       enemy_advancement_of_doubles +
                       control_of_center +
                       control_of_edges +
                       friendly_density +
                       friendly_mobility +
                       enemy_density +
                       enemy_mobility +
                       friendly_single_in_edges +
                       friendly_double_in_edges +
                       friendly_single_in_center +
                       friendly_double_in_center +
                       enemy_single_in_edges +
                       enemy_double_in_edges +
                       enemy_single_in_center +
                       enemy_double_in_center +
                       friendly_double_in_back_corner +
                       friendly_doubles_in_line +
                       friendly_single_double_in_line +
                       friendly_singles_in_line +
                       friendly_piece_is_last)

        # features = {
        #     'bias': (self.weights['bias'], bias),
        #     'friendly_singles_value': (self.weights['friendly_singles_value'], friendly_singles_value),
        #     'friendly_doubles_value': (self.weights['friendly_doubles_value'], friendly_doubles_value),
        #     'friendly_material_score': (self.weights['friendly_material_score'], friendly_material_score),
        #     'enemy_singles_value': (self.weights['enemy_singles_value'], enemy_singles_value),
        #     'enemy_doubles_value': (self.weights['enemy_doubles_value'], enemy_doubles_value),
        #     'enemy_material_score': (self.weights['enemy_material_score'], enemy_material_score),
        #     'friendly_most_advanced_singles': (
        #         self.weights['friendly_most_advanced_singles'], friendly_most_advanced_singles),
        #     'friendly_most_advanced_doubles': (
        #         self.weights['friendly_most_advanced_doubles'], friendly_most_advanced_doubles),
        #     'enemy_most_advanced_singles': (self.weights['enemy_most_advanced_singles'], enemy_most_advanced_singles),
        #     'enemy_most_advanced_doubles': (self.weights['enemy_most_advanced_doubles'], enemy_most_advanced_doubles),
        #     'friendly_advancement_of_singles': (
        #         self.weights['friendly_advancement_of_singles'], friendly_advancement_of_singles),
        #     'friendly_advancement_of_doubles': (
        #         self.weights['friendly_advancement_of_doubles'], friendly_advancement_of_doubles),
        #     'enemy_advancement_of_singles': (
        #         self.weights['enemy_advancement_of_singles'], enemy_advancement_of_singles),
        #     'enemy_advancement_of_doubles': (
        #         self.weights['enemy_advancement_of_doubles'], enemy_advancement_of_doubles),
        #     'control_of_center': (self.weights['control_of_center'], control_of_center),
        #     'control_of_edges': (self.weights['control_of_edges'], control_of_edges),
        #     'friendly_density': (self.weights['friendly_density'], friendly_density),
        #     'friendly_mobility': (self.weights['friendly_mobility'], friendly_mobility),
        #     'enemy_density': (self.weights['enemy_density'], enemy_density),
        #     'enemy_mobility': (self.weights['enemy_mobility'], enemy_mobility),
        #     'single_in_edges': (self.weights['single_in_edges'], single_in_edges),
        #     'double_in_edges': (self.weights['double_in_edges'], double_in_edges),
        #     'single_in_center': (self.weights['single_in_center'], single_in_center),
        #     'double_in_center': (self.weights['double_in_center'], double_in_center)
        # }

        return total_score

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
        
def main():
    board = Board()
    board.fen_notation_into_bb("b0b0b0b0b0b0/1b0b0b0b0b0b01/8/8/8/8/1r0r0r0r0r0r01/r0r0r0r0r0r0")
    blue_player = AIPlayer("Blue", board)
    red_player = AIPlayer("Red", board)
    #result_alphabeta_value, result_alphabeta_move = blue_player.alphabeta(alpha=float('-inf'), beta=float('inf'), max_player=True, depth=0, max_depth=1)
    #result_alphabeta_value = blue_player.alphabeta(alpha=float('-inf'), beta=float('inf'), max_player=True, depth=0, max_depth=1)
    #print(result_alphabeta_value)
    #print(result_alphabeta_move)
    
    
    # Value-Iteration (didn't work)
    # new_weights = value_iteration(blue_player, red_player, board)

    # Initialize loop control variables
    i = 0
    N = 1
    total = 0

    # Loop through each game iteration
    for j in range(N):
        # Simulate game moves until game over
        while True:
            # Determine which player's turn
            if i % 2 == 0:
                turn = blue_player
            else:
                turn = red_player

            # Print the current game state
            board.print_board()
            print("-----------------------")
            print(f"Blue score: {blue_player.get_score()}")
            print(f"Red score: {red_player.get_score()}")
            print(f"Actual player score: {turn.get_score()}")

            # Check if the game is over
            game_over = board.is_game_over()
            if game_over != "Game not over":
                print(board.is_game_over())
                break

            print("-----------------------")
            print(f"Its {turn.color}'s turn.")

            # Get next move from the current player
            if turn == blue_player:
                # next_move = board.ask_for_move()
                next_move = turn.get_random_move()
                #next_move = turn.alphabeta(alpha=float('-inf'), beta=float('inf'), max_player=True, depth=0, max_depth=1)
            else:
                next_move = turn.get_random_move()

            # Apply move
            from_square, to_square = next_move.upper().split('-')
            from_coordinate = Coordinate[from_square]
            to_coordinate = Coordinate[to_square]
            move = Move(player=turn.color, fromm=from_coordinate, to=to_coordinate)
            response = board.apply_move(move)
            print("-----------------------")
            print(next_move)
            print(response)
            print("-----------------------")
            if response.startswith('Error'):
                break

            # Increment turn
            i += 1

        print(f"------- TIEFE: {i} -------")
        total += i
        i = 0

        board.reset()

    # Print results
    print(f"N: {N}")
    print(f"media: {total / N}")


if __name__ == "__main__":

    main()
