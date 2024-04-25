class JumpSturdyBoard:
    def __init__(self):
        # initialisiere leeres board
        # in dem fall noch ein 8x8 board
        #self.board = [0, 0, 0, 0, 0, 0, 0, 0]
        self.board = [[0 for i in range(8)] for j in range(8)]
        self.move_history = ["123"] #ich teste hier gerade wie ich eine 
        # move-History einfüge. eigtl müsste es so klappen aber mein
    #gehirn lagged gerade 
        
    def turn_counter(self):
        # zähle die Anzahl an Zügen
        self.turn_counter += 1
        
    
    def put_pieces_on_board(self):
        # setze die Steine auf das Board
        # in dem fall 12 weiße und 12 schwarze Steine
        # viellecht sollten wir das auch in der __init__ Methode machen
        pass

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
        # Stelle das Board "grafisch" dar....irgendwie
        print(self.board)
        
