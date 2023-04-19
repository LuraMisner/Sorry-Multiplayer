import constants
import socket
import pickle
from _thread import *
from game import Game

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

                    elif data == 'start':
                        reply = all(ready[game_id])

                    connect.sendall(pickle.dumps(reply))
            else:
                break
        except Exception as er:
            print("Error: ", er)
            break

    print("Lost connection")
    connect.close()


id_count = 0
g_id = 0
while True:
    """
    Accepts incoming connections, and places them into a game.
    Creates a new game if none are available.
    Starts the client on a thread
    """
    conn, addr = s.accept()
    print("Connected to: ", addr)
    id_count += 1

    # If the game is full or already started, then move to a different game
    if g_id in games:
        if all(ready[g_id]) or len(ready[g_id]) == 4:
            print('HERE')
            g_id += 1

    # If the game does not exist, make a new one
    if g_id not in games:
        print("Creating a new game...")
        print(g_id)
        games[g_id] = Game()
        ready[g_id] = []
        id_count = 0

    ready[g_id].append(False)
    start_new_thread(threaded_client, (conn, id_count, g_id))
