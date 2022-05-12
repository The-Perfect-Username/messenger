import sys
import socket
import threading
import queue
from typing import final

HOST, PORT = sys.argv[1], int(sys.argv[2])

MAX_SIZE = 2048

class ThreadedClient:
    def __init__(self, connection):
        self.connection = connection
        self.send_q = queue.Queue(maxsize=10)
        
    def run(self):
        try:
            self.connection.send("Welcome to the server!".encode('utf-8'))
            self.listen()
        except Exception as e:
            print (e)
        finally:
            self.connection.close()

    def listen(self):
        while True:
            print ("Checking queue...")
            if not self.send_q.empty():
                self.send_message()
            else:
                print ("No message in queue")

            message = self.connection.recv(MAX_SIZE)

            self.add_message(message=message)

    def add_message(self, message):
        self.send_q.put(message)
    
    def get_message(self):
        if self.send_q.empty():
            print ("No message found")
            return

        return self.send_q.get()

    def send_message(self):
        message = self.get_message()

        if message:
            self.connection.sendall(message)
       
class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = set()
        self.clients_lock = threading.Lock()

    def run(self):
        try:
            self.socket.bind((self.host, self.port))
            self.socket.listen(10)

            while True:
                Client, address = self.socket.accept()

                print('Connected to: ' + address[0] + ':' + str(address[1]))

                with self.clients_lock:
                    self.clients.add(Client)

                threading.Thread(target=self.target, args=(Client,)).start()

        except KeyboardInterrupt:
            print("Caught keyboard interrupt, exiting")
            self.socket.close() 
        finally:
            print ("Closing socket")
            self.socket.close() 

    def target(self, Client):
        client_thread = ThreadedClient(Client)
        client_thread.run()

if __name__ == "__main__":
    server = Server(HOST, PORT)
    server.run()
