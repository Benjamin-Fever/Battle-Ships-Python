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


def handle_client(client):
    name = client.recv(1024).decode()
    clients[client] = name
    print("test")


if __name__ == "__main__":
    s.listen(2)

    accept_connections = Thread(target=client_connect)
    accept_connections.start()
    accept_connections.join()  # Until thread closes, keep application open

    s.close()
