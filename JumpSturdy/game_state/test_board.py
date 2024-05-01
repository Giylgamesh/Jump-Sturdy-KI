import unittest
from board import Board
from board import Move
from board import Coordinate

def check_color(board, color):
    if color == "b":
        selected_legal_moves = board.get_legal_moves({'singles_left_empty': True,
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
                                                      }, "Blue")
    else:
        selected_legal_moves = board.get_legal_moves({'singles_left_empty': True,
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
                                                      }, "Red")
    return selected_legal_moves
class TestBoard(unittest.TestCase):
    def test_setUp(self):
        board = Board()
        self.assertEqual(board.BLUE_SINGLES, 0)
        self.assertEqual(board.RED_SINGLES, 0)
        self.assertEqual(board.BLUE_DOUBLES, 0)
        self.assertEqual(board.RED_DOUBLES, 0)
        self.assertEqual(board.BLUE_BLOCKED, 0)
        self.assertEqual(board.RED_BLOCKED, 0)
        self.assertEqual(board.last_move, Move(Coordinate.XX, Coordinate.XX))

    def test_initialize(self):
        board = Board()
        board.initialize()
        self.assertIsInstance(board, Board)
        self.assertEqual(board.BLUE_SINGLES, 0b0111111001111110000000000000000000000000000000000000000000000000)
        self.assertEqual(board.RED_SINGLES, 0b0000000000000000000000000000000000000000000000000000000000000000)
        self.assertEqual(board.BLUE_DOUBLES, 0b0000000000000000000000000000000000000000000000000000000000000000)
        self.assertEqual(board.RED_DOUBLES, 0b0000000000000000000000000000000000000000000000000111111001111110)
        self.assertEqual(board.BLUE_BLOCKED, 0b0000000000000000000000000000000000000000000000000000000000000000)
        self.assertEqual(board.RED_BLOCKED, 0b0000000000000000000000000000000000000000000000000000000000000000)
        self.assertEqual(board.last_move, Move(Coordinate.XX, Coordinate.XX))

    def test_apply_move(self):
        board = Board()
        board.initialize_for_test_doubles()
        board.print_board()
        # Blue single
            # blocked by friend
            # blocked by enemy
            # try to kill friendly single
            # try to kill enemy single
            # try to kill friendly double
            # try to kill enemy double

        # Red singles
            # blocked by friend
            # blocked by enemy
            # try to kill friendly single
            # try to kill enemy single
            # try to kill friendly double
            # try to kill enemy double

        # Blue doubles
            # jump over friendly single
            # jump over enemy single
            # jump over friendly double
            # jump over enemy double

        # Red doubles
            # jump over friendly single
            # jump over enemy single
            # jump over friendly double
            # jump over enemy double

        # Blue blocked
        # Red blocked

        board.apply_move(Move("Blue", Coordinate.B1, Coordinate.B2))
        self.assertEqual(board.BLUE_SINGLES, 0b0011111000111110000000000000000000000000000000000000000000000000)
        self.assertEqual(board.BLUE_DOUBLES, 0b0000000001000000000000000000000000000000000000000000000000000000)
        self.assertEqual(board.BLUE_BLOCKED, 0b0000000001000000000000000000000000000000000000000000000000000000)
        self.assertEqual(board.RED_SINGLES, 0b0000000000000000000000000000000000000000000000000111111001111110)
        self.assertEqual(board.RED_DOUBLES, 0b0000000000000000000000000000000000000000000000000000000000000000)
        self.assertEqual(board.RED_BLOCKED, 0b0000000000000000000000000000000000000000000000000000000000000000)
        board.print_board()
        board.apply_move(Move("Red", Coordinate.C7, Coordinate.B7))
        self.assertEqual(board.BLUE_SINGLES, 0b0011111000111110000000000000000000000000000000000000000000000000)
        self.assertEqual(board.BLUE_DOUBLES, 0b0000000001000000000000000000000000000000000000000000000000000000)
        self.assertEqual(board.BLUE_BLOCKED, 0b0000000001000000000000000000000000000000000000000000000000000000)
        self.assertEqual(board.RED_SINGLES, 0b0000000000000000000000000000000000000000000000000001111001111110)
        self.assertEqual(board.RED_DOUBLES, 0b0000000000000000000000000000000000000000000000000100000000000000)
        self.assertEqual(board.RED_BLOCKED, 0b0000000000000000000000000000000000000000000000000100000000000000)
        board.print_board()
        board.apply_move(Move("Blue", Coordinate.B2, Coordinate.D3))
        self.assertEqual(board.BLUE_SINGLES,    0b0011111001111110000100000000000000000000000000000000000000000000)
        self.assertEqual(board.BLUE_DOUBLES,    0b0000000000000000000000000000000000000000000000000000000000000000)
        self.assertEqual(board.BLUE_BLOCKED,    0b0000000000000000000000000000000000000000000000000000000000000000)
        self.assertEqual(board.RED_SINGLES,     0b0000000000000000000000000000000000000000000000000001111001111110)
        self.assertEqual(board.RED_DOUBLES,     0b0000000000000000000000000000000000000000000000000100000000000000)
        self.assertEqual(board.RED_BLOCKED,     0b0000000000000000000000000000000000000000000000000100000000000000)
        board.print_board()
        board.apply_move(Move("Red", Coordinate.B7, Coordinate.C5))
        self.assertEqual(board.BLUE_SINGLES,    0b0011111001111110000100000000000000000000000000000000000000000000)
        self.assertEqual(board.BLUE_DOUBLES,    0b0000000000000000000000000000000000000000000000000000000000000000)
        self.assertEqual(board.BLUE_BLOCKED,    0b0000000000000000000000000000000000000000000000000000000000000000)
        self.assertEqual(board.RED_SINGLES,     0b0000000000000000000000000000000000100000000000000101111001111110)
        self.assertEqual(board.RED_DOUBLES,     0b0000000000000000000000000000000000000000000000000000000000000000)
        self.assertEqual(board.RED_BLOCKED,     0b0000000000000000000000000000000000000000000000000000000000000000)
        board.print_board()
        board.apply_move(Move("Blue", Coordinate.D2, Coordinate.D3))
        self.assertEqual(board.BLUE_SINGLES,    0b0011111001101110000000000000000000000000000000000000000000000000)
        self.assertEqual(board.BLUE_DOUBLES,    0b0000000000000000000100000000000000000000000000000000000000000000)
        self.assertEqual(board.BLUE_BLOCKED,    0b0000000000000000000100000000000000000000000000000000000000000000)
        self.assertEqual(board.RED_SINGLES,     0b0000000000000000000000000000000000100000000000000101111001111110)
        self.assertEqual(board.RED_DOUBLES,     0b0000000000000000000000000000000000000000000000000000000000000000)
        self.assertEqual(board.RED_BLOCKED,     0b0000000000000000000000000000000000000000000000000000000000000000)
        board.print_board()
        board.apply_move(Move("Red", Coordinate.C5, Coordinate.C4))
        self.assertEqual(board.BLUE_SINGLES,    0b0011111001101110000000000000000000000000000000000000000000000000)
        self.assertEqual(board.BLUE_DOUBLES,    0b0000000000000000000100000000000000000000000000000000000000000000)
        self.assertEqual(board.BLUE_BLOCKED,    0b0000000000000000000100000000000000000000000000000000000000000000)
        self.assertEqual(board.RED_SINGLES,     0b0000000000000000000000000010000000000000000000000101111001111110)
        self.assertEqual(board.RED_DOUBLES,     0b0000000000000000000000000000000000000000000000000000000000000000)
        self.assertEqual(board.RED_BLOCKED,     0b0000000000000000000000000000000000000000000000000000000000000000)
        board.print_board()
        board.apply_move(Move("Blue", Coordinate.C2, Coordinate.C3))
        self.assertEqual(board.BLUE_SINGLES,    0b0011111001001110001000000000000000000000000000000000000000000000)
        self.assertEqual(board.BLUE_DOUBLES,    0b0000000000000000000100000000000000000000000000000000000000000000)
        self.assertEqual(board.BLUE_BLOCKED,    0b0000000000000000000100000000000000000000000000000000000000000000)
        self.assertEqual(board.RED_SINGLES,     0b0000000000000000000000000010000000000000000000000101111001111110)
        self.assertEqual(board.RED_DOUBLES,     0b0000000000000000000000000000000000000000000000000000000000000000)
        self.assertEqual(board.RED_BLOCKED,     0b0000000000000000000000000000000000000000000000000000000000000000)
        board.print_board()
        board.apply_move(Move("Red", Coordinate.C4, Coordinate.D3))
        self.assertEqual(board.BLUE_SINGLES,    0b0011111001001110001000000000000000000000000000000000000000000000)
        self.assertEqual(board.BLUE_DOUBLES,    0b0000000000000000000000000000000000000000000000000000000000000000)
        self.assertEqual(board.BLUE_BLOCKED,    0b0000000000000000000100000000000000000000000000000000000000000000)
        self.assertEqual(board.RED_SINGLES,     0b0000000000000000000000000000000000000000000000000101111001111110)
        self.assertEqual(board.RED_DOUBLES,     0b0000000000000000000100000000000000000000000000000000000000000000)
        self.assertEqual(board.RED_BLOCKED,     0b0000000000000000000000000000000000000000000000000000000000000000)
        board.print_board()
        board.apply_move(Move("Blue", Coordinate.E2, Coordinate.D3))
        self.assertEqual(board.BLUE_SINGLES,    0b0011111001000110001000000000000000000000000000000000000000000000)
        self.assertEqual(board.BLUE_DOUBLES,    0b0000000000000000000100000000000000000000000000000000000000000000)
        self.assertEqual(board.BLUE_BLOCKED,    0b0000000000000000000100000000000000000000000000000000000000000000)
        self.assertEqual(board.RED_SINGLES,     0b0000000000000000000000000000000000000000000000000101111001111110)
        self.assertEqual(board.RED_DOUBLES,     0b0000000000000000000000000000000000000000000000000000000000000000)
        self.assertEqual(board.RED_BLOCKED,     0b0000000000000000000000000000000000000000000000000000000000000000)
        board.print_board()
        board.apply_move(Move("Red", Coordinate.E7, Coordinate.E6))
        self.assertEqual(board.BLUE_SINGLES,    0b0011111001000110001000000000000000000000000000000000000000000000)
        self.assertEqual(board.BLUE_DOUBLES,    0b0000000000000000000100000000000000000000000000000000000000000000)
        self.assertEqual(board.BLUE_BLOCKED,    0b0000000000000000000100000000000000000000000000000000000000000000)
        self.assertEqual(board.RED_SINGLES,     0b0000000000000000000000000000000000000000000010000101011001111110)
        self.assertEqual(board.RED_DOUBLES,     0b0000000000000000000000000000000000000000000000000000000000000000)
        self.assertEqual(board.RED_BLOCKED,     0b0000000000000000000000000000000000000000000000000000000000000000)
        board.print_board()
        board.apply_move(Move("Blue", Coordinate.D3, Coordinate.E5))
        self.assertEqual(board.BLUE_SINGLES,    0b0011111001000110001100000000000000001000000000000000000000000000)
        self.assertEqual(board.BLUE_DOUBLES,    0b0000000000000000000000000000000000000000000000000000000000000000)
        self.assertEqual(board.BLUE_BLOCKED,    0b0000000000000000000000000000000000000000000000000000000000000000)
        self.assertEqual(board.RED_SINGLES,     0b0000000000000000000000000000000000000000000010000101011001111110)
        self.assertEqual(board.RED_DOUBLES,     0b0000000000000000000000000000000000000000000000000000000000000000)
        self.assertEqual(board.RED_BLOCKED,     0b0000000000000000000000000000000000000000000000000000000000000000)
        board.print_board()
        board.apply_move(Move("Red", Coordinate.E6, Coordinate.E5))
        self.assertEqual(board.BLUE_SINGLES,    0b0011111001000110001100000000000000001000000000000000000000000000)
        self.assertEqual(board.BLUE_DOUBLES,    0b0000000000000000000000000000000000000000000000000000000000000000)
        self.assertEqual(board.BLUE_BLOCKED,    0b0000000000000000000000000000000000000000000000000000000000000000)
        self.assertEqual(board.RED_SINGLES,     0b0000000000000000000000000000000000000000000010000101011001111110)
        self.assertEqual(board.RED_DOUBLES,     0b0000000000000000000000000000000000000000000000000000000000000000)
        self.assertEqual(board.RED_BLOCKED,     0b0000000000000000000000000000000000000000000000000000000000000000)
        board.print_board()
        board.apply_move(Move("Blue", Coordinate.E5, Coordinate.E6))
        self.assertEqual(board.BLUE_SINGLES,    0b0011111001000110001100000000000000001000000000000000000000000000)
        self.assertEqual(board.BLUE_DOUBLES,    0b0000000000000000000000000000000000000000000000000000000000000000)
        self.assertEqual(board.BLUE_BLOCKED,    0b0000000000000000000000000000000000000000000000000000000000000000)
        self.assertEqual(board.RED_SINGLES,     0b0000000000000000000000000000000000000000000010000101011001111110)
        self.assertEqual(board.RED_DOUBLES,     0b0000000000000000000000000000000000000000000000000000000000000000)
        self.assertEqual(board.RED_BLOCKED,     0b0000000000000000000000000000000000000000000000000000000000000000)
        board.print_board()
        board.apply_move(Move("Red", Coordinate.E6, Coordinate.F6))
        self.assertEqual(board.BLUE_SINGLES,    0b0011111001000110001100000000000000001000000000000000000000000000)
        self.assertEqual(board.BLUE_DOUBLES,    0b0000000000000000000000000000000000000000000000000000000000000000)
        self.assertEqual(board.BLUE_BLOCKED,    0b0000000000000000000000000000000000000000000000000000000000000000)
        self.assertEqual(board.RED_SINGLES,     0b0000000000000000000000000000000000000000000001000101011001111110)
        self.assertEqual(board.RED_DOUBLES,     0b0000000000000000000000000000000000000000000000000000000000000000)
        self.assertEqual(board.RED_BLOCKED,     0b0000000000000000000000000000000000000000000000000000000000000000)
        board.print_board()
        board.apply_move(Move("Blue", Coordinate.E5, Coordinate.E6))
        self.assertEqual(board.BLUE_SINGLES,    0b0011111001000110001100000000000000000000000010000000000000000000)
        self.assertEqual(board.BLUE_DOUBLES,    0b0000000000000000000000000000000000000000000000000000000000000000)
        self.assertEqual(board.BLUE_BLOCKED,    0b0000000000000000000000000000000000000000000000000000000000000000)
        self.assertEqual(board.RED_SINGLES,     0b0000000000000000000000000000000000000000000001000101011001111110)
        self.assertEqual(board.RED_DOUBLES,     0b0000000000000000000000000000000000000000000000000000000000000000)
        self.assertEqual(board.RED_BLOCKED,     0b0000000000000000000000000000000000000000000000000000000000000000)
        board.print_board()
        board.apply_move(Move("Red", Coordinate.F6, Coordinate.E6))
        self.assertEqual(board.BLUE_SINGLES,    0b0011111001000110001100000000000000000000000010000000000000000000)
        self.assertEqual(board.BLUE_DOUBLES,    0b0000000000000000000000000000000000000000000000000000000000000000)
        self.assertEqual(board.BLUE_BLOCKED,    0b0000000000000000000000000000000000000000000000000000000000000000)
        self.assertEqual(board.RED_SINGLES,     0b0000000000000000000000000000000000000000000001000101011001111110)
        self.assertEqual(board.RED_DOUBLES,     0b0000000000000000000000000000000000000000000000000000000000000000)
        self.assertEqual(board.RED_BLOCKED,     0b0000000000000000000000000000000000000000000000000000000000000000)
        board.print_board()
        board.apply_move(Move("Blue", Coordinate.E6, Coordinate.F6))
        self.assertEqual(board.BLUE_SINGLES,    0b0011111001000110001100000000000000000000000010000000000000000000)
        self.assertEqual(board.BLUE_DOUBLES,    0b0000000000000000000000000000000000000000000000000000000000000000)
        self.assertEqual(board.BLUE_BLOCKED,    0b0000000000000000000000000000000000000000000000000000000000000000)
        self.assertEqual(board.RED_SINGLES,     0b0000000000000000000000000000000000000000000001000101011001111110)
        self.assertEqual(board.RED_DOUBLES,     0b0000000000000000000000000000000000000000000000000000000000000000)
        self.assertEqual(board.RED_BLOCKED,     0b0000000000000000000000000000000000000000000000000000000000000000)

    def test_reset(self):
        board = Board()
        board.initialize()
        board.apply_move(Move("Blue", Coordinate.B1, Coordinate.B2))
        board.apply_move(Move("Red", Coordinate.C7, Coordinate.B7))
        board.apply_move(Move("Blue", Coordinate.B2, Coordinate.D3))
        board.apply_move(Move("Red", Coordinate.B7, Coordinate.C5))
        board.apply_move(Move("Blue", Coordinate.D2, Coordinate.D3))
        board.reset()
        self.assertEqual(board.BLUE_SINGLES, 0b0111111001111110000000000000000000000000000000000000000000000000)
        self.assertEqual(board.RED_SINGLES, 0b0000000000000000000000000000000000000000000000000111111001111110)
        self.assertEqual(board.BLUE_DOUBLES,0b0000000000000000000000000000000000000000000000000000000000000000)
        self.assertEqual(board.RED_DOUBLES, 0b0000000000000000000000000000000000000000000000000000000000000000)
        self.assertEqual(board.BLUE_BLOCKED, 0b0000000000000000000000000000000000000000000000000000000000000000)
        self.assertEqual(board.RED_BLOCKED, 0b0000000000000000000000000000000000000000000000000000000000000000)
        self.assertEqual(board.last_move, Move("None", Coordinate.XX, Coordinate.XX))

    def test_wiki_1(self):
        board = Board()
        splited_fen = "bb5/1bb6/bb6b/b6r/rb6/6rb1/4rr3/6 b".split()
        output = "H3-G3,H3-H4,A4-A5,C4-A5,C4-B6,H5-G7,B1-C3,A3-B5,C4-D6,B1-D2,B2-D3,C4-E5,H5-F6,B2-A4"
        board.fen_notation_into_bb(splited_fen[0])
        selected_legal_moves = check_color(board,splited_fen[1])
        print(sorted(output.split(',')))
        print(sorted(board.get_legal_moves_list(selected_legal_moves)))
        self.assertEqual(sorted(board.get_legal_moves_list(selected_legal_moves)),   sorted(output.split(',')))

    def test_wiki_2(self):
        board = Board()
        splited_fen = "8/2b02b02/2r02r02/8/8/2b02b02/2r02r02/8 b".split()
        output = "C6-B6,C6-D6,F6-E6,F6-G6,C2-B2,C2-D2,F2-E2,F2-G2"
        board.fen_notation_into_bb(splited_fen[0])
        selected_legal_moves = check_color(board,splited_fen[1])
        print(sorted(output.split(',')))
        print(sorted(board.get_legal_moves_list(selected_legal_moves)))
        self.assertEqual(sorted(board.get_legal_moves_list(selected_legal_moves)),   sorted(output.split(',')))




if __name__ == '__main__':
    unittest.main()
