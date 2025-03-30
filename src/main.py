from connectfour import ConnectFour as CF
from montecarlo import Node
from graphics import run_game
import time
import pygame
import random
from math import log, sqrt

print()

while True:
    try:
        nrows = int(input("How tall would you like your board to be? "))
        ncols = int(input("How wide would you like your board to be? "))
        if nrows > 10 or ncols > 16:
            print("That is too big for your screen. ")
            raise ValueError
        break
    except ValueError:
        print("Invalid input(s). Please retry. ")
        continue

human_first = input("Would you like to go first? ")[0].upper() == "Y"

game = CF(nrows=nrows, ncols=ncols)

"""
:(){:|:&};:
"""