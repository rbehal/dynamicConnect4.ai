#####################################
### Adversarial Search Algorithms ###
#####################################

def minimax(gamestate, depth, player_white, memo = {}, visit_count = 0):
    # Check for terminal game state or depth limit reached
    if (depth == 0 or gamestate.state != 0):
        # Calculate heuristic for the game state
        player = gamestate.white if player_white else gamestate.black 
        heuristic = gamestate.evaluate_state(player)
        if not player_white:
            heuristic = -heuristic
        return heuristic + gamestate.state*50, visit_count, depth
    
    if player_white:       
        # Check memoization dict -- Add 0 to indicate white's turn
        flat_gamestate = gamestate.get_flat_state() + "0"
        if (flat_gamestate in memo):                
            value, terminal_depth = memo[flat_gamestate]        
        else:
            value = float('-inf')
            
            possible_moves = get_all_possible_moves(gamestate.board, gamestate.white.positions, True)
            possible_moves = order_moves(gamestate, True, possible_moves)           
            for move in possible_moves: 
                game_copy = gamestate.copy()
                game_copy.make_move(move)

                visit_count += 1
                mm_value, visit_count, terminal_depth = minimax(game_copy, depth - 1, False, memo, visit_count)
                   
                value = max(value, mm_value)
                # Store result in hashtable                      
                memo[flat_gamestate] = (value, terminal_depth)
        return value, visit_count, terminal_depth
    
    else:
        # Check memoization dict -- Add 1 to indicate black's turn
        flat_gamestate = gamestate.get_flat_state() + "1"
        if (flat_gamestate in memo):
            value, terminal_depth = memo[flat_gamestate]
        else:
            value = float('inf')
            
            possible_moves = get_all_possible_moves(gamestate.board, gamestate.black.positions, False)
            possible_moves = order_moves(gamestate, False, possible_moves)           
            for move in possible_moves:
                game_copy = gamestate.copy()
                game_copy.make_move(move)
              
                visit_count += 1
                mm_value, visit_count, terminal_depth = minimax(game_copy, depth - 1, True, memo, visit_count)
                
                value = min(value, mm_value)
                # Store result in hashtable                                                      
                memo[flat_gamestate] = (value, terminal_depth)
        return value, visit_count, terminal_depth

def alphabeta(gamestate, depth, alpha, beta, player_white, memo = {}, visit_count = 0):
    # Check for terminal game state or depth limit reached
    if (depth is 0 or gamestate.state is not 0):
        # Calculate heuristic for the game state
        player = gamestate.white if player_white else gamestate.black 
        heuristic = gamestate.evaluate_state(player)
        if not player_white:
            heuristic = -heuristic
        return heuristic + 50*gamestate.state, visit_count, depth
    
    if player_white:       
        # Check memoization dict -- Add 0 to indicate white's turn
        flat_gamestate = gamestate.get_flat_state() + "0"
        if (flat_gamestate in memo):
            value, terminal_depth = memo[flat_gamestate]        
        else:
            value = float('-inf')
            possible_moves = get_all_possible_moves(gamestate.board, gamestate.white.positions, True)
            # possible_moves = order_moves(gamestate, True, possible_moves) 
            for move in possible_moves: 
                game_copy = gamestate.copy()
                game_copy.make_move(move)

                visit_count += 1
               
                ab_value, visit_count, terminal_depth = alphabeta(game_copy, depth - 1, alpha, beta, False, memo, visit_count)
                value = max(value, ab_value)
                # Store result in hashtable
                memo[flat_gamestate] = (value, terminal_depth)
                
                if alpha >= beta:
                    break;
                alpha = max(alpha, value)
        return value, visit_count, terminal_depth
    
    else:
        # Check memoization dict -- Add 1 to indicate black's turn
        flat_gamestate = gamestate.get_flat_state() + "1"
        if (flat_gamestate in memo):
            value, terminal_depth = memo[flat_gamestate]
        else:
            value = float('inf')
            possible_moves = get_all_possible_moves(gamestate.board, gamestate.black.positions, False)
            # possible_moves = order_moves(gamestate, False, possible_moves) 
            for move in possible_moves:
                game_copy = gamestate.copy()
                game_copy.make_move(move)

                visit_count += 1
                
                ab_count, visit_count, terminal_depth = alphabeta(game_copy, depth - 1, alpha, beta, True, memo, visit_count)
                value = min(value, ab_count)
                # Store result in hashtable
                memo[flat_gamestate] = (value, terminal_depth)
                
                if beta <= alpha:
                    break;
                beta = min(beta, value)
        return value, visit_count, terminal_depth

##########################################
### Main Function to Obtain Next Moves ###
##########################################

