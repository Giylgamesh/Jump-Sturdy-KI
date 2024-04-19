# Jump-Sturdy
University Symbolic AI Project

This repository houses the code for a symbolic AI project developed by three Bachelor students at Technische Universität Berlin for the "Symbolische Künstliche Intelligenz" (Symbolic Artificial Intelligence) project.

The project focuses on building an AI agent to play the game "Jump Sturdy".

We welcome contributions and discussions!

---
### Key Features:
- Alpha-Beta Pruning: We will utilize alpha-beta pruning for efficient decision making within the game tree.
- State Representation: We will design a suitable representation of the game state.
- Heuristic-based Action Selection: The AI will use a heuristic-based system to choose the best action based on the game state and game logic.

### Game Rules:
**Goal:**
- Be the first player to reach the opponent's back row. Alternatively, winning can be achieved by capturing all the enemy pieces or completely blocking their movement.

**Board and Pieces:**
- 8x8 board with corners removed.
- Two players: white and black.
- Pieces are single or double stacks (two pieces on top of each other).

**Single Stacks:**
- Single pieces can move one space sideways or forward to empty spaces or with one piece of the same color (forming a double stack).
- Single pieces can capture enemy singles or the top piece of a double stack diagonally forward by one space (like a chess pawn).

**Double Stacks:**
- The top piece of a double stack can move or capture as a chess knight, but only the four forward moves.
- The top piece of a double stack can capture enemy singles or the top piece of a double stack.
- The bottom piece of a double stack cannot move or capture.

**Start:**
- Each player starts with 12 pieces. 6 in its home row and 6 in the second row without the corners.
- White moves first, and then turns alternate between players. 

**Capture:**
- Each player starts with 12 pieces: 6 in their home row and 6 in the second row, excluding the corners.

**Notes:**
- There is no skipping turns.

For more detailed rules and examples, you can visit https://abstractmeanderings.wordpress.com/2014/10/06/jump-sturdy/ or https://www.mindsports.nl/index.php/the-pit/576-jumpsturdy

### Game Representation: 

### Learning Algorithm:

### Action Selection:
