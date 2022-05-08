from concurrent.futures import thread
import sys
import socket
import threading

HOST, PORT = sys.argv[1], int(sys.argv[2])

MAX_SIZE = 1024

thread_count = 0

clients = set()
clients_lock = threading.Lock()

def threaded_client(connection):
    try:
        connection.send(str.encode('Welcome to the Server'))
        
        while True:
            data = connection.recv(2048)
            reply = 'Server Says: ' + data.decode('utf-8')
            if not data:
                break

            print (reply)
            with clients_lock:
                for c in clients:
                    c.send(str.encode(reply))

        connection.close()
    except KeyboardInterrupt:
        connection.close()
    finally:
        connection.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as lsock:
    try:
        lsock.bind((HOST, PORT))
        lsock.listen()

        while True:
            Client, address = lsock.accept()
            with clients_lock:
                clients.add(Client)
            print('Connected to: ' + address[0] + ':' + str(address[1]))
            threading.Thread(target=threaded_client, args=(Client, )).start()
            thread_count += 1
            print('Thread Number: ' + str(thread_count))     
    
    except KeyboardInterrupt:
        print("Caught keyboard interrupt, exiting")
        lsock.close() 
    finally:
        lsock.close() 