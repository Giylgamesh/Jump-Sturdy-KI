# Selecting the most suitable game representation

Choosing the right game representation involves considering how efficiently certain operations can be performed with each type of representation. Here are some crucial queries that the AI will need to answer frequently and quickly and possible approaches to answering them efficiently:

### Basic Piece Information:
- Where are all friendly/enemy pieces?
  - Bitboard: Use separate bitboards for friendly and enemy pieces. Each bit represents a square on the board, and a 1 signifies a piece presence.
  - Object Oriented: Iterate through each piece or space on the board.

- How many friendly/enemy pieces are there?
  - Bitboard: Use a popcount operation like 'int.bit_count()' to count the number of 1s in the corresponding friendly/enemy bitboard.
  - Object Oriented: Maintain a counter variable for friendly and enemy pieces, updated during gameplay.

- Which friendly/enemy pieces are on top of a double stack?
  - Bitboard: Each piece type can be represented by a dedicated bitboard. Analyze bitwise combinations of piece positions and top piece conditions.
  - Object Oriented: Iterate through each piece, each piece object holds a variable that determines its status: blocked, single, double stack.
    
- What are the most advanced friendly/enemy pieces?
  - Bitboard: Separate the corresponding bitboard in groups of 8 bits and iterate through each group.
  - Object Oriented: Iterate through each piece, tracking the most advanced position encountered. Alternatively, update global list.

### Piece Status:
- Which friendly/enemy pieces are blocked?
  - Bitboard: Analog to double stacks, maintain dedicated bitboards for pieces considered blocked. Analyze bitwise combinations of piece positions and blocking conditions.
  - Object Oriented: Iterate through each piece, checking its status.

- Which friendly/enemy pieces are under attack/ can attack?
  - Bitboard: Use bitwise shifts (left/right 7 and 9 positions) on friendly/enemy piece bitboards and perform a bitwise AND with the enemy/friendly piece bitboard to identify squares under attack/potential attacking positions.   
  - Object Oriented: Iterate through each piece, marking diagonally forward squares as attacked positions, and check whether its own position is under attack.

### Actionable Information:
- What moves are available for me/the enemy?
  - Bitboard: Perform bitwise operations to map all potential moves for pieces based on current game state, i.e. considering piece types, blocking, capturing, and movement conditions.
  - Object Oriented: Iterate through each piece, simulating potential moves, and checking for validity.

- What are the legal moves for a specific piece?
  - Bitboard: Similar to "What moves are available..." but focused on a specific piece. Utilize bitwise operations and pre-calculated move patterns specific to the piece's type and position.
  - Object Oriented: Similar to "What moves are available..." but focused on a specific piece. Iterate through potential moves for the piece, checking for validity.

- What are the consequences of a particular move?
  - Bitboard: Simulate the move on a copy of the bitboard and analyze the resulting board state.
  - Object Oriented: Temporarily execute the move on the object model, assess changes, then revert to the original state. Alternatively, copy the game state but this would be to expensive.

### Game State:
- Is the game finished?
  - Bitboard: Analyze the bitboard representing the positions of friendly and enemy pieces. Check if either player has no pieces remaining on the board, all their pieces are blocked, or some of their pieces are in the last row. This can be achieved with a few simple bitwise operations on the corresponding bitboards.
  - Object Oriented: Iterate through all friendly and enemy pieces. Check if any are remaining, all are blocked, or if any has arrived at its enemy's back row.

### Advanced game state analysis:

- What is the fastest path for advancement for each of my pieces?
  - Bitboard: [TODO]
  - Object Oriented: [TODO]
    
- What are the potential traps or forced moves? 
  - Bitboard: [TODO]
  - Object Oriented: [TODO] 
