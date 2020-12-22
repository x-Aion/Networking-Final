from time import sleep
import threading
import tkinter as tk
import socket



window = tk.Tk()
window.title("Tic Tac Toe Server")
#The part of the UI that shows start and stop buttons
Frame1 = tk.Frame(window)
Clicker0 = tk.Button(Frame1, text="Start", command=lambda : start_server())
Clicker0.pack(side=tk.LEFT)
Clicker1 = tk.Button(Frame1, text="Stop", command=lambda : serverStop(), state=tk.DISABLED)
Clicker1.pack(side=tk.LEFT)
Frame1.pack(side=tk.TOP, pady=(5, 0))

# The part of the user interface that shows the IP and PORT
Frame3 = tk.Frame(window)
HostSticker = tk.Label(Frame3, text = "IP: N.O.N.E")
HostSticker.pack(side=tk.LEFT)
PortSticker = tk.Label(Frame3, text = "Port:ABCD")
PortSticker.pack(side=tk.LEFT)
Frame3.pack(side=tk.TOP, pady=(5, 0))

# UI for the Client
Frame4 = tk.Frame(window)
LineSticker = tk.Label(Frame4, text="----------List of Players----------").pack()
scrolling = tk.Scrollbar(Frame4)
scrolling.pack(side=tk.RIGHT, fill=tk.Y)
tkDisplay = tk.Text(Frame4, height=10, width=30)
tkDisplay.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
scrolling.config(command=tkDisplay.yview)
tkDisplay.config(yscrollcommand=scrolling.set, background="#FDD799", highlightbackground="brown", state="disabled")
Frame4.pack(side=tk.BOTTOM, pady=(5, 10))

clients = []
clients_names = []
player_data = []
server = None
HOST_IP = socket.gethostbyname(socket.gethostname())
PORT_OF_HOST = 1234
client_name = " "

# Starting up the server
def start_server():
    global server, HOST_IP, PORT_OF_HOST
    Clicker0.config(state=tk.DISABLED)
    Clicker1.config(state=tk.NORMAL)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(socket.AF_INET)
    print(socket.SOCK_STREAM)

    server.bind((HOST_IP, PORT_OF_HOST))
    server.listen(5)  # server is listening for client connection

    threading._start_new_thread(clientAcceptance, (server, " "))

    HostSticker["text"] = "Address: " + HOST_IP
    PortSticker["text"] = "Port: " + str(PORT_OF_HOST)


# Stopping the server
def serverStop():
    global server
    Clicker0.config(state=tk.NORMAL)
    Clicker1.config(state=tk.DISABLED)


def clientAcceptance(the_server, y):
    while True:
        if len(clients) < 2:
            client, addr = the_server.accept()
            clients.append(client)

            # use a thread so as not to clog the gui thread
            threading._start_new_thread(send_receive, (client, addr))


# Sending and receiving
def send_receive(client_connection, client_ip_addr):
    global server, client_name, clients, player_data, player0, player1

    client_msg = " "

    client_name = client_connection.recv(4096).decode()

    if len(clients) < 2:
        client_connection.send(str.encode("welcome1"))
    else:
        client_connection.send(str.encode("welcome2"))

    clients_names.append(client_name)
    update_client_names_display(clients_names)  # update client names display

    if len(clients) > 1:
        sleep(1)
        symbols = ["O", "X"]

        # This will tell the enemy what their symbol is (x or o)
        clients[0].send(str.encode("opponent_name$" + clients_names[1] + "symbol" + symbols[0]))
        clients[1].send(str.encode("opponent_name$" + clients_names[0] + "symbol" + symbols[1]))


    while True:


        data = client_connection.recv(4096)
        if not data: break

        if data.decode().startswith("$xy$"):

            if client_connection == clients[0]:

                clients[1].send(data)
            else:

                clients[0].send(data)


    idx = get_client_index(clients, client_connection)
    del clients_names[idx]
    del clients[idx]
    client_connection.close()

    update_client_names_display(clients_names)



def get_client_index(client_list, curr_client):
    idx = 0
    for conn in client_list:
        if conn == curr_client:
            break
        idx = idx + 1

    return idx


# Tells you if someone has connected to server or left.
def update_client_names_display(name_list):
    tkDisplay.config(state=tk.NORMAL)
    tkDisplay.delete('1.0', tk.END)

    for c in name_list:
        tkDisplay.insert(tk.END, c+"\n")
    tkDisplay.config(state=tk.DISABLED)


window.mainloop()