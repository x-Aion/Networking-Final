import socket
from _thread import *
import time
import random
from Board import Board


def TicTacToeX(client, opponentName, game_board):
    global log_file, include_packets
    print("Enter a message or type 'quit'")
    log_file.write("Enter a message or type 'quit'\n")
    print(game_board.printBoard(mode=0))
    log_file.write(game_board.printBoard(mode=0) + "\n")

    while 1:

        # displaying current start of the board
        # and asking for a valid move to play
        print(game_board.printBoard(mode=1))
        log_file.write(game_board.printBoard(mode=1)+"\n")
        print()
        log_file.write("\n\n")

        move = input("Your turn: ").lower().strip()
        log_file.write("Your turn: " + move+"\n")

        if move == 'quit':
            print("You have quit the game")
            log_file.write("You have quit the game\n")
            client.sendall(move.encode('ascii', 'strict'))
            if include_packets: log_file.write(
                f"-> Packet to server: {move}   | Byte encoded is {move.encode('ascii', 'strict')}\n")
            break

        else:
            # making sure the move input is valid, if not
            # ask again
            valid_move = game_board.makeMove(move, "X")
            while valid_move < 1:
                print("Please enter a valid cell number")
                log_file.write("Please enter a valid cell number\n")

                move = input("Your turn: ").strip()
                log_file.write("Your turn: " + move+"\n")

                if move == "quit":
                    print("You have quit the game")
                    log_file.write("You have quit the game\n")
                    return

                valid_move = game_board.makeMove(move, "X")

        # Send a move/message to server (which sends said move/message to opponent)
        client.sendall(move.encode('ascii', 'strict'))
        if include_packets: log_file.write(
            f"-> Packet to server: {move}   | Byte encoded is {move.encode('ascii', 'strict')}\n")

        print(game_board)
        log_file.write(game_board.printBoard(mode=0)+"\n")

        print("Move sent. Waiting for opponent... ")
        log_file.write("Move sent. Waiting for opponent... \n")

        # checking if the move played won the game
        if game_board.isWinner(move):
            print("You have won against " + opponentName+"\n")
            log_file.write("You have won against " + opponentName+"\n")
            break

        # checking if the move played tied the game
        elif game_board.isBoardFull():
            print("You have tied the game with " + opponentName)
            log_file.write("You have tied the game with " + opponentName+"\n")
            break

        # if didn't win and didn't tie game must be in play still
        # Receive a move/message
        received = client.recv(1024).decode('ascii', 'strict')
        if include_packets: log_file.write(
            f"-> Packet from server: {received}   | Byte encoded is {received.encode('ascii', 'strict')}\n")

        # Process players move
        game_board.makeMove(received, "O")

        print("Message received: \n" + received)
        log_file.write("Message received: \n" + received+"\n")

        print(game_board.printBoard(mode=0))
        log_file.write(game_board.printBoard(mode=0)+"\n")

        gameOver = "gameover".encode('ascii', 'strict')

        if received.lower().strip() == "quit":
            print(opponentName + " has quit the game. You win")
            log_file.write(opponentName + " has quit the game. You win\n")
            break

        # checking if the opponent's move won the game
        elif game_board.isWinner(received):
            print("You have lost against " + opponentName)
            log_file.write("You have lost against " + opponentName+"\n")
            client.sendall(gameOver)
            if include_packets: log_file.write(
                f"-> Packet to server: gameover  | Byte encoded is {gameOver}\n")
            break

        # checking if the opponent's move tied the game
        elif game_board.isBoardFull():
            print("You have tied the game with " + opponentName)
            log_file.write("You have tied the game with " + opponentName+"\n")
            client.sendall(gameOver)
            if include_packets: log_file.write(
                f"-> Packet to server: gameover   | Byte encoded is {gameOver}\n")
            break


