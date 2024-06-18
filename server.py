from dotenv import load_dotenv
import socket
from _thread import *
import os
import pickle
from game import Game

load_dotenv()

server = os.getenv('IP_ADDRESS')
port = int(os.getenv('PORT'))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting for a connection, Server Started")

connected = set()
games = {}
idCount = 0

def threaded_client(conn, player_index, game_index):
    conn.send(pickle.dumps((games[game_index], player_index)))
    while True:
        try:
            data = conn.recv(4096)
            if not data:
                print("No data received. Client might have disconnected.")
                break

            game_data = pickle.loads(data)
            games[game_index] = game_data[0]

            # Send updated game state to all connected clients
            for c in connected:
                c.sendall(pickle.dumps((games[game_index], None)))

        except Exception as e:
            print(f"Error: {e}")
            break

    print("Lost connection")
    connected.remove(conn)
    conn.close()

currentPlayer = 0

while True:
    conn, addr = s.accept()
    print(f'Connected to: {addr}')
    connected.add(conn)

    idCount += 1
    p = 0

    gameID = (idCount - 1) // 2
    if idCount % 2 == 1:
        games[gameID] = Game(gameID)
        print('Creating a new game...')
    else:
        p = 1

    start_new_thread(threaded_client, (conn, p, gameID))
