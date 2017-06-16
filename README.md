# Encrypted Chat Client

This is a small chat client I made for fun, and all chat messages are encrypted!

# Requirements

Client:

I had to install cryptography library, it seems to be 32bit only... Running fine using Python3.5 and 3.6
```pip install cryptography```

Server and Gateway:

Should work 32bit/64bit on Python3.5+ (tested)

# Setting up the server + gateway + client

Server:

1) Head over to server directory
2) Open config.ini
3) Change ``port`` to your desired port
4) Run the server script

Gateway:

1) Head over to gateway directory
2) Open config.ini
3) Change ``localport`` to the desired port for the gateway
4) Change ``serverport`` to the port your server is running
5) Change ``serverip`` to the ip of your server

Client:

1) Head over to client directory
2) Run key_generator.py
3) Copy its output
4) Open config.ini
5) Replace three bottom lines with what you just copied
6) Replace ``serverip`` to the ip of your gateway
7) Replace ``serverport`` to the port of your gateway
8) Replace ``username`` to whatever you want that to be

# How does this whole chat client work?

Server:

The server simply receives messages and sends them to all connected clients without decrypting the message

Gateway:

The gateway simply relays messages it receives from clients to the server and relays the messages from the server
to all its clients, never decrypts the messages

Client:

Sends off encrypted messages to gateway
Receives encrypted messages from gateway, then decrypts them

```
Client -> Presses "Send Message"
Client -> Encrypts Message
Client -> Sends Message To Gateway
Gateway -> Receives Message
Gateway -> Sends Message To Server
Server -> Receives Message
Server -> Sends Message To All Connected Gateways
Gateways -> Receives Message
Gateways -> Sends Message To All Connected Clients
Clients -> Receives Message
Clients -> Decrypts Message
Clients -> Displays Message
```