def TicTacToeO(client, opponentName, game_board):
    global log_file, include_packets
    print("After your opponents turn enter a message or type 'quit'")
    log_file.write("After your opponents turn enter a message or type 'quit'\n")

    print(game_board.printBoard(mode=0))
    log_file.write(game_board.printBoard(mode=0)+"\n")

    while 1:
        # Receive a move/message
        received = client.recv(1024).decode('ascii', 'strict')
        if include_packets: log_file.write(
            f"-> Packet from server: {received}   | Byte encoded is {received.encode('ascii', 'strict')}\n")

        # Send this to server if the message recieved from the opponent is quit, lost, won or tied so server knows to reset

        # Process players move

        print("Message received: \n" + received)
        log_file.write("Message received: \n" + received+"\n")

        game_board.makeMove(received, "X")

        print(game_board.printBoard())
        log_file.write(game_board.printBoard()+"\n")

        gameOver = "gameover".encode('ascii', 'strict')

        # checking if opponent left or quit the game
        if received.lower().strip() == "quit":
            print(opponentName + " has quit the game. You win")
            log_file.write(opponentName + " ha quit the game. You win\n")
            break

        # checking if the opponent's move won the game
        elif game_board.isWinner(received):
            print("You have lost against " + opponentName)
            log_file.write("You have lost against " + opponentName+"\n")
            client.sendall(gameOver)
            if include_packets: log_file.write(
                f"-> Packet to server: gameover   | Byte encoded is {gameOver}\n")
            break

        # checking if the opponent's move tied the game
        elif game_board.isBoardFull():
            print("You have tied the game with " + opponentName)
            log_file.write("You have tied against " + opponentName+"\n")
            client.sendall(gameOver)
            if include_packets: log_file.write(
                f"-> Packet to server: gameover  | Byte encoded is {gameOver}\n")
            break

        move = input("Your turn: ").strip().lower()
        log_file.write("Your turn: " + move+"\n")

        # asking the user to select a cell on the board
        # if a valid cell is chosen that info is relayed to
        # the opponent
        print(game_board.printBoard())
        log_file.write(game_board.printBoard()+"\n")

        print()
        log_file.write("\n")

        if move == 'quit':
            print("You have quit the game")
            log_file.write("You have quit the game\n")
            client.sendall(move.encode('ascii', 'strict'))
            if include_packets: log_file.write(
                f"-> Packet to server: {move}   | Byte encoded is {move.encode('ascii', 'strict')}\n")
            break

        else:
            # making sure the move input is valid, if not
            # ask again
            valid_move = game_board.makeMove(move, "O")
            while valid_move < 1:
                print("Please enter a valid cell number")
                log_file.write("Please enter a valid cell number\n")

                move = input("Your turn: ").strip()
                log_file.write("Your turn: " + move + "\n")

                if move == "quit":
                    print("You have quit the game")
                    log_file.write("You have quit the game\n")
                    return

                valid_move = game_board.makeMove(move, "O")

        # Send a move/message to server (which sends said move/message to opponent)
        client.sendall(move.encode('ascii', 'strict'))
        if include_packets: log_file.write(
            f"-> Packet to server: {move}   | Byte encoded is {move.encode('ascii', 'strict')}\n")

        print(game_board)
        log_file.write(game_board.printBoard(mode=0) + "\n")

        print("Move sent. Waiting for opponent... ")
        log_file.write("Move sent. Waiting for opponent... \n")

        # checking if the move played won the game
        if game_board.isWinner(move):
            print("You have won against " + opponentName)
            log_file.write("You have won against " + opponentName+"\n")
            break

        # checking if the move played tied the game
        elif game_board.isBoardFull():
            print("You have tied the game with " + opponentName)
            log_file.write("You have tied the game with " + opponentName+"\n")
            break


