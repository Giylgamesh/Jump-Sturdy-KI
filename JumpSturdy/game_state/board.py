from enum import Enum
import os
from random import choice

def there_is(bitboard, n):
    """Check if the nth bit of the bitboard is set (1)."""
    mask = 1 << 64 >> (n.value)
    return (bitboard & mask) != 0

def add_nth_bit(bitboard, n):
    """Set the nth bit of the bitboard to 1."""
    mask = 1 << 64 >> n.value
    return bitboard | mask

def clear_nth_bit(bitboard, n):
    """Clear the nth bit of 'number' to 0."""
    all_ones = 0xFFFFFFFFFFFFFFFF
    nth_bit_set = 1 << 64 >> n.value
    mask = all_ones ^ nth_bit_set
    return bitboard & mask

def get_deepest_keys(d, container):
    for k, v in d.items():
        if isinstance(v, dict):
            get_deepest_keys(v, container)
        else:
            container[v] = True

    return container

def parse_move_categories(input_str, move_categories_dict):
    selected_move_categories = {}

    # If input contains "alle", add all moves
    if "alle" in input_str:
        # Flatten all the move category names into a list and add them to the dictionary
        selected_move_categories = {'singles_left_empty': True,
                                    'singles_front_empty': True,
                                    'singles_right_empty': True,
                                    'singles_kill_left_singles': True,
                                    'singles_kill_left_doubles': True,
                                    'singles_kill_right_singles': True,
                                    'singles_kill_right_doubles': True,
                                    'singles_upgrade_left': True,
                                    'singles_upgrade_front': True,
                                    'singles_upgrade_right': True,
                                    'doubles_l_l_f_empty': True,
                                    'doubles_f_f_l_empty': True,
                                    'doubles_f_f_r_empty': True,
                                    'doubles_r_r_f_empty': True,
                                    'doubles_kill_l_l_f_singles': True,
                                    'doubles_kill_l_l_f_doubles': True,
                                    'doubles_kill_f_f_l_singles': True,
                                    'doubles_kill_f_f_l_doubles': True,
                                    'doubles_kill_f_f_r_singles': True,
                                    'doubles_kill_f_f_r_doubles': True,
                                    'doubles_kill_r_r_f_singles': True,
                                    'doubles_kill_r_r_f_doubles': True,
                                    'doubles_l_l_f_singles': True,
                                    'doubles_f_f_l_singles': True,
                                    'doubles_f_f_r_singles': True,
                                    'doubles_r_r_f_singles': True
                                    }
        return selected_move_categories

    # Split input_str by comma to process each part separately
    categories = input_str.split(',')

    for category in categories:
        current_dict = move_categories_dict

        # Follow the keys to get to the deepest value
        for key in category:
            try:
                current_dict = current_dict[key]
            except KeyError:
                # If a key is not found, report it and skip this part
                print(f"Invalid key '{key}' in path '{category}'.")
                current_dict = {}
                break

        # If we end up with a dictionary, get all the end values
        if isinstance(current_dict, dict):
            # Use a recursive helper function to get all the end values
            selected_move_categories = get_deepest_keys(current_dict, selected_move_categories)
        elif isinstance(current_dict, str):
            # If we end up with a string, it's an end value
            selected_move_categories[current_dict] = True

    return selected_move_categories

def shift_pieces(bitboard, shift):
    if shift > 0:
        return bitboard >> shift
    else:
        return bitboard << -shift

def validate_string(input_string):
    allowed_chars = set("0123456789rb/")
    for char in input_string:
        if char not in allowed_chars:
            return False
    return True


