import unittest
from ai.player import AIPlayer
from game_state.board import Board
from tests.test_ai import create_random_fen
from tests.test_ai import get_random_piece



# create board
board = Board()
board.initialize()
get_random_piece(1)
random_fen = create_random_fen()

# create player
player = AIPlayer("Blue", board)

# create zobrist hash
# define contants
BOARD_SIZE = 2
NUM_PIECES = 2
# init hash table
Hash_table = player.initialize_zobrist_table(BOARD_SIZE, NUM_PIECES)
print("----------------------------")
print("This is Hashtable:", Hash_table)
print("This is get_Hashtable:", player.get_zobrist_table())

# calculate hash
print("---------------------------------")
print("Calculate zobrist hash: ")
player.calculate_zobrist_hash(player.get_zobrist_table(), BOARD_SIZE, 0, NUM_PIECES)


# Tests
print("This is board: ", board.print_board())
print("This is player: ", player.color)