import socket
import threading
import pickle

# Choose username
username = input("Welcome to ClassChat! Please choose your username: ")

# Connect to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 2000))

# Listen to server, send username
def receive():
    while True:
        try:
            # Receive message from the server
            # If 'USER' send the username
            message = client.recv(1024).decode('ascii')
            if message == 'USER':
                client.send(username.encode('ascii'))
            else:
                print(message)
        except:
            # If error, close down the connection
            print("An error occured!")
            client.close()
            break

# Send messages to server
def write():
    while True:
        message = '{}: {}'.format(username, input(''))
        client.send(message.encode('ascii'))

# Start up threads
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
