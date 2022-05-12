import sys
import socket
import threading

from server import MAX_SIZE

HOST, PORT = sys.argv[1], int(sys.argv[2])

class Client:
    def __init__(self, sock, host, port):
        self.sock = sock
        self.port = port
        self.host = host
        self.lthread = threading.Lock()
        self.t1 = None
        self.t2 = None

    def start(self):
        try:
            self.establish_connection()
            
            response = self.sock.recv(MAX_SIZE)
            
            print (response.decode('utf-8'))
            
            self.lthread.acquire()
            
            while True:
                self.t1 = threading.Thread(target=self.handle_recieved_data)
                self.t2 = threading.Thread(target=self.handle_user_input)

                self.t1.start()
                self.t2.start()

                self.t1.join()
                self.t2.join()

        except KeyboardInterrupt:
            if self.t1 and self.t2:
                self.t1.join()
                self.t2.join()
            self.sock.close()
        except SystemExit:
            if self.t1 and self.t2:
                self.t1.join()
                self.t2.join()
            self.sock.close()

    def establish_connection(self):
        self.sock.connect((self.host, self.port))

    def handle_user_input(self):
        try:
            user_message = input("Type message: ")
            
            if (user_message):
                self.sock.send(bytes(user_message, encoding="utf-8"))
        except ConnectionAbortedError:
            print ("Connection was aborted handle user")

    def handle_recieved_data(self):
        try:
            response = self.sock.recv(MAX_SIZE)

            if not response:
                self.lthread.release()

            if len(response):
                print (response.decode("utf-8"))

        except ConnectionAbortedError as e:
            print ("Connection was aborted handle response")
            print (e)

if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        c = Client(sock, HOST, PORT)
        c.start()