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

connected_clients = {}
connected = set()
games = {}
idCount = 0

def threaded_client(conn, player_index, game_index):
    print(f'Thread started for Player {player_index} in Game {game_index}')
    try:
        conn.sendall(pickle.dumps((games[game_index], player_index)))
        while True:
            data = conn.recv(4096)
            if not data:
                print(f"No data received from Player {player_index}. Client might have disconnected.")
                break

            game_data = pickle.loads(data)
            games[game_index] = game_data[0]

            conn.sendall(pickle.dumps((games[game_index], player_index)))
    except pickle.UnpicklingError as e:
        print(f"Error unpickling data: {e}")
    except socket.error as e:
        print(f"Socket error occurred: {e}")
    except Exception as e:
        print(f"Error in thread for Player {player_index}: {e}")
    finally:
        print(f"Lost connection from Player {player_index}")
        connected.discard(conn)
        conn.close()

while True:
    conn, addr = s.accept()
    
    if conn in connected:
        conn.close()
    else:
        connected.add(conn)

    idCount += 1
    player_index = 0
    gameID = (idCount - 1) // 2

    if idCount % 2 == 1:
        games[gameID] = Game(gameID)
        print('Creating a new game...')
    else:
        player_index = 1

    print(f'Game Index: {gameID}, Player: {player_index}, ID Count: {idCount}')
    start_new_thread(threaded_client, (conn, player_index, gameID))
