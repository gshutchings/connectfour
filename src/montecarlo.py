"""
Creates a class for a Node object, which is the basis of a Monte Carlo Tree Search (MCTS)
To create a tree, simply do:
node = Node(env, exploration, sims)
env should be a ConnectFour object
exploration should be between 0.5 and 2, and affects exploration vs exploitation in the UCB1 equation (2 is high exploration)
sims should be around 100, and affects how much time is spent at each node

You should then run node.visit() repeatedly--this is what actually evolves the tree
Finally, run 
max(node.children, key=lambda child: child.wins / child.visits).move
to get which move the algorithm believes has the highest win rate
"""

from connectfour import ConnectFour as CF
import random
import time
from math import log, sqrt

class Node:

    # Creates a new node. 
    def __init__(self, env: CF, exploration: float, sims: int=100, parent=None) -> None:
        self.children = []
        self.terminal = env.winner is not None
        self.parent = parent
        self.leaf = True # Whether this node is a leaf (doesn't have children)
        self.visits = 0 # How many rollouts
        self.wins = 0 # Rollout outcomes
        self.env = env # Keeps the game state of the node
        self.exploration = exploration # Rate of exploration used in UCB equation: should be around 0.5-2
        self.turn = self.env.player
        self.sims = sims
        if self.env.moves:
            self.move = self.env.moves[-1]
        else:
            self.move = None # What move separates this node from its parent
        wins, losses = self.rollout(self.env, self.sims) # Initial rollout
        self.backpass(self.sims, wins, losses)
    
    # Upper confidence bound formula--will never be applied to a node without a parent
    def ucb(self) -> float:
        return (self.wins / self.visits) + self.exploration * sqrt(log(self.parent.visits) / self.visits)
    
    # Select a child to go to using the UCB formula
    def favorite_child(self): # -> Node
        if self.terminal == False:
            return max(self.children, key=lambda child: child.ucb())
    
    # Heart of Monte Carlo: play many games with randomly chosen moves
    # and see who wins the most in order to evaluate a position. 
    @staticmethod
    def rollout(env: CF, sims: int) -> int:
        positive_wins = 0
        negative_wins = 0
        for _ in range(sims):
            new_env = env.copy()
            while new_env.winner is None:
                new_env.make_move(random.choice(new_env.get_legal_moves())) # Random simulation
            if new_env.winner == 1:
                positive_wins += 1
            if new_env.winner == -1:
                negative_wins += 1
        return [positive_wins, negative_wins]
    
    # Take rollout information from a leaf node and recurse back down the tree
    def backpass(self, runs: int, wins: int, losses: int) -> None:
        self.visits += runs
        if self.turn == -1:
            self.wins += wins
        else:
            self.wins += losses
        if self.parent is not None: # Stop at the root node
            self.parent.backpass(runs, wins, losses) # Recurse through parents
    
    # Take a leaf node, create and rollout all of its children. 
    def expand(self) -> None:
        for move in self.env.get_legal_moves():
            child = self.env.copy()
            child.make_move(move)
            self.children.append(Node(child, self.exploration, self.sims, self)) # Create children
        self.leaf = False
    
    # If it is a not a leaf node, it chooses its favorite child repeatedly (using UCB) until it reaches a leaf node
    # Then, it stops being a leaf node and create leaf nodes of all of its children
    def visit(self):
        if self.leaf == False:
            self.favorite_child().visit()
        elif self.terminal == True:
            wins, losses = self.rollout(self.env, self.sims) # Do a rollout from the terminal node
            self.backpass(self.sims, wins, losses)        
        else: # It is a leaf node -> initialize all of its children
            self.expand()
    
    # Returns the maximum depth the tree reaches
    def depth(self):
        if len(self.children) == 0:
            return 0
        return 1 + max(child.depth() for child in self.children)

    # Returns the total number of nodes in the tree (positions evaluated)
    def size(self):
        if len(self.children) == 0:
            return 1
        return sum(child.size() for child in self.children)

# Uses a MCTS to calculate the best move from a given position, in a certain amount of time
# sims is how many simulations are run from each leaf node 
# Lower sims and lower exploration means higher depth, but lower accuracy
def find_best_move(env: CF, thinking_time: float, sims: int, exploration: float) -> int:
    node = Node(env=env, sims=sims, exploration=exploration)
    start = time.time()
    while time.time() - start < thinking_time:
        node.visit()
    return max(node.children, key=lambda child: child.wins / child.visits).move # Which child has the highest win rate
