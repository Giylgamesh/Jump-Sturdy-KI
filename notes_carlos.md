## Alpha-Beta Pruning

## State Representation

## Positional Evaluation: Early vs. Late Game
The AI uses positional evaluation to score each square based on its strategic advantage. This is particularly useful early in the game, where strong piece positioning and formation strategies can significantly influence the outcome. Due to computational limitations, the AI might not be able to explore the entire game tree, forcing it to rely on predefined scores determined by heuristics or loosely defined rules. These scores can be biased and may not be optimal.

Therefore, in the mid and late game, relying solely on positional scores becomes less effective. Here, the focus should shift towards achieving victory, not achieving a strong formation. One approach is to use positional scores as part of the heuristic function only during the early game (first n rounds or until a specific condition is met). Later, the AI can prioritize achieving a winning position.

Factors that could influence the score:
- **Defensive Potential:**
  - squares that defend the center of the board could prevent the enemy from advancing. 
  - squares that defend the first rows could prevent the opponent from winning.
- **Board Control:**
  - Squares that cover provide defensive cover for your valuable pieces or block opponent's attacks will have a higher positive score.
  - all squares in the opponent's back row should have the same very high value
  - the squares in the row before it should also have a high value, but dont know if the all should have the same value or what value.

### Notes
- There is a difference between occupying a certain square with a single piece, the top of a stack, or the bottom of a stack.
- Instead of assigning values to specific squares on the board, we could assign values to formations/structurey. This way, instead of focusing on achieving a complicated formation and changing the focus from then on, we could focus on achieving simpler but flexible formation and moving it across the board.
  - In this case we would have to think of backup plans for when our pieces get compromised or the opponent moves unexpectedly.
- In the case of implementing normal positional evaluation we should be carefull of being too focused on achieving the specific formation instead of winning. Imagine what would happen if there was a super fast winning AI.

## Heuristic-Based Decision Making
Factors that could influence the heuristic value:
- **Distance to Opponent's Back Row:** Movements that lead closer to the opponent's back row should have a higher heuristic value.
- **Attacking Potential:** Number of opponent pieces a move can attack/capture.
- **Defensive Potential:** Number of your pieces a move can defend or squares it protects.
- **Threat Level:** Movements that lead to attacked squares should ha a lowe heuristic value.
- **Piece Mobility:** How many squares a piece can move to after the action.
- **Piece Value:** Formation of double stacks.
- **Capturing bonus** Capturing pieces should be valuable.

### Other posible factors
- **Formation Bonus:** Bonus for achieving or maintaining a desired formation structure.
- **Center Control:** Control over central squares on the board.
- **Tempo Advantage:** Gaining an extra move or action compared to the opponent.
- **King Safety:** If we are using formations and have some kind of a king.
- **Piece Coordination:** If we are moving in formations (but this could be done above in positional evaluation)
