"""
This class handles basic game logic for a connect four game of variable size, including:
    making moves
    unmaking moves
    getting legal moves
"""
class ConnectFour:

    def __init__(self, nrows: int=6, ncols: int=7, moves: list=[]) -> None:
        if nrows < 4 and ncols < 4 or nrows < 1 or ncols < 1:
            raise ValueError("This board size is too small for Connect Four to be played at all. ")
        self.nrows = nrows
        self.ncols = ncols
        self.moves = []
        self.player = 1
        self.winner = None
        self.board = [[0 for _ in range(ncols)] for _ in range(nrows)] 
        for index, move in enumerate(moves):
            if self.make_move(move) == False:
                raise ValueError(f"The inputted sequence of moves is invalid. Encountered error at move {index} ({move}). ")
    
    # Resets the board and variables
    def reset(self) -> None:
        self.moves = []
        self.player = 1
        self.board = [[0 for _ in range(self.ncols)] for _ in range(self.nrows)]
        self.winner = None
    
    # Gets a list of all legal moves, starting from 0 for the leftmost column; no moves are legal after game is over
    def get_legal_moves(self) -> list[int]:
        if self.winner is not None:
            return []
        return [col for col, piece in enumerate(self.board[0]) if piece == 0]
    
    # Finds and returns the [row, col] position of the last piece placed
    def get_most_recent_move(self) -> list[int]:
        if not self.moves:
            return None
        return [min(row for row in range(self.nrows) if self.board[row][self.moves[-1]] != 0), self.moves[-1]] 
        # takes the column (self.moves[-1]) and the geographically highest (lowest-number row) piece which is not 0 in that column

    # Updates the board, checks for a winner, etc. Returns whether the move was valid and successfully made
    def make_move(self, move: int) -> bool:
        if move not in self.get_legal_moves():
            return False 
        height = self.moves.count(move) # Counts how many times a particular column has been played before to see how high to put the piece
        self.board[self.nrows-1-height][move] = self.player
        self.moves.append(move)
        self._check_winner()
        self.player *= -1
        return True 
    
    # Undoes the most recent move. Returns whether there was a move to undo
    def unmake_move(self) -> bool:
        if not self.moves:
            return False
        most_recent_move = self.get_most_recent_move()
        self.player *= -1
        self.board[most_recent_move[0]][most_recent_move[1]] = 0
        self.moves.pop()
        self.winner = None
        return True
    
    # Checks if the game is won with the most recent piece. Used inside of self.make_move(). Returns whether the game is over yet
    def _check_winner(self) -> bool: 
        if len(self.moves) < 7:
            return False # There can't be a winner yet
        
        # Returns whether a given line contains a four-in-a-row
        def _check_line(line: list[int]) -> bool:
            for i in range(len(line)-3):
                if abs(sum(line[i:i+4])) == 4:
                    return True
            return False
        
        mrm = self.get_most_recent_move()
        left_dis = min(3, mrm[1])               # pieces further away from the most recent move than this aren't 
        right_dis = min(3, self.ncols-1-mrm[1]) # necessary to check for a four-in-a-row as they are too far away 
        up_dis = min(3, mrm[0])                 # or not within the board 
        down_dis = min(3, self.nrows-1-mrm[0])

        horizontal_line = [self.board[mrm[0]][i] for i in range(mrm[1]-left_dis, mrm[1]+right_dis+1)]   # Returns the horizontal line containing the most recent move
        vertical_line = [self.board[i][mrm[1]] for i in range(mrm[0]-up_dis, mrm[0]+down_dis+1)]        # that does need to be checked for a four-in-a-row
        positive_line = [self.board[mrm[0]-i][mrm[1]+i] for i in range(-min(down_dis, left_dis), min(up_dis, right_dis) + 1)]   # Contains every element from current-left_dis
        negative_line = [self.board[mrm[0]+i][mrm[1]+i] for i in range(-min(up_dis, left_dis), min(down_dis, right_dis) + 1)]   # to current+right_dis, for instance
                                                                                                        # For diagonals, chooses the smaller distance to not go out of bounds

        if _check_line(horizontal_line) or _check_line(vertical_line) or _check_line(positive_line) or _check_line(negative_line):
            self.winner = self.player
            return True 
        if len(self.moves) == self.nrows * self.ncols: # In case of draw (board is full and there is no winner)
            self.winner = 0
            return True 
        return False

    def __str__(self) -> str: # So you can do print(object) and get a reasonable format
        board_rep = "\n"
        board_rep += "----" * self.ncols + "- \n"
        for row in self.board:
            for piece in row:
                if piece == 1:
                    board_rep += "| X "
                if piece == -1:
                    board_rep += "| O "
                if piece == 0:
                    board_rep += "|   "
            board_rep += "| \n"
        board_rep += "----" * self.ncols + "- \n"
        for i in range(self.ncols):
            board_rep += f"  {i} "
        board_rep += "\n"
        return board_rep
