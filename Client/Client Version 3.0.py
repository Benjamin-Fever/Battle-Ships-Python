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
        location = {"board": str(event.widget)[1:7],
                    "pos": (int(str(event.widget)[9:10]), int(str(event.widget)[12:13]))}
        print(location)

    elif state == "place":
        print(event.widget)


def draw_board():
    global state
    board = \
        [
            [
                Label(window, width=2, height=1, bd=2, relief=GROOVE, name="eFleet: " + str(r) + ", " + str(c), text="")
                for c in
                range(10)
            ] for r in range(10)
        ]
    chars = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    col = row = 0
    for col in range(1, 11):
        Label(text=chars[col - 1]).grid(column=col, row=0)
        for row in range(1, 11):
            Label(text=row).grid(column=0, row=row)
            board[col - 1][row - 1].grid(row=row, column=col)
            board[col - 1][row - 1].bind("<Button-1>", click_event)

    board = \
        [
            [
                Label(window, width=2, height=1, bd=2, relief=GROOVE, name="pFleet: " + str(r) + ", " + str(c), text="")
                for c in
                range(10)
            ] for r in range(10)
        ]
    col = row = 0
    for col in range(1, 11):
        Label(text=chars[col - 1]).grid(column=col, row=11, pady=(25, 0))
        for row in range(11, 22):
            if row - 11 != 0:
                Label(text=row - 11).grid(column=0, row=row)
            board[col - 1][row - 12].grid(row=row, column=col)
            board[col - 1][row - 12].bind("<Button-1>", click_event)
    del chars

    if state == "place":
        place_labels = [
            Label(text="Place your fleet"),
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
        place_labels[1].grid(row=9, column=11, padx=(20, 0))
        place_labels[2].grid(row=10, column=11, padx=(20, 0))
        place_labels[3].grid(row=11, column=11, padx=(20, 0))
        place_labels[4].grid(row=9, column=13, padx=(0, 20))
        place_labels[5].grid(row=10, column=13, padx=(0, 20))
        place_labels[6].grid(row=11, column=13, padx=(0, 20))
        place_labels[7].grid(row=12, column=12, padx=(0, 20))


draw_board()
window.mainloop()
