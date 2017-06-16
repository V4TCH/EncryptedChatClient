# import required libraries
import socket
import _thread
import configparser
import json
import time

# creating our server socket
server_socket = socket.socket()

# grab our config
CONFIG = configparser.ConfigParser()    
CONFIG.read("config.ini")

# getting our hostname and setting port
HOSTNAME = socket.gethostname()
PORT = int(CONFIG["Settings"]["port"])

# binding hostname and port to socket
server_socket.bind((HOSTNAME, PORT))

# start listening on our server socket
server_socket.listen(5)

# create our array for active connections
connections = []


# handling client function
def handle_client(__client):
    try:
        # append this connection to connection list
        connections.append(__client)

        # infinite loop ready to receive messages
        while True:
            # receive message
            message = __client.recv(16384).decode("ascii")
            # if message isn't blank
            if message != "":
                # iterate over connections
                for active_client in connections:
                    # send message to client
                    active_client.send(message.encode("ascii"))
    except ConnectionResetError:
        # on connection error remove client from active connections
        connections.remove(__client)


# infinite loop to accept clients
while True:
    # accept client
    client, address = server_socket.accept()
    # create a new thread to handle the client
    _thread.start_new_thread(handle_client, (client,))
