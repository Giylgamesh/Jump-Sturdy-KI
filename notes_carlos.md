## Alpha-Beta Pruning

## State Representation

## Positional Evaluation
The AI will evaluate the game board by assigning a score to each square based on the strategic advantage of controlling that square.

Factors that **could** influence the score:
- **Distance to Opponent's Back Row:**
  - Squares closer to the opponent's back row should have a higher score.
  - Squares in the opponent's back row should have the same value as the game has no punctation, you either win or lose.
  - This score can be further increased if controlling the square often/probably leads to winning the game.
- **Defensive Potential:**
  - squares that defend key areas, like the first rows, could be higher valued as they could help to prevent the opponent from winning by reaching one's home row.
  - Squares occupied by opponent's pieces will receive a negative score, with a penalty for squares that directly threaten your valuable pieces.
- **Defensive Potential:**
- **Board Control:**
  - Squares that cover provide defensive cover for your valuable pieces or block opponent's attacks will have a higher positive score.
  - all squares in the opponent's back row should have the same very high value
  - the squares in the row before it should also have a high value, but dont know if the all should have the same value or what value.

### Dynamic Positional Evaluation
- We could also base the score of each square on the current state of the game but it could be computationally expensive and could be addressed with heuristics for example controlling a square one row before the opponents back row could be valuable or not depemding on the state of the game. If we thing that the value assigned to a specific square should be lowered if the opponent can capture the piece after it is moved there, we would need to analyse if there are cases in which it is good to sacrifice a piece. We could implement this as a Heuristic so Alpha Beta explores this posibility sonner or later.
- On defense we could also move should think about how to 

For it we could use [examples of techniques]


## Heuristic-Based Decision Making
