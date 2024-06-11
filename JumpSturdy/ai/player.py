import os
import random
import math
import time
from collections import deque
from JumpSturdy.game_state.board import Board, Coordinate, Move


def value_iteration(blue_player, red_player, board, learning_rate=0.1, discount_factor=0.95):
    """
    Performs value iteration to update weights of blue player based on outcome of simulated games

    Parameters:
    - blue_player: The blue player object.
    - red_player: The red player object.
    - board: The game board.
    - learning_rate: The learning rate for weight updates. Default is 0.1.
    - discount_factor: The discount factor for future rewards. Default is 0.95.

    Returns:
    - The updated weights of the blue player.
    """
    
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
    """
    Simulates a game between two players on a given board.

    Parameters:
    - board (Board): The game board on which the game is being played.
    - friendly_player (Player): The player representing the friendly side.
    - enemy_player (Player): The player representing the enemy side.

    Returns:
    - history (list): A list of tuples representing the state, action, reward history of the game.
    - reward (int): The reward obtained by the friendly player at the end of the game.
    """
    
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
            reward = 100 if "Blue wins" in game_over else 0

            # Get heuristic value
            heuristic, features = friendly_player.get_score()
            # Store the state, action, reward tuple
            state = board.get_state()
            history.append((state, features, next_move, heuristic, turn))

            # Reset board
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

    if len(positions) == 0:
        return 0
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
    amount = 0
    for i in range(56):
        if first_bitboard[i] == '1' and second_bitboard[i + 8] == '1':
            amount += 1
    return amount


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


