import unittest
import time
import random

from JumpSturdy.ai.player import AIPlayer
from JumpSturdy. game_state. board import Board

def create_random_fen():
    fen = ""
    blue_pieces = random.randrange(4, 13, 1)
    red_pieces = random.randrange(4, 13, 1)
    for i in range(8):
        j = 0
        if i == 0 or i == 7:
            while j < 6:
                if i == 0:
                    red_only = False
                    blue_only = True
                else:
                    red_only = True
                    blue_only = False
                if empty_String() == True:
                    fen += "1"
                else:
                    random_piece = get_random_piece(get_random_piece_number(blue_pieces,red_pieces,red_only,blue_only))
                    fen += random_piece
                    if random_piece == "b0":
                        blue_pieces = blue_pieces-1
                    elif random_piece == "bb":
                        blue_pieces = blue_pieces-2
                    elif random_piece == "br":
                        blue_pieces = blue_pieces-1
                        red_pieces = red_pieces-1
                    elif random_piece == "r0":
                        red_pieces = red_pieces - 1
                    elif random_piece == "rr":
                        red_pieces = red_pieces-2
                    elif random_piece == "rb":
                        blue_pieces = blue_pieces-1
                        red_pieces = red_pieces - 1
                j+=1
        else:
            while j < 8:
                if empty_String() == True:
                    fen += "1"
                else:
                    random_piece = get_random_piece(
                        get_random_piece_number(blue_pieces, red_pieces, False, False))
                    fen += random_piece
                    if random_piece == "b0":
                        blue_pieces = blue_pieces-1
                    elif random_piece == "bb":
                        blue_pieces = blue_pieces-2
                    elif random_piece == "br":
                        blue_pieces = blue_pieces-1
                        red_pieces = red_pieces-1
                    elif random_piece == "r0":
                        red_pieces = red_pieces - 1
                    elif random_piece == "rr":
                        red_pieces = red_pieces-2
                    elif random_piece == "rb":
                        blue_pieces = blue_pieces-1
                        red_pieces = red_pieces - 1
                j+=1
        fen += "/"
    return transform_string(fen)
def empty_String():
    chance = random.randrange(0, 101, 1)
    return True if chance > 0 and chance<75 else False

def get_random_piece(random_piece:int):
    if random_piece == 1:
        return "b0"
    elif random_piece == 2:
        return "bb"
    elif random_piece == 3:
        return "br"
    elif random_piece == 4:
        return "r0"
    elif random_piece == 5:
        return "rr"
    elif random_piece == 6:
        return "rb"
    else:
        return "1"

def get_random_piece_number(blue_pieces:int, red_pieces:int, red_only:bool, blue_only:bool):
    start=0
    end = 0
    if blue_only:
        end=5
    elif red_only:
        start=4
        end=1
    if (red_pieces == 0 and red_only == True) or (blue_pieces == 0 and blue_only == True) or (
            blue_pieces == 0 and red_pieces == 0):
        return 7
    while True:
        random_index = random.randrange(0+start, 7-end, 1)
        if random_index == 1 and blue_pieces>0:
            return  random_index
        elif random_index == 2 and blue_pieces>1:
            return random_index
        elif (random_index == 3 or random_index == 6) and blue_pieces>0 and red_pieces>0:
            return random_index
        elif random_index == 4 and red_pieces>0:
            return random_index
        elif random_index == 5 and red_pieces>1:
            return random_index


def transform_string(input_string: str) -> str:
    # Remove the trailing "/" if it exists
    if input_string.endswith("/"):
        input_string = input_string[:-1]

    # Initialize the result string and a counter for consecutive '1's
    result = ""
    count_ones = 0

    for char in input_string:
        if char == '1':
            count_ones += 1
        else:
            if count_ones > 0:
                result += str(count_ones)
                count_ones = 0
            result += char

    # Add any remaining count of ones to the result
    if count_ones > 0:
        result += str(count_ones)

    return result

def swap_board(fen):
    swaped_fen = ""
    for i in range(7, -1, -1):
        if i == 0:
            swaped_fen += fen.split(" ")[0].split("/")[i]
        else:
            swaped_fen += fen.split(" ")[0].split("/")[i]+"/"
    #print(swaped_fen)
    return swaped_fen


