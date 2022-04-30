import socket
import threading

serverHost = '127.0.0.1'
serverPort = 2000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((serverHost, serverPort))
server.listen()

clients = []
usernames = []

# Send messages to all clients
def broadcast(message):
    for client in clients:
        client.send(message)
    
# Handle function
def handle(client):
    while True:
        try:
            # Broadcast messages
            message = client.recv(1024)
            broadcast(message)
        except:
            # Delete and close down clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            username = usernames[index]
            broadcast('{} has left the chat!'.format(username).encode('ascii'))
            usernames.remove(username)
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
        usernames.append(username)
        clients.append(client)

        # Print and show username
        print("Username is {}".format(username))
        broadcast("{} has joined the chat!".format(username).encode('ascii'))
        users = []
        users.append(username)
        client.send('Connected to server! \n'.encode('ascii'))
        client.send('Connected users: \n'.encode('ascii'))

        # Start thread for client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server is up and listening for incoming connections!")
receive()
