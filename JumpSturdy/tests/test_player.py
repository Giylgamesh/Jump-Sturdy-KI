import unittest
from JumpSturdy.ai.player import AIPlayer


test_data = [
    # ... (Add all your test data dictionaries here)
    {"fen": "6/7b0/8/8/1r06/4b03/2rr1rrr02/5r0 b",
     "best_move": "E6-D6"},
    {"fen": "6/4bbb02/b02b01b02/1b02b03/2b01rrrr2/6r01/r01r0r0r03/5r0 r",
     "best_move": "E5-F3"},  # Only one of the best moves is needed for testing
    # ... (Add the rest of your test data)
]


class TestAIPlayer(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.blue_player = AIPlayer("blue", self.board)
        self.red_player = AIPlayer("red", self.board)

    def test_get_best_move(self):
        # Test if the best move is returned
        for data in test_data:
            self.board.fen_notation_into_bb(data["fen"])
            best_move = self.blue_player.get_best_move(self.board)  
            self.assertEqual(best_move, data["best_move"])

    def test_get_random_move(self):
        # Test if a random move is returned
        random_move = self.blue_player.get_random_move()
        self.assertIsInstance(random_move, Move)

    def test_get_score(self):
        # Test if the score is calculated correctly
        score = self.blue_player.get_score(self.board)
        self.assertIsInstance(score, int)

    def test_alphabeta_loop(self):
        # Test if the alphabeta loop runs without errors
        self.blue_player.alphabeta_loop(3)

    def test_alphabeta(self):
        # Test if the alphabeta algorithm returns a valid move
        move = self.blue_player.alphabeta(3, float('-inf'), float('inf'), True)
        self.assertIsInstance(move, Move)

    def test_value_iteration(self):
        # Test if value iteration runs without errors
        self.blue_player.value_iteration(self.red_player, self.board)

    def test_simulate_game(self):
        # Test if simulate game runs without errors
        self.blue_player.simulate_game(self.board, self.red_player)

    def test_most_advanced_pieces(self):
        # Test if most advanced pieces returns the correct result
        result = self.blue_player.most_advanced_pieces(bitboard, True)
        self.assertIsInstance(result, int)

    def test_advancement_of_pieces(self):
        # Test if advancement of pieces returns the correct result
        result = self.blue_player.advancement_of_pieces(bitboard, True)
        self.assertIsInstance(result, int)

    def test_piece_density(self):
        # Test if piece density returns the correct result
        result = self.blue_player.piece_density(singles_binary, doubles_binary)
        self.assertIsInstance(result, float)

if __name__ == "__main__":
    unittest.main()