def piece_under_attack(weights, friend_pieces, enemy_singles, enemy_doubles):
    """Calculate how many friendly pieces are under attack."""
    amount = 0
    for i in range(64):  # Adjusted to include the entire 64 bits
        if friend_pieces[i] == '1':  # Check if there's a friendly piece at position i
            # Check for single-piece attacks
            if i + 7 < 64 and enemy_singles[i + 7] == '1':
                amount += 1
            if i + 9 < 64 and enemy_singles[i + 9] == '1':
                amount += 1
            # Check for double-piece attacks
            if i + 6 < 64 and enemy_doubles[i + 6] == '1':
                amount += 1
            if i + 10 < 64 and enemy_doubles[i + 10] == '1':
                amount += 1
            if i + 15 < 64 and enemy_doubles[i + 15] == '1':
                amount += 1
            if i + 17 < 64 and enemy_doubles[i + 17] == '1':
                amount += 1
    return amount


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
            "friendly_material_score": 2,
            "enemy_singles_value": -1,
            "enemy_doubles_value": -3,
            "enemy_material_score": -2,

            "friendly_most_advanced_singles": 1,
            "friendly_most_advanced_doubles": 2,
            "enemy_most_advanced_singles": -2,
            "enemy_most_advanced_doubles": -2,
            "friendly_advancement_of_singles": 5,
            "friendly_advancement_of_doubles": 5,
            "enemy_advancement_of_singles": -2,
            "enemy_advancement_of_doubles": -2,

            "control_of_center": 2,
            "control_of_edges": 2,

            "friendly_single_in_edges": 3,
            "friendly_double_in_edges": 1,
            "friendly_single_in_center": 2,
            "friendly_double_in_center": 2,
            "enemy_single_in_edges": -3,
            "enemy_double_in_edges": -1,
            "enemy_single_in_center": -2,
            "enemy_double_in_center": -1,

            "friendly_double_in_back_corner": -1,
            "friendly_doubles_in_line": 4,
            "friendly_single_double_in_line": 5,
            "friendly_singles_in_line": 1,
            "friendly_piece_is_last": 20,

            "friendly_density": 3,
            "friendly_mobility": 1,
            "enemy_density": -1,
            "enemy_mobility": -3,

            "friendly_single_under_attack": -4,
            "friendly_double_under_attack": -4
        }

    def alpha_beta(self, board, depth, alpha, beta, maximizing_player, display, cutoff, count):
        """
        Implements the alpha-beta pruning algorithm for game tree search.

        Parameters:
        - board (Baord): current game board state.
        - depth (int): current depth of the search tree.
        - alpha (float): best value that the maximizing player can guarantee at this level or above.
        - beta (float): best value that the minimizing player can guarantee at this level or above.
        - maximizing_player (boolean): indicating whether the current player is maximizing or not.
        - display (boolean):  indicating whether to display the board during the search.
        - cutoff (boolean): indicating whether to apply cutoff when alpha >= beta.
        - count (int): number of nodes visited during the search.

        Returns:
        - best_value (float): The best value that can be achieved from the current game state.
        - best_move (String): The best move to make from the current game state.
        - count (int): The updated number of nodes visited during the search.
        """
        
        if display:
            board.print_board()

        if board.is_game_over()[0]:
            return float('-inf') if maximizing_player else float('inf'), None, count

        if depth == 0:
            return self.get_score(board), None, count

        best_value = float('-inf') if maximizing_player else float('inf')
        best_move = None

        color = "Blue" if maximizing_player else "Red"
        possible_moves = board.get_legal_moves_moves(
            board.get_legal_moves({'singles_left_empty': True,  'singles_front_empty': True,
                                   'singles_right_empty': True, 'singles_kill_left_singles': True,
                                   'singles_kill_left_doubles': True,   'singles_kill_right_singles': True,
                                   'singles_kill_right_doubles': True,  'singles_upgrade_left': True,
                                   'singles_upgrade_front': True,   'singles_upgrade_right': True,
                                   'doubles_l_l_f_empty': True, 'doubles_f_f_l_empty': True,
                                   'doubles_f_f_r_empty': True, 'doubles_r_r_f_empty': True,
                                   'doubles_kill_l_l_f_singles': True,  'doubles_kill_l_l_f_doubles': True,
                                   'doubles_kill_f_f_l_singles': True,  'doubles_kill_f_f_l_doubles': True,
                                   'doubles_kill_f_f_r_singles': True,  'doubles_kill_f_f_r_doubles': True,
                                   'doubles_kill_r_r_f_singles': True,  'doubles_kill_r_r_f_doubles': True,
                                   'doubles_l_l_f_singles': True,   'doubles_f_f_l_singles': True,
                                   'doubles_f_f_r_singles': True,   'doubles_r_r_f_singles': True
                                   }, color), color)

        if display:
            move_score_list = []
        for move in possible_moves:
            if display:
                print("BP")
                board.print_board()
            assert "Error" not in board.apply_move(move)
            value, _, count = self.alpha_beta(board, depth - 1, alpha, beta, not maximizing_player, display, cutoff, count+1)
            if display:
                move_score_list.append((move, value))
                print("BP")
                board.print_board()
            assert "Good" in board.undo_move()

            if maximizing_player:
                if value > best_value:
                    best_value, best_move = value, move
                alpha = max(alpha, value)
                if beta <= alpha and cutoff:
                    break
            else:
                if value < best_value:
                    best_value, best_move = value, move
                beta = min(beta, value)
                if beta <= alpha and cutoff:
                    break
        return best_value, best_move, count

    def get_best_move(self, max_depth, display, cutoff):
        """
        Finds the best move for the player using the alpha-beta pruning algorithm

        Args:
            max_depth (int): The maximum depth to search in the game tree.
            display (bool): Flag indicating whether to display the game board during the search. We use this for debugging purposes.
            cutoff (bool): Flag indicating whether to use cutoffs to improve search efficiency.

        Returns:
            str: The best move as a string (e.g. B2 - B3, for a move from position B2 to the position B3.)

        """
        isBlue = True if self.color == "Blue" else False
        best_move = None
        best_value = float('-inf') if self.color == "Blue" else float('inf')
        count = 1
        prev_count = count
        print(f"Tiefe: 0 und Anzahl Zustände: 1")
        start = time.time()
        for depth in range(1, max_depth + 1):
            board_copy = self.board.copy_board()
            startzeit = time.time()
            value, move, countPerDepth = self.alpha_beta(board_copy, depth, float('-inf'), float('inf'), isBlue, display, cutoff, count)
            print(move)
            print(f"Benötigte Zeit für die Tiefe {depth} " + str((time.time() - startzeit) * 1000) + "ms")
            count = countPerDepth
            print(f"Tiefe: {depth} und Anzahl Zustände: {count - prev_count}")
            prev_count=count
            if isBlue:
                if value > best_value:
                    best_value, best_move = value, move
            else:
                if value < best_value:
                    best_value, best_move = value, move
            print(best_move)
            if cutoff == True:
                if value == float('inf'):
                    return move
        print(f"Anzahl durchlaufener Zustände: {count}")
        print("Gesamtlaufzeit: " + str((time.time() - start) * 1000)+ "ms")
        best_move = str(best_move)[-5:]
        return best_move

    def get_random_move(self):
        """
        Generates a random move for the player

        Returns:
            Move: "move" object representing the randomly generated move
        """
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
        next_move = posible_moves[random_index]
        from_square, to_square = next_move.upper().split('-')
        from_coordinate = Coordinate[from_square]
        to_coordinate = Coordinate[to_square]
        move = Move(player=self.color, fromm=from_coordinate, to=to_coordinate)
        return move

    def get_all_selected_moves(self):
        return self.board.get_legal_moves({'singles_left_empty': True,'singles_front_empty': True,'singles_right_empty': True,'singles_kill_left_singles': True,'singles_kill_left_doubles': True,'singles_kill_right_singles': True,'singles_kill_right_doubles': True,'singles_upgrade_left': True,'singles_upgrade_front': True,'singles_upgrade_right': True,'doubles_l_l_f_empty': True,'doubles_f_f_l_empty': True,'doubles_f_f_r_empty': True,'doubles_r_r_f_empty': True,'doubles_kill_l_l_f_singles': True,'doubles_kill_l_l_f_doubles': True,'doubles_kill_f_f_l_singles': True,'doubles_kill_f_f_l_doubles': True,'doubles_kill_f_f_r_singles': True,'doubles_kill_f_f_r_doubles': True,'doubles_kill_r_r_f_singles': True,'doubles_kill_r_r_f_doubles': True,'doubles_l_l_f_singles': True,'doubles_f_f_l_singles': True,'doubles_f_f_r_singles': True,'doubles_r_r_f_singles': True}, self.color)


    def get_score(self, board):
        """
        This method calculates the score for the current player based on various factors such as material score, advanced pieces,
        control over the board, strategic positions, and other cases. It uses binary representations of the board's state to
        perform the calculations. The calculated score is returned as the result.

        Parameters:
        - board: The current board state.

        Returns:
        - (float) calculated score for the current player.

        Note: board state is represented with following attributes:
        - BLUE_SINGLES: Binary representation of the blue player's singles pieces.
        - BLUE_DOUBLES: Binary representation of the blue player's doubles pieces.
        - RED_SINGLES: Binary representation of the red player's singles pieces.
        - RED_DOUBLES: Binary representation of the red player's doubles pieces.

        "weights" come from the player object itself.
        """
        
        # board.print_board()
        blue_singles_binary = bin(board.BLUE_SINGLES)[2:].zfill(64)
        blue_doubles_binary = bin(board.BLUE_DOUBLES)[2:].zfill(64)
        red_singles_binary = bin(board.RED_SINGLES)[2:].zfill(64)
        red_doubles_binary = bin(board.RED_DOUBLES)[2:].zfill(64)

        edges_indices = [8, 16, 24, 32, 40, 48, 15, 23, 31, 39, 47, 55]
        center_indices = [18, 19, 20, 21, 26, 27, 28, 29, 34, 35, 36, 37, 42, 43, 44, 45]
        corner_indices = [1, 6]

        # Material score
        friendly_singles_value = self.weights["friendly_singles_value"] * blue_singles_binary.count('1')
        friendly_doubles_value = self.weights["friendly_doubles_value"] * blue_doubles_binary.count('1')
        friendly_material_score = self.weights["friendly_material_score"] * (
                friendly_singles_value + friendly_doubles_value)
        enemy_singles_value = self.weights["enemy_singles_value"] * red_singles_binary.count('1')
        enemy_doubles_value = self.weights["enemy_doubles_value"] * red_doubles_binary.count('1')
        enemy_material_score = self.weights["enemy_material_score"] * (enemy_singles_value + enemy_doubles_value) * (-1)

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
        # control_of_center = self.weights["control_of_center"] * control_of_indices(self.weights, blue_singles_binary,
        #                                                                            blue_doubles_binary,
        #                                                                            red_singles_binary,
        #                                                                            red_doubles_binary,
        #                                                                            center_indices)
        # control_of_edges = self.weights["control_of_edges"] * control_of_indices(self.weights, blue_singles_binary,
        #                                                                          blue_doubles_binary,
        #                                                                          red_singles_binary,
        #                                                                          red_doubles_binary,
        #                                                                          edges_indices)
        # friendly_density = self.weights["friendly_density"] * piece_density(blue_singles_binary, blue_doubles_binary)
        # friendly_mobility = self.weights["friendly_mobility"] * len(
        #     self.board.get_legal_moves_list(self.board.get_all_legal_moves(self.color)))
        # enemy_density = self.weights["enemy_density"] * piece_density(red_singles_binary, red_doubles_binary)
        # if self.color == "Blue":
        #     enemy_mobility = self.weights["enemy_mobility"] * len(
        #         self.board.get_legal_moves_list(self.board.get_all_legal_moves("Red")))
        # else:
        #     enemy_mobility = self.weights["enemy_mobility"] * len(
        #         self.board.get_legal_moves_list(self.board.get_all_legal_moves("Blue")))

        # Strategic positions
        # friendly_single_in_edges = self.weights["friendly_single_in_edges"] * piece_on_indices(self.weights,
        #                                                                                        blue_singles_binary,
        #                                                                                        edges_indices, "singles",
        #                                                                                        True)
        # enemy_single_in_edges = self.weights["enemy_single_in_edges"] * piece_on_indices(self.weights,
        #                                                                                  red_singles_binary,
        #                                                                                  edges_indices, "singles",
        #                                                                                  False)
        # friendly_double_in_edges = self.weights["friendly_double_in_edges"] * piece_on_indices(self.weights,
        #                                                                                        blue_doubles_binary,
        #                                                                                        edges_indices, "doubles",
        #                                                                                        True)
        # enemy_double_in_edges = self.weights["enemy_double_in_edges"] * piece_on_indices(self.weights,
        #                                                                                  red_doubles_binary,
        #                                                                                  edges_indices, "doubles",
        #                                                                                  False)
        # friendly_single_in_center = self.weights["friendly_single_in_center"] * piece_on_indices(self.weights,
        #                                                                                          blue_singles_binary,
        #                                                                                          center_indices,
        #                                                                                          "singles", True)
        # enemy_single_in_center = self.weights["enemy_single_in_center"] * piece_on_indices(self.weights,
        #                                                                                    red_singles_binary,
        #                                                                                    center_indices, "singles",
        #                                                                                    False)
        #
        # friendly_double_in_center = self.weights["friendly_double_in_center"] * piece_on_indices(self.weights,
        #                                                                                          blue_doubles_binary,
        #                                                                                          center_indices,
        #                                                                                          "doubles", True)
        # enemy_double_in_center = self.weights["enemy_double_in_center"] * piece_on_indices(self.weights,
        #                                                                                    red_doubles_binary,
        #                                                                                    center_indices, "doubles",
        #                                                                                    False)
        #
        # # Other cases
        # friendly_double_in_back_corner = self.weights["friendly_double_in_back_corner"] * piece_on_indices(self.weights,
        #                                                                                                    blue_doubles_binary,
        #                                                                                                    corner_indices,
        #                                                                                                    "doubles",
        #                                                                                                    True)
        # friendly_doubles_in_line = self.weights["friendly_doubles_in_line"] * piece_in_front(self.weights,
        #                                                                                      blue_doubles_binary,
        #                                                                                      "doubles",
        #                                                                                      blue_doubles_binary,
        #                                                                                      "doubles")
        # friendly_single_double_in_line = self.weights["friendly_single_double_in_line"] * piece_in_front(self.weights,
        #                                                                                                  blue_singles_binary,
        #                                                                                                  "singles",
        #                                                                                                  blue_doubles_binary,
        #                                                                                                  "doubles")
        # friendly_singles_in_line = self.weights["friendly_singles_in_line"] * piece_in_front(self.weights,
        #                                                                                      blue_singles_binary,
        #                                                                                      "singles",
        #                                                                                      blue_singles_binary,
        #                                                                                      "singles")
        # friendly_piece_is_last = self.weights["friendly_piece_is_last"] * piece_is_last(self.weights,
        #                                                                                 blue_singles_binary,
        #                                                                                 blue_doubles_binary,
        #                                                                                 red_singles_binary,
        #                                                                                 red_doubles_binary)

        # Under-Attack
        friendly_single_under_attack = self.weights["friendly_single_under_attack"] * piece_under_attack(self.weights,
                                                                                                         blue_singles_binary,
                                                                                                         red_singles_binary,
                                                                                                         red_doubles_binary)
        friendly_double_under_attack = self.weights["friendly_double_under_attack"] * piece_under_attack(self.weights,
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
                       # control_of_center +
                       # control_of_edges +
                       # friendly_density +
                       # friendly_mobility +
                       # enemy_density +
                       # enemy_mobility +
                       # friendly_single_in_edges +
                       # friendly_double_in_edges +
                       # friendly_single_in_center +
                       # friendly_double_in_center +
                       # enemy_single_in_edges +
                       # enemy_double_in_edges +
                       # enemy_single_in_center +
                       # enemy_double_in_center +
                       # friendly_double_in_back_corner +
                       # friendly_doubles_in_line +
                       # friendly_single_double_in_line +
                       # friendly_singles_in_line +
                       # friendly_piece_is_last +
                       friendly_single_under_attack +
                       friendly_double_under_attack)

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
        # print(f"Player:{self.color}, Score:{total_score}")
        return total_score


