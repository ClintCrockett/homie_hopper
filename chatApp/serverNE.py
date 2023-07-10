import socket
from  threading import Thread

'''Global variables (DO NOT CHANGE)'''
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5002
separator_token = "<SEP>"

# Init a set of all connected client's sockets
# Set does not allow for duplicates
client_sockets = set()
# Create TCP socket
s = socket.socket()

# Set the port to be reusable
s.setsockopt(socket.SQL_SOCKET, socket.SO_REUSEADDR, 1)
# Bind the socket
# Or connect the the server host and port to a specific socket in order to avoid conflicting with other TCP services, and efficiently secure a connection
s.bind((SERVER_HOST, SERVER_PORT))
# Set the server to listen and collet any client sockets
s.listen(5)

# Confirmation message
print(f"Listening on {SERVER_HOST}:{SERVER_PORT}")


def listen_for_client(cs):
    '''Method for listening for any message from a client socket, where when a message is recieved, it is broadcasted to all other clients'''

    while True:
        try:
            msg = cs.recv(1024).decode()
        except Exception as e:
            print(f"!! Error !! {e}")
            client_sockets.remove(cs)
        else:
            msg = msg.replace(separator_token, ": ")
        for client_socket in client_sockets:
            client_socket.send(msg.encode())

while True:
    client_sockets, client_address = s.accept()
    print(f"{client_address} connected")
    client_sockets.add(client_sockets)

    t = Thread(target=listen_for_client, args=(client_sockets,))
    t.daemon = True
    t.start()

    for i in client_sockets:
        i.close()