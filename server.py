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
games = {}
idCount = 0

def threaded_client(conn, player_index, game_index, client_id):
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

            # Send updated game state to all connected clients
            for client_conn, _ in connected_clients.values():
                client_conn.sendall(pickle.dumps((games[game_index], player_index)))

    except pickle.UnpicklingError as e:
        print(f"Error unpickling data: {e}")
    except socket.error as e:
        print(f"Socket error occurred: {e}")
    except Exception as e:
        print(f"Error in thread for Player {player_index}: {e}")
    finally:
        print(f"Lost connection from Player {player_index}")
        del connected_clients[client_id]
        conn.close()

while True:
    conn, addr = s.accept()
    print(f'Connected to: {addr}')

    client_id = addr  # Using address as a unique identifier
    if client_id in connected_clients:
        print(f"Client {client_id} is already connected. Ignoring this connection.")
        conn.close()
        continue

    idCount += 1
    player_index = 0
    gameID = (idCount - 1) // 2

    if idCount % 2 == 1:
        games[gameID] = Game(gameID)  # Ensure Game objects are properly initialized and pickleable
        print('Creating a new game...')
    else:
        player_index = 1

    connected_clients[client_id] = (conn, player_index)
    print(f'Game Index: {gameID}, Player: {player_index}, ID Count: {idCount}')
    start_new_thread(threaded_client, (conn, player_index, gameID, client_id))
