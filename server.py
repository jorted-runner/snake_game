from dotenv import load_dotenv
import socket
from _thread import *
import os
from game_snake import Snake
from game_food import Food
from game_portals import Portal
import pickle

load_dotenv()

server = os.environ.get('IP_ADDRESS')
port = int(os.environ.get('PORT'))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen(2)
print('Waiting for a connection, Server Started')

WINDOW_SIZE = 600
TILE_SIZE = 20
FPS = 7
snakes = [Snake([(100, 100), (100, 75), (100, 50)], 'green'), Snake([(550, 100), (550, 75), (550, 50)], 'purple')]
food = Food(WINDOW_SIZE, WINDOW_SIZE, TILE_SIZE)
portals = Portal()

def threaded_client(conn, currentPlayer, food, portals, FPS):
    conn.send(pickle.dumps((snakes, food, portals, FPS)))
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            if not data:
                print('Disconnected')
                break

            snakes[currentPlayer] = data[0][currentPlayer]
            food = data[1]
            portals = data[2]
            FPS = data[3]

            reply = (snakes, food, portals, FPS)
            conn.sendall(pickle.dumps(reply))

        except Exception as e:
            print(f"Error: {e}")
            break

    print('Lost connection')
    conn.close()

currentPlayer = 0

while True:
    conn, addr = s.accept()
    print(f'Connected to: {addr}')

    start_new_thread(threaded_client, (conn, currentPlayer, food, portals, FPS))
    currentPlayer += 1
