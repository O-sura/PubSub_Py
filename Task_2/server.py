import socket
import threading
import sys

host = "127.0.0.1"
port = int(sys.argv[1])

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
print(f"[*] Server started on port {port}")
clients = []
ipAndPorts = []
publishers = []  # List to store publisher clients

# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024).decode()
            if message == 'terminate':
                closeConn(client)
                break
            elif client in publishers:  # Check if client is a publisher
                broadcast(message)  # Send message to all subscribers
            else:
                index = clients.index(client)
                print(f"[{ipAndPorts[index]}]: {message}")
        except ValueError:
            # Client socket is not in the list, handle the error
            print("Error: Client not found in the list")
            break
        except:
            # Other exceptions occurred, handle them accordingly
            print("Error: Exception occurred")
            break

# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("[+] Connected with {}".format(str(address)))
        clients.append(client)
        newUser = str(address[0]) + "/" + str(address[1])
        ipAndPorts.append(newUser)

        # Check if client is a publisher or subscriber
        mode = client.recv(1024).decode()
        if mode == "publisher":
            publishers.append(client)

        # Print the connected message
        client.send(b'[+] Connected to server!')

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

def closeConn(client):
    # Removing And Closing Clients
    index = clients.index(client)
    print(f"[-] {ipAndPorts[index]} disconnected...")
    clients.remove(client)
    ipAndPorts.remove(ipAndPorts[index])
    if client in publishers:
        publishers.remove(client)
    client.close()

def broadcast(message):
    for client in clients:
        if client not in publishers:  # Send message to all subscribers
            client.send(f"Publisher Message: {message}".encode('ascii'))

receive()
