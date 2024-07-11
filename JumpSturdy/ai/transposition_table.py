from collections import OrderedDict # we use an ordered directorz to manage the table memory by removing least recently used (LRU) entries if table is full

class TranspositionTable():
    """the TranspositionTable class is used as cache for our alpha beta search

    Attributes:
        table (dict): a dictionary with hash values as keys and (score, depth, best_move) tuples as values.
        size (int): maximum size of the transposition table (for memory controll so it doesn't explode in size)

    Methods:
        __init__(self, size=10**6): initializes the TranspositionTable object
        get(self, hash_value): retriev a game state by its hash value
        put(self, hash_value, score, depth, best_move): puts an entry in the transposition table."""

    def __init__(self, size=10**6):
        self.table = OrderedDict()
        self.size = size
    
    def get(self, hash_value):
        """
        Retrieve a game state by its hash value.

        Args:
            hash_value (64-bit int): hash value of a game state to find in the ttable

        Return:
            3-tuple or None: the (score, depth, best_move) tuple with the hash value, or None if not found
        """
        if hash_value not in self.table: # check if hash exists in ttable
            return -1   # return -1 if doesn't exist
        
        # else, hash exists in table
        self.table.move_to_end(hash_value) # move used hash to end of dict, because it was recently used
        return self.table[hash_value]
    
    def put(self, hash_value, score, depth, best_move, alpha, beta):
        #If transposition table is full (max size) --> removes least recently used entry

        #Args:
        #    hash_value (64-bit): hash value of the current game state
        #    score (float): The score associated with this game state.
        #    depth (int): The depth at which the board state was evaluated.
        # NOTE no colision avoidance yet. Maybe we need one
        if len(self.table) >= self.size: # check if ttable max size reached
            self.table.popitem(last=False) # if True -> remove least recently used item from ttable
        self.table[hash_value] = (score, depth, best_move, alpha, beta) # add new entry in ttable
        self.table.move_to_end(hash_value) # move new enrty to end of table as was it was recently used

    def print_table(self):
        """
        Print the transposition table.
        """
        print()
        for hash_value, (score, depth, best_move, alpha, beta) in self.table.items():
            print(f"Hash Value: {hash_value}")
            print(f"Score: {score}")
            print(f"Depth: {depth}")
            print(f"Best Move: {best_move}")
            print(f"Alpha: {alpha}")
            print(f"Beta: {beta}")
            print("--------------------")