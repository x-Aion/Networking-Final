
if __name__ == "__main__":
    print("Welcome to our COMP-3670 Final Project")
    print("Created by: Harpreet Dhamarait, Ryan Dreise, Sawyer King, Jack Pistagnesi, and Ikenna Uduh")

    # prompting the user to see we should start a client and a server or just a server
    while True:
        choice = input("What would you like to do next? [0] Host new game [1] Join a game: ").strip()
        if choice == "0" or choice == "1":
            break
        print("Invalid input, please enter a 0 or 1")

    if choice == "0":
        # start a server in a new process
        pass

    # start a client in this process
    # pass a new TicTacToe instance to it

