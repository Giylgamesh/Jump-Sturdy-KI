import os
import random
from JumpSturdy.game_state.board import Board, Coordinate, Move


class AIPlayer:
    def __init__(self, color, board):
        # Initialize AI components
        self.color = color
        self.board = board

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

def main():
    board=Board()
    board.fen_notation_into_bb("b0b0b0b0b0b0/1b0b0b0b0b0b01/8/8/8/8/1r0r0r0r0r0r01/r0r0r0r0r0r0")
    blue_player = AIPlayer("Blue", board)
    red_player = AIPlayer("Red", board)

    i = 0
    turn = blue_player

    while True:
        board.print_board()
        if board.is_game_over() != "Game not over":
            print(board.is_game_over())
            break
        if i%2==0:
            turn = blue_player.color
            next_move = blue_player.get_random_move()
        else:
            turn = red_player.color
            next_move = red_player.get_random_move()
        try:
            from_square, to_square = next_move.upper().split('-')
            from_coordinate = Coordinate[from_square]
            to_coordinate = Coordinate[to_square]
        except ValueError:
            print("Please enter moves in the format 'H8-H7'.")
            continue
        except KeyError:
            print("Invalid coordinates. Try again.")
            continue
        move = Move(player=turn, fromm=from_coordinate, to=to_coordinate)
        response = board.apply_move(move)
        print("-----------------------")
        print(response)
        print("-----------------------")

        # Increment turn
        if response.startswith('Good:'):
            i += 1


if __name__ == "__main__":
    main()