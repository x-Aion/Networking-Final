
import socket
import threading
from time import sleep
import tkinter as tk
from tkinter import messagebox
# This will be the main window
main_win = tk.Tk()
main_win.title("Tic Tac Toe Client")
Frame1= tk.Frame(main_win)
Lbel = tk.Label(Frame1, text = "Enter Name:")
Lbel.pack(side=tk.LEFT)
CharName = tk.Entry(Frame1)
CharName.pack(side=tk.LEFT)

label_ip = tk.Label(Frame1, text = "Enter Server IP:")
label_ip.pack(side=tk.LEFT)
entry_ip = tk.Entry(Frame1)
entry_ip.pack(side=tk.LEFT)

Clicker = tk.Button(Frame1, text="Connect", command=lambda : connect())
Clicker.pack(side=tk.LEFT)
Frame1.pack(side=tk.TOP)
Frame2 = tk.Frame(main_win)


# network client
client = None
HOST_IP = "0.0.0.0"
PORT_OF_HOST = 1234

my_turn = False
iStart = False
Label_List = []
Columns = 3

my_details = {
    "name": "HP",
    "score" : 0,
    "symbol" : "X",
    "colour" : "",
}

enemy_detail = {
    "name": " ",
    "score": 0,
    "symbol": "O",
    "colour": "",
}

for x in range(3):
    for y in range(3):
        sticker = tk.Label(Frame2, text=" ", font="Helvetica 45 bold", height=2, width=5, highlightbackground="grey",
                       highlightcolor="grey", highlightthickness=1)
        sticker.bind("<Button-1>", lambda e, xy=[x, y]: get_cordinate(xy))
        sticker.grid(row=x, column=y)

        dict_labels = {"xy": [x, y], "symbol": "", "label": sticker, "ticked": False}
        Label_List.append(dict_labels)

sticker_status = tk.Label(Frame2, text="Status: Not connected with the server.", font="Helvetica 14 bold")
sticker_status.grid(row=3, columnspan=3)

Frame2.pack_forget()


def init(arg0, arg1):
    global Label_List, my_turn, my_details, enemy_detail, iStart

    sleep(3)

    for i in range(len(Label_List)):
        Label_List[i]["symbol"] = ""
        Label_List[i]["ticked"] = False
        Label_List[i]["label"]["text"] = ""
        Label_List[i]["label"].config(foreground="black", highlightbackground="grey",
                                       highlightcolor="grey", highlightthickness=1)

    sticker_status.config(foreground="black")
    sticker_status["text"] = "Please wait while the game starts..."
    sleep(1)
    sticker_status["text"] = "Please wait while the game starts..."
    sleep(1)
    sticker_status["text"] = "Please wait while the game starts..."
    sleep(1)

    if iStart:
        iStart = False
        my_turn = False
        sticker_status["text"] = "STATUS: " + enemy_detail["name"] + "'s turn!"
    else:
        iStart = True
        my_turn = True
        sticker_status["text"] = "STATUS: Your turn!"


def get_cordinate(xy):
    global client, my_turn
    # convert 2D to 1D cordinate i.e. index = x * Columns + y
    label_index = xy[0] * Columns + xy[1]
    label = Label_List[label_index]

    if my_turn:
        if label["ticked"] is False:
            label["label"].config(foreground=my_details["color"])
            label["label"]["text"] = my_details["symbol"]
            label["ticked"] = True
            label["symbol"] = my_details["symbol"]
            # send xy cordinate to server
            client.send(str.encode("$xy$" + str(xy[0]) + "$" + str(xy[1])))
            print("$xy$" + str(xy[0]) + "$" + str(xy[1]))
            my_turn = False

            # Does this play leads to a win or a draw
            result = logic()
            if result[0] is True and result[1] != "":  # a win
                my_details["score"] = my_details["score"] + 1
                sticker_status["text"] = "Game over, You won! You(" + str(my_details["score"]) + ") - " \
                    "" + enemy_detail["name"] + "(" + str(enemy_detail["score"])+")"
                sticker_status.config(foreground="green")
                threading._start_new_thread(init, ("", ""))

            elif result[0] is True and result[1] == "":  # a draw
                sticker_status["text"] = "Game over, Draw! You(" + str(my_details["score"]) + ") - " \
                    "" + enemy_detail["name"] + "(" + str(enemy_detail["score"]) + ")"
                sticker_status.config(foreground="blue")
                threading._start_new_thread(init, ("", ""))

            else:
                sticker_status["text"] = "STATUS: " + enemy_detail["name"] + "'s turn!"
    else:
        sticker_status["text"] = "STATUS: Wait for your turn!"
        sticker_status.config(foreground="red")

        # send xy coordinate to server to server


