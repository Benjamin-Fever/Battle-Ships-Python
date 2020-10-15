import socket
from threading import Thread
from time import sleep

clients = []

def penis(client):
    print("Connection made!")
    while True:
        cum = client["piss"].recv(1024)
        print(cum.decode())
        client["state"] = cum.decode()
        if cum == b'':
            pass


def client_connection():
    global clients
    while True:
        clients.append[{"piss": s.accept()[0], "state": ""}]
        Thread(target=penis, args=(clients[len(clients) - 1],)).start()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "localhost"
port = 6969
s.bind((host, port))

s.listen(2)

test = Thread(target=client_connection)
test.start()
test.join()