def main():
    """
    This is the main method that sets up the game board and players, 
    and then simulates a game between two AI players. Here we give the board a FEN-String to generate the initial board state.
    This allows us to start the game from any state (e.g. Game-start, early-game, mid-game, late-game)
    """
    board = Board()
    # board.fen_notation_into_bb("b0b0b0b0b0b0/1b0b0b0b0b0b01/8/8/8/8/1r0r0r0r0r0r01/r0r0r0r0r0r0")
    # board.fen_notation_into_bb("b0b0b0b02/b0b01b01b0b01/5r02/1b02r03/b01r02r02/3r03r0/2rb1rr3/1r03r0")
    board.fen_notation_into_bb("b0b0b0b0b0b0/1b0b0b0b0b0b01/8/8/8/8/1r0r0r0r0r0r01/r0r0r0r0r0r0")
    blue_player = AIPlayer("Blue", board)
    red_player = AIPlayer("Red", board)

    # Value-Iteration (didn't work)
    # new_weights = value_iteration(blue_player, red_player, board)

    # Initialize loop control variables
    i = 0
    N = 1
    total = 0
    winner = 0

    # Loop through each game iteration
    for j in range(N):
        # Simulate game moves until game over
        last_3_moves = deque(maxlen=3)
        while True:
            # Determine which player's turn
            if i % 2 == 0:
                turn = blue_player
            else:
                turn = red_player

            # Print the current game state
            board.print_board()
            print("-----------------------")
            print(f"Blue score: {blue_player.get_score(board)}")
            print(f"Red score: {red_player.get_score(board)}")

            # Check if the game is over
            game_over = board.is_game_over()
            if game_over[0]:
                print(f"game over, {game_over[1]} wins")
                break

            print("-----------------------")
            print(f"Its {turn.color}'s turn.")

            # Get next move from the current player
            if turn == blue_player:
                # next_move = board.ask_for_move()
                next_move = turn.get_best_move(2, False, False)
                last_3_moves.append(next_move)

                if last_3_moves.count(next_move) > 1 and len(last_3_moves) == 3:
                    next_move = turn.get_random_move()
            else:
                next_move = turn.get_random_move()

            move = next_move

            # Apply move
            response = board.apply_move(move)
            print("-----------------------")
            print(next_move)
            print(response)
            print("-----------------------")
            if response.startswith('Error'):
                break

            # Increment turn
            i += 1

        print(f"------- Züge: {i/2+0.5} -------")
        total += i
        i = 0
        winner += 1 if "Blue" in board.is_game_over()[1] else 0

        board.reset()

    # Print results
    print(f"N: {N}")
    print(f"media: {total / N}")
    print(f"winner: {winner}")


if __name__ == "__main__":
    main()
