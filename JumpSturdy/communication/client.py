import json
import pygame
from JumpSturdy.ai.player import AIPlayer
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
                ai_player = AIPlayer("Red", board,game["time"],turn)
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