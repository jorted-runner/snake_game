from dotenv import load_dotenv
import socket
from _thread import *
import os
import pickle
from game import Game

load_dotenv()

server = os.environ.get('IP_ADDRESS')
port = int(os.environ.get('PORT'))

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
            data = pickle.loads(conn.recv(2048))
            game = data[0]
            games[game_index] = game
            if not data:
                print("Disconnected")
                break
            conn.sendall(pickle.dumps(games[game_index], player_index))

        except Exception as e:
            print(f"Error: {e}")
            break

    print("Lost connection")
    conn.close()

currentPlayer = 0

while True:
    conn, addr = s.accept()
    print(f'Connected to: {addr}')

    idCount += 1
    p = 0

    gameID = (idCount - 1) // 2
    if idCount % 2 == 1:
        games[gameID] = Game(gameID)
        print('Creating a new game...')
    else:
        p = 1

    start_new_thread(threaded_client, (conn, p, gameID))
