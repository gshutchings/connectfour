"""
Creates a class for a Node object, which is the basis of a Monte Carlo Tree Search (MCTS)
To create a tree, simply do:
env = CF(args)
node = Node(env, exploration, sims)
env should be a ConnectFour
exploration should be between 0.5 and 2, and affects exploration vs exploitation in the UCB1 equation
sims should be around 100, and affects how much time is spent at each node

You should then run node.visit() repeatedly
Finally, run 
max(node.children, key=lambda child: child.wins / child.visits).move
to get which move the algorithm chose
"""

from connectfour import ConnectFour as CF
import random
from math import log, sqrt
import time

class Node:

    # Creates a new node. 
    def __init__(self, env: CF, exploration: float, sims: int=100, parent=None):
        self.children = []
        self.terminal = env.winner is not None
        self.parent = parent
        self.leaf = True
        self.visits = 0 # How many rollouts
        self.wins = 0 # Rollout outcomes
        self.env = env
        self.exploration = exploration # Rate of exploration used in UCB equation: should be around 0.5-2
        self.turn = self.env.player
        self.sims = sims
        if self.env.moves:
            self.move = self.env.moves[-1]
        else:
            self.move = None # What move separates this node from its parent
        wins, losses = self.rollout(self.env, self.sims) # Initial rollout
        self.backpass(self.sims, wins, losses)
    
    # Upper confidence bound formula
    def ucb(self) -> float:
        return (self.wins / self.visits) + self.exploration * sqrt(log(self.parent.visits) / self.visits)
    
    # Select a child to go to using the UCB1 formula
    def favorite_child(self):
        if self.terminal == False:
            return max(self.children, key=lambda child: child.ucb())
    
    # Main facet of the Monte Carlo strategy: play many games with randomly chosen moves
    # and see who wins the most in order to evaluate a position. 
    @staticmethod
    def rollout(env: CF, sims: int) -> int:
        positive_wins = 0
        negative_wins = 0
        for _ in range(sims):
            new_env = env.copy()
            while new_env.winner is None:
                new_env.make_move(random.choice(new_env.get_legal_moves()))
            if new_env.winner == 1:
                positive_wins += 1
            if new_env.winner == -1:
                negative_wins += 1
        return [positive_wins, negative_wins]
    
    # Take win information from a leaf node, send it back down through its parents to the root
    def backpass(self, runs, wins, losses):
        self.visits += runs
        if self.turn == -1:
            self.wins += wins # The player in that node was the player who won
        else:
            self.wins += losses
        if self.parent is not None: # Can't go back further than the leaf node
            self.parent.backpass(runs, wins, losses) # Recurse
    
    # Take a leaf node, create and rollout all of its children. Returns nothing
    def expand(self):
        for move in self.env.get_legal_moves():
            child = self.env.copy()
            child.make_move(move)
            self.children.append(Node(child, self.exploration, self.sims, self))
        self.leaf = False
    
    # If it is a not a leaf node, it chooses its favorite child to recurse
    # Otherwise, it will stop being a leaf node and create leaf nodes of all of its children
    def visit(self):
        if self.leaf == False:
            self.favorite_child().visit()
        elif self.terminal == True:
            wins, losses = self.rollout(self.env, self.sims) # Do a rollout from that node
            self.backpass(self.sims, wins, losses)        
        else: # It is a leaf node -> initialize all of its children
            self.expand()
    
    # Returns the maximum depth the tree reaches after a node (use the root node for the whole tree)
    def depth(self):
        if len(self.children) == 0:
            return 0
        return 1 + max(child.depth() for child in self.children)

    # Returns the total number of nodes in the tree (positions)
    def size(self):
        if len(self.children) == 0:
            return 1
        return sum(child.size() for child in self.children)

if __name__ == "__main__":
    env = CF()
    print(env)
    sims = 100
    node = Node(env, exploration=5, sims=sims)
    THINKING_TIME = 50
    start = time.time()

    while time.time() - start < THINKING_TIME:
        node.visit()
        print("Win probabilities: ", [round(child.wins / child.visits, 4) for child in node.children])
        print("Depth: ", node.depth())
        print("Total number of rollouts: ", node.visits)
        print("Total number of nodes: ", node.size())
        print("Total time: ", round(time.time()-start, 2))
        print("\n")

    for move, child in enumerate(node.children): 
        print("Move ", move, " depth: ", child.depth())

    try:
        print(max(node.children, key=lambda child: child.wins / child.visits).move)
    except ValueError:
        print("The game is over! GG")
    print(env)
