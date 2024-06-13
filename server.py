from dotenv import load_dotenv
import socket
from _thread import *
import os
from game_food import Food
from player import Player
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
print("Waiting for a connection, Server Started")

WINDOW_SIZE = 600
TILE_SIZE = 20

class Game:
    def __init__(self) -> None:
        snakes = [Player([(100, 100), (100, 75), (100, 50)], 'green'), Player([(500, 100), (500, 75), (500, 50)], 'purple')]
        food = [Food(WINDOW_SIZE, WINDOW_SIZE, TILE_SIZE)]

games = []
def threaded_client(conn, player_index):
    global snakes, food
    conn.send(pickle.dumps((snakes, food)))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            if not data:
                print("Disconnected")
                break

            snakes[player_index] = data[0][player_index]
            food = data[1]
            if snakes[0].send_food_update or snakes[1].send_food_update:    
                food[0].rect.center = food[0].get_random_position(WINDOW_SIZE, WINDOW_SIZE, TILE_SIZE)
                snakes[0].send_food_update = False
                snakes[1].send_food_update = False
            reply = (snakes, food)
            conn.sendall(pickle.dumps(reply))

        except Exception as e:
            print(f"Error: {e}")
            break

    print("Lost connection")
    conn.close()

currentPlayer = 0

while True:
    conn, addr = s.accept()
    print(f"Connected to: {addr}")
# I want to work on this section so that a new game is created after two people have connected and the game is stored on the server
    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
