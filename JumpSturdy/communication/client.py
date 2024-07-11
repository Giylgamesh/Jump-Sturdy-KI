import json
import pygame
from JumpSturdy.ai.player import AIPlayer
from JumpSturdy.ai.evolved_player import EvolvedAIPlayer
from JumpSturdy.communication.network import Network
from JumpSturdy.game_state. board import Board
pygame.font.init()

def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    turn = 0
    print("You are player", player)

    while run:
        clock.tick(60)
        try:
            #try to send get as a json to server over network, rest is error handling
            game = n.send(json.dumps("get"))
            if game is None:
                raise ValueError("Game data is None")
        except:
            run = False
            print("Couldn't get game")
            break

        #response is also a json, json.loads transforms into a python dictionary
        #dictionary consists of board string, a variable player1 which is true, when player 1 (or better 0), 
        #variable player2 with the same concept and bothConnected, also a boolean
        #{'board': 'b0b0b0b0b0b0/1b0b0b0b0b0b01/8/8/8/8/1r0r0r0r0r0r01/r0r0r0r0r0r0 r', 'player1': True, 'player2': False, 'bothConnected': False}

        game = json.loads(game)
        
        if game["end"]:
            continue

        #allow input just when both players are in
        if game["bothConnected"]:

            #allow to only give input, when it is your turn
            if player == 0 and game["player1"]:
                turn=turn+1
                #printing not necessary, game["board"] is the way to get the board string
                print("New Board: " + game["board"])
                print("New Time: " + str(game["time"]))
                board = Board()
                board.fen_notation_into_bb(game["board"].split(" ")[0])
                board.print_board()
                ai_player = EvolvedAIPlayer("Red", board,game["time"],turn,{'bias': 1, 'friendly_singles_value': 2.603969578025859, 'friendly_doubles_value': 6.908252986319241, 'friendly_material_score': 4.702191422351861, 'enemy_singles_value': -3.1059742454880244, 'enemy_doubles_value': -6.585053920054966, 'enemy_material_score': -5.082586464587797, 'friendly_most_advanced_singles': 2.3484089893411957, 'friendly_most_advanced_doubles': 4.482095480436495, 'enemy_most_advanced_singles': -4.777521338886239, 'enemy_most_advanced_doubles': -4.996821432361024, 'friendly_advancement_of_singles': 11.052931969951985, 'friendly_advancement_of_doubles': 10.891678701974092, 'enemy_advancement_of_singles': -4.9318960997701815, 'enemy_advancement_of_doubles': -4.282210719449231, 'control_of_center': 4.853225089997874, 'control_of_edges': 4.650310616293443, 'friendly_single_in_edges': 7.27697313330563, 'friendly_double_in_edges': 2.2731793113021226, 'friendly_single_in_center': 4.714144976664993, 'friendly_double_in_center': 4.471746226955499, 'enemy_single_in_edges': -6.919771876182096, 'enemy_double_in_edges': -2.941061641863923, 'enemy_single_in_center': -4.737131426074215, 'enemy_double_in_center': -2.6570364902218095, 'friendly_double_in_back_corner': -2.5817459843888235, 'friendly_doubles_in_line': 8.87453553004497, 'friendly_single_double_in_line': 10.952258050678351, 'friendly_singles_in_line': 2.960689407641968, 'friendly_piece_is_last': 42.20845388132646, 'friendly_density': 6.764715009938298, 'friendly_mobility': 3.1355488727116247, 'enemy_density': -2.72067263609914, 'enemy_mobility': -6.737861201410557, 'friendly_single_under_attack': -9.288535612156842, 'friendly_double_under_attack': -9.18440755878567}  )
                #change to any input you like. This one is just console input. Change it here to respond with your Ai's answer.
                #Answer must have format: start-end like E7-F7
                i = ai_player.get_best_move_through_time()
                print(i)
                print(game)
                #json.dumps(i) transforms the input into a json. You can print it, if you want to see the difference
                data = json.dumps(i)

                #send data via network
                n.send(data)
            elif player == 1 and game["player2"]:
                turn=turn+1
                print("New Board: " + game["board"])
                print("New Time: " + str(game["time"]))
                board = Board()
                board.fen_notation_into_bb(game["board"].split(" ")[0])
                board.print_board()
                ai_player = AIPlayer("Blue", board,game["time"],turn)
                i = ai_player.get_best_move_through_time()
                print(i)
                print(game)
                data = json.dumps(i)
                n.send(data)

while True:
    main()