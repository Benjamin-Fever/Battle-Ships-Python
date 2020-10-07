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
hits = []
state = "place"


def click_event(event):
    global hits
    if state == "attack":
        location = (int(str(event.widget)[1:2]), int(str(event.widget)[4:5]))
        hit = False
        ship = ""
        for ship in e_ships:
            for pos in e_ships[ship]:
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
            for x in e_ships[ship]:
                for y in hits:
                    if x == y:
                        z += 1
            if z == len(e_ships[ship]):
                print("You sunk my", ship)

        else:
            print("Miss")
            event.widget["text"] = "O"
    elif state == "place":
        pass


def draw_board():
    global state
    board = \
        [
            [
                Label(window, width=8, height=4, bd=2, relief=GROOVE, name=str(r) + ", " + str(c), text="") for c in
                range(10)
            ] for r in range(10)
        ]
    chars = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    col = row = 0
    for col in range(1, 11):
        Label(text=chars[col - 1]).grid(column=col, row=0)
        for row in range(1, 11):
            Label(text=row - 1).grid(column=0, row=row)
            board[col - 1][row - 1].grid(row=row, column=col)
            board[col - 1][row - 1].bind("<Button-1>", click_event)
    del chars

    if state == "place":
        Label(text="Place your fleet").grid(row=2, column=12)
        Label(window, width=12, bd=2, relief=GROOVE, name="", text="Destroyer1").grid(row=4, column=11, padx=(20, 0))
        Label(window, width=12, bd=2, relief=GROOVE, name="", text="Destoyer2").grid(row=5, column=11, padx=(20, 0))
        Label(window, width=12, bd=2, relief=GROOVE, name="", text="Battleship").grid(row=6, column=11, padx=(20, 0))
        Label(window, width=12, bd=2, relief=GROOVE, name="", text="Cruiser").grid(row=4, column=13, padx=(0, 20))
        Label(window, width=12, bd=2, relief=GROOVE, name="", text="Aircraft Carrier").grid(row=5, column=13, padx=(0, 20))
        Label(window, width=12, bd=2, relief=GROOVE, name="", text="Submarine1").grid(row=6, column=13, padx=(0, 20))
        Label(window, width=12, bd=2, relief=GROOVE, name="", text="Submarine2").grid(row=7, column=12, padx=(20, 0))





draw_board()
window.mainloop()
