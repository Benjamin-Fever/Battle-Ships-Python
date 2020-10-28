import socket
from threading import Thread
from time import sleep
import json

clients = []


def client_index(client):
    num = 0
    for x in clients:
        if x == client:
            break
        else:
            num += 1
    return num


def handle_client(client):
    global clients
    while True:
        z = client["connection"].recv(1024)

        if b'state' in z:
            clients[client_index(client)]["state"] = client["state"] = z.decode()[7:]

        elif b'fleet0' in z or b'fleet1' in z:
            z = z.decode()
            client["fleet"] = clients[int(z[5:6])]["fleet"] = json.loads(z[8:])

        elif b'attack:' in z:
            if client_index(client) == 0:
                clients[1]["connection"].send(z[8:9] + b', ' + z[11:12])
            else:
                clients[0]["connection"].send(z[8:9] + b', ' + z[11:12])

        if client["state"] == "placed":
            if clients[0]["state"] == "placed" and clients[1]["state"] == "placed":
                client["connection"].send(b'fleet placed ' + str(client_index(client)).encode())

        elif client["state"] == "recFleet":
            if client_index(client) == 0:
                client["connection"].send(json.dumps(clients[1]["fleet"]).encode())

            elif client_index(client) == 1:
                client["connection"].send(json.dumps(clients[0]["fleet"]).encode())


def debug(client):
    global clients
    while True:
        print(clients[client_index(client)]["state"])
        sleep(3)


def client_connection():
    global clients
    while True:
        clients.append({"connection": s.accept()[0], "state": "", "fleet": None})
        Thread(target=handle_client, args=(clients[len(clients) - 1],)).start()
        Thread(target=debug, args=(clients[len(clients) - 1],)).start()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "localhost"
port = 6969
s.bind((host, port))

s.listen(2)

test = Thread(target=client_connection)
test.start()
test.join()
