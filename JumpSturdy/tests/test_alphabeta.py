import unittest
from game_state.board import Board
from ai.alphabeta import alphabeta

class TestAlphaBeta(unittest.TestCase):
    def test_alphabeta(self):
        test_board = Board()
        test_board.fen_notation_into_bb("8/2b02b02/2r02r02/8/8/2b02b02/2r02r02/8")
        alpha = float('-inf')
        beta = float('inf')
        maximizing_player = True
        depth = 3
        result = alphabeta(test_board, alpha, beta, maximizing_player, depth)
        # self.assertEqual(result, some_expected_result_which_I_dont_know_yet)

if __name__ == "__main__":
    unittest.main()