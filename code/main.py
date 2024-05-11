from Jump_Sturdy_Board_Class import JumpSturdyBoard
from Jump_Sturdy_Player_Agent_Class import JumpSturdyPlayerAgent

if __name__ == '__main__':
    # erzeugen ein Objekt der Klasse JumpSturdyBoard
    board = JumpSturdyBoard()
    # setzen steine auf das Brett
    print(bin(board.pieceBB[0]| board.pieceBB[1]| board.pieceBB[2] |board.pieceBB[3] |board.pieceBB[4] |board.pieceBB[5])[2:])
    print(bin((~board.occupiedBB& 0b111111111111111111111111111111111111111111111111111111111111))[2:])
    print()
    #board.fen_notation_into_bb("2bb3/5b02/1bb1bb2b0b0/2br3r01/2b0r04/5r0rr1/2rr2r02/3r02")
    board.fen_notation_into_bb("b0b0b0b0b0b0/b0r0r0r0r0r0r01/8/8/8/8/1r0r0r0r0r0r01/r0r0r0r0r0r0")
    print(bin(board.pieceBB[0])[2:])
    print(bin(board.pieceBB[1])[2:])
    print(bin(board.pieceBB[2])[2:])
    print(bin(board.pieceBB[3])[2:])
    print(bin(board.pieceBB[4])[2:])
    print(bin(board.pieceBB[5])[2:])
    print()
    print(bin(board.emptyBB)[2:])
    print(bin(board.occupiedBB)[2:])
    print(bin(board.blue_pieces))
    print(bin((board.pieceBB[0]>>7)&board.blue_pieces&(~board.file_a& 0b111111111111111111111111111111111111111111111111111111111111)))
    # stelle board dar
    board.print_board()
    print()
    moves = board.posible_moves_r()
    print()
    print(moves)
