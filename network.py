from dotenv import load_dotenv
import socket
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
            return self.receive_data()
        except Exception as e:
            print(f"Error connecting to server: {e}")
            return None  # or handle the error according to your application's logic

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return self.receive_data()
        except socket.error as e:
            print(f"Socket error occurred: {e}")
            return None  # or handle the error according to your application's logic
        except pickle.UnpicklingError as e:
            print(f"Error unpickling data: {e}")
            return None  # or handle the error according to your application's logic
        except Exception as e:
            print(f"Unknown error occurred: {e}")
            return None  # or handle the error according to your application's logic

    def receive_data(self):
        try:
            data = pickle.loads(self.client.recv(4096))
            return data
        except pickle.UnpicklingError as e:
            print(f"Error unpickling received data: {e}")
            return None  # or handle the error according to your application's logic
        except Exception as e:
            print(f"Error receiving data: {e}")
            return None  # or handle the error according to your application's logic