# [(0,0) -> (0,1) -> (0,2)], [(1,0) -> (1,1) -> (1,2)], [(2,0), (2,1), (2,2)]
def check_row():
    list_symbols = []
    Label_List_temp = []
    winner = False
    win_symbol = ""
    for i in range(len(Label_List)):
        list_symbols.append(Label_List[i]["symbol"])
        Label_List_temp.append(Label_List[i])
        if (i + 1) % 3 == 0:
            if (list_symbols[0] == list_symbols[1] == list_symbols[2]):
                if list_symbols[0] != "":
                    winner = True
                    win_symbol = list_symbols[0]

                    Label_List_temp[0]["label"].config(foreground="green", highlightbackground="green",
                                                        highlightcolor="green", highlightthickness=2)
                    Label_List_temp[1]["label"].config(foreground="green", highlightbackground="green",
                                                        highlightcolor="green", highlightthickness=2)
                    Label_List_temp[2]["label"].config(foreground="green", highlightbackground="green",
                                                        highlightcolor="green", highlightthickness=2)

            list_symbols = []
            Label_List_temp = []

    return [winner, win_symbol]


# [(0,0) -> (1,0) -> (2,0)], [(0,1) -> (1,1) -> (2,1)], [(0,2), (1,2), (2,2)]
def check_col():
    winner = False
    win_symbol = ""
    for i in range(Columns):
        if Label_List[i]["symbol"] == Label_List[i + Columns]["symbol"] == Label_List[i + Columns + Columns][
            "symbol"]:
            if Label_List[i]["symbol"] != "":
                winner = True
                win_symbol = Label_List[i]["symbol"]

                Label_List[i]["label"].config(foreground="green", highlightbackground="green",
                                               highlightcolor="green", highlightthickness=2)
                Label_List[i + Columns]["label"].config(foreground="green", highlightbackground="green",
                                                          highlightcolor="green", highlightthickness=2)
                Label_List[i + Columns + Columns]["label"].config(foreground="green", highlightbackground="green",
                                                                     highlightcolor="green", highlightthickness=2)

    return [winner, win_symbol]


def check_diagonal():
    winner = False
    win_symbol = ""
    i = 0
    j = 2

    # top-left to bottom-right diagonal (0, 0) -> (1,1) -> (2, 2)
    a = Label_List[i]["symbol"]
    b = Label_List[i + (Columns + 1)]["symbol"]
    c = Label_List[(Columns + Columns) + (i + 1)]["symbol"]
    if Label_List[i]["symbol"] == Label_List[i + (Columns + 1)]["symbol"] == \
            Label_List[(Columns + Columns) + (i + 2)]["symbol"]:
        if Label_List[i]["symbol"] != "":
            winner = True
            win_symbol = Label_List[i]["symbol"]

            Label_List[i]["label"].config(foreground="green", highlightbackground="green",
                                           highlightcolor="green", highlightthickness=2)

            Label_List[i + (Columns + 1)]["label"].config(foreground="green", highlightbackground="green",
                                                            highlightcolor="green", highlightthickness=2)
            Label_List[(Columns + Columns) + (i + 2)]["label"].config(foreground="green",
                                                                         highlightbackground="green",
                                                                         highlightcolor="green", highlightthickness=2)

    # top-right to bottom-left diagonal (0, 0) -> (1,1) -> (2, 2)
    elif Label_List[j]["symbol"] == Label_List[j + (Columns - 1)]["symbol"] == Label_List[j + (Columns + 1)][
        "symbol"]:
        if Label_List[j]["symbol"] != "":
            winner = True
            win_symbol = Label_List[j]["symbol"]

            Label_List[j]["label"].config(foreground="green", highlightbackground="green",
                                           highlightcolor="green", highlightthickness=2)
            Label_List[j + (Columns - 1)]["label"].config(foreground="green", highlightbackground="green",
                                                            highlightcolor="green", highlightthickness=2)
            Label_List[j + (Columns + 1)]["label"].config(foreground="green", highlightbackground="green",
                                                            highlightcolor="green", highlightthickness=2)
    else:
        winner = False

    return [winner, win_symbol]


# it's a draw if grid is filled
def check_draw():
    for i in range(len(Label_List)):
        if Label_List[i]["ticked"] is False:
            return [False, ""]
    return [True, ""]


