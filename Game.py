from Player import Player 
from copy import copy, deepcopy

class Game:
    def __init__(self, gamestate, txt_import = False, black_positions = None, white_positions = None):
        self.state = 0

        self.black = Player("X") 
        self.white = Player("O")
        
        if txt_import:
            # txt_import should be txt file containing 7 rows of 13 chars (6 commas) + \n
            self.init_game(gamestate)
        else: # Used to clone game state
            self.board = deepcopy(gamestate)
            self.black.positions = deepcopy(black_positions)
            self.white.positions = deepcopy(white_positions)

    def init_game(self, gamestate):
        # Convert text file to 2D array
        self.board = []
        row = []
        
        for char in gamestate:
            if (char is '\n'):
                self.board.append(row)
                row = [] 
                continue; 

            if (char is 'X'):
                row.append('X')
                self.black.add_pos((len(self.board), len(row)-1)) 
            elif (char is 'O'):
                row.append('O')
                self.white.add_pos((len(self.board), len(row)-1)) 
            elif (char is ' '):
                row.append(' ')

    # Checks a given state to see if the agent won, returns state
    def check_overall_state(self): 
        check_white = [[0] * 8 for _ in range(8)]
        check_black = [[0] * 8 for _ in range(8)]

        for i in range(1, 8):
            for j in range(1, 8):
                # Checking if 2x2 square for Black
                if (self.board[i-1][j-1] is 'X'):
                    # Get min of three other values in check submatrix
                    top_left = check_black[i-1][j-1]
                    top_right = check_black[i-1][j]
                    left = check_black[i][j-1]

                    matrix_size = 1 + min(top_left, top_right, left)

                    if (matrix_size >= 2):
                        self.state = -1 
                        return -1

                    check_black[i][j] = matrix_size       

                # Checking if 2x2 square for White -- Same as Black's
                if (self.board[i-1][j-1] is 'O'):
                    top_left = check_white[i-1][j-1]
                    top_right = check_white[i-1][j]
                    left = check_white[i][j-1]

                    matrix_size = 1 + min(top_left, top_right, left)

                    if (matrix_size >= 2):
                        self.state = 1 
                        return 1

                    check_white[i][j] = matrix_size       
        return 0
    
    # Checking if a given piece is part of a win
    def check_local_state(self, x, y):
        # Initialize secondary matrix to keep track of pieces
        check = [[0] * 4 for _ in range(4)]
        player = self.board[y][x]
        
        for i in range(y-1, y+2):
            if i < 0 or i > 6:
                continue; 
            for j in range(x-1, x+2):
                if j < 0 or j > 6:
                    continue; 
                # Checking if 2x2 square exists
                if (self.board[i][j] is player):
                    # Get min of three other values in check submatrix
                    top_left = check[i-y][j-x]
                    top_right = check[i-y][j-x+1]
                    left = check[i-y+1][j-x]

                    matrix_size = 1 + min(top_left, top_right, left)

                    if (matrix_size >= 2):
                        if (player is 'X'):
                            self.state = -1
                            return -1
                        elif (player is 'O'):
                            self.state = 1
                            return 1

                    check[i-y+1][j-x+1] = matrix_size  
        return 0 
    
    # Assume input is legitimate, and make appropriate move
    # Move is input in the form "XYDM"
    def make_move(self, move):
        old_x = int(move[0]) - 1
        old_y = int(move[1]) - 1
        num_spaces = int(move[3])
        if (move[2] is "N"):
            direction = (-1, 0)
        elif (move[2] is "S"):
            direction = (1, 0)
        elif (move[2] is "E"):
            direction = (0, 1)
        elif (move[2] is "W"):
            direction = (0, -1)

        new_y = old_y + direction[0]*num_spaces
        new_x = old_x + direction[1]*num_spaces
        
        # Make move
        self.board[new_y][new_x] = self.board[old_y][old_x]
        self.board[old_y][old_x] = " "
        
        # Update position sets 
        if (self.board[new_y][new_x] is 'O'):
            self.white.positions.remove((old_y, old_x))
            self.white.positions.add((new_y, new_x))
        elif (self.board[new_y][new_x] is 'X'):
            self.black.positions.remove((old_y, old_x))
            self.black.positions.add((new_y, new_x))  
            
        # Check to see if the move casued a win
        self.check_local_state(new_x, new_y)
        return self
        
    def copy(self):
        game_copy = Game(self.board, black_positions = self.black.positions,
                         white_positions = self.white.positions)
        return game_copy
    
    def get_flat_state(self):
        # Outputs flattened version of array in a string
        # For use with a memoization array to store evaluation func. values
        flat_state = ""
        for row in self.board:
            for char in row:
                flat_state += char
        return flat_state

    # Calculate heuristic for current game state and player
    def evaluate_state(self, player):
        heuristic = 0
        sym = player.symbol
        layers = 3
        for position in player.positions: 
            y = position[0]
            x = position[1]
            # Add to pieces if neighbouring piece is player's
            # Subtract from pieces if neighbouring piece is opponent's
            pieces = 0
            for i in range(-1, 2):
                for j in range(-1, 2):
                    for k in range(1, layers):
                        # Checking pieces around position
                        if (0 > y + k*i or y + k*i > 6):
                            continue
                        if (0 > x + k*j or x + k*j> 6):
                            continue
        
                        surrounding_piece = self.board[y + k*i][x + k*j]
                        if (surrounding_piece == sym):
                            pieces = pieces + (layers-k)*1
                        elif (surrounding_piece != ' '):
                            pieces = pieces - (layers-k)*0.25                            
            heuristic += pieces
        return heuristic 

                       