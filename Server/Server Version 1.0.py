import socket
from threading import Thread


def handle_client(client):
    print("Connection made!")
    while True:
        data = client.recv(1024)
        print(data.decode())


def client_connection():
    while True:
        client = s.accept()[0]
        Thread(target=handle_client, args=(client,)).start()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "localhost"
port = 6969
s.bind((host, port))

s.listen(2)

test = Thread(target=client_connection)
test.start()
test.join()
