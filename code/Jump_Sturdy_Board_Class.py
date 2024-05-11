def validate_string(input_string):
    allowed_chars = set("0123456789rb/")
    for char in input_string:
        if char not in allowed_chars:
            return False
    return True
class JumpSturdyBoard:
    def __init__(self):
        # initialisiere leeres board
        # leere BitBoards die zum Board gehören
        # Array mit allen Bit Boards der Figuren aus Jump-Sturdy bestehen
        self.pieceBB = [0b0, 0b0, 0b0, 0b0, 0b0, 0b0]
        #Notwendige BitBoards für die Brechnung von Moves:
        self.file_a = 0b000000100000001000000010000000100000001000000010000000000000
        self.file_g = 0b000001000000100000001000000010000000100000001000000010000001
        self.file_h = 0b000000000000010000000100000001000000010000000100000001000000
        self.rank_1 = 0b000000000000000000000000000000000000000000000000000000111111
        self.rank_7 = 0b000000111111110000000000000000000000000000000000000000000000
        self.rank_8 = 0b111111000000000000000000000000000000000000000000000000000000
        self.blue_pieces=0b0
        self.occupiedBB = 0b0
        self.emptyBB = 0b0
        # move-History einfüge
        self.move_history = ["123"] 
        
    def turn_counter(self):
        # zähle die Anzahl an Zügen
        self.turn_counter += 1

    def fen_notation_into_bb(self, notation):
        # Auslesen der vorgegebenen String Notation vom Server in unsere BitBoards für Pieces
        if validate_string(notation)==True:
            #Checke,ob der FEN String ein gültiger ist
            binary = ""
            boardPos = 59
            i = 0
            # Gehe die String Notation bis zum Schluss durch.
            while i < len(notation):
                # Setze den String in eine Binäre Darstellung und befülle ihn 60 mal mit der "0", weil unsere BitBoards nur 60 Felder haben.
                binary = "0" * 60
                # Teile den String an der Board Position in der wir uns gerade gefinden und setze eine 1 dazwischen.
                binary = binary[boardPos + 1:] + "1" + binary[0:boardPos]
                # Schaue ob das Zeichen aus der Notation ein "r" ist.
                if notation[i] == "r":
                    # Schaue, ob das nächste Zeichen aus der Notation ebenfalls ein "r" ist, denn daraus Ergibt sich ein Pferd.
                    if notation[i] == notation[i + 1]:
                        # Wandle den String in ein binäres int um und addiere es auf das aktuelle BitBoard für rote Pferde.
                        self.pieceBB[2] += int(binary, 2)
                    # Schaue, ob das nächste Zeichen aus der Notation ein "b" ist, denn daraus Ergibt sich ein captured red pawn(Mir fällt der deutsche Name nicht ein).
                    elif notation[i + 1] == "b":
                        # Wandle den String in ein binäres int um und addiere es auf das aktuelle BitBoard für captured red pawn.
                        self.pieceBB[4] += int(binary, 2)
                    else:
                        # Wandle den String in ein binäres int um und addiere es auf das aktuelle BitBoard für rote Bauern.
                        self.pieceBB[0] += int(binary, 2)
                # Falls das Zeichen ein "/" soll dieser Schleifendurchlauf überprüfen werden, da es kein Zeichen ist, welches im Board notwendig ist.
                elif notation[i] == "/":
                    i += 1
                    continue
                # Falls das Zeichen aus der Notation ein "b" ist.
                elif notation[i] == "b":
                    if notation[i] == notation[i + 1]:
                        # Wandle den String in ein binäres int um und addiere es auf das aktuelle BitBoard für blaue Pferde.
                        self.pieceBB[3] += int(binary, 2)
                    elif notation[i + 1] == "r":
                        # Wandle den String in ein binäres int um und addiere es auf das aktuelle BitBoard für captured blue pawn.
                        self.pieceBB[5] += int(binary, 2)
                    else:
                        # Wandle den String in ein binäres int um und addiere es auf das aktuelle BitBoard für blaue Bauern.
                        self.pieceBB[1] += int(binary, 2)
                # Falls das Zeichen aus der Notation eine Zahl ist.
                else:
                    # Reduziere die Board Position um die angegebene Zahl für die leeren Felder.
                    boardPos -= int(notation[i])
                    i += 1
                    continue
                # Reduziere die Board Position um 1 und erhöhe die nächste Iteration für die Schleife um 2.
                boardPos -= 1
                i += 2
            self.occupiedBB=self.pieceBB[0]| self.pieceBB[1]| self.pieceBB[2] |self.pieceBB[3] |self.pieceBB[4] |self.pieceBB[5]
            self.emptyBB=(~self.occupiedBB& 0b111111111111111111111111111111111111111111111111111111111111)
            self.blue_pieces = self.pieceBB[1] | self.pieceBB[3] | self.pieceBB[4]
        else:
            self.pieceBB = [0b1111110111111, 0b111111011111100000000000000000000000000000000000000000000000, 0b0, 0b0, 0b0, 0b0]
            self.emptyBB = 0b000000100000011111111111111111111111111111111110000001000000
            self.occupiedBB = 0b111111011111100000000000000000000000000000000001111110111111
            self.blue_pieces = self.pieceBB[1] | self.pieceBB[3] | self.pieceBB[4]

    def put_pieces_on_board(self):
        # setze die Steine auf das Board
        # in dem fall 12 weiße und 12 schwarze Steine
        # viellecht sollten wir das auch in der __init__ Methode machen
        # hier soll der code mit bitboards sein.
        # vielleicht kann man move_piece und put_pieces lieber als
        # als nur eine methode schreiebn und nicht als zwei
        pass

    def posible_moves_r(self):
        self.blue_pieces = self.pieceBB[1]|self.pieceBB[3]|self.pieceBB[4]
        self.occupiedBB = self.pieceBB[0] | self.pieceBB[1] | self.pieceBB[2] | self.pieceBB[3] | self.pieceBB[4] | \
                          self.pieceBB[5]
        self.emptyBB = (~self.occupiedBB & 0b111111111111111111111111111111111111111111111111111111111111)
        posible_list = self.posible_rp()
        return  posible_list

    def posible_rp(self):
        list = ""
        #Right capture until RANK 6
        red_pawn_move = ((self.pieceBB[0]&(
                    ~self.rank_7 & 0b111111111111111111111111111111111111111111111111111111111111)) << 7)&self.blue_pieces&(~self.file_a& 0b111111111111111111111111111111111111111111111111111111111111)
        for i in range(60):
            if ((red_pawn_move>>i)&1)==1:
                list+=self.number_to_board_position(i-7) + "-" + self.number_to_board_position(i)+" "
        #Left capture until RANK 6
        red_pawn_move = ((self.pieceBB[0]&(
                    ~self.rank_7 & 0b111111111111111111111111111111111111111111111111111111111111)) << 9) & self.blue_pieces & (
                    ~self.file_h & 0b111111111111111111111111111111111111111111111111111111111111)
        for i in range(60):
            if ((red_pawn_move >> i) & 1) == 1:
                list += self.number_to_board_position(i - 9) + "-" + self.number_to_board_position(i) + " "
        #Right capture from RANK 7
        red_pawn_move = ((self.pieceBB[0] &
                self.rank_7) << 6) & self.blue_pieces & (
                                    ~self.file_a & 0b111111111111111111111111111111111111111111111111111111111111)
        for i in range(60):
            if ((red_pawn_move >> i) & 1) == 1:
                list += self.number_to_board_position(i - 6) + "-" + self.number_to_board_position(i) + " "
        # Left capture from RANK 7
        red_pawn_move = ((self.pieceBB[0] &
                          self.rank_7) << 8) & self.blue_pieces & (
                                ~self.file_h & 0b111111111111111111111111111111111111111111111111111111111111)
        for i in range(60):
            if ((red_pawn_move >> i) & 1) == 1:
                list += self.number_to_board_position(i - 8) + "-" + self.number_to_board_position(i) + " "
        #One move forward until Rank 6
        red_pawn_move = ((self.pieceBB[0] & (
                ~self.rank_7 & 0b111111111111111111111111111111111111111111111111111111111111)) << 8) & self.blue_pieces & (
                                    ~self.file_a & 0b111111111111111111111111111111111111111111111111111111111111)
        for i in range(60):
            if ((red_pawn_move >> i) & 1) == 1:
                list += self.number_to_board_position(i - 7) + "-" + self.number_to_board_position(i) + " "

        return list

    def number_to_board_position(self, number):
        board_positions = [
            'G1', 'F1', 'E1', 'D1', 'C1', 'B1',
            'H2', 'G2', 'F2', 'E2', 'D2', 'C2', 'B2', 'A2',
            'H3', 'G3', 'F3', 'E3', 'D3', 'C3', 'B3', 'A3',
            'H4', 'G4', 'F4', 'E4', 'D4', 'C4', 'B4', 'A4',
            'H5', 'G5', 'F5', 'E5', 'D5', 'C5', 'B5', 'A5',
            'H6', 'G6', 'F6', 'E6', 'D6', 'C6', 'B6', 'A6',
            'H7', 'G7', 'F7', 'E7', 'D7', 'C7', 'B7', 'A7',
            'G8', 'F8', 'E8', 'D8', 'C8', 'B8',
        ]
        return board_positions[number]

    def move_piece(self, move):
        # nimmt die move variable aus der pick_move Methode aus der Jump_Sturdy_Player_Agent Klasse und macht den Zug der JumpSturdyPlayerAgent Klasse und 
        # aktualisiert das Board
        pass

    def game_end_check(self):
        # checke ob Spiel vorbei ist
        # also ob alle gegnerischen Steine geschlagen wurden, oder ob keine Züge mehr möglich sind, oder ob ein Stein die andere Seite erreicht hat
        # return 1, wenn spiel vorbei ist, sonst return 0
        pass

    def print_board(self):
        #Printe das Board der Übersicht halber
        for i in range(59, -1, -1):
            #Shifte dabei immer die jeweiligen BitBoards um i stellen und schaue ob dieses Zeichen eine 1 ist.
            #Falls ja Printe den Buchstaben des jeweiligen Pieces vom BitBoard
            if (self.pieceBB[0]>>i)&1==1:
                print("r", end='')
            elif (self.pieceBB[1]>>i)&1==1:
                print("b", end='')
            elif (self.pieceBB[2]>>i)&1==1:
                print("R", end='')
            elif (self.pieceBB[3]>>i)&1==1:
                print("B", end='')
            elif (self.pieceBB[4]>>i)&1==1:
                print("c", end='')
            elif (self.pieceBB[5]>>i)&1==1:
                print("C", end='')
            else:
                print("0", end='')
            if i%8==6:
                print()
        
