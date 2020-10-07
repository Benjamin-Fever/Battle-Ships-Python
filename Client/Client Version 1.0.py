from tkinter import *

window = Tk()

ships = {
    "Battleship": [(1, 2), (1, 3), (1, 4), (1, 5)],
    "Destroyer1": [(8, 1), (8, 2)],
    "Destroyer2": [(0, 8), (0, 9)],
    "Cruiser": [(5, 9), (6, 9), (7, 9)],
    "Aircraft Carrier": [(7, 3), (7, 4), (7, 5), (7, 6), (7, 7)],
    "Submarine1": [(5, 5)],
    "Submarine2": [(5, 8)],
}
hits = []


def attack(event):
    global hits
    location = (int(str(event.widget)[1:2]), int(str(event.widget)[4:5]))
    hit = False
    ship = ""
    for ship in ships:
        for pos in ships[ship]:
            if pos == location:
                hit = True
                break
        if hit:
            break
    if hit:
        print("Hit")
        event.widget["text"] = "X"
        hits.append(location)
        z = 0
        for x in ships[ship]:
            for y in hits:
                if x == y:
                    z += 1
        if z == len(ships[ship]):
            print("You sunk my", ship)

    else:
        print("Miss")
        event.widget["text"] = "O"


board = \
    [
        [
            Label(window, width=8, height=4, bd=2, relief=GROOVE, name=str(r) + ", " + str(c), text="") for c in
            range(10)
        ] for r in range(10)
    ]

for col in range(10):
    for row in range(10):
        board[col][row].grid(row=row, column=col)
        board[col][row].bind("<Button-1>", attack)

window.mainloop()
