import socket
import threading
import sys

host = "127.0.0.1" #IP of the server
port = int(sys.argv[1]) #port

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
print(f"[*] Server started on port {port}")
clients = [] # List of connected clients
ipAndPorts = [] # Stores the ip and port which the user is connected with
pubTopics = {}  # Dictionary to store topics and their corresponding publishers
subTopics = {}  # Dictionary to store topics and their corresponding subscribers

# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024).decode()
            if message == 'terminate':
                closeConn(client)
                break
            else:
                index = clients.index(client)
                print(f"[{ipAndPorts[index]}]: {message}")

                # Check if client is a subscriber
                for publishers in pubTopics.values():
                    if client in publishers:
                        sendToSubscribers(message, client)
                        break
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
        topic = client.recv(1024).decode()

        if mode == "publisher":
            addPublisher(client, topic)
        else:
            addSubscriber(client, topic)

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

    # Remove client from topics dictionary
    cleanDictionary(client)
    #close the client connection
    client.close()

def addPublisher(client, topic):
    # Add client as a publisher for the specified topic
    if topic not in pubTopics:
        pubTopics[topic] = []
    pubTopics[topic].append(client)

def addSubscriber(client, topic):
    # Add client as a subscriber interested in the specified topic
    if topic in subTopics:
        subTopics[topic].append(client)
    else:
        subTopics[topic] = [client]

#Function for broadcasting the message only for the relevent topic subscribers
def sendToSubscribers(message, publisher):
    #find the topic
    topic = None
    for topic_key, publishers in pubTopics.items():
        if publisher in publishers:
            topic = topic_key
            break
    
    #send the message to all subscribers
    if topic is not None:
        subscribers = subTopics[topic]
        for subscriber in subscribers:
            subscriber.send(f"Publisher Message ({topic}): {message}".encode('ascii'))
                
#Function created for clearing the list of publishers and subscribers when they are disconnecting
def cleanDictionary(client):
    #find whether user is a pub or sub
    role = None
    if client in pubTopics.values():
        role = pubTopics
    else: 
        role = subTopics
    
    #clear the relevent list
    for topic, members in role.items():
        if client in members:
            members.remove(client)
            if len(members) == 0:
                del role[topic]
            break

receive()

#Ex:
#python client.py 127.0.0.1 8000
#python client.py 127.0.0.1 8000 publisher topicA