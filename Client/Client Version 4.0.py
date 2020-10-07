from tkinter import *

window = Tk()

e_ships = {
    "Battleship": [(1, 2), (1, 3), (1, 4), (1, 5)],
    "Destroyer1": [(8, 1), (8, 2)],
    "Destroyer2": [(0, 8), (0, 9)],
    "Cruiser": [(5, 9), (6, 9), (7, 9)],
    "Aircraft Carrier": [(7, 3), (7, 4), (7, 5), (7, 6), (7, 7)],
    "Submarine1": [(5, 5)],
    "Submarine2": [(5, 8)],
}

player_fleet = {}

fleet = {
    "battleship": {"char": "B", "size": 4},
    "destroyer1": {"char": "D", "size": 2},
    "destroyer2": {"char": "D", "size": 2},
    "cruiser": {"char": "C", "size": 3},
    "aircraft carrier": {"char": "A", "size": 5},
    "submarine1": {"char": "S", "size": 1},
    "submarine2": {"char": "S", "size": 1}
}
hits = []
pBoard = eBoard = []
place_labels = []
vertical = False
selected = None
state = "place"
ship = ""


def click_event(event):
    global hits, selected, place_labels, ship, player_fleet, fleet, pBoard, eBoard
    if state == "attack":
        location = {"board": str(event.widget)[1:7],
                    "pos": (int(str(event.widget)[9:10]), int(str(event.widget)[12:13]))}
        print(location)

    elif state == "place":
        selected = str(event.widget)[1:]
        if selected in fleet:
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
                        for x in range(len(pBoard)):
                            for y in range(len(pBoard[x])):
                                loc = (int(str(pBoard[x][y])[9:10]), int(str(pBoard[x][y])[12:13]))
                                if loc == location["pos"]:
                                    l = 1
                                    for z in range(0, fleet[ship]["size"]):
                                        try:
                                            pBoard[x][y + z]["text"] = fleet[ship]["char"]
                                            positions.append((x, y + z))
                                        except IndexError:
                                            pBoard[x][y - l]["text"] = fleet[ship]["char"]
                                            positions.append((x, y - l))
                                            l += 1
                    else:
                        for x in range(len(pBoard)):
                            for y in range(len(pBoard[x])):
                                loc = (int(str(pBoard[x][y])[9:10]), int(str(pBoard[x][y])[12:13]))
                                if loc == location["pos"]:
                                    l = 1
                                    for z in range(0, fleet[ship]["size"]):
                                        try:
                                            pBoard[x + z][y]["text"] = fleet[ship]["char"]
                                            positions.append((x + z, y))
                                        except IndexError:
                                            pBoard[x - l][y]["text"] = fleet[ship]["char"]
                                            positions.append((x - l, y))
                                            l += 1
                    p_ships[ship] = positions
                    print(p_ships)
                    clear_board(None)
                    ship = ""


def hover_enter(event):
    global state
    global pBoard
    location = {"board": str(event.widget)[1:7],
                "pos": (int(str(event.widget)[9:10]), int(str(event.widget)[12:13]))}
    if state == "place":
        if location["board"] == "pFleet":
            if selected is None:
                return
            elif selected in fleet:
                if vertical:
                    for x in range(len(pBoard)):
                        for y in range(len(pBoard[x])):
                            loc = (int(str(pBoard[x][y])[9:10]), int(str(pBoard[x][y])[12:13]))
                            if loc == location["pos"]:
                                pBoard[x][y]["text"] = fleet[selected]["char"]
                                l = 1
                                for z in range(1, fleet[selected]["size"]):
                                    try:
                                        pBoard[x][y + (1 * z)]["text"] = fleet[selected]["char"]
                                    except IndexError:
                                        pBoard[x][y - l]["text"] = fleet[selected]["char"]
                                        l += 1
                else:
                    for x in range(len(pBoard)):
                        for y in range(len(pBoard[x])):
                            loc = (int(str(pBoard[x][y])[9:10]), int(str(pBoard[x][y])[12:13]))
                            if loc == location["pos"]:
                                pBoard[x][y]["text"] = fleet[selected]["char"]
                                l = 1
                                for z in range(0, fleet[selected]["size"]):
                                    try:
                                        pBoard[x + z][y]["text"] = fleet[selected]["char"]
                                    except IndexError:
                                        pBoard[x - l][y]["text"] = fleet[selected]["char"]
                                        l += 1


def clear_board(event):
    global state, pBoard, player_fleet, fleet
    if state == "place":
        for x in range(len(pBoard)):
            for y in range(len(pBoard[x])):
                clear = True
                for ship in p_ships:
                    for z in p_ships[ship]:
                        if (x, y) == z:
                            clear = False
                            break
                    if not clear:
                        break
                if clear:
                    pBoard[x][y]["text"] = ""
                else:
                    pBoard[x][y]["text"] = fleet[ship]["char"]


def draw_board():
    global state, place_labels, pBoard, eBoard
    eBoard = [
        [
            Label(window, width=2, height=1, bd=2, relief=GROOVE, name="eFleet: " + str(r) + ", " + str(c), text="")
            for c in
            range(10)
        ] for r in range(10)
    ]
    pBoard = [
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
            eBoard[col - 1][row - 1].grid(row=row, column=col)
            eBoard[col - 1][row - 1].bind("<Button-1>", click_event)
            eBoard[col - 1][row - 1].bind("<Enter>", hover_enter)
            eBoard[col - 1][row - 1].bind("<Leave>", clear_board)

    for col in range(1, 11):
        Label(text=x_label[col - 1]).grid(column=col, row=11)
        for row in range(12, 22):
            Label(text=row - 11).grid(column=0, row=row)
            pBoard[col - 1][row - 12].grid(row=row, column=col)
            pBoard[col - 1][row - 12].bind("<Button-1>", click_event)
            pBoard[col - 1][row - 12].bind("<Enter>", hover_enter)
            pBoard[col - 1][row - 12].bind("<Leave>", clear_board)

    if state == "place":
        place_labels = [
            Label(text="Place your fleet"),
            Label(text=""),
            Label(window, width=12, bd=2, relief=GROOVE, name="destroyer1", text="Destroyer1"),
            Label(window, width=12, bd=2, relief=GROOVE, name="destroyer2", text="Destoyer2"),
            Label(window, width=12, bd=2, relief=GROOVE, name="battleship", text="Battleship"),
            Label(window, width=12, bd=2, relief=GROOVE, name="cruiser", text="Cruiser"),
            Label(window, width=12, bd=2, relief=GROOVE, name="aircraft carrier", text="Aircraft Carrier"),
            Label(window, width=12, bd=2, relief=GROOVE, name="submarine1", text="Submarine1"),
            Label(window, width=12, bd=2, relief=GROOVE, name="submarine2", text="Submarine2")
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


def rotate(event):
    global vertical, state
    if state == "place":
        if event.char == "r":
            vertical = not vertical


draw_board()
window.bind("<Key>", rotate)
window.mainloop()
