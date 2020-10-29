from tkinter import *
import socket
from threading import Thread
from time import sleep
import json
import os

window = Tk()

host = "10.70.22.21"
port = 6969

fleet = {
    "battleship": {"char": "B", "size": 4},
    "destroyer1": {"char": "D", "size": 2},
    "destroyer2": {"char": "D", "size": 2},
    "cruiser": {"char": "C", "size": 3},
    "aircraft carrier": {"char": "A", "size": 5},
    "submarine1": {"char": "S", "size": 1},
    "submarine2": {"char": "S", "size": 1}
}
enemy_fleet = {}
player_fleet = {}

board = [
    [], []
]
place_labels = []

selected = ""
ship = ""
state = "place"

playerNum = 0

vertical = False
last_hover_pos = NONE


def click_event(event):
    global selected, place_labels, ship, player_fleet, fleet, board, state, enemy_fleet, s
    if state == "attack":
        if "eFleet" in str(event.widget):
            location = (int(str(event.widget)[9:10]), int(str(event.widget)[12:13]))
            hit = False
            for ship in enemy_fleet:
                for pos in enemy_fleet[ship]:
                    if location == (pos[0], pos[1]):
                        hit = True
                        break
            if hit:
                board[1][location[0]][location[1]]["text"] = "X"
            else:
                board[1][location[0]][location[1]]["text"] = "O"
            try:
                s.send(b'attack: ' + str(location[0]).encode() + b', ' + str(location[1]).encode())
            except ConnectionResetError:
                os._exit(1)
            state = "wait"

    elif state == "place":
        collide = False
        selected = str(event.widget)[1:]
        if selected == "confirm":
            if len(player_fleet) == len(fleet):
                state = "placed"
                place_labels[1]["text"] = "Fleet placed"

        elif selected in fleet:
            place_labels[1]["text"] = "Ship: " + selected
            ship = selected
        else:
            if ship != "":
                positions = []
                place_labels[1]["text"] = ""
                location = {"board": str(event.widget)[1:7],
                            "pos": (int(str(event.widget)[9:10]), int(str(event.widget)[12:13]))}
                if location["board"] == "pFleet":
                    if vertical:
                        for x in range(len(board[0])):
                            for y in range(len(board[0][x])):
                                loc = (int(str(board[0][x][y])[9:10]), int(str(board[0][x][y])[12:13]))
                                if loc == location["pos"]:
                                    v = 1
                                    for z in range(0, fleet[ship]["size"]):
                                        try:
                                            for player_ship in player_fleet:
                                                if player_ship != ship:
                                                    for pos in player_fleet[player_ship]:
                                                        if pos == (x, y + z):
                                                            collide = True
                                            if collide:
                                                place_labels[1]["text"] = "You can't place that there"
                                                clear_board(None)
                                                return
                                            board[0][x][y + z]["text"] = fleet[ship]["char"]
                                            positions.append((x, y + z))
                                        except IndexError:
                                            for player_ship in player_fleet:
                                                if player_ship != ship:
                                                    for pos in player_fleet[player_ship]:
                                                        if pos == (x, y - v):
                                                            collide = True
                                            if collide:
                                                place_labels[1]["text"] = "You can't place that there"
                                                clear_board(None)
                                                return
                                            board[0][x][y - v]["text"] = fleet[ship]["char"]
                                            positions.append((x, y - v))
                                            v += 1
                    else:
                        for x in range(len(board[0])):
                            for y in range(len(board[0][x])):
                                loc = (int(str(board[0][x][y])[9:10]), int(str(board[0][x][y])[12:13]))
                                if loc == location["pos"]:
                                    v = 1
                                    for z in range(0, fleet[ship]["size"]):
                                        try:
                                            for player_ship in player_fleet:
                                                if player_ship != ship:
                                                    for pos in player_fleet[player_ship]:
                                                        if pos == (x + z, y):
                                                            collide = True
                                            if collide:
                                                place_labels[1]["text"] = "You can't place that there"
                                                clear_board(None)
                                                return
                                            board[0][x + z][y]["text"] = fleet[ship]["char"]
                                            positions.append((x + z, y))
                                        except IndexError:
                                            for player_ship in player_fleet:
                                                if player_ship != ship:
                                                    for pos in player_fleet[player_ship]:
                                                        if pos == (x - v, y):
                                                            collide = True
                                            if collide:
                                                place_labels[1]["text"] = "You can't place that there"
                                                clear_board(None)
                                                return
                                            board[0][x - v][y]["text"] = fleet[ship]["char"]
                                            positions.append((x - v, y))
                                            v += 1
                    player_fleet[ship] = positions
                    clear_board(None)
                    ship = ""