def text_minMax(fen):
    board = Board()
    fen = fen
    board.fen_notation_into_bb(fen)
    board.print_board()
    blue_player = AIPlayer("Blue", board)
    best_move = blue_player.get_best_move(4, False, False)
    print(best_move)

def text_alpha_beta(fen):
    board = Board()
    fen = fen
    board.fen_notation_into_bb(fen)
    board.print_board()
    blue_player = AIPlayer("Blue", board)
    best_move = blue_player.get_best_move(4, False, True)
    print(best_move)

def test_problemstellung(fen,redFirst:int):
    board = Board()
    board.fen_notation_into_bb(fen)
    print(f"FEN: {fen}")
    blue_player = AIPlayer("Blue", board)
    red_player = AIPlayer("Red", board)

    i = redFirst
    total = 0
    winner = 0

    while True:
        # Determine which player's turn
        if i % 2 == 0:
            turn = blue_player
        else:
            turn = red_player

        # Print the current game state
        board.print_board()
        print("-----------------------")

        # Check if the game is over
        game_over = board.is_game_over()
        if game_over[0]:
            print(f"game over, {game_over[1]} wins")
            break

        print("-----------------------")
        print(f"Its {turn.color}'s turn.")

        # Get next move from the current player
        if turn == blue_player:
            # next_move = board.ask_for_move()
            next_move = turn.get_best_move(4, False, False)
        else:
            next_move = turn.get_random_move()

        move = next_move

        # Apply move
        response = board.apply_move(move)
        print("-----------------------")
        print(next_move)
        print("-----------------------")
        if response.startswith('Error'):
            break

        # Increment turn
        i += 1
    l = 0.5 if "Blue" in board.is_game_over()[1] else 0
    print(f"------- Züge: {i / 2 + l} -------")
    total += i
    i = 0
    winner += 1 if "Blue" in board.is_game_over()[1] else 0

