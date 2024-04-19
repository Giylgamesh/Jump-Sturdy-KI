# Jump-Sturdy: Building an AI agent to play Jump Sturdy.
University Symbolic AI Project

This repository houses the code for a symbolic AI project developed by three Bachelor students at Technische Universität Berlin for the "Symbolische Künstliche Intelligenz" project. 

We welcome contributions and discussions.

## Key Features
<table>
  <tr>
    <td><strong>Optimized Search with Alpha-Beta Pruning</strong></td>
    <td>Enables efficient exploration of the game tree, minimizing unnecessary calculations and maximizing resource utilization.</td>
  </tr>
  <tr>
    <td><strong>Efficient State Representation</strong></td>
    <td>Allows the AI agent to quickly identify potential next moves and distinguish between different game states.</td>
  </tr>
  <tr>
    <td><strong>Heuristic-Based Decision Making</strong></td>
    <td>The AI agent utilizes a set of rules (heuristics) to prioritize promising moves based on the current game state.</td>
  </tr>
</table>

## Game Rules
<table>
  <tr>
    <td><strong>Goal</strong></td>
    <td>- Be the first player to reach the opponent's back row. <br> - Alternatively, win by capturing all the enemy pieces or completely blocking their movement.</td>
  </tr>
  <tr>
    <td><strong>Board and Pieces</strong></td>
    <td>- 8x8 board with corners removed. <br> - Two players: white and black. <br> - Pieces are single or double stacks.</td>
  </tr>
  <tr>
    <td><strong>Single Stacks</strong></td>
    <td>- Single pieces can move one space sideways or forward to empty spaces or onto one piece of the same color. <br> - They capture diagonally forward like chess pawns.</td>
  </tr>
  <tr>
    <td><strong>Double Stacks</strong></td>
    <td>- The top piece of a double stack can move or capture as a chess knight, but only forward.</td>
  </tr>
  <tr>
    <td><strong>Starting Setup</strong></td>
    <td>- Each player starts with 12 pieces: 6 in their home row and 6 in the second row without the corners.</td>
  </tr>
  <tr>
    <td><strong>Turns</strong></td>
    <td>- White moves first, after which turns alternate between players.</td>
  </tr>
  <tr>
    <td><strong>Capture</strong></td>
    <td>- When a friendly piece captures an enemy piece, it takes over its position on the board, and the captured enemy piece is removed.</td>
  </tr>
  <tr>
    <td><strong>No Skipping</strong></td>
    <td>- There is no skipping turns.</td>
  </tr>
</table>


For more detailed rules and examples, you can visit https://abstractmeanderings.wordpress.com/2014/10/06/jump-sturdy/ or https://www.mindsports.nl/index.php/the-pit/576-jumpsturdy

## Game Tree Exploration

## Game Representation

## Action Selection

## Limitations

## Notes
