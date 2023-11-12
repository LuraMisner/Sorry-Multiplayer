import constants
import socket
import pickle
from _thread import *
from game import Game
from ast import literal_eval

# Running on local host
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((constants.SERVER, constants.PORT))
except socket.error as e:
    print(str(e))

# Listen for connections ( Number indicates maximum amount of connections )
s.listen(4)
print("Waiting for a connection, Server Started")

games = {}
ready = {}
vote_new_game = {}


def create_new_game(game_id):
    print(f'Creating new game for game {game_id}')
    new_game = Game()

    for player in games[game_id].players:
        new_game.add_player(player.get_color())

    games[game_id] = new_game

    # Undo new game flags
    for key in vote_new_game[game_id].keys():
        vote_new_game[game_id][key] = False


def threaded_client(connect, p_id, game_id):
    """
    Function that handles communication between the client and the server
    :param connect: Address of client
    :param p_id: Integer id of player
    :param game_id: Integer id of game
    """
    connect.send(str.encode(str(p_id)))
    color = None
    reply = ""
    vote_new_game[game_id][p_id] = False

    while True:
        try:
            data = connect.recv(2048).decode()

            if game_id in games:
                game = games[game_id]

                if not data:
                    break
                else:
                    if data == 'available_colors':
                        reply = game.available_colors

                    # Tells client how many players are ready out of the players in this game
                    elif data == 'num_ready':
                        reply = [len(ready[game_id])]
                        num_ready = 0
                        for player in ready[game_id]:
                            if player:
                                num_ready += 1
                        reply.append(num_ready)

                    # Verify that this choice is valid
                    elif data[:13] == 'verify_choice':
                        choice = data[14:]
                        reply = game.add_player(choice)

                        # If verified, mark this player as ready and keep track of their choice
                        if reply:
                            ready[game_id][p_id] = True
                            color = choice

                    # For restarting a game, sets player as ready
                    elif data == 'ready':
                        ready[game_id][p_id] = True

                    # Check if all players are ready to start
                    elif data == 'start':
                        reply = all(ready[game_id])

                        if reply:
                            game.order_players()

                    # Returns the player object to the client
                    elif data == 'my_player':
                        reply = game.get_player(color)

                    # Returns a dictionary of all players positions
                    elif data == 'get_player_positions':
                        reply = game.get_player_positions()

                    # Update the player position
                    elif data[:15] == 'update_position':
                        position = literal_eval(data[16:])
                        game.update_player_location(color, position)

                    elif data[:20] == 'update_all_positions':
                        positions = literal_eval(data[21:])
                        game.update_all_locations(positions)

                    # Ends the turn and moves to the next player
                    elif data == 'end_turn':
                        game.next_player()

                    # Returns the players color of whose turn it is
                    elif data == 'whos_turn':
                        reply = game.get_turn()

                    # Draw the next card from the deck
                    elif data == 'draw_card':
                        game.draw_card()

                    # Get the card value of the current card
                    elif data == 'get_card':
                        reply = game.current_card()

                    # Ends the players turn and moves to the next player
                    elif data == 'end_turn':
                        game.check_win()
                        game.next_player()

                    # Check if there's a message for our user
                    elif data == 'check_log':
                        reply = game.get_msg(color)

                    # Add a message for another player
                    elif data[:7] == 'add_log':
                        col, msg = data[8:].split(',')
                        game.add_msg(col, msg)

                    # Check if there is a winner
                    elif data == 'check_won':
                        game.check_win()
                        reply = game.won

                    # Get the winners name
                    elif data == 'winner':
                        reply = game.winner

                    elif data == 'new_game':
                        vote_new_game[game_id][p_id] = True

                    elif data == 'new_game_votes':
                        length = 0
                        votes = 0
                        for key in vote_new_game[game_id].keys():
                            if vote_new_game[game_id][key]:
                                votes += 1
                            length += 1

                        reply = [votes, length]

                    elif data == 'start_new_game':
                        # Check that all votes have been made for a new game, and then create the new game
                        flag = True
                        for key in vote_new_game[game_id].keys():
                            if not vote_new_game[game_id][key]:
                                flag = False

                        if flag:
                            create_new_game(game_id)

                    elif data == 'check_vote':
                        reply = vote_new_game[game_id][p_id]

                    elif data == 'add_bot':
                        game.add_bot()

                    elif data == 'remove_bot':
                        game.remove_bot()

                    # If a player quits, this will remove them from the game
                    elif data == 'quit':
                        if color:
                            game.remove_player(color)

                        ready[game_id].pop()
                        del vote_new_game[game_id][p_id]

                    connect.sendall(pickle.dumps(reply))

            else:
                break
        except Exception as er:
            print("Error: ", er)
            break

    print("Lost connection")
    connect.close()


g_id = 0
while True:
    """
    Accepts incoming connections, and places them into a game.
    Creates a new game if none are available.
    Starts the client on a thread
    """
    conn, addr = s.accept()
    print("Connected to: ", addr)

    # If the game is full or already started, then move to a different game
    if g_id in games:
        if all(ready[g_id]) or len(ready[g_id]) == 4:
            g_id += 1

    # If the game does not exist, make a new one
    if g_id not in games:
        print("Creating a new game...")
        games[g_id] = Game()
        ready[g_id] = []
        vote_new_game[g_id] = {}

    ready[g_id].append(False)
    start_new_thread(threaded_client, (conn, len(ready[g_id]) - 1, g_id))
