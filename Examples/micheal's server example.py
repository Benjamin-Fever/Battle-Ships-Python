import socket
from threading import Thread

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object
host = socket.gethostname()  # Get local machine name
port = 12345  # Reserve a port for your service.
s.bind((host, port))  # Bind to the port

clients = {}


def client_connect():
    while True:
        client, address = s.accept()

        Thread(target=handle_client, args=(client,)).start()


def client_count():
    if len(clients) != client_count:
        new_list = []
        for i in clients.items():
            new_list.append(i[1])
    client_count = len(clients)


def handle_client(client):
    name = client.recv(1024).decode()

    welcome = "Welcome to the chat %s! To quit, type ;q to disconnect." % name
    client.send(welcome.encode())

    msg = "%s has connected to the chat! Send them a warm welcome!" % name
    broadcast(msg.encode())

    clients[client] = name

    while True:
        msg = client.recv(1024)
        if not msg.decode().startswith(";"):
            broadcast(msg, "\n" + clients[client] + ": ")
        else:
            cmd = msg.decode().split(" ")
            if cmd[0] == ";q":
                client.close()
                del clients[client]

                leave = "%s has disconnected from the chat." % name
                broadcast(leave.encode())

                break
            elif cmd[0] == ";name":
                clients[client] = cmd[1]

                msg = "%s has changed their username to %s" % (name, cmd[1])
                broadcast(msg.encode())


def broadcast(msg, msg_prefix="\n"):
    for client in clients:
        client.send(msg_prefix.encode() + msg)


if __name__ == "__main__":
    s.listen(2)

    accept_connections = Thread(target=client_connect)
    accept_connections.start()
    accept_connections.join()  # Until thread closes, keep application open

    s.close()