def start_server():
    global log_file, include_packets
    connections = []
    usernames = []
    waitingUsers = []
    waitingUsersConnections = []

    # create server socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # get host name
    name = socket.gethostname()
    print("The name of the host is: " + name)
    log_file.write("The name of the host is: " + name+"\n")

    # get ip of host
    ip = socket.gethostbyname(name)
    print("The IP of the host is: " + ip)
    log_file.write("The IP of the host is: " + ip+"\n")

    # opening up a connection to the server
    port = 4321
    adrs = (ip, port)
    server.bind(adrs)
    server.listen(1)
    print("Started listening on ", ip, ":", port)
    log_file.write(f"Started listening on {ip}:{port}\n")

    def clientThread(client):
        global log_file, include_packets
        name = client.recv(1024).decode('ascii', 'strict')
        if include_packets: log_file.write(
            f"<- Packet from client: {name}   | Byte encoded is {name.encode('ascii', 'strict')}\n")

        usernames.append(name)
        while 1:
            received = client.recv(1024).decode('ascii', 'strict')
            if include_packets: log_file.write(
                f"<- Packet from client: {received}   | Byte encoded is {received.encode('ascii', 'strict')}\n")

            if received == "wait":

                # Adding the client to the wait list
                waitingUsers.append(name)
                waitingUsersConnections.append(client)
                userNo = len(waitingUsers) - 1
                print(name + " has been added to the wait list")
                log_file.write(name + " has been added to the wait list\n")

                # Defining the connections to both players so communication can be established
                connection1 = client
                connection2No = client.recv(1024)  # Received from the client
                if include_packets: log_file.write(f"<- Packet from client: {connection2No}\n")
                connection2No = int.from_bytes(connection2No, byteorder='big')
                connection2 = connections[connection2No]

                # Receive messages from the waiting client and send them
                # to the looking client freely until win, lose or quit is given
                while 1:
                    msg = connection1.recv(1024).decode('ascii', 'strict').lower().strip()
                    if include_packets: log_file.write(
                        f"<- Packet from client: {msg}   | Byte encoded is {msg.encode('ascii', 'strict')}\n")

                    if msg == "win" or msg == "lose" or msg == "quit" or msg == "tie":
                        connection2.send(msg.encode('ascii', 'strict'))
                        if include_packets: log_file.write(
                            f"<- Packet to client: {msg}   | Byte encoded is {msg.encode('ascii', 'strict')}\n")

                        break
                    elif msg == "gameover":
                        break
                    else:
                        connection2.send(msg.encode('ascii', 'strict'))
                        if include_packets: log_file.write(
                            f"<- Packet to client: {msg}   | Byte encoded is {msg.encode('ascii', 'strict')}\n")

                # When game is over delete user from waiting list
                del waitingUsersConnections[userNo]
                del waitingUsers[userNo]
                print(name + " removed from waiting list")
                log_file.write(name + " removed from waiting list\n")

            elif received == "look":
                print(name + " has been added")
                log_file.write(name + " has been added\n")

                # Send the list of waiting users to the client
                x = 1
                wUsers = ""
                for w in waitingUsers:
                    wUsers = wUsers + w + "  (" + str(x) + ")\n"
                    x = x + 1
                client.send(wUsers.encode('ascii', 'strict'))
                if include_packets: log_file.write(
                    f"<- Packet to client: {wUsers}   | Byte encoded is {wUsers.encode('ascii', 'strict')}\n")

                # Defining the connections to both players so communication can be established
                connection1 = client
                connection2No = int(
                    float(client.recv(1024).decode('ascii', 'strict'))) - 1  # Get chosen opponent from client2
                if include_packets: log_file.write(f"<- Packet from client: {connection2No}\n")

                connection2 = waitingUsersConnections[connection2No]
                connection2name = waitingUsers[connection2No]

                # Get the number of where our client is in the usernames
                connection1No = 0
                for y in usernames:
                    if y == name:
                        break
                    else:
                        connection1No = connection1No + 1
                connection1No = bytes([connection1No])

                # Send the connection and connection name of the looking client to the chosen waiting client so the
                # waiting client can update its side of the server with the looking clients info
                time.sleep(1)
                connection2.send(connection1No)
                if include_packets: log_file.write(
                    f"<- Packet to client: {connection1No}\n")

                time.sleep(1)
                connection2.send(name.encode('ascii', 'strict'))
                print("A game has started between " + name + " and " + connection2name)
                log_file.write("A game has started between " + name + " and " + connection2name+"\n")

                # Receive messages from the looking client and send
                # them to the waiting client freely until win,
                # lose, quit, tie or gameover is given
                while 1:
                    msg = connection1.recv(1024).decode('ascii', 'strict').lower().strip()
                    if include_packets: log_file.write(
                        f"<- Packet from client: {msg}   | Byte encoded is {msg.encode('ascii', 'strict')}\n")

                    if msg == "win" or msg == "lose" or msg == "quit" or msg == "tie":
                        connection2.send(msg.encode('ascii', 'strict'))
                        if include_packets: log_file.write(
                            f"<- Packet to client: {msg}   | Byte encoded is {msg.encode('ascii', 'strict')}\n")
                        break
                    elif msg == "gameover":
                        print(name + "'s and " + connection2name + "'s game has ended")
                        log_file.write(name + "'s and " + connection2name + "'s game has ended\n")
                        break
                    else:
                        connection2.send(msg.encode('ascii', 'strict'))
                        if include_packets: log_file.write(
                            f"<- Packet to client: {msg}   | Byte encoded is {msg.encode('ascii', 'strict')}\n")

            elif received == "quit":
                break

    while 1:
        client, addr = server.accept()
        connections.append(client)
        print("Obtained a Connection from ", addr[0], " : ", addr[1])
        log_file.write(f"Obtained a Connections from {addr[0]}:{addr[1]}\n")
        start_new_thread(clientThread, (client,))
    server.close()


