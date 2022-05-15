import queue

from common import MAX_SIZE

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