def hover_enter(event):
    global state, board, last_hover_pos
    location = {"board": str(event.widget)[1:7],
                "pos": (int(str(event.widget)[9:10]), int(str(event.widget)[12:13]))}
    last_hover_pos = event
    if state == "place":
        if location["board"] == "pFleet":
            if selected is None:
                return
            elif selected in fleet:
                if vertical:
                    for x in range(len(board[0])):
                        for y in range(len(board[0][x])):
                            loc = (int(str(board[0][x][y])[9:10]), int(str(board[0][x][y])[12:13]))
                            if loc == location["pos"]:
                                board[0][x][y]["text"] = fleet[selected]["char"]
                                v = 1
                                for z in range(1, fleet[selected]["size"]):
                                    try:
                                        board[0][x][y + (1 * z)]["text"] = fleet[selected]["char"]
                                    except IndexError:
                                        board[0][x][y - v]["text"] = fleet[selected]["char"]
                                        v += 1
                else:
                    for x in range(len(board[0])):
                        for y in range(len(board[0][x])):
                            loc = (int(str(board[0][x][y])[9:10]), int(str(board[0][x][y])[12:13]))
                            if loc == location["pos"]:
                                board[0][x][y]["text"] = fleet[selected]["char"]
                                v = 1
                                for z in range(0, fleet[selected]["size"]):
                                    try:
                                        board[0][x + z][y]["text"] = fleet[selected]["char"]
                                    except IndexError:
                                        board[0][x - v][y]["text"] = fleet[selected]["char"]
                                        v += 1


# noinspection PyUnusedLocal
def clear_board(event):
    global state, board, player_fleet, fleet
    _ship = None
    if state == "place":
        for x in range(len(board[0])):
            for y in range(len(board[0][x])):
                clear = True
                for _ship in player_fleet:
                    for z in player_fleet[_ship]:
                        if (x, y) == z:
                            clear = False
                            break
                    if not clear:
                        break
                if clear:
                    board[0][x][y]["text"] = ""
                else:
                    board[0][x][y]["text"] = fleet[_ship]["char"]


