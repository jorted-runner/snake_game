from dotenv import load_dotenv
import socket
from _thread import *
import os
from COPY_game import Game
from game_snake import Snake
import pickle

load_dotenv()

server = os.environ.get('IP_ADDRESS')
port = int(os.environ.get('PORT'))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)
game = Game()
s.listen(2)
print('Waiting for a connection, Server Started')
players = [Snake([(100,100), (100,75), (100,50)],'green'), Snake([(550,100),(550,75),(550,50)], 'purple')]

def threaded_client(conn, currentPlayer):
    conn.send(pickle.dumps(players[currentPlayer]))
    reply = ''
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            players[currentPlayer] = data
            if not data:
                print('Disconnected')
                break
            else:
                if currentPlayer == 1:
                    reply = players[0]
                else:
                    reply = players[1]
                print(f'Received: {data}')
                print(f'Sending: {reply}')

            conn.sendall(pickle.dumps(reply))

        except:
            break

    print('Lost connection')
    conn.close()

currentPlayer = 0

while True:
    conn, addr = s.accept()
    print(f'Connected to: {addr}')

    start_new_thread(threaded_client, (conn,currentPlayer,))
    currentPlayer += 1