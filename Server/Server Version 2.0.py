import socket
from threading import Thread
from time import sleep

clients = []


def handle_client(client):
    global clients
    print("User has connected")
    while True:
        z = client["connection"].recv(1024)
        client["state"] = z.decode()
        if clients[0]["state"] == "wait" and clients[1]["state"] == "wait":
            num = 0
            for x in clients:
                if x == client:
                    break
                else:
                    num += 1
            client["connection"].send(b'fleet placed ' + str(num).encode())


def client_connection():
    global clients
    while True:
        clients.append({"connection": s.accept()[0], "state": ""})
        Thread(target=handle_client, args=(clients[len(clients) - 1],)).start()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "localhost"
port = 6969
s.bind((host, port))

s.listen(2)

test = Thread(target=client_connection)
test.start()
test.join()
