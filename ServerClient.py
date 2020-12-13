import socket
from _thread import *
import time
import random

def TicTacToeX(client, opponentName): 
    print("Enter a message or type 'quit', 'lose', 'win' or 'tie'")
    while 1:
        print("Your turn: ")

        # Send a move/message to server (which sends said move/message to opponent)
        move = input()
        client.sendall(move.encode('ascii', 'strict'))
        
        # Process your move
        if move == "quit":
            print("You have quit the game")
            break
        elif move == "lose":
            print("You have lost the game against " + opponentName)
            break
        elif move == "win":
            print("You have won against " + opponentName)
            break
        elif move == "tie":
            print ("You have tied the game with " + opponentName)
            break


        # Receive a move/message
        print("Move sent. Waiting for opponent... ")
        received = client.recv(1024).decode('ascii', 'strict')

        # Send this to server if the received message is quit, lost, won or tied so server knows to reset
        gameOver = "gameover" 

        # Process players move
        if received == "quit":
            print(opponentName + " has quit the game. You win")
            client.sendall(gameOver.encode('ascii', 'strict'))
            break
        elif received == "lose":
            print("You have won the game against " + opponentName)
            client.sendall(gameOver.encode('ascii', 'strict'))
            break
        elif received == "win":
            print("You have lost against " + opponentName)
            client.sendall(gameOver.encode('ascii', 'strict'))
            break
        elif received == "tie":
            print ("You have tied the game with " + opponentName)
            client.sendall(gameOver.encode('ascii', 'strict'))
            break
        else:
            print("Message received: \n" + received)


def TicTacToeO(client, opponentName):
    print("After your opponents turn enter a message or type 'quit', 'lose', 'win' or 'tie'")
    while 1:
        # Receive a move/message
        received = client.recv(1024).decode('ascii', 'strict')

        # Send this to server if the message recieved from the opponent is quit, lost, won or tied so server knows to reset
        gameOver = "gameover" 

        # Process players move
        if received == "quit":
            print(opponentName + " has quit the game. You win")
            client.sendall(gameOver.encode('ascii', 'strict'))
            break
        elif received == "lose":
            print("You have won the game against " + opponentName)
            client.sendall(gameOver.encode('ascii', 'strict'))
            break
        elif received == "win":
            print("You have lost against " + opponentName)
            client.sendall(gameOver.encode('ascii', 'strict'))
            break
        elif received == "tie":
            print ("You have tied the game with " + opponentName)
            client.sendall(gameOver.encode('ascii', 'strict'))
            break
        else:
            print("Message received: \n" + received)
            

        print("Your turn: ")

        # Send a move/message to server (which sends said move/message to opponent)
        move = input()
        client.sendall(move.encode('ascii', 'strict'))
        
        # Process your move 
        if move == "quit":
            print("You have quit the game")
            break
        elif move == "lose":
            print("You have lost the game against " + opponentName)
            break
        elif move == "win":
            print("You have won against " + opponentName)
            break
        elif move == "tie":
            print ("You have tied the game with " + opponentName)
            break
        print("Move sent. Waiting for opponent... ")
        