def draw_board():
    global state, place_labels, board
    board[1] = [
        [
            Label(window, width=2, height=1, bd=2, relief=GROOVE, name="eFleet: " + str(r) + ", " + str(c), text="")
            for c in
            range(10)
        ] for r in range(10)
    ]
    board[0] = [
        [
            Label(window, width=2, height=1, bd=2, relief=GROOVE, name="pFleet: " + str(r) + ", " + str(c), text="")
            for c in
            range(10)
        ] for r in range(10)
    ]
    x_label = [
        "A", "B", "C", "D", "E", "F", "G", "H", "I", "J"
    ]
    for col in range(1, 11):
        Label(text=x_label[col - 1]).grid(column=col, row=0)
        for row in range(1, 11):
            Label(text=row).grid(column=0, row=row)
            board[1][col - 1][row - 1].grid(row=row, column=col)
            board[1][col - 1][row - 1].bind("<Button-1>", click_event)
            board[1][col - 1][row - 1].bind("<Enter>", hover_enter)
            board[1][col - 1][row - 1].bind("<Leave>", clear_board)

    for col in range(1, 11):
        Label(text=x_label[col - 1]).grid(column=col, row=11)
        for row in range(12, 22):
            Label(text=row - 11).grid(column=0, row=row)
            board[0][col - 1][row - 12].grid(row=row, column=col)
            board[0][col - 1][row - 12].bind("<Button-1>", click_event)
            board[0][col - 1][row - 12].bind("<Enter>", hover_enter)
            board[0][col - 1][row - 12].bind("<Leave>", clear_board)

    if state == "place":
        place_labels = [
            Label(text="Place your fleet"),
            Label(text=""),
            Label(window, width=12, bd=2, relief=GROOVE, name="destroyer1", text="Destroyer1"),
            Label(window, width=12, bd=2, relief=GROOVE, name="destroyer2", text="Destroyer2"),
            Label(window, width=12, bd=2, relief=GROOVE, name="battleship", text="Battleship"),
            Label(window, width=12, bd=2, relief=GROOVE, name="cruiser", text="Cruiser"),
            Label(window, width=12, bd=2, relief=GROOVE, name="aircraft carrier", text="Aircraft Carrier"),
            Label(window, width=12, bd=2, relief=GROOVE, name="submarine1", text="Submarine1"),
            Label(window, width=12, bd=2, relief=GROOVE, name="submarine2", text="Submarine2"),
            Label(window, width=12, bd=2, relief=GROOVE, name="confirm", text="Confirm")
        ]
        for x in place_labels:
            x.bind("<Button-1>", click_event)
        place_labels[0].grid(row=2, column=12)
        place_labels[1].grid(row=4, column=12)

        place_labels[2].grid(row=7, column=11, padx=(40, 0))
        place_labels[3].grid(row=9, column=11, padx=(40, 0))
        place_labels[4].grid(row=11, column=11, padx=(40, 0))

        place_labels[5].grid(row=7, column=13, padx=(0, 40))
        place_labels[6].grid(row=9, column=13, padx=(0, 40))
        place_labels[7].grid(row=11, column=13, padx=(0, 40))

        place_labels[8].grid(row=13, column=12)
        place_labels[9].grid(row=15, column=12)


def rotate(event):
    global vertical, state
    if state == "place":
        if event.char == "r":
            vertical = not vertical
            clear_board(None)
            if last_hover_pos is not None:
                hover_enter(last_hover_pos)


def send_server_info():
    global s, state
    while True:
        try:
            s.send(b'state: ' + state.encode())
        except ConnectionResetError:
            os._exit(1)
        sleep(1)


def intro():
    global place_labels
    for z in ["Welcome to", "Battleships", "Click", "The", "Buttons", "Below", "To", "Place", "Your", "Fleet", "Push", "R", "To",
              "Rotate", ""]:
        place_labels[1]["text"] = z
        sleep(1)


def get_server_info():
    global s, state, playerNum, player_fleet, enemy_fleet
    while True:
        try:
            z = s.recv(1024).decode()
        except ConnectionResetError:
            os._exit(1)
        if state == "placed":
            if "fleet placed" in z:
                if int(z[13:]) == 0:
                    playerNum = 0
                    window.title("Player 1")
                else:
                    playerNum = 1
                    window.title("Player 2")
                state = "sendFleet"
        elif state == "wait":
            location = (int(z[0:1]), int(z[3:4]))
            hit = False
            # noinspection PyShadowingNames
            for ship in player_fleet:
                for pos in player_fleet[ship]:
                    if location == (pos[0], pos[1]):
                        hit = True
                        break
            if hit:
                board[0][location[0]][location[1]]["bg"] = "red"
            else:
                board[0][location[0]][location[1]]["bg"] = "blue"
            state = "attack"
            place_labels[1]["text"] = "Your turn"


        if state == "recFleet":
            try:
                data = s.recv(1024).decode()
            except ConnectionResetError:
                os._exit(1)
            enemy_fleet = json.loads(data)
            if playerNum == 0:
                state = "attack"
                place_labels[1]["text"] = "Your turn"
            elif playerNum == 1:
                state = "wait"
                place_labels[1]["text"] = "Enemy Turn"

        elif state == "sendFleet":
            for i in range(2, 10):
                place_labels[i].destroy()
            data_string = json.dumps(player_fleet)
            try:
                s.send(b'fleet' + str(playerNum).encode() + b': ' + data_string.encode())
            except ConnectionResetError:
                os._exit(1)
            sleep(1)
            state = "recFleet"


if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    Thread(target=send_server_info).start()
    Thread(target=get_server_info).start()
    draw_board()
    Thread(target=intro).start()
    window.bind("<Key>", rotate)
    window.mainloop()
