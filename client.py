import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    try:
        while True:
            user_message = input("Type message: ")

            if len(user_message) > 0:
                s.sendall(bytes(user_message, encoding="utf-8"))
            else:
                break

            data = s.recv(1024)
            print(str(data, encoding="utf-8"))
    except KeyboardInterrupt:
        print("Closed session with server")