def start_client():
    global log_file, include_packets
    # initialize the gameboard
    game_board = Board()

    # create socket
    client = socket.socket()

    # get ip
    # host = socket.gethostname()
    # hostip = socket.gethostbyname(host)
    hostip = input("Enter the ip of the server: ").strip()
    log_file.write("Enter the ip of the server: " + hostip+"\n")

    # connect to server
    print(f"Attempting to connect to: {hostip}")
    log_file.write(f"Attempting to connect to: {hostip}\n")
    client.connect((hostip, 4321))

    print("Connection successful!")
    log_file.write("Connection successful!\n")

    username = input("Enter your username: ")
    log_file.write("Enter your username: " + username+"\n")

    client.sendall(username.encode('ascii', 'strict'))
    if include_packets: log_file.write(
        f"-> Packet to server: {username}   | Byte encoded is {username.encode('ascii', 'strict')}\n")

    while 1:
        data = input(
            "Would you like to wait for a game or look for other users currently waiting? Type 'wait', 'look' or 'quit' ").lower().strip()
        log_file.write(
            "Would you like to wait for a game or look for other users currently waiting? Type 'wait', 'look' or 'quit' " + data+"\n")

        if data == 'wait':
            # Tell server client is now waiting for a game
            waiting = "wait"
            client.sendall(waiting.encode('ascii', 'strict'))
            if include_packets: log_file.write(
                f"-> Packet to server: {waiting}   | Byte encoded is {waiting.encode('ascii', 'strict')}\n")

            # Wait for a game
            print("Waiting for a game...")
            log_file.write("Waiting for a game...\n")

            opponentConnectionNo = client.recv(1024)
            if include_packets: log_file.write(
                f"<- Packet from client: {opponentConnectionNo}\n")

            opponentName = client.recv(1024).decode('ascii', 'strict')
            if include_packets: log_file.write(
                f"<- Packet from client: {opponentName}   | Byte encoded is {opponentName.encode('ascii', 'strict')}\n")

            print("You are playing against: " + opponentName)
            log_file.write("You are playing against: " + opponentName + "\n")

            # Tell server where the opponents connection in the list of connections is
            time.sleep(1)
            client.sendall(opponentConnectionNo)
            if include_packets: log_file.write(
                f"-> Packet to server: {opponentConnectionNo}\n")

            # Sending server this clients name which then tells the opponent
            time.sleep(1)
            client.sendall(username.encode('ascii', 'strict'))
            if include_packets: log_file.write(
                f"-> Packet to server: {username}   | Byte encoded is {username.encode('ascii', 'strict')}\n")

            # Getting whether client is X or O from opponent
            randXorO = client.recv(1024)
            if include_packets: log_file.write(
                f"-> Packet from server: {randXorO.decode()}   | Byte encoded is {randXorO}\n")

            randXorO = int.from_bytes(randXorO, byteorder='big')

            # Start game
            if randXorO == 1:
                print("You have been randomly assigned: Os")
                log_file.write("You have been randomly assigned: Os\n")
                TicTacToeO(client, opponentName, game_board)

            elif randXorO == 2:
                print("You have been randomly assigned: Xs")
                log_file.write("You have been randomly assigned: Xs\n")
                TicTacToeX(client, opponentName, game_board)

        elif data == 'look':

            # Tell server client is now looking for a game
            looking = "look"
            time.sleep(1)
            client.sendall(looking.encode('ascii', 'strict'))
            if include_packets: log_file.write(
                f"-> Packet to server: {looking}   | Byte encoded is {looking.encode('ascii', 'strict')}\n")

            # Ask which user in the waiting list the client would like to play against and tell the server
            users = client.recv(1024).decode('ascii', 'strict')
            if include_packets: log_file.write(
                f"-> Packet from server: {users}   | Byte encoded is {users.encode('ascii', 'strict')}\n")

            print(
                "The users currently looking for a game are:\n" + users + "\nPick which one you want to play against by typing their number")
            userNo = input()
            log_file.write(
                f"The users currently looking for a game are:\n{users}\nPick which one you want to play against by typing their number\n")
            log_file.write(userNo+"\n")

            time.sleep(1)
            client.sendall(userNo.encode('ascii', 'strict'))
            if include_packets: log_file.write(
                f"-> Packet to server: {userNo}   | Byte encoded is {userNo.encode('ascii', 'strict')}\n")

            opponentName = client.recv(1024).decode('ascii', 'strict')
            if include_packets: log_file.write(
                f"-> Packet from server: {opponentName}   | Byte encoded is {opponentName.encode('ascii', 'strict')}\n")

            # Randomly choose if client is X or O and tell opponent
            randXorO = random.choice([1, 2])
            time.sleep(1)
            client.sendall(bytes([randXorO]))
            if include_packets: log_file.write(
                f"-> Packet to server: {randXorO}   | Byte encoded is {bytes([randXorO])}\n")

            # Start game
            if randXorO == 1:
                print("You have been randomly assigned: Xs")
                log_file.write("You have been randomly assigned: Xs\n")
                TicTacToeX(client, opponentName, game_board)

            elif randXorO == 2:
                print("You have been randomly assigned: Os")
                log_file.write("You have been randomly assigned: Os\n")
                TicTacToeO(client, opponentName, game_board)

        elif data == "quit":
            break

        else:
            print("Wrong input. Type 'wait', 'look' or 'quit' ")
            log_file.write("Wrong input. Type 'wait', 'look' or 'quit' \n")


# if __name__ == "__main__":
include_packets = True
print("Welcome to our COMP-3670 Final Project")
print("Created by: Harpreet Dhamarait, Ryan Dreise, Sawyer King, Jack Pistagnesi, and Ikenna Uduh")
with open("gamelog.txt", "w") as log_file:
    while 1:
        data = input(
            "Would you like to start a [1] server, start a [2] client, or [3] quit ? Type 1, 2, or 3: ").strip()
        log_file.write(
            "Would you like to start a [1] server, start a [2] client, or [3] quit ? Type 1, 2, or 3: " + data+"\n")

        if data == "1":
            start_server()
            break
        elif data == "2":
            start_client()
            break
        elif data == "3":
            break
        else:
            print("Wrong input. Type either 1, 2 or 3")
            log_file.write("Wrong input. Type either 1, 2 or 3\n")
