import sys
import socket
import threading

HOST, PORT = sys.argv[1], int(sys.argv[2])

lthread = threading.Lock()

def handle_user_input(connection):
    user_message = input("Type message: ")
    if (user_message):
        connection.sendall(bytes(user_message, encoding="utf-8"))

def handle_recieved_data(connection):
    response = connection.recv(2048)

    if not response:
        lthread.release()

    print (response.decode("utf-8"))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    try:
        sock.connect((HOST, PORT))

        response = sock.recv(2048)

        print (response.decode('utf-8'))

        lthread.acquire()

        while True:
            threading.Thread(target=handle_recieved_data, args=(sock, )).start()
            threading.Thread(target=handle_user_input, args=(sock, )).start()

    except KeyboardInterrupt:
        print("Closed session with server")
        sock.close()
    except SystemExit:
        print("Closed session with server")
        sock.close()
    finally:
        sock.close()