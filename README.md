# Jump-Sturdy: Building an AI agent to play Jump Sturdy.
University Symbolic AI Project

This repository houses the code for a symbolic AI project developed by three Bachelor students at Technische Universität Berlin for the "Symbolische Künstliche Intelligenz" project. 

We welcome contributions and discussions.

## Key Features:
|||
|-------------------------|-------------------------------------------------------------------------------------------------------------------------------------------|
| Optimized Search with Alpha-Beta Pruning | Enables efficient exploration of the game tree, minimizing unnecessary calculations and maximizing resource utilization. |
| Efficient State Representation | Allows the AI agent to quickly identify potential next moves and distinguish between different game states.                        |
| Heuristic-Based Decision Making | The AI agent utilizes a set of rules (heuristics) to prioritize promising moves based on the current game state.                  |

## Game Rules:

|||
|------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Goal                   | Be the first player to reach the opponent's back row. Alternatively, win by capturing all the enemy pieces or completely blocking their movement.                                         |
| Board and Pieces       | 8x8 board with corners removed. Two players: white and black. Pieces are single or double stacks.                                                                                         |
| Single Stacks Movement | Single pieces can move one space sideways or forward to empty spaces or onto one piece of the same color (forming a double stack). They capture diagonally forward like chess pawns.      |
| Double Stacks Movement | The top piece of a double stack can move or capture as a chess knight, but only forward.                                                                                                  |
| Starting Setup         | Each player starts with 12 pieces: 6 in their home row and 6 in the second row without the corners.                                                                                       |
| Turns                  | White moves first, after which turns alternate between players.                                                                                                                           |
| Capture                | When a friendly piece captures an enemy piece, it takes over its position on the board, and the captured enemy piece is removed.                                                          |
| No Skipping            | There is no skipping turns.                                                                                                                                                               |

For more detailed rules and examples, you can visit https://abstractmeanderings.wordpress.com/2014/10/06/jump-sturdy/ or https://www.mindsports.nl/index.php/the-pit/576-jumpsturdy

## Game Representation: 

### Learning Algorithm:

### Action Selection:
