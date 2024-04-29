import unittest
from board import Board
from board import Move
from board import Coordinate


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




if __name__ == '__main__':
    unittest.main()