def logic():
    result = check_row()
    if result[0]:
        return result

    result = check_col()
    if result[0]:
        return result

    result = check_diagonal()
    if result[0]:
        return result

    result = check_draw()
    return result


def connect():
    global my_details
    if len(CharName.get()) < 1:
        tk.messagebox.showerror(title="ERROR!!!", message="You MUST enter your first name <e.g. John>")
    elif len(entry_ip.get()) < 1:
        tk.messagebox.showerror(title="ERROR!!!", message="You MUST enter an IP <e.g. 192.168.0.1>")
    else:
        my_details["name"] = CharName.get().strip()
        my_details["server_ip"] = entry_ip.get().strip()

        connect_to_server(my_details["name"], my_details["server_ip"])


def connect_to_server(name, HOST_IP):
    global client, PORT_OF_HOST #, HOST_IP

    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST_IP, PORT_OF_HOST))
        client.send(name.encode())
        threading._start_new_thread(receive_message_from_server, (client, "m"))
        Frame1.pack_forget()
        Frame2.pack(side=tk.TOP)
        main_win.title("Tic Tac Toe Client - " + name)
    except Exception as e:
        tk.messagebox.showerror(title="ERROR!!!", message="Cannot connect to host: " + HOST_IP + " on port: " + str(
            PORT_OF_HOST) + " Server may be Unavailable. Try again later")



def receive_message_from_server(sck, m):
    global my_details, enemy_detail, my_turn, you_started
    while True:
        from_server = sck.recv(4096)

        if not from_server: break

        from_server = from_server.decode()
        if from_server.startswith("welcome"):
            if from_server == "welcome1":
                my_details["color"] = "purple"
                enemy_detail["color"] = "orange"
                sticker_status["text"] = "Server: Welcome " + my_details["name"] + "! Waiting for player 2"
            elif from_server == "welcome2":
                sticker_status["text"] = "Server: Welcome " + my_details["name"] + "! Game will start soon"
                my_details["color"] = "orange"
                enemy_detail["color"] = "purple"

        elif from_server.startswith("opponent_name$"):
            temp = from_server.replace("opponent_name$", "")
            temp = temp.replace("symbol", "")
            name_index = temp.find("$")
            symbol_index = temp.rfind("$")
            enemy_detail["name"] = temp[0:name_index]
            my_details["symbol"] = temp[symbol_index:len(temp)]

            # set enemy symbol
            if my_details["symbol"] == "O":
                enemy_detail["symbol"] = "X"
            else:
                enemy_detail["symbol"] = "O"

            sticker_status["text"] = "STATUS: " + enemy_detail["name"] + " is connected!"
            sleep(3)
            # is it your turn to play? hey! 'O' comes before 'X'
            if my_details["symbol"] == "O":
                sticker_status["text"] = "STATUS: Your turn!"
                my_turn = True
                you_started = True
            else:
                sticker_status["text"] = "STATUS: " + enemy_detail["name"] + "'s turn!"
                you_started = False
                my_turn = False
        elif from_server.startswith("$xy$"):
            temp = from_server.replace("$xy$", "")
            _x = temp[0:temp.find("$")]
            _y = temp[temp.find("$") + 1:len(temp)]

            # update board
            label_index = int(_x) * Columns + int(_y)
            label = Label_List[label_index]
            label["symbol"] = enemy_detail["symbol"]
            label["label"]["text"] = enemy_detail["symbol"]
            label["label"].config(foreground=enemy_detail["color"])
            label["ticked"] = True

            # Does this cordinate leads to a win or a draw
            result = logic()
            if result[0] is True and result[1] != "":  # opponent win
                enemy_detail["score"] = enemy_detail["score"] + 1
                if result[1] == enemy_detail["symbol"]:  #
                    sticker_status["text"] = "Game over, You Lost! You(" + str(my_details["score"]) + ") - " \
                        "" + enemy_detail["name"] + "(" + str(enemy_detail["score"]) + ")"
                    sticker_status.config(foreground="red")
                    threading._start_new_thread(init, ("", ""))
            elif result[0] is True and result[1] == "":  # a draw
                sticker_status["text"] = "Game over, Draw! You(" + str(my_details["score"]) + ") - " \
                    "" + enemy_detail["name"] + "(" + str(enemy_detail["score"]) + ")"
                sticker_status.config(foreground="blue")
                threading._start_new_thread(init, ("", ""))
            else:
                my_turn = True
                sticker_status["text"] = "STATUS: Your turn!"
                sticker_status.config(foreground="black")

    sck.close()


main_win.mainloop()


