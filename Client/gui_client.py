# importing libraries
import tkinter
import _thread
import socket
import configparser
import json
from cryptography.fernet import Fernet

# grab our config
CONFIG = configparser.ConfigParser()
CONFIG.read("config.ini")

# creating our hostname, port, and username constant globals
HOSTNAME = CONFIG["Settings"]["serverip"]
PORT = int(CONFIG["Settings"]["serverport"])
USERNAME = CONFIG["Settings"]["username"]

# grab our encryption keys and setup Fernet instances with them
CRYPT = [Fernet(CONFIG["Settings"]["encryptkeyone"].encode("ascii")),
         Fernet(CONFIG["Settings"]["encryptkeytwo"].encode("ascii")),
         Fernet(CONFIG["Settings"]["encryptkeythree"].encode("ascii"))]


# quick function for encrypting text
def encrypt(text):
    new_text = text
    for crypt in CRYPT:
        new_text = crypt.encrypt(new_text)
    return new_text


# quick function for decrypting text
def decrypt(text):
    new_text = text
    for crypt in CRYPT[::-1]:
        new_text = crypt.decrypt(new_text)
    return new_text


# used for adding text into the chat box widget
def add_text(text):
    global chat
    chat.config(state=tkinter.NORMAL)
    chat.insert(1.0, text + "\n")
    chat.pack()
    chat.config(state=tkinter.DISABLED)


# used for sending whats in the current user input box
def send_message(event=None):
    # grab text from user input box and strip it
    message = user_input.get(1.0, tkinter.END).strip()

    data_to_send = {"message": message, "username": USERNAME}
    data_to_send = json.dumps(data_to_send)

    # if message isn't blank
    if message != "":
        # delete current text from user input box
        user_input.delete(1.0, tkinter.END)
        user_input.pack()

        # encode message
        data_to_send = data_to_send.encode("ascii")
        # encrypt message
        data_to_send = encrypt(data_to_send)

        # send our message to the server
        client_socket.send(data_to_send)


def handle_receiving():
    # infinite loop used to keep receiving messages
    while True:
        # receive message and decypt then decode it
        message = client_socket.recv(16384)
        message = decrypt(message)
        message = message.decode("ascii")
        message = json.loads(message)

        # if message isn't blank
        if message != "":
            # add the message text into the chat box
            add_text(message["username"] + ": " + message["message"])

# create our tk instance
tk = tkinter.Tk()

# rename our tk instance
tk.wm_title("Chat Client")

# create the text box for receiving messages
chat = tkinter.Text(state=tkinter.DISABLED, fg="white", bg="#3a3d41", wrap=tkinter.WORD, cursor="arrow")
chat.pack()

# create user input box for sending messages
user_input = tkinter.Text(height=10, fg="white", bg="#3a3d41", wrap=tkinter.WORD)
user_input.pack()

# bind enter key to send a message
user_input.bind("<Return>", send_message)

# create button used for sending messages
verify_button = tkinter.Button(width=80, command=send_message, text="Send Message")
verify_button.pack()

# create our client socket
client_socket = socket.socket()

# connect to server
client_socket.connect((HOSTNAME, PORT))

# start new thread that handles with receiving messages
_thread.start_new_thread(handle_receiving, ())

# run the tk mainloop
tk.mainloop()