def start_server():
    connections = []
    usernames = []
    waitingUsers = []
    waitingUsersConnections = []

    # create server socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # get host name
    name = socket.gethostname()
    print("The name of the host is: "+name)

    # get ip of host
    ip = socket.gethostbyname(name)
    print("The IP of the host is: "+ip)

    # opening up a connection to the server
    port = 4321
    adrs = (ip,port)
    server.bind(adrs)
    server.listen(1)
    print("Started listening on ",ip,":",port)

    def clientThread(client):
        name = client.recv(1024).decode('ascii', 'strict')
        usernames.append(name)
        while 1:
            received = client.recv(1024).decode('ascii', 'strict')

            if received == "wait":

                # Adding the client to the wait list
                waitingUsers.append(name)
                waitingUsersConnections.append(client)
                userNo = len(waitingUsers) - 1
                print(name + " has been added to the wait list")

                # Defining the connections to both players so communication can be established
                connection1 = client
                connection2No = client.recv(1024)  # Recieved from the client
                connection2No = int.from_bytes(connection2No,byteorder='big')
                connection2 = connections[connection2No]

                # Receive messages from the waiting client and send them to the looking client freely until win, lose or quit is given
                while 1:
                    msg = connection1.recv(1024).decode('ascii', 'strict')
                    if msg == "win" or msg == "lose" or msg == "quit" or msg == "tie":
                        connection2.send(msg.encode('ascii','strict'))
                        break
                    elif msg == "gameover":
                        break
                    else:
                        connection2.send(msg.encode('ascii','strict'))

                # When game is over delete user from waiting list
                del waitingUsersConnections[userNo]
                del waitingUsers[userNo]
                print(name + " removed from waiting list")


            elif received == "look":
                print(name + " has been added")

                # Send the list of waiting users to the client
                x = 1
                wUsers = ""
                for w in waitingUsers:
                    wUsers = wUsers + w + "  (" + str(x) + ")\n"
                    x = x + 1
                client.send(wUsers.encode('ascii','strict'))

                # Defining the connections to both players so communication can be established
                connection1 = client
                connection2No = int(float(client.recv(1024).decode('ascii', 'strict'))) - 1  #Get chosen opponent from client2
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
                time.sleep(1)
                connection2.send(name.encode('ascii','strict'))
                print("A game has started between " + name + " and " + connection2name)

                # Receive messages from the looking client and send them to the waiting client freely until win, lose, quit, tie or gameover is given
                while 1:
                    msg = connection1.recv(1024).decode('ascii', 'strict')
                    if msg == "win" or msg == "lose" or msg == "quit" or msg == "tie":
                        connection2.send(msg.encode('ascii','strict'))
                        break
                    elif msg == "gameover":
                        print(name + "'s and " + connection2name + "'s game has ended")
                        break
                    else:
                        connection2.send(msg.encode('ascii','strict'))


    while 1:
        client,addr = server.accept()
        connections.append(client)
        print("Obtained a Connection from ",addr[0]," : ",addr[1])
        start_new_thread(clientThread,(client,))
    server.close()





def start_client():
    # create socket
    client=socket.socket()

    # get ip
    host=socket.gethostname()
    hostip=socket.gethostbyname(host)

    # connect to server
    client.connect((hostip,4321))

    print("Enter your username: ")
    username = input()
    client.sendall(username.encode('ascii', 'strict'))

    while 1:
        print("Would you like to wait for a game or look for other users currently waiting? Type 'wait' or 'look'")
        data = input()
        if data == 'wait':
            # Tell server client is now waiting for a game
            waiting = "wait"
            client.sendall(waiting.encode('ascii', 'strict'))

            # Wait for a game
            print("Waiting for a game...")
            opponentConnectionNo = client.recv(1024)
            opponentName = client.recv(1024).decode('ascii', 'strict')
            print("You are playing against: " + opponentName)

            # Tell server where the opponents connection in the list of connections is
            time.sleep(1)
            client.sendall(opponentConnectionNo)

            # Sending server this clients name which then tells the opponent
            time.sleep(1)
            client.sendall(username.encode('ascii', 'strict'))
            
            # Getting whether client is X or O from opponent
            randXorO = client.recv(1024)
            randXorO = int.from_bytes(randXorO,byteorder='big')

            # Start game
            if randXorO == 1:
                print("You have been randomly assigned: Os")
                TicTacToeO(client, opponentName)
            elif randXorO == 2:
                print("You have been randomly assigned: Xs")
                TicTacToeX(client, opponentName)

    

        elif data == 'look':
            # Tell server client is now looking for a game
            looking = "look"
            time.sleep(1)
            client.sendall(looking.encode('ascii', 'strict'))

            # Ask which user in the waiting list the client would like to play against and tell the server
            users = client.recv(1024).decode('ascii', 'strict')
            print("The users currently looking for a game are:\n" + users + "\nPick which one you want to play against by typing their number")
            userNo = input()
            time.sleep(1)
            client.sendall(userNo.encode('ascii', 'strict'))

            opponentName = client.recv(1024).decode('ascii', 'strict')  
            
            # Randomly choose if client is X or O and tell opponent
            randXorO = random.choice([1,2])
            time.sleep(1)
            client.sendall(bytes([randXorO]))  

            # Start game
            if randXorO == 1:
                print("You have been randomly assigned: Xs")
                TicTacToeX(client, opponentName)
            elif randXorO == 2:
                print("You have been randomly assigned: Os")
                TicTacToeO(client, opponentName)


            
        else: 
            print("Wrong input. Type 'wait' or 'look'")
        


print("Would you like to start a server or start a client? Type 1 or 2:")
while 1:
    data = input()
    if data == "1":
        start_server()
    elif data == "2":
        start_client()
    else:
        print("Wrong input. Type either 1 or 2")