class Board:
    # Class-level constants for masks
    FIRST_6_SQUARES_MASK = 0b001111110
    LAST_6_SQUARES_MASK = 9079256848778919936
    FORBIDDEN_SQUARES_MASK = 9295429630892703873
    FORBIDDEN_LEFT_MASK = 0b0000000100000001000000010000000100000001000000010000000100000001
    FORBIDDEN_RIGHT_MASK = 0b1000000010000000100000001000000010000000100000001000000010000000
    FORBIDDEN_LEFT_LEFT_MASK = 0b0000001100000011000000110000001100000011000000110000001100000011
    FORBIDDEN_RIGHT_RIGHT_MASK = 0b1100000011000000110000001100000011000000110000001100000011000000

    move_categories_dict = {
        # singles
        '1': {
            # move
            '1': {
                '1': 'singles_left_empty',
                '2': 'singles_front_empty',
                '3': 'singles_right_empty',
            },
            # kill
            '2': {
                # left
                '1': {
                    '1': 'singles_kill_left_singles',
                    '2': 'singles_kill_left_doubles'
                },
                # right
                '2': {
                    '1': 'singles_kill_right_singles',
                    '2': 'singles_kill_right_doubles',
                }
            },
            # upgrade
            '3': {
                '1': 'singles_upgrade_left',
                '2': 'singles_upgrade_front',
                '3': 'singles_upgrade_right'
            }
        },
        # doubles
        '2': {
            # move
            '1': {
                '1': 'doubles_l_l_f_empty',
                '2': 'doubles_f_f_l_empty',
                '3': 'doubles_f_f_r_empty',
                '4': 'doubles_r_r_f_empty',
            },
            # kill
            '2': {
                # l_l_f
                '1': {
                    '1': 'doubles_kill_l_l_f_singles',
                    '2': 'doubles_kill_l_l_f_doubles'
                },
                # f_f_l
                '2': {
                    '1': 'doubles_kill_f_f_l_singles',
                    '2': 'doubles_kill_f_f_l_doubles',
                },
                # f_f_r
                '3': {
                    '1': 'doubles_kill_f_f_r_singles',
                    '2': 'doubles_kill_f_f_r_doubles',
                },
                # r_r_f
                '4': {
                    '1': 'doubles_kill_r_r_f_singles',
                    '2': 'doubles_kill_r_r_f_doubles',
                }
            },
            # change double
            '3': {
                '1': 'doubles_l_l_f_singles',
                '2': 'doubles_f_f_l_singles',
                '3': 'doubles_f_f_r_singles',
                '4': 'doubles_r_r_f_singles',
            }
        }
    }

    shift_map = {
        "singles_front_empty": 8,
        "singles_left_empty": -1,
        "singles_right_empty": 1,
        "singles_front_singles": 8,
        "singles_left_singles": -1,
        "singles_right_singles": 1,
        "singles_kill_left_singles": 7,
        "singles_kill_right_singles": 9,
        "singles_kill_left_doubles": 7,
        "singles_kill_right_doubles": 9,
        "singles_upgrade_left": -1,
        "singles_upgrade_right": 1,
        "singles_upgrade_front": 8,
        "doubles_l_l_f_empty": 6,
        "doubles_f_f_l_empty": 15,
        "doubles_f_f_r_empty": 17,
        "doubles_r_r_f_empty": 10,
        "doubles_l_l_f_singles": 6,
        "doubles_f_f_l_singles": 15,
        "doubles_f_f_r_singles": 17,
        "doubles_r_r_f_singles": 10,
        "doubles_kill_l_l_f_singles": 6,
        "doubles_kill_f_f_l_singles": 15,
        "doubles_kill_f_f_r_singles": 17,
        "doubles_kill_r_r_f_singles": 10,
        "doubles_kill_l_l_f_doubles": 6,
        "doubles_kill_f_f_l_doubles": 15,
        "doubles_kill_f_f_r_doubles": 17,
        "doubles_kill_r_r_f_doubles": 10,
    }

    def __init__(self):
        # Initialize the board state
        self.BLUE_SINGLES = 0b0000000000000000000000000000000000000000000000000000000000000000
        self.BLUE_DOUBLES = 0b0000000000000000000000000000000000000000000000000000000000000000
        self.BLUE_BLOCKED = 0b0000000000000000000000000000000000000000000000000000000000000000
        self.RED_SINGLES = 0b0000000000000000000000000000000000000000000000000000000000000000
        self.RED_DOUBLES = 0b0000000000000000000000000000000000000000000000000000000000000000
        self.RED_BLOCKED = 0b0000000000000000000000000000000000000000000000000000000000000000
        self.last_state = None
        self.actual_state = self.capture_state()

    def fen_notation_into_bb(self, notation):
        # Auslesen der vorgegebenen String Notation vom Server in unsere BitBoards für Pieces
        if validate_string(notation) == True:
            # Checke,ob der FEN String ein gültiger ist
            boardPos = 63
            i = 0
            # Gehe die String Notation bis zum Schluss durch.
            while i < len(notation):
                if boardPos==63 or boardPos==56 or boardPos==7 or boardPos==0:
                    boardPos-=1
                    continue
                # Setze den String in eine Binäre Darstellung und befülle ihn 60 mal mit der "0", weil unsere BitBoards nur 60 Felder haben.
                binary = "0" * 64
                # Teile den String an der Board Position in der wir uns gerade gefinden und setze eine 1 dazwischen.
                binary = binary[boardPos + 1:] + "1" + binary[0:boardPos]
                # Schaue ob das Zeichen aus der Notation ein "r" ist.
                if notation[i] == "r":
                    # Schaue, ob das nächste Zeichen aus der Notation ebenfalls ein "r" ist, denn daraus Ergibt sich ein Pferd.
                    if notation[i] == notation[i + 1]:
                        # Wandle den String in ein binäres int um und addiere es auf das aktuelle BitBoard für rote Pferde.
                        self.RED_DOUBLES += int(binary, 2)
                        self.RED_BLOCKED += int(binary, 2)
                    # Schaue, ob das nächste Zeichen aus der Notation ein "b" ist, denn daraus Ergibt sich ein captured red pawn(Mir fällt der deutsche Name nicht ein).
                    elif notation[i + 1] == "b":
                        # Wandle den String in ein binäres int um und addiere es auf das aktuelle BitBoard für captured red pawn.
                        self.BLUE_DOUBLES += int(binary, 2)
                        self.RED_BLOCKED += int(binary, 2)
                    else:
                        # Wandle den String in ein binäres int um und addiere es auf das aktuelle BitBoard für rote Bauern.
                        self.RED_SINGLES += int(binary, 2)
                # Falls das Zeichen ein "/" soll dieser Schleifendurchlauf überprüfen werden, da es kein Zeichen ist, welches im Board notwendig ist.
                elif notation[i] == "/":
                    i += 1
                    continue
                # Falls das Zeichen aus der Notation ein "b" ist.
                elif notation[i] == "b":
                    if notation[i] == notation[i + 1]:
                        # Wandle den String in ein binäres int um und addiere es auf das aktuelle BitBoard für blaue Pferde.
                        self.BLUE_DOUBLES += int(binary, 2)
                        self.BLUE_BLOCKED += int(binary, 2)
                    elif notation[i + 1] == "r":
                        # Wandle den String in ein binäres int um und addiere es auf das aktuelle BitBoard für captured blue pawn.
                        self.RED_DOUBLES += int(binary, 2)
                        self.BLUE_BLOCKED += int(binary, 2)
                    else:
                        # Wandle den String in ein binäres int um und addiere es auf das aktuelle BitBoard für blaue Bauern.
                        self.BLUE_SINGLES += int(binary, 2)
                # Falls das Zeichen aus der Notation eine Zahl ist.
                else:
                    # Reduziere die Board Position um die angegebene Zahl für die leeren Felder.
                    boardPos -= int(notation[i])
                    i += 1
                    continue
                # Reduziere die Board Position um 1 und erhöhe die nächste Iteration für die Schleife um 2.
                boardPos -= 1
                i += 2
        else:
            self.initialize()

    def capture_state(self):
        # Capture the current state of the board attributes
        actual_state = {
            'BLUE_SINGLES': self.BLUE_SINGLES,
            'BLUE_DOUBLES': self.BLUE_DOUBLES,
            'BLUE_BLOCKED': self.BLUE_BLOCKED,
            'RED_SINGLES': self.RED_SINGLES,
            'RED_DOUBLES': self.RED_DOUBLES,
            'RED_BLOCKED': self.RED_BLOCKED,
            'last_state': self.last_state}
        return actual_state

    # Initialization and Resetting
    def initialize(self):
        # Initialize the board
        self.reset()

    def initialize_for_test_singles(self):
        # Initialize the board with all testing cases
        self.BLUE_SINGLES = 0b0000000011000010100000000000000000000100000001000000000000000000
        self.BLUE_DOUBLES = 0b0000000000100000001000000000000000000001000000010000000000000000
        self.BLUE_BLOCKED = 0b0000000000100000001000000000000000000001000000010000000000000000
        self.RED_SINGLES = 0b0000000000000100000001000000000011000010100000000000000000000000
        self.RED_DOUBLES = 0b0000000000000001000000010000000000100000001000000000000000000000
        self.RED_BLOCKED = 0b0000000000000001000000010000000000100000001000000000000000000000
        self.last_state = None
        self.actual_state = self.capture_state()

    def initialize_for_test_doubles(self):
        # Initialize the board with all testing cases
        self.BLUE_SINGLES = 0b0000000000000000100000000000000000000000000000000000100000000000
        self.BLUE_DOUBLES = 0b0000000000100000000000000100000000000000000000000000000000010000
        self.BLUE_BLOCKED = 0b0000000000100000000000000100000000000000000000000000000000010000
        self.RED_SINGLES = 0b0000000000000000000010000000000000000000000000001000000000000000
        self.RED_DOUBLES = 0b0000000000000000000000000001000000000000001000000000000001000000
        self.RED_BLOCKED = 0b0000000000000000000000000001000000000000001000000000000001000000
        self.last_state = None
        self.actual_state = self.capture_state()

    def reset(self):
        # Reset the board to its initial state
        self.BLUE_SINGLES = 0b0111111001111110000000000000000000000000000000000000000000000000
        self.BLUE_DOUBLES = 0b0000000000000000000000000000000000000000000000000000000000000000
        self.BLUE_BLOCKED = 0b0000000000000000000000000000000000000000000000000000000000000000
        self.RED_SINGLES = 0b0000000000000000000000000000000000000000000000000111111001111110
        self.RED_DOUBLES = 0b0000000000000000000000000000000000000000000000000000000000000000
        self.RED_BLOCKED = 0b0000000000000000000000000000000000000000000000000000000000000000
        self.last_state = None
        self.actual_state = self.capture_state()

    # Move-related Methods
    def apply_move(self, move):
        # Check invalid input
        if move.from_ == move.to:
            return "Error: Skipping turns is not allowed"
        if move.from_ in [Coordinate.A1, Coordinate.A8, Coordinate.H1, Coordinate.H8] or \
                move.to in [Coordinate.A1, Coordinate.A8, Coordinate.H1, Coordinate.H8]:
            return "Error: Invalid coordinates"
        # Check if the coordinates are not within the valid range (A1 to H8)
        elif not (Coordinate.A1.value <= move.from_.value <= Coordinate.H8.value and
                  Coordinate.A1.value <= move.to.value <= Coordinate.H8.value):
            return "Error: Invalid coordinates"

        # Apply the move
        # Blue piece
        if move.player == "Blue":
            # Blue single
            if there_is(self.BLUE_SINGLES, move.from_):
                # to the front or to the left or to the right
                if move.to.value == move.from_.value + 8 or move.to.value == move.from_.value - 1 or move.to.value == move.from_.value + 1:
                    # there is a blue single
                    if there_is(self.BLUE_SINGLES, move.to):
                        self.last_state = self.capture_state()
                        self.BLUE_SINGLES = clear_nth_bit(self.BLUE_SINGLES, move.from_)
                        self.BLUE_SINGLES = clear_nth_bit(self.BLUE_SINGLES, move.to)
                        self.BLUE_DOUBLES = add_nth_bit(self.BLUE_DOUBLES, move.to)
                        self.BLUE_BLOCKED = add_nth_bit(self.BLUE_BLOCKED, move.to)
                        self.actual_state = self.capture_state()
                        return "Good: New double"
                    # there are blue doubles, red singles or red doubles
                    elif (there_is(self.BLUE_DOUBLES, move.to) or
                          there_is(self.RED_SINGLES, move.to) or
                          there_is(self.RED_DOUBLES, move.to)):
                        return "Error: Invalid move"
                    # there is nothing
                    else:
                        if move.to.value == move.from_.value - 1 and move.to.value in [16,24,32,40,48,56]:
                            return "Error: Invalid move"
                        elif move.to.value == move.from_.value + 1 and move.to.value in [9,17,25,33,41,49]:
                            return "Error: Invalid move"
                        self.last_state = self.capture_state()
                        self.BLUE_SINGLES = clear_nth_bit(self.BLUE_SINGLES, move.from_)
                        self.BLUE_SINGLES = add_nth_bit(self.BLUE_SINGLES, move.to)
                        self.actual_state = self.capture_state()
                        if move.to.value == move.from_.value + 8:
                            return "Good: Frontal move"
                        elif move.to.value == move.from_.value - 1:
                            return "Good: Left move"
                        else:
                            return "Good: Right move"
                # to the left-front or right-front
                elif move.to.value == move.from_.value + 7 or move.to.value == move.from_.value + 9:
                    # there red single
                    if there_is(self.RED_SINGLES, move.to):
                        self.last_state = self.capture_state()
                        self.BLUE_SINGLES = clear_nth_bit(self.BLUE_SINGLES, move.from_)
                        self.RED_SINGLES = clear_nth_bit(self.RED_SINGLES, move.to)
                        self.BLUE_SINGLES = add_nth_bit(self.BLUE_SINGLES, move.to)
                        self.actual_state = self.capture_state()
                        return "Good: Killing move"
                    # there is red double
                    elif there_is(self.RED_DOUBLES, move.to):
                        self.last_state = self.capture_state()
                        self.BLUE_SINGLES = clear_nth_bit(self.BLUE_SINGLES, move.from_)
                        self.RED_DOUBLES = clear_nth_bit(self.RED_DOUBLES, move.to)
                        self.BLUE_DOUBLES = add_nth_bit(self.BLUE_DOUBLES, move.to)
                        self.actual_state = self.capture_state()
                        return "Good: Double killing move"
                    else:
                        return "Error: Invalid move"
                # to somewhere else
                else:
                    return "Error: Unknown move"
            # Blue double
            elif there_is(self.BLUE_DOUBLES, move.from_):
                # to left-left-front or front-front-left or to front-front-right or right-right-front
                if move.to.value == move.from_.value + 6 or move.to.value == move.from_.value + 15 or move.to.value == move.from_.value + 17 or move.to.value == move.from_.value + 10:
                    # there is blue single
                    if there_is(self.BLUE_SINGLES, move.to):
                        self.last_state = self.capture_state()
                        self.BLUE_DOUBLES = clear_nth_bit(self.BLUE_DOUBLES, move.from_)
                        self.BLUE_SINGLES = clear_nth_bit(self.BLUE_SINGLES, move.to)
                        self.BLUE_DOUBLES = add_nth_bit(self.BLUE_DOUBLES, move.to)
                        self.BLUE_BLOCKED = add_nth_bit(self.BLUE_BLOCKED, move.to)
                        # on top of blue blocked
                        if there_is(self.BLUE_BLOCKED, move.from_):
                            self.BLUE_BLOCKED = clear_nth_bit(self.BLUE_BLOCKED, move.from_)
                            self.BLUE_SINGLES = add_nth_bit(self.BLUE_SINGLES, move.from_)
                            self.actual_state = self.capture_state()
                            return "Good: change of double"
                        # on top of red blocked
                        elif there_is(self.RED_BLOCKED, move.from_):
                            self.RED_BLOCKED = clear_nth_bit(self.RED_BLOCKED, move.from_)
                            self.RED_SINGLES = add_nth_bit(self.RED_SINGLES, move.from_)
                            self.actual_state = self.capture_state()
                            return "Good: change of double"
                        else:
                            self.last_state = self.last_state.last_state.copy()
                            return "Error: Missing blocked piece"
                    # there is red single
                    elif there_is(self.RED_SINGLES, move.to):
                        self.last_state = self.capture_state()
                        self.BLUE_DOUBLES = clear_nth_bit(self.BLUE_DOUBLES, move.from_)
                        self.RED_SINGLES = clear_nth_bit(self.RED_SINGLES, move.to)
                        self.BLUE_SINGLES = add_nth_bit(self.BLUE_SINGLES, move.to)
                        # on top of blue blocked
                        if there_is(self.BLUE_BLOCKED, move.from_):
                            self.BLUE_BLOCKED = clear_nth_bit(self.BLUE_BLOCKED, move.from_)
                            self.BLUE_SINGLES = add_nth_bit(self.BLUE_SINGLES, move.from_)
                            self.actual_state = self.capture_state()
                            return "Good: Killing move"
                        # on top of red blocked
                        elif there_is(self.RED_BLOCKED, move.from_):
                            self.RED_BLOCKED = clear_nth_bit(self.RED_BLOCKED, move.from_)
                            self.RED_SINGLES = add_nth_bit(self.RED_SINGLES, move.from_)
                            self.actual_state = self.capture_state()
                            return "Good: Killing move"
                        else:
                            self.last_state = self.last_state.last_state.copy()
                            return "Error: Missing blocked piece"
                    # there is red double
                    elif there_is(self.RED_DOUBLES, move.to):
                        self.last_state = self.capture_state()
                        self.BLUE_DOUBLES = clear_nth_bit(self.BLUE_DOUBLES, move.from_)
                        self.RED_DOUBLES = clear_nth_bit(self.RED_DOUBLES, move.to)
                        self.BLUE_DOUBLES = add_nth_bit(self.BLUE_DOUBLES, move.to)
                        # on top of blue blocked
                        if there_is(self.BLUE_BLOCKED, move.from_):
                            self.BLUE_BLOCKED = clear_nth_bit(self.BLUE_BLOCKED, move.from_)
                            self.BLUE_SINGLES = add_nth_bit(self.BLUE_SINGLES, move.from_)
                            self.actual_state = self.capture_state()
                            return "Good: Double killing move"
                        # on top of red blocked
                        elif there_is(self.RED_BLOCKED, move.from_):
                            self.RED_BLOCKED = clear_nth_bit(self.RED_BLOCKED, move.from_)
                            self.RED_SINGLES = add_nth_bit(self.RED_SINGLES, move.from_)
                            self.actual_state = self.capture_state()
                            return "Good: Double killing move"
                        else:
                            self.last_state = self.last_state.last_state.copy()
                            return "Error: Missing blocked piece"
                    # there is blue double
                    elif there_is(self.BLUE_DOUBLES, move.to):
                        return "Error: Invalid move"
                    # there is nothing
                    else:
                        if move.to.value == move.from_.value + 6 and move.to.value in [15,16,23,24,31,32,39,40,47,48,55,56]:
                            return "Error: Invalid move"
                        elif move.to.value == move.from_.value + 10 and move.to.value in [9,10,17,18,25,26,33,34,41,42,49,50]:
                            return "Error: Invalid move"
                        elif move.to.value == move.from_.value + 15 and move.to.value in [16,24,32,40,48,56]:
                            return "Error: Invalid move"
                        elif move.to.value == move.from_.value + 17 and move.to.value in [9,17,25,33,41,49,]:
                            return "Error: Invalid move"

                        self.last_state = self.capture_state()
                        self.BLUE_DOUBLES = clear_nth_bit(self.BLUE_DOUBLES, move.from_)
                        self.BLUE_SINGLES = add_nth_bit(self.BLUE_SINGLES, move.to)
                        # on top of blue blocked
                        if there_is(self.BLUE_BLOCKED, move.from_):
                            self.BLUE_BLOCKED = clear_nth_bit(self.BLUE_BLOCKED, move.from_)
                            self.BLUE_SINGLES = add_nth_bit(self.BLUE_SINGLES, move.from_)
                            self.actual_state = self.capture_state()
                            if move.to.value == move.from_.value + 6:
                                return "Good: left-left-front move"
                            elif move.to.value == move.from_.value + 15:
                                return "Good: front-front-left move"
                            elif move.to.value == move.from_.value + 17:
                                return "Good: front-front-right move"
                            else:
                                return "Good: right-right-front move"
                        # on top of red blocked
                        elif there_is(self.RED_BLOCKED, move.from_):
                            self.RED_BLOCKED = clear_nth_bit(self.RED_BLOCKED, move.from_)
                            self.RED_SINGLES = add_nth_bit(self.RED_SINGLES, move.from_)
                            self.actual_state = self.capture_state()
                            if move.to.value == move.from_.value + 6:
                                return "Good: left-left-front move"
                            elif move.to.value == move.from_.value + 15:
                                return "Good: front-front-left move"
                            elif move.to.value == move.from_.value + 17:
                                return "Good: front-front-right move"
                            else:
                                return "Good: right-right-front move"
                        else:
                            self.last_state = self.last_state.last_state.copy()
                            return "Error: Missing blocked piece"
                # to somewhere else
                else:
                    return "Error: Unknown move"
            # Blue blocked
            elif there_is(self.BLUE_BLOCKED, move.from_):
                return "Error: Blocked can not move"
            else:
                return "Error: Could not find the piece"
        # Red piece
        elif move.player == "Red":
            # Red single
            if there_is(self.RED_SINGLES, move.from_):
                # to the front or to the left or to the right
                if move.to.value == move.from_.value - 8 or move.to.value == move.from_.value - 1 or move.to.value == move.from_.value + 1:
                    # there is red single
                    if there_is(self.RED_SINGLES, move.to):
                        self.last_state = self.capture_state()
                        self.RED_SINGLES = clear_nth_bit(self.RED_SINGLES, move.from_)
                        self.RED_SINGLES = clear_nth_bit(self.RED_SINGLES, move.to)
                        self.RED_DOUBLES = add_nth_bit(self.RED_DOUBLES, move.to)
                        self.RED_BLOCKED = add_nth_bit(self.RED_BLOCKED, move.to)
                        self.actual_state = self.capture_state()
                        return "Good: New double"
                    elif (there_is(self.RED_DOUBLES, move.to) or
                          there_is(self.BLUE_SINGLES, move.to) or
                          there_is(self.BLUE_DOUBLES, move.to)):
                        return "Error: Invalid move"
                    # there is nothing
                    else:
                        if move.to.value == move.from_.value - 1 and move.to.value in [16,24,32,40,48,56]:
                            return "Error: Invalid move"
                        elif move.to.value == move.from_.value + 1 and move.to.value in [9,17,25,33,41,49]:
                            return "Error: Invalid move"

                        self.last_state = self.capture_state()
                        self.RED_SINGLES = clear_nth_bit(self.RED_SINGLES, move.from_)
                        self.RED_SINGLES = add_nth_bit(self.RED_SINGLES, move.to)
                        self.actual_state = self.capture_state()
                        if move.to.value == move.from_.value - 8:
                            return "Good: Frontal move"
                        elif move.to.value == move.from_.value - 1:
                            return "Good: Left move"
                        else:
                            return "Good: Right move"
                # to the left-front or right-front
                elif move.to.value == move.from_.value - 7 or move.to.value == move.from_.value - 9:
                    # there is blue single
                    if there_is(self.BLUE_SINGLES, move.to):
                        self.last_state = self.capture_state()
                        self.RED_SINGLES = clear_nth_bit(self.RED_SINGLES, move.from_)
                        self.BLUE_SINGLES = clear_nth_bit(self.BLUE_SINGLES, move.to)
                        self.RED_SINGLES = add_nth_bit(self.RED_SINGLES, move.to)
                        self.actual_state = self.capture_state()
                        return "Good: Killing move"
                    # there is blue double
                    elif there_is(self.BLUE_DOUBLES, move.to):
                        self.last_state = self.capture_state()
                        self.RED_SINGLES = clear_nth_bit(self.RED_SINGLES, move.from_)
                        self.BLUE_DOUBLES = clear_nth_bit(self.BLUE_DOUBLES, move.to)
                        self.RED_DOUBLES = add_nth_bit(self.RED_DOUBLES, move.to)
                        self.actual_state = self.capture_state()
                        return "Good: Double killing move"
                    else:
                        return "Error: Invalid move"
                # to somewhere else
                else:
                    return "Error: Unknown move"
            # Red double
            elif there_is(self.RED_DOUBLES, move.from_):
                # left-left-front or front-front-left or to front-front-right or right-right-front
                if move.to.value == move.from_.value - 6 or move.to.value == move.from_.value - 15 or move.to.value == move.from_.value - 17 or move.to.value == move.from_.value - 10:
                    # there is blue single
                    if there_is(self.BLUE_SINGLES, move.to):
                        self.last_state = self.capture_state()
                        self.BLUE_DOUBLES = clear_nth_bit(self.BLUE_DOUBLES, move.from_)
                        self.BLUE_SINGLES = clear_nth_bit(self.BLUE_SINGLES, move.to)
                        self.RED_SINGLES = add_nth_bit(self.RED_SINGLES, move.to)
                        # on top of blue blocked
                        if there_is(self.BLUE_BLOCKED, move.from_):
                            self.BLUE_BLOCKED = clear_nth_bit(self.BLUE_BLOCKED, move.from_)
                            self.BLUE_SINGLES = add_nth_bit(self.BLUE_SINGLES, move.from_)
                            self.actual_state = self.capture_state()
                            return "Good: Killing move"
                        # on top of red blocked
                        elif there_is(self.RED_BLOCKED, move.from_):
                            self.RED_BLOCKED = clear_nth_bit(self.RED_BLOCKED, move.from_)
                            self.RED_SINGLES = add_nth_bit(self.RED_SINGLES, move.from_)
                            self.actual_state = self.capture_state()
                            return "Good: Killing move"
                        else:
                            return "Error: Missing blocked piece"
                    # there is red single
                    elif there_is(self.RED_SINGLES, move.to):
                            self.last_state = self.capture_state()
                            self.RED_DOUBLES = clear_nth_bit(self.RED_DOUBLES, move.from_)
                            self.RED_SINGLES = clear_nth_bit(self.RED_SINGLES, move.to)
                            self.RED_DOUBLES = add_nth_bit(self.RED_DOUBLES, move.to)
                            self.RED_BLOCKED = add_nth_bit(self.RED_BLOCKED, move.to)
                            # on top of blue blocked
                            if there_is(self.BLUE_BLOCKED, move.from_):
                                self.BLUE_BLOCKED = clear_nth_bit(self.BLUE_BLOCKED, move.from_)
                                self.BLUE_SINGLES = add_nth_bit(self.BLUE_SINGLES, move.from_)
                                self.actual_state = self.capture_state()
                                return "Good: change of double"
                            # on top of red blocked
                            elif there_is(self.RED_BLOCKED, move.from_):
                                self.RED_BLOCKED = clear_nth_bit(self.RED_BLOCKED, move.from_)
                                self.RED_SINGLES = add_nth_bit(self.RED_SINGLES, move.from_)
                                self.actual_state = self.capture_state()
                                return "Good: change of double"
                            else:
                                return "Error: Missing blocked piece"
                    # there is blue double
                    elif there_is(self.BLUE_DOUBLES, move.to):
                        self.last_state = self.capture_state()
                        self.BLUE_DOUBLES = clear_nth_bit(self.BLUE_DOUBLES, move.from_)
                        self.RED_DOUBLES = clear_nth_bit(self.RED_DOUBLES, move.to)
                        self.BLUE_DOUBLES = add_nth_bit(self.BLUE_DOUBLES, move.to)
                        # on top of blue blocked
                        if there_is(self.BLUE_BLOCKED, move.from_):
                            self.BLUE_BLOCKED = clear_nth_bit(self.BLUE_BLOCKED, move.from_)
                            self.BLUE_SINGLES = add_nth_bit(self.BLUE_SINGLES, move.from_)
                            self.actual_state = self.capture_state()
                            return "Good: Double killing move"
                        # on top of red blocked
                        elif there_is(self.RED_BLOCKED, move.from_):
                            self.RED_BLOCKED = clear_nth_bit(self.RED_BLOCKED, move.from_)
                            self.RED_SINGLES = add_nth_bit(self.RED_SINGLES, move.from_)
                            self.actual_state = self.capture_state()
                            return "Good: Double killing move"
                        else:
                            return "Error: Missing blocked piece"
                    # there is red double
                    elif there_is(self.RED_DOUBLES, move.to):
                        return "Error: Invalid move"
                    # there is nothing
                    else:
                        if move.to.value == move.from_.value - 6 and move.to.value in [9,10,17,18,25,26,33,34,41,42,49,50]:
                            return "Error: Invalid move"
                        elif move.to.value == move.from_.value - 10 and move.to.value in [15,16,23,24,31,32,39,40,47,48,55,56]:
                            return "Error: Invalid move"
                        elif move.to.value == move.from_.value - 15 and move.to.value in [9,17,25,33,41,49]:
                            return "Error: Invalid move"
                        elif move.to.value == move.from_.value - 17 and move.to.value in [16,24,32,40,48,56]:
                            return "Error: Invalid move"

                        self.last_state = self.capture_state()
                        self.RED_DOUBLES = clear_nth_bit(self.RED_DOUBLES, move.from_)
                        self.RED_SINGLES = add_nth_bit(self.RED_SINGLES, move.to)
                        # on top of blue blocked
                        if there_is(self.BLUE_BLOCKED, move.from_):
                            self.BLUE_BLOCKED = clear_nth_bit(self.BLUE_BLOCKED, move.from_)
                            self.BLUE_SINGLES = add_nth_bit(self.BLUE_SINGLES, move.from_)
                            self.actual_state = self.capture_state()
                            if move.to.value == move.from_.value - 6:
                                return "Good: left-left-front move"
                            elif move.to.value == move.from_.value - 15:
                                return "Good: front-front-left move"
                            elif move.to.value == move.from_.value - 17:
                                return "Good: front-front-right move"
                            else:
                                return "Good: right-right-front move"
                        # on top of red blocked
                        elif there_is(self.RED_BLOCKED, move.from_):
                            self.RED_BLOCKED = clear_nth_bit(self.RED_BLOCKED, move.from_)
                            self.RED_SINGLES = add_nth_bit(self.RED_SINGLES, move.from_)
                            self.actual_state = self.capture_state()
                            if move.to.value == move.from_.value - 6:
                                return "Good: left-left-front move"
                            elif move.to.value == move.from_.value - 15:
                                return "Good: front-front-left move"
                            elif move.to.value == move.from_.value - 17:
                                return "Good: front-front-right move"
                            else:
                                return "Good: right-right-front move"
                        else:
                            return "Error: Missing blocked piece"
                # to somewhere else
                else:
                    return "Error: Unknown move"
            # Red blocked
            elif there_is(self.RED_BLOCKED, move.from_):
                return "Error: Blocked can not move"
            else:
                return "Error: Could not find the piece"
        else:
            return "Error: Unknown player"

    def undo_move(self):
        # Undo last move from the board
        # Check if there is a move to undo
        if self.last_state is None:
            return "Error: No move to undo"

        # Undo the last move
        self.BLUE_SINGLES = self.last_state['BLUE_SINGLES']
        self.BLUE_DOUBLES = self.last_state['BLUE_DOUBLES']
        self.RED_SINGLES = self.last_state['RED_SINGLES']
        self.RED_DOUBLES = self.last_state['RED_DOUBLES']
        self.BLUE_BLOCKED = self.last_state['BLUE_BLOCKED']
        self.RED_BLOCKED = self.last_state['RED_BLOCKED']
        self.last_state = self.last_state['last_state']
        self.actual_state = self.capture_state()
        return "Good: Move undone"

    # Game-state Checking Methods
    def is_game_over(self):
        # Check for end-game

        # Check if BLUE or RED have reached the opposite side
        if self.BLUE_SINGLES & Board.FIRST_6_SQUARES_MASK:
            return "Game over: Blue wins"
        elif self.RED_SINGLES & Board.LAST_6_SQUARES_MASK:
            return "Game over: Red wins"

        # Check if all BLUE or RED pieces are blocked or captured
        if self.BLUE_SINGLES == 0 and self.BLUE_DOUBLES == 0:
            return "Game over: Red wins"
        elif self.RED_SINGLES == 0 and self.RED_DOUBLES == 0:
            return "Game over: Blue wins"

        # No end-game conditions met
        return "Game not over"

    def parse_to_coordinate_to_move(self, to_coordinates, shift):
        # This function should return the "from-to" string based on the to_position and the shift
        moves = []
        for to_position in range(64):
            if to_coordinates & (9223372036854775808 >> to_position):
                from_position = to_position + shift
                moves.append(f"{Coordinate(from_position + 1).name}-{Coordinate(to_position + 1).name}")
        return moves

    # Information Retrieval Methods
    def get_legal_moves(self, selected_categories, player_color):
        # Get a dict of legal moves depending on the requested category and player color
        legal_moves = {}
        friend_singles = self.BLUE_SINGLES if player_color == "Blue" else self.RED_SINGLES
        friend_doubles = self.BLUE_DOUBLES if player_color == "Blue" else self.RED_DOUBLES
        enemy_singles = self.RED_SINGLES if player_color == "Blue" else self.BLUE_SINGLES
        enemy_doubles = self.RED_DOUBLES if player_color == "Blue" else self.BLUE_DOUBLES

        for category in selected_categories:
            direction_multiplier = -1 if player_color == "Red" else 1

            to_coordinates = shift_pieces(friend_singles if category.startswith("singles") else friend_doubles,
                                          direction_multiplier * self.shift_map[category])

            # Apply masks and filters based on the category specifics
            if "left" in category or "f_f_l" in category:
                if player_color == "Red":
                    to_coordinates &= ~self.FORBIDDEN_RIGHT_MASK
                else:
                    to_coordinates &= ~self.FORBIDDEN_LEFT_MASK
            elif "right" in category or "f_f_r" in category:
                if player_color == "Red":
                    to_coordinates &= ~self.FORBIDDEN_LEFT_MASK
                else:
                    to_coordinates &= ~self.FORBIDDEN_RIGHT_MASK
            elif "l_l_f" in category:
                if player_color == "Red":
                    to_coordinates &= ~self.FORBIDDEN_RIGHT_RIGHT_MASK
                else:
                    to_coordinates &= ~self.FORBIDDEN_LEFT_LEFT_MASK
            elif "r_r_f" in category:
                if player_color == "Red":
                    to_coordinates &= ~self.FORBIDDEN_LEFT_LEFT_MASK
                else:
                    to_coordinates &= ~self.FORBIDDEN_RIGHT_RIGHT_MASK

            if "kill" in category:
                to_coordinates &= enemy_singles if category.endswith("singles") else enemy_doubles
            elif "upgrade" in category:
                to_coordinates &= friend_singles
            else:
                if category.endswith("empty"):
                    to_coordinates &= ~(friend_singles | enemy_singles | friend_doubles | enemy_doubles | self.FORBIDDEN_SQUARES_MASK)
                elif category.endswith("singles"):
                    to_coordinates &= friend_singles
                elif category.endswith("doubles"):
                    to_coordinates &= friend_doubles

            legal_moves[category] = self.parse_to_coordinate_to_move(to_coordinates, direction_multiplier * -1 * self.shift_map[category])

        return legal_moves

    def get_state(self):
        # Get the current state of the board
        return self.actual_state

    def get_score(self):
        # Get the score of the current state of the board
        return 0

    def array_board(self):
        # Initialize an empty 8x8 array
        board_array = [['_' for _ in range(8)] for _ in range(8)]
        board_array[0][0] = ' '
        board_array[0][7] = ' '
        board_array[7][0] = ' '
        board_array[7][7] = ' '


        for i in range(64):
            row = i // 8  # Calculate row index
            col = i % 8  # Calculate column index

            # Check the state for each bit and update the board array
            if (self.BLUE_SINGLES >> i) & 1:
                board_array[row][col] = 's'
            elif (self.RED_SINGLES >> i) & 1:
                board_array[row][col] = 'S'
            elif (self.BLUE_DOUBLES >> i) & 1:
                if (self.BLUE_BLOCKED >> i) & 1:
                    board_array[row][col] = 'bd'
                elif (self.RED_BLOCKED >> i) & 1:
                    board_array[row][col] = 'Bd'
                else:
                    board_array[row][col] = "bD-ERROR"
            elif (self.RED_DOUBLES >> i) & 1:
                if (self.RED_BLOCKED >> i) & 1:
                    board_array[row][col] = 'BD'
                elif (self.BLUE_BLOCKED >> i) & 1:
                    board_array[row][col] = 'bD'
                else:
                    board_array[row][col] = "rD-ERROR"
            elif (self.BLUE_BLOCKED >> i) & 1:
                board_array[row][col] = 'bB-ERROR'
            elif (self.RED_BLOCKED >> i) & 1:
                board_array[row][col] = 'rB-ERROR'

        return board_array  # Return the 2D array of the board state

    def print_board(self):
        # Print the current state of the board
        board_array = self.array_board()

        print('------------------------------------------------------------------------------------------')
        print('   A B C D E F G H')
        for row in range(8, 0, -1):
            print(f'{row} ', end=' ')
            for col in range(7, -1, -1):
                print(board_array[8 - row][col], end=' ')
            print(f' {row}')
        print('   A B C D E F G H')

    def print_legal_moves(self, selected_legal_moves):
        for move_category, moves in selected_legal_moves.items():
            print(f"{move_category}: {', '.join(moves)}")
        print('------------------------------------------------------------------------------------------')

    def get_legal_moves_list(self,selected_legal_moves):
        legal_moves_array = []
        for move_category, moves in selected_legal_moves.items():
            legal_moves_array.extend(moves)
        return legal_moves_array

    def select_random_move(self, selected_legal_moves):
        # Get a random move from the selected legal moves
        non_empty_categories = {category: moves for category, moves in selected_legal_moves.items() if moves}

        if non_empty_categories:
            # Choose a random category from those that are not empty
            random_category = choice(list(non_empty_categories.keys()))
            # Choose a random move from the selected category's list
            random_move = choice(non_empty_categories[random_category])
            return random_move
        else:
            return "No legal moves available"


