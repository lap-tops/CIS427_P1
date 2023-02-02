# Create a socket server that listens on port 8000 and logs messages from clients
# to the console.

import socket

import database

database.init()

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ("127.0.0.1", 8000)
print('starting up on %s port %s' % server_address)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

database.buy_stock("AAPL", 50, 1, 1)

print("First List", database.list_stocks(1))

print("Get Balance", database.get_balance(1))

print("Sell stock", database.sell_stock("AAPL", 50, 1, 1))

print("List stock", database.list_stocks(1))

print("New balance", database.get_balance(1))


connection, address = sock.accept()  # accept new connection
print("Connection from: " + str(address))
while True:

    # receive data stream. it won't accept data packet greater than 1024 bytes
    data = connection.recv(1024).decode()
    if not data:
        # if data is not received break
        break
    print("from connected user: " + str(data))

    # send data to the client
    connection.send(str("Received: " + str(data)).encode())

connection.close()
