import socket
from threading import Thread
from time import sleep
import json

clients = []


def handle_client(client):
    global clients
    print("User has connected")
    while True:
        z = client["connection"].recv(1024)

        if b'state' in z:
            num = 0
            for x in clients:
                if x == client:
                    break
                else:
                    num += 1
            clients[num]["state"] = client["state"] = z.decode()[7:]


        if client["state"] == "placed":
            if clients[0]["state"] == "placed" and clients[1]["state"] == "placed":
                num = 0
                for x in clients:
                    if x == client:
                        break
                    else:
                        num += 1
                client["connection"].send(b'fleet placed ' + str(num).encode())

        if b'fleet0' in z or b'fleet1' in z:
            z = z.decode()
            clients[int(z[5:6])]["fleet"] = json.loads(z[8:])
        if client["state"] == "recvFleet":
            num = 0
            for x in clients:
                if x == client:
                    break
                else:
                    num += 1
            if num == 0:
                client["connection"].send(json.dumps(clients[1]["fleet"]).encode())
            else:
                client["connection"].send(json.dumps(clients[0]["fleet"]).encode())


def debug(client):
    global clients
    while True:
        num = 0
        for x in clients:
            if x == client:
                break
            else:
                num += 1
        print(clients[num]["state"])
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