class TestAI(unittest.TestCase):

    def test_bewertungsfunktion_speed(self):
        #Test zum Messen der Geschwindigkeit der Bewertungsfunktion
        #Soll Zukünftig helfen ggf. Optimierungen durchzuführen
        board = Board()
        board.fen_notation_into_bb("3bb2/b02b02b01/3b02bbb0/1b06/1r0r02r01r0/6r01/5r0r0r0/6")
        blue_player = AIPlayer("Blue", board)
        times = []
        start = time.time()
        for i in range(1000):
            startzeit = time.time()
            blue_player.get_score(board)
            times.append((time.time() - startzeit) * 1000)
        print("Gesamtlaufzeit " + str((time.time() - start) * 1000)+ "ms")
        print("Durchschnitt: " + str(sum(times) / len(times))+ "ms")

    def test_bewertungsfunktion_correctness(self):
        #Dient uns zum Nachvollziehen der Bewertungsfunktion auf verschiedenen random Stellungen
        for i in range(1000):
            board = Board()
            fen = create_random_fen()
            print(fen)
            board.fen_notation_into_bb(fen)
            blue_player = AIPlayer("Blue", board)
            print(blue_player.get_score(board))

    def test_bewertungsfunktion_in_depth_0(self):
        board = Board()
        fen = create_random_fen()
        print(fen)
        board.fen_notation_into_bb(fen)
        board.print_board()
        blue_player = AIPlayer("Blue", board)
        start = time.time()
        best_move = blue_player.get_best_move(1, False, False)
        print("Gesamtlaufzeit " + str((time.time() - start) * 1000)+ "ms")
        print(best_move)

    def test_compare_bewertungsfunktion_in_depth_0(self):
        board = Board()
        board.fen_notation_into_bb(create_random_fen())
        board.print_board()
        blue_player = AIPlayer("Blue", board)
        start = time.time()
        best_move = blue_player.get_best_move(1, False, False)
        print("Gesamtlaufzeit " + str((time.time() - start) * 1000)+ "ms")
        print(best_move)
        start = time.time()
        best_move_from_ai_2 = blue_player.get_best_move(1, False, False)
        print("Gesamtlaufzeit " + str((time.time() - start) * 1000)+ "ms")
        print(best_move_from_ai_2)

    def test_minMax_correctness_color_in_depth_0(self):
        board = Board()
        fen = create_random_fen()
        board.fen_notation_into_bb(fen)
        board.print_board()
        blue_player = AIPlayer("Blue", board)
        red_player = AIPlayer("Red", board)
        start_ai_1 = time.time()
        best_move = blue_player.get_best_move(1, False, False)
        print("Gesamtlaufzeit " + str((time.time() - start_ai_1) * 1000)+ "ms")
        print(best_move)
        start_ai_2 = time.time()
        best_move_from_ai_2 = red_player.get_best_move(1, False, False)
        print("Gesamtlaufzeit " + str((time.time() - start_ai_2) * 1000)+ "ms")
        print(best_move_from_ai_2)

    def test_minMax_speed_random(self):
        for i in range(1000):
            board = Board()
            fen = create_random_fen()
            board.fen_notation_into_bb(fen)
            board.print_board()
            blue_player = AIPlayer("Blue", board)
            best_move = blue_player.get_best_move(2, False, False)
            print(best_move)
    def test_minMax_fen_1(self):
        text_minMax("b0b0b0b0b0b0/1b0b0b0b0b0b01/8/8/8/8/1r0r0r0r0r0r01/r0r0r0r0r0r0")

    def test_minMax_fen_2(self):
        text_minMax("b01bbb01b0/1b02b03/3bbr01b01/8/3rr1b0b01/8/2r01r01rr1/r0r0r01r01")

    def test_minMax_fen_3(self):
        text_minMax("2b02bb/1bb2b03/5bb2/8/1r03r02/6r01/8/r01r01rrr0")

    def test_alpha_beta_fen_1(self):
        text_alpha_beta("b0b0b0b0b0b0/1b0b0b0b0b0b01/8/8/8/8/1r0r0r0r0r0r01/r0r0r0r0r0r0")

    def test_alpha_beta_fen_2(self):
        text_alpha_beta("b01bbb01b0/1b02b03/3bbr01b01/8/3rr1b0b01/8/2r01r01rr1/r0r0r01r01")

    def test_alpha_beta_fen_3(self):
        text_alpha_beta("2b02bb/1bb2b03/5bb2/8/1r03r02/6r01/8/r01r01rrr0")

    def test_compare_minMax_alphaBeta(self):
        text_minMax("b0b0b0b0b0b0/1b0b0b0b0b0b01/8/8/8/8/1r0r0r0r0r0r01/r0r0r0r0r0r0")
        text_alpha_beta("b0b0b0b0b0b0/1b0b0b0b0b0b01/8/8/8/8/1r0r0r0r0r0r01/r0r0r0r0r0r0")

    def test_compare_minMax_alphaBeta(self):
        text_minMax("b01bbb01b0/1b02b03/3bbr01b01/8/3rr1b0b01/8/2r01r01rr1/r0r0r01r01")
        text_alpha_beta("b01bbb01b0/1b02b03/3bbr01b01/8/3rr1b0b01/8/2r01r01rr1/r0r0r01r01")

    def test_compare_minMax_alphaBeta(self):
        text_minMax("2b02bb/1bb2b03/5bb2/8/1r03r02/6r01/8/r01r01rrr0")
        text_alpha_beta("2b02bb/1bb2b03/5bb2/8/1r03r02/6r01/8/r01r01rrr0")

    def test_problemstellung_AC_1(self):
        test_problemstellung(create_random_fen(),0)

    def test_problemstellung_AC_2(self):
        test_problemstellung("3b01b0/3b04/3bb4/2r05/rbbr5rb/4rr3/br4r02/6",0)

    def test_problemstellung_H_1(self):
        test_problemstellung("1bb4/1b0b05/b01b0bb4/1b01b01b02/3r01rr2/b0r0r02rr2/4r01rr1/4r0r0",0)

    def test_problemstellung_H_2(self):
        test_problemstellung("1bb4/1b0b05/b01b0bb4/1b01b01b02/3r01rr2/b0r0r02rr2/4r01rr1/4r0r0",1)

    def test_problemstellung_H_3(self):
        test_problemstellung("6/3b0b03/3r02bb1/b0b03bb2/rrrr1bb2rr1/2b01b01r01/2r01r02r0/4r01",0)

    def test_problemstellung_H_4(self):
        test_problemstellung("6/3b0b03/3r02bb1/b0b03bb2/rrrr1bb2rr1/2b01b01r01/2r01r02r0/4r01",1)

    '''Stellungsbeschreibung: Blau gewinnt in 5 (Halb-)Zügen
        Bester Zug: E6-D6''' 
    def test_problemstellung_F_1(self):
        test_problemstellung("6/7b0/8/8/1r06/4b03/2rr1rrr02/5r0",0)

    """Stellungsbeschreibung: Rot gewinnt in 5 (Halb-)Zügen
Bester Zug: E5-F3 oder E5-D3"""
    def test_problemstellung_F_2(self):
        test_problemstellung("6/4bbb02/b02b01b02/1b02b03/2b01rrrr2/6r01/r01r0r0r03/5r0",1)

    """Stellungsbeschreibung: Blau gewinnt in 2 Zügen
Bester Zug: C6-C7"""
    def test_problemstellung_T_1(self):
        test_problemstellung("1b0b0b02/8/3b04/3b04/r0r06/2b05/5r0r01/6",0)

    """Stellungsbeschreibung: Blau gewinnt in einem Zug durch Blocken
Bester Zug: E2-F4"""
    def test_problemstellung_T_2(self):
        test_problemstellung("6/4bb3/8/8/4b0r0b01/8/8/6",0)

    """Stellungsbeschreibung: Blau gewinnt in 2 Zügen
Bester Zug: C6-D7"""
    def test_problemstellung_AG_1(self):
        test_problemstellung("6/8/8/8/b0b02b0b0/2b05/2r0r0r0r02/6",0)

    """Stellungsbeschreibung: Blau gewinnt in 2 Zügen
Bester Zug: D6-D7"""
    def test_problemstellung_AG_2(self):
        test_problemstellung("3b01b0/3bb1b02/8/8/8/2r0b0r02/8/0r04r0",0)

    """Stellungsbeschreibung: Blau gewinnt in 3 Zügen
Beste Züge: C5-C6 oder C5-B5"""
    def test_problemstellung_C_1(self):
        test_problemstellung("6/4b01b01/8/5b01b0/2b04r0/1b04r01/5r01rr/1r04",0)

    """Stellungsbeschreibung: Blau gewinnt in 4 Zügen
Bester Zug: B4-C5"""
    def test_problemstellung_C_2(self):
        test_problemstellung("3bb2/b02b02b01/3b02bbb0/1b06/1r0r02r01r0/6r01/5r0r0r0/6",0)

    """Stellungsbeschreibung: Blau gewinnt in 2 Zügen
Bester Zug: D4-C6"""
    def test_problemstellung_S_1(self):
        test_problemstellung(" 2b03/1b0b05/6b01/3bb2r01/3r02r01/2b05/2r03r01/3r02",0)

    """Stellungsbeschreibung: Blau gewinnt in 3 Zügen
Bester Zug: B5-C5"""
    def test_problemstellung_S_2(self):
        test_problemstellung("2b03/1b0b05/6b01/3b02r01/1b01r02r01/2b05/2r03r01/3r02",0)

    """Stellungsbeschreibung: Rot gewinnt durch Schlagen
Bester Zug: B5-C4"""
    def test_problemstellung_Z_1(self):
        test_problemstellung("6/8/6r01/2b01r0r02/1r03r02/8/8/6",1)

    """Stellungsbeschreibung: Blau muss verteidigen
Bester Zug: C1-B2"""
    def test_problemstellung_Z_2(self):
        test_problemstellung("1b02b0b0/1r06/1b04b01/8/2r02b02/1r01r01r02/5r0r01/r0r01r011",0)

    """Stellungsbeschreibung: C4-B3
Bester Zug: Rot gewinnt in 3 Zügen"""
    def test_problemstellung_Z_3(self):
        test_problemstellung("3b0b01/8/1b0b01b0b02/2r01b01b01/8/2rr2r02/1r06/2r03",1)

    """Stellungsbeschreibung: Gewinn in 2
Bester Zug: A3-B2"""
    def test_problemstellung_J_1(self):
        test_problemstellung("6/1bb1b0bbb0b01/r02b04/2b01b0b02/2r02r02/1r02rrr02/6rr1/2r01r01",1)

    """Stellungsbeschreibung: Gewinn in 3
Bester Zug: B3-A3"""
    def test_problemstellung_J_2(self):
        test_problemstellung("3b02/1bb6/1r0b02r02/2r05/4r03/8/2r03r01/6",1)

