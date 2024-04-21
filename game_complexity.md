# Analyzing the Complexity of Jump Sturdy

## Understanding Game Complexity

It is important to know how deep the rabbit hole goes before jumping in. For it there are several factors we need to consider:

- **State Space:**
<br>This refers to the total number of possible game states (board configurations) that can arise during gameplay. 

- **Branching Factor:**
<br>This refers to the average/max number of legal moves available to a player at any given state. 

- **Game Tree Depth:** 
<br>This refers to the maximum depth of the game tree. This helps us determine how many moves ahead the AI should analyze.

While state space, branching factor, and depth are fundamental, additional factors influence the overall performance of the AI agent:

- **Game Rules:**
<br>Understand the rules thoroughly to define the game logic and understand how complex the computation would be for each move. Calculations involved in determining legal moves can add to the complexity of the overall problem.

<br>

## Analyzing Jump Sturdy

- **Branching Factor:**
<br>In Jump Sturdy, each player has a maximum of 12 pieces at any point. For calculating the branching factor, we only consider pieces that are "free" as blocked pieces do not contribute to the branching factor since they cannot move or attack.
	
	Free pieces can be classified as either single pieces or double stacks:
	- **Single Pieces**: 
	<br>Each free single piece has the potential to move into up to 5 new positions. These are the standard one step ahead move, the two lateral moves (left and right), and the two diagonal attacks (front-left and front-right).
	
	- **Double Stacks**: 
	<br>For double stacks, the top piece has up to 4 new positions it can move to. These are (left, left, front), (front, front, left), (front, front, right), and (right, right, front).
	
	To calculate the branching factor, we consider each of the, at most, 12 free pieces and the maximum number of potential moves for single pieces and the top piece of a double stack. Therefore, the branching factor is determined by multiplying the maximum number of free pieces by the maximum number of possible moves for each one of those pieces. This gives us a **branching factor of 12 × 5 , which equates to 60**.

- **Game Tree Depth:** 
<br>In each turn, every player must move at least one of their pieces. Each player has at least one free piece, meaning there is at least one possible legal move. If all of a player's pieces are blocked, the player cannot move, and the game ends. Considering the movement rules, with each turn, at least one piece from one player will advance at least one space on the field, regardless of whether it is a single piece or the top piece of a double stack. Thus, we can infer that the 6 pieces at the front of the starting formation will be moved a maximum of 6 times, and the pieces at the back will be moved a maximum of 7 times before they reach the opponent's back row. This results in a maximum of 6×6 + 6×7, totaling 78 turns. Therefore, **the depth of the game tree cannot be greater than 78.**
<br><br>Additionally, it's important to note that the actual maximum depth of the game tree might be less than 78 when considering the opponent's movements and the rules of the game. Since one player's pieces are not alone on the field, interactions between opposing pieces can significantly alter the progression of the game and, consequently, the maximum depth of the game tree. Captures and blocking of pieces may be inevitable, which would reduce the number of turns needed for a player to reach the opponent's back row, thus decreasing the maximum depth of the game tree.
<br><br>Analyzing the complexity of the game also involves examining the minimal depth of the game tree. This depth must be greater or equal to 3, as each player's pieces can advance a maximum of 2 spaces per turn. However, it should be less or equal to 6. This scenario would occur when the opponents do not attempt to block the advance of one of the frontline pieces in the starting formation, and these pieces advance one space at a time.


- **State Space:**
<br>Based on the maximum game tree depth and the branching factor, we can deduce that the total number of possible game states that can arise during gameplay is **less than or equal to 60 (branching factor) raised to the power of 78 (maximum game tree depth)**. This number is exceedingly large and must be considered when implementing the gaming agent. We will need to define a horizon (maximum depth at which we want to analyze future developments of the game), implement efficient tree search algorithms, and minimize computational costs at each turn.

<br>

## Summary of Findings

This analysis reveals several key factors influencing the complexity of the game Jump Sturdy.

- **Branching Factor:** Relatively high (potentially 60).
- **Game Tree Depth:** Theoretically up to 78 turns, but likely lower in practice due to captures and blockings.
- **State Space:** Extremely large (potentially 60^78).

The vast potential branching factor, game length, and resulting state space pose significant challenges for the AI agent. 
