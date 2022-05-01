import socket
import threading
import json

serverHost = '127.0.0.1'
serverPort = 2000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((serverHost, serverPort))
server.listen()

clients = []
usernames = []
users = {}

# Send messages to all clients
def broadcast(message):
    for client in users.values():
        client.send(message)

def processclientMessage(message):
    clientdata = json.loads(message)
    outgoingmessage = clientdata["from"].encode('ascii') + \
            ": ".encode('ascii') + \
            clientdata["message"].encode('ascii')
    if clientdata["user"] == "all":
        broadcast(outgoingmessage)
    else:
        users[clientdata["user"]].send(
            outgoingmessage
        )
    
# Handle function
def handle(client, user):
    while True:
        try:
            # Broadcast messages
            message = client.recv(1024)
            processclientMessage(message)
        except Exception as e:
            # Delete and close down clients
            del users[user]
            client.close()
            broadcast('{} has left the chat!'.format(user).encode('ascii'))
            #print(e)
            break
    
# Receive/Listen
def receive():
    while True:
        # Accept the connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Get and store username
        client.send('USER'.encode('ascii'))
        username = client.recv(1024).decode('ascii')
        users[username] = client

        # Print and show username
        print("Username is {}".format(username))
        broadcast("{} has joined the chat!".format(username).encode('ascii'))
        #users = {}
        #users[username] = client
        client.send('Connected to server! \n'.encode('ascii'))
        client.send('Connected users: \n'.encode('ascii'))

        # Start thread for client
        thread = threading.Thread(target=handle, args=(client, username))
        thread.start()

print("Server is up and listening for incoming connections!")
receive()
