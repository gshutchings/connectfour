# Connect Four
This project implements a Monte Carlo Tree Search (MCTS) to play the popular board game of Connect Four, extended to any size. Unlike regular search algorithms, such as minimax, MCTS requires no prior knowledge as to how the game is played, as it bases its evaluation function off of random simulations of the game. 

# Monte Carlo algorithm
The Monte Carlo algorithm is typically composed of four steps:
 - Selection: The tree is traversed, choosing a child node using the Upper Confidence Bound (UCB) formula, which balances exploration (reaching nodes which haven't been well explored yet) and exploitation (reaching nodes which are more likely to occur in a game). This continues until a leaf node is reached. 
 - Expansion: The leaf node is made into a regular node, and its children (the positions immediately reachable from the node's position) are made into leaf nodes. 
 - Simulation: Simulate numerous games from that position, choosing moves randomly each time, to estimate how promising that node is. 
 - Backpropagation: The results from those new nodes are passed back down through the tree, recursively updating the UCB values of its parent. 
Repeating those four steps numerous times eventually creates a well-formed tree, which conveniently converges (after many iterations, of course) to the tree formed by a minimax algorithm. 

# Dependencies
Python>=3.9.6

pygame>=2.6.1

# Running 
To run, run `python3 src/main.py`. You will be asked to choose the board size and whether you go first. 