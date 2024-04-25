import random
from Jump_Sturdy_Board_Class import JumpSturdyBoard
from Jump_Sturdy_Player_Agent_Class import JumpSturdyPlayerAgent

    
# erzeugen ein Objekt der Klasse JumpSturdyBoard
# wir erzeugen also ein 8x8 Spielbrett
board = JumpSturdyBoard()
# setzen steine auf das Brett
board.put_pieces_on_board()
# initialisieren turn_counter um züge zu zählen. Könnte relevant sein für Zeitmanagement
board_turn_count = 0
# stelle board dar
board.print_board()
#print(board.board)

# erzeugen zwei objektre der Klasse JumpSturdyPlayerAgent
# ein Spieler spielt mit den weißen Steinen, der andere mit den schwarzen
white_player = JumpSturdyPlayerAgent('white')
black_player = JumpSturdyPlayerAgent('black')

# beginne jeden Zug in dem wir checken ob das Spiel vorbei ist
# wenn spiel noch nicht vorbei ist, macht ein Spieler-Agent einen Zug

#-----------------------------------------------------------------------
# die for-schleife soll beim testen helfen
for i in range(5): 
    #solange spiel nicht vorbei ist, wird weitergespielt
    # game_end_check() gibt True == 1 zurück, wenn das Spiel vorbei ist, sonst 0 
    while board.game_end_check() == False:
        # zähle züge und schreibe sie in die konsole 
        board_turn_count += 1
        print("Turn: ", board_turn_count, ", White players turn")
        # spieler mit weißen steinen beginnt
        white_player.pick_move(board)
        
        board.print_board()
        print("this is the move history: ", board.move_history)

        # wenn spiel vorbei ist, dann beende das spiel. 
        if board.game_end_check():
            print("game is over")
            break
    
        # analog zu oben
        board_turn_count += 1
        print("Turn: ", board_turn_count, ", Black players turn")    
        black_player.pick_move(board)
        
        board.print_board()

        if board.game_end_check():
            print("game is over")
            break
    
    
 #---------------------------------------------------------------------------------
    
# while board.game_end_check() == False:
#     white_player.mpick_move(board)
    
#     board.print_board()

#     # wenn spiel vorbei ist, dann beende das spiel
#     if board.game_end_check():
#         print("you probably won or lost or it's a draw or something. Congrats!")
#         break

#     black_player.pick_move(board)
    
#     board.print_board()