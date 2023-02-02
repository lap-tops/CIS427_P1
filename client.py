# Create a client that can send messages to the server and receive replies running on port 8000 from the server in server.py

import socket

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# Connect the socket to the port where the server is listening
server_address = ("127.0.0.1", 8000)
print('connecting to %s port %s' % server_address)
sock.connect(server_address)

try:

    message = ""
    while message.lower().strip() != 'quit':
        message = input(" -> ")  # take input
        sock.send(message.encode())  # send message
        data = sock.recv(1024).decode()  # receive response

        if not data:
            # if data is not received break
            break

        print(data)  # show in terminal


finally:
    print('closing socket')
