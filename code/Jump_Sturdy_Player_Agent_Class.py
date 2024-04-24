import random

class JumpSturdyPlayerAgent:
    def __init__(self, spieler_farbe):
        self.spieler_farbe = spieler_farbe

    # die generate_moves Methode nimmt sich den Zustand des Spielbretts als Input und erzeugt Liste mit allen möglichen Zügen 
    def generate_moves(self, board):
        # züge sollen hier generiert werden. 
        # wollen eine Liste mit allen möglichen Zügen.
        # erstellen dafür eine leere Liste
        legal_moves = []
        for i in range(8):
            for j in range(8):
                # das brett ist hier noc nicht richtig, da wir kein richtiges 8x8 brett haben
                # wir prüfen, ob das Feld "leer" ist. Hier wllen wir eigentlich ein Bitbaord erstellen und prüfen ob in dem Feld eine 0 ist.
                if board.board[i][j] == 0:
                    legal_moves.append((i, j))
                    # wenn das Feld leer ist, fügen wir die koordinaten zu der legal_moves liste hinzu.
        return legal_moves
    
    def pick_move(self, board):
        # um eine Zug zu machen, generiert sich die KI die Liste aller mögliche mit HIlfe der generate_moves Methode
        legal_moves = self.generate_moves(board)

        # haben noch keine Heuristik,darum soll einfach Knallhart ein zufölliger Zug gemacht werden.
        # random.choice ist aus der random library und wählt ein zufälliges Element aus unserer Liste alles möglichen Züge
        # Ich vermute move muss dann bei uns entweder ein Tupel oder ein Bitboard sein
        move = random.choice(legal_moves)

        # 
        board.move_piece(move)