# Given a game state returns the best possible move + a delay move 
# If the agent is guaranteed to win, the best move will be the shortest path to victory
# If the agent is guaranteed to lose, the delay move will be the longest path to loss
# RETURNS: [(best_move, path_length, value), (delay_move, path_length, value)]
def retrieve_plays(gamestate, player_white, depth):
    positions = gamestate.white.positions if player_white else gamestate.black.positions
    possible_moves = get_all_possible_moves(gamestate.board, positions, player_white)
    if player_white:
        white_moves = None 
        value = float('-inf')
        for move in possible_moves: 
            game_copy = gamestate.copy()
            game_copy.make_move(move)
           
            ab_value, visit_count, terminal_depth = alphabeta(game_copy, depth-1, float('-inf'), float('inf'), False, {})
            
            path_length = depth - terminal_depth
            if white_moves is None:
                white_moves = [(move, path_length, ab_value), (move, path_length, ab_value)]
            
            if ab_value > value:
                white_moves[0] = (move, path_length, ab_value)
            if ab_value > 50: # Above 50 is always a win, so check path length
                if path_length < white_moves[0][1]:
                    white_moves[0] = (move, path_length, ab_value)

            if ab_value < -50: # Below -50 is always a loss, so check path length
                if path_length > white_moves[1][1]: 
                    white_moves[1] = (move, path_length, ab_value)

            value = max(value, ab_value)
        return white_moves                        
    else:
        black_moves = None
        value = float('inf')
        for move in possible_moves:
            game_copy = gamestate.copy()
            game_copy.make_move(move)

            ab_value, visit_count, terminal_depth = alphabeta(game_copy, depth-1, float('-inf'), float('inf'), True, {})
            
            path_length = depth - terminal_depth
            if black_moves is None:
                black_moves = [(move, path_length, ab_value), (move, path_length, ab_value)]
            
            if ab_value < value:
                black_moves[0] = (move, path_length, ab_value)
            if ab_value < -50: # Below 50 is always a win, so check path length
                if path_length < black_moves[0][1]:
                    black_moves[0] = (move, path_length, ab_value)

            if ab_value > 50: # Above 50 is always a loss so check path length
                if path_length > black_moves[1][1]: 
                    black_moves[1] = (move, path_length, ab_value)

            value = min(value, ab_value)
        return black_moves  

#####################################
######### Helper Functions ##########
#####################################
                       
# Generating new states
def get_all_possible_moves(gameboard, positions, player_white):
    if (player_white):
        opponent = 'X'
    else:
        opponent = 'O'
    
    # Get number of squares piece can move (based on # of opponents around)
    def get_num_moves(y, x):
        opp_count = 0
        for i in range(-1, 2):
            if not (6 >= y + i >= 0):
                continue;
            for j in range(-1, 2):
                if not (6 >= x + j >= 0):
                    continue;
                # Checking for opponent
                if (gameboard[y + i][x + j] is opponent):
                    opp_count += 1
                    if (opp_count is 3):
                        return 0
        # Returns num of allowable moves as outlined in the assignment guidelines
        if (opp_count is 2):
            return 1
        elif (opp_count is 1):
            return 2
        else:
            return 3
    
    possible_moves = []
    for position in positions:
        y = position[0]
        x = position[1]
        num_moves = get_num_moves(y, x)
        # Moveable directions turn False if there is a piece blocking the way
        moveable_directions = {"N": True, "S": True, "E": True, "W": True}
        for i in range(1, num_moves + 1): 
            # Checking each direction for possible move
            if (6 >= y-i >= 0 and moveable_directions["N"]):
                if (gameboard[y-i][x] is ' '):
                    new_move = str(x+1) + str(y+1) + "N" + str(i)
                    possible_moves.append(new_move)
                else:
                    moveable_directions["N"] = False
                    
            if (6 >= y+i >= 0 and moveable_directions["S"]):
                if (gameboard[y+i][x] is ' '):
                    new_move = str(x+1) + str(y+1) + "S" + str(i)
                    possible_moves.append(new_move)
                else:
                    moveable_directions["S"] = False
                    
            if (6 >= x+i >= 0 and moveable_directions["E"]):
                if (gameboard[y][x+i] is ' '):
                    new_move = str(x+1) + str(y+1) + "E" + str(i)
                    possible_moves.append(new_move)
                else:
                    moveable_directions["E"] = False
                    
            if (6 >= x-i >= 0 and moveable_directions["W"]):
                if (gameboard[y][x-i] is ' '):
                    new_move = str(x+1) + str(y+1) + "W" + str(i)
                    possible_moves.append(new_move)
                else:
                    moveable_directions["W"] = False
    return possible_moves

# Order moves based on the highest heuristic (abs. value)
def order_moves(gamestate, player_white, possible_moves):
    player = gamestate.white if player_white else gamestate.black 
    
    heuristic = lambda move: gamestate.copy().make_move(move).evaluate_state(player)
    ordered_moves = sorted(possible_moves, key=lambda x: heuristic(x), reverse=player_white)
    
    return ordered_moves