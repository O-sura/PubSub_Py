import socket
import threading
import sys

host = sys.argv[1]
port = int(sys.argv[2])

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

# Listening to Server and Sending Nickname
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

# Sending Messages To Server
def write():
    while True:
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
