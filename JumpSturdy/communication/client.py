import json
import pygame
from JumpSturdy.ai.mcts_player import MCTS, Player
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
                ai_player = EvolvedAIPlayer("Red", board,game["time"],turn,{'bias': 1, 'friendly_singles_value': 0.7341041163830963, 'friendly_doubles_value': 2.274233660960818, 'friendly_material_score': 1.5026103652388332, 'enemy_singles_value': -0.7291608705251027, 'enemy_doubles_value': -2.265430977891856, 'enemy_material_score': -1.5074077330290985, 'friendly_most_advanced_singles': 0.748247621491522, 'friendly_most_advanced_doubles': 1.515407356131302, 'enemy_most_advanced_singles': -1.510285668824605, 'enemy_most_advanced_doubles': -1.50961031645031, 'friendly_advancement_of_singles': 3.7785644200333097, 'friendly_advancement_of_doubles': 3.728760057392521, 'enemy_advancement_of_singles': -1.4892627538963819, 'enemy_advancement_of_doubles': -1.5077596634911712, 'control_of_center': 1.488164124061923, 'control_of_edges': 1.4856870496218675, 'friendly_single_in_edges': 2.2544290664740716, 'friendly_double_in_edges': 0.7380353065066093, 'friendly_single_in_center': 1.504606566797584, 'friendly_double_in_center': 1.506622449400612, 'enemy_single_in_edges': -2.2586791963463746, 'enemy_double_in_edges': -0.7524670320911624, 'enemy_single_in_center': -1.49559265658973, 'enemy_double_in_center': -0.7445612570569379, 'friendly_double_in_back_corner': -0.7563267575338303, 'friendly_doubles_in_line': 2.9624074414727244, 'friendly_single_double_in_line': 3.7508566377756627, 'friendly_singles_in_line': 0.7524614046343802, 'friendly_piece_is_last': 14.910873615920098, 'friendly_density': 2.2578436465288503, 'friendly_mobility': 0.7504994504492232, 'enemy_density': -0.7497067955526692, 'enemy_mobility': -2.2321338830066946, 'friendly_single_under_attack': -2.9762775175952796, 'friendly_double_under_attack': -2.9890296486546855})
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
                ai_player = EvolvedAIPlayer("Blue", board,game["time"],turn,{'bias': 1, 'friendly_singles_value': 0.7341041163830963, 'friendly_doubles_value': 2.274233660960818, 'friendly_material_score': 1.5026103652388332, 'enemy_singles_value': -0.7291608705251027, 'enemy_doubles_value': -2.265430977891856, 'enemy_material_score': -1.5074077330290985, 'friendly_most_advanced_singles': 0.748247621491522, 'friendly_most_advanced_doubles': 1.515407356131302, 'enemy_most_advanced_singles': -1.510285668824605, 'enemy_most_advanced_doubles': -1.50961031645031, 'friendly_advancement_of_singles': 3.7785644200333097, 'friendly_advancement_of_doubles': 3.728760057392521, 'enemy_advancement_of_singles': -1.4892627538963819, 'enemy_advancement_of_doubles': -1.5077596634911712, 'control_of_center': 1.488164124061923, 'control_of_edges': 1.4856870496218675, 'friendly_single_in_edges': 2.2544290664740716, 'friendly_double_in_edges': 0.7380353065066093, 'friendly_single_in_center': 1.504606566797584, 'friendly_double_in_center': 1.506622449400612, 'enemy_single_in_edges': -2.2586791963463746, 'enemy_double_in_edges': -0.7524670320911624, 'enemy_single_in_center': -1.49559265658973, 'enemy_double_in_center': -0.7445612570569379, 'friendly_double_in_back_corner': -0.7563267575338303, 'friendly_doubles_in_line': 2.9624074414727244, 'friendly_single_double_in_line': 3.7508566377756627, 'friendly_singles_in_line': 0.7524614046343802, 'friendly_piece_is_last': 14.910873615920098, 'friendly_density': 2.2578436465288503, 'friendly_mobility': 0.7504994504492232, 'enemy_density': -0.7497067955526692, 'enemy_mobility': -2.2321338830066946, 'friendly_single_under_attack': -2.9762775175952796, 'friendly_double_under_attack': -2.9890296486546855})
                i = ai_player.get_best_move_through_time()
                print(i)
                print(game)
                data = json.dumps(i)
                n.send(data)

while True:
    main()