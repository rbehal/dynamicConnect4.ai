# To use: python main.py -c "colour" -p "port" "serverIP" "gameID"
from Game import Game
from algorithms import retrieve_plays
import argparse
import socket
import time

# Construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("host")
ap.add_argument("gameID")
ap.add_argument("-c", "--colour", required=True)
ap.add_argument("-p", "--port", required=True)
args = vars(ap.parse_args())

# Connect to server and set constants
SERVER_IP = args['host']
SERVER_PORT = int(args['port'])
GAME_ID = args['gameID']
COLOUR = args['colour']
BUFFER_SIZE = 10000
DIRECTIONS = ["N", "S", "E", "W"]

def print_game(gameboard):
    # Prints game board to terminal readably 
    for row in gameboard:
        print(row)

def send_move(gamestate, player_white, s):
    # Contains best move, delay move, and scores 
    moves = retrieve_plays(gamestate, player_white, 3)
    move = None
    # Check if player always loses, if so choose the delay move, otherwise choose best move
    if (moves[0][2] < -50 and player_white or moves[0][2] > 50 and not player_white):
        move = moves[1][0]
    else:
        move = moves[0][0]
    # Update internal belief state 
    gamestate.make_move(move)
    # Store move readably to keep track of moves made
    move_chars = move
    # Print move to terminal
    move = move + "\n"
    print("My move: %s" % move)
    print_game(gamestate.board)
    # Encode and send move to server
    move = str.encode(move)
    s.send(move)

    return move_chars

def read_move(move, gamestate, player_white):
    # Print move to terminal and update internal belief state
    gamestate.make_move(move)
    print("Opponent's move: {}".format(move + "\n"))
    print_game(gamestate.board)

def main():
    # Initialize connection to server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((SERVER_IP, SERVER_PORT))

    # Initialize game belief state
    path = "init.txt"
    f = open(path, "r")
    game_statef = f.read()
    game_statef = game_statef + "\n"

    game = Game(game_statef, txt_import = True)
    print_game(game.board)

    # Send server request to join a given game as a given player
    init_game = str.encode("{} {}\n".format(GAME_ID, COLOUR))
    s.send(init_game)

    # Start game
    game_on = True
    last_move = None
    while(game_on):
        time.sleep(1)
        
        player_white = COLOUR == "white"

        data = s.recv(BUFFER_SIZE)
        data = data.decode("ASCII")
        
        if (len(data) == 5): # Opponent's move
            incoming_move = data[0:4]
            if (incoming_move == last_move):
                # If client is reading its own move, skip
                continue; 
            else: # Otherwise, read the move and send one
                read_move(incoming_move, game, not player_white)
                time.sleep(1)
                last_move = send_move(game, player_white, s)
        elif "Game over" in data: # End game
            game_on = False
            print("Game over!")            
        elif GAME_ID in data: # Start game
            print("Game started!")
            if player_white:
                time.sleep(2)
                last_move = send_move(game, True, s)
        elif (len(data) != 0): # Misc. messages
            print(data, len(data))

if __name__ == "__main__":
    main()