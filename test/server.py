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

WINDOW_SIZE = 600
TILE_SIZE = 20

connected = set()
games = {}
idCount = 0

def threaded_client(conn, p_index, game_index):
    games[game_index]['connections'].append(conn)
    print(f'1st Sending: {games[game_index]["game"]}, {p_index}')
    conn.send(pickle.dumps((games[game_index]['game'], p_index)))
    while True:
        try:
            data = pickle.loads(conn.recv(2048*2))
            print(f'Received: {data[0]}, {data[1]}')
            games[game_index]['game'] = data[0]
            games[game_index]['game'].connect(data[1], p_index)
            print(games[game_index]['game'].snakes)
            print(f'2nd Sending: {games[game_index]["game"]}, {games[game_index]["game"].snakes[p_index]}')

            conn.sendall(pickle.dumps((games[game_index]['game'], games[game_index]["game"].snakes[p_index])))

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
    p_index = 0

    gameID = (idCount - 1) // 2
    if idCount % 2 == 1:
        games[gameID] = {'game': Game(gameID), 'connections': []}
        print('Creating a new game...')
    else:
        p_index = 1

    start_new_thread(threaded_client, (conn, p_index, gameID))
