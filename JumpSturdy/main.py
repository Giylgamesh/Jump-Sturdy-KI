from game_state.board import Board
from ai.player import AIPlayer
from communication.middle_man import MiddleMan


def main():
    board = Board()
    ai_player = AIPlayer()
    middle_man = MiddleMan(board, ai_player)

    while not board.is_game_over():
        pass


if __name__ == "__main__":
    main()
