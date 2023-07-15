import socket
import threading
import sys

host = sys.argv[1]
port = int(sys.argv[2])
mode = sys.argv[3]  # Add mode argument (publisher or subscriber)

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
            print("[!] An error occurred! Connection lost...")
            client.close()
            break

def write():
    global isModeSet  # Declare isModeSet as a global variable
    while True:
        # Send the mode to the server
        if not isModeSet:
            client.send(mode.encode('ascii'))
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
