import sys
import socket
import threading

from threaded_client import ThreadedClient

HOST, PORT = sys.argv[1], int(sys.argv[2])

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
