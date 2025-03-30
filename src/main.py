from connectfour import ConnectFour as CF
from montecarlo import find_best_move
from graphics import run_game

print()
print()
print("Welcome to Connect Four. You drop your tiles into a column and try to get four in a row.")
print("You can press escape to close out of the window at any time. ")
print("You can go back a move using left arrow. ")
print("Just click to drop. Have fun! ")
print()
print()

while True:
    try:
        ncols = int(input("How wide would you like your board to be? "))
        nrows = int(input("How tall would you like your board to be? "))
        if ncols > 16 or nrows > 10:
            print("This might be too big for your screen. Consider a smaller board. ")
            raise ValueError
        game = CF(ncols=ncols, nrows=nrows)
        break
    except ValueError:
        print("Something went wrong. Please enter integers 2-16 and 1-10")
        continue

try:
    human_first = input("Would you like to go first? ")[0].upper() == "Y"
except IndexError:
    human_first = True

print()

run_game(game, human_first)