class Move:
    def __init__(self, player, fromm, to):
        # Initialize the move
        self.player = player
        self.from_ = fromm
        self.to = to

    def __eq__(self, other):
        if not isinstance(other, Move):
            return NotImplemented

        return (self.player == other.player and
                self.from_ == other.from_ and
                self.to == other.to)

    def __hash__(self):
        return hash((self.player, self.from_, self.to))


class Coordinate(Enum):
    XX = 0
    A1 = 1
    B1 = 2
    C1 = 3
    D1 = 4
    E1 = 5
    F1 = 6
    G1 = 7
    H1 = 8
    A2 = 9
    B2 = 10
    C2 = 11
    D2 = 12
    E2 = 13
    F2 = 14
    G2 = 15
    H2 = 16
    A3 = 17
    B3 = 18
    C3 = 19
    D3 = 20
    E3 = 21
    F3 = 22
    G3 = 23
    H3 = 24
    A4 = 25
    B4 = 26
    C4 = 27
    D4 = 28
    E4 = 29
    F4 = 30
    G4 = 31
    H4 = 32
    A5 = 33
    B5 = 34
    C5 = 35
    D5 = 36
    E5 = 37
    F5 = 38
    G5 = 39
    H5 = 40
    A6 = 41
    B6 = 42
    C6 = 43
    D6 = 44
    E6 = 45
    F6 = 46
    G6 = 47
    H6 = 48
    A7 = 49
    B7 = 50
    C7 = 51
    D7 = 52
    E7 = 53
    F7 = 54
    G7 = 55
    H7 = 56
    A8 = 57
    B8 = 58
    C8 = 59
    D8 = 60
    E8 = 61
    F8 = 62
    G8 = 63
    H8 = 64


def main():
    board = Board()
    #board.initialize()
    board.fen_notation_into_bb("8/2b02b02/2r02r02/8/8/2b02b02/2r02r02/8")

    i = 0
    players = ["Blue", "Red"]
    turn = players[0]

    while True:
        # Clear console
        os.system('cls')

        # Display the board
        board.print_board()

        # Ask for the next move
        print("-----------------------")
        print(turn + "'s turn")
        print("-----------------------")

        print("ex: A1-B1")
        print("- 'quit'")
        print("- 'back'")
        print("- 'get'")
        print("- 'random'")
        next_move = input("Enter next move:")
        if next_move.lower() == 'quit':
            break
        elif next_move.lower() == 'back':
            board.undo_move()
            if i == 0:
                print("Already in first turn")
            else:
                i -= 1
                turn = players[i % 2]
            continue
        elif next_move.lower() == 'get':
            print()
            print('- alle')
            print('- number')
            print('- help')

            move_categories = "help"
            while move_categories.lower() == 'help':
                move_categories = input('Enter move category: ')

                if move_categories.lower() == 'help':
                    print('Dictionary of legal moves:')
                    print(board.move_categories_dict)

            # parse move_categories
            selected_categories = parse_move_categories(move_categories, board.move_categories_dict)
            # get legal moves
            selected_legal_moves = board.get_legal_moves(selected_categories, turn)
            board.get_legal_moves_list(selected_legal_moves)
            # print legal moves
            board.print_legal_moves(selected_legal_moves)
            continue
        elif next_move.lower() == 'random':
            print("- alle")
            print("- number")

            move_categories = "help"
            while move_categories.lower() == 'help':
                move_categories = input('Enter move category: ')

                if move_categories.lower() == 'help':
                    print('Dictionary of legal moves:')
                    print(board.move_categories_dict)

            # parse move_categories
            selected_categories = parse_move_categories(move_categories, board.move_categories_dict)
            # get legal moves
            selected_legal_moves = board.get_legal_moves(selected_categories, turn)
            # select random move
            next_move = board.select_random_move(selected_legal_moves)

            if next_move == "No legal moves available":
                print(f"No legal moves of {move_categories} available")
                continue

        # Convert input to Coordinates
        try:
            from_square, to_square = next_move.upper().split('-')
            from_coordinate = Coordinate[from_square]
            to_coordinate = Coordinate[to_square]
        except ValueError:
            print("Please enter moves in the format 'H8-H7'.")
            continue
        except KeyError:
            print("Invalid coordinates. Try again.")
            continue


        # Create and apply the move
        move = Move(player=turn, fromm=from_coordinate, to=to_coordinate)
        response = board.apply_move(move)
        print("-----------------------")
        print(response)
        print("-----------------------")

        # Increment turn
        if response.startswith('Good:'):
            i += 1
            turn = players[i % 2]

        # Check if the game is over
        game_over = board.is_game_over()
        if game_over != "Game not over":
            print(game_over)
            break


if __name__ == "__main__":
    main()
