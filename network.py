from dotenv import load_dotenv
import socket
from _thread import *
import os
import pickle

load_dotenv()

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = os.environ.get('IP_ADDRESS')
        self.port = int(os.environ.get('PORT'))
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048 * 4))
        except:
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048 * 4))
        except socket.error as e:
            print(e)
