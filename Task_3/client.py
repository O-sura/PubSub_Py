import socket
import threading
import sys
import time

host = sys.argv[1] #host IP
port = int(sys.argv[2]) #port
mode = sys.argv[3]  # Add mode argument (publisher or subscriber)
topic = sys.argv[4] #selected topic

isModeSet = False

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

# Listening to Server and Sending Messages
def receive():
    while True:
        try:
            # Receive Message From Server
            message = client.recv(1024).decode('ascii')
            print(message)
        except:
            # Close Connection When Error
            print("[!] Connection terminated...")
            client.close()
            break

#Sending messages to server-end
def write():
    global isModeSet
    while True:
        # Send the mode to the server
        if isModeSet == False:
            client.send(mode.encode('ascii')) #registering the mode
            client.send(topic.encode('ascii')) #registering the topic
            isModeSet = True

        message = input('')
        client.send(message.encode('ascii'))
        if message == 'terminate':
            client.close()
            break

# Starting Threads For Listening And Writing
t_receive = threading.Thread(target=receive)
t_receive.start()

t_write = threading.Thread(target=write)
t_write.start()
