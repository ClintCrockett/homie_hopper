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
            # Keep listening for a message from cs socket
            msg = cs.recv(1024).decode()
            # Replace the <SEP> token with ": "
            msg = msg.replace(separator_token, ": ")
        except Exception as e:
            # If the client is no longer connected, then remove it from the set
            print(f"!! Error !! {e}")
            client_sockets.remove(cs)
            break
            
        # Iterate through all connected sockets and send message
        for client_socket in client_sockets:
            client_socket.send(msg.encode())

while True:
    # Constantly keep listening for new connections
    client_sockets, client_address = s.accept()
    print(f"{client_address} connected")
    # Add the new client to the set of connected sockets
    client_sockets.add(client_sockets)

    # Start a thread that listens for individual client messages
    t = Thread(target=listen_for_client, args=(client_sockets,))
    # Daemon thread so it terminates whenever the main thread ends
    t.daemon = True
    t.start()

for client_socket in client_sockets:
    client_socket.close()
