# module imports
import socket
import _thread
import configparser

# grabbing our config file
CONFIG = configparser.ConfigParser()
CONFIG.read("config.ini")

# creating our constant globals
LOCAL_PORT = int(CONFIG["Settings"]["localport"])
SERVER_PORT = int(CONFIG["Settings"]["serverport"])
SERVER_IP = CONFIG["Settings"]["serverip"]

# creating our gateway to client socket
gateway_to_client = socket.socket()
gateway_to_client.bind((socket.gethostname(), LOCAL_PORT))
gateway_to_client.listen(5)

# create our gateway to server socket
gateway_to_server = socket.socket()
gateway_to_server.connect((SERVER_IP, SERVER_PORT))

# crate a blank array for our active connections
active_connections = []


# simple function for handling clients
def handle_client(__client):
    try:
        # append this client to active connections
        active_connections.append(__client)

        # infinite loop for receiving messages
        while True:
            # receive message
            message = __client.recv(16384).decode("ascii")
            # if message isn't nothing
            if message != "":
                # send message to server
                gateway_to_server.send(message.encode("ascii"))
    except ConnectionResetError:
        # on connection error remove client from active connections
        active_connections.remove(__client)


def receive_from_server():
    # infinite loop for receiving from server
    while True:
        # receive message
        message = gateway_to_server.recv(16384).decode("ascii")
        # if message isn't nothing
        if message != "":
            # iterate over clients
            for client in active_connections:
                # send data to client
                client.send(message.encode("ascii"))


# simple function for accepting clients
def accept_clients():
    # accept a connection
    client, address = gateway_to_client.accept()
    # start a new thread for handling the client
    _thread.start_new_thread(handle_client, (client,))

_thread.start_new_thread(receive_from_server, ())
# infinite loop for accepting clients
while True:
    accept_clients()
