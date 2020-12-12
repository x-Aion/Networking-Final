from Board import Board
from Player import Player


# May need to be modified to work better with the Server and Client functions/Classes
class TicTacToe:
    def __init__(self):
        self.players = []
        self.used_names = set()
        self.used_tile_pieces = set()
        self.game_board = Board(board_size=3)
        self.gameRunning = True  # idk if it should be true or false to begin with

        # player at this index of self.players will
        # have it be their turn
        self.current_turn = 0

    def addPlayer(self):
        """ Adds a player to a the game """

        while True:
            name = input("Input name: ").strip()
            if name.lower() not in self.used_names:
                break
            print("Name already in use!")

        while True:
            tile_piece = input("Input a symbol: ").strip()
            if tile_piece.lower() not in self.used_tile_pieces:
                break
            print("Sorry symbol already in use!")

        self.used_names.add(name.lower())
        self.used_tile_pieces.add(tile_piece.lower())

        # adding the player to the list of players
        self.players.append(Player(name, tile_piece))

        # TODO when the sets and lists are updated, that info should be sent to other clients
        # TODO the Player Object can be sent as a string

    def addPlayerFromString(self, player_string):
        """ Adds a player to the game from a serialized Player String"""

        player = Player()
        player.load_from_string(player_string)

        self.used_names.add(player.name.lower())
        self.used_tile_pieces.add(player.tile_piece.lower())

        # adding the player to the list of players
        self.players.append(player)

        # TODO should be called after a different client sets player info

    def turn(self, pos=None):
        """ prompts the user to make a move, then changes the current player to the next one
            :param pos is an optional parameter, should only be used when a different client made a move
            and we need to update the board for this client """
        current_player = self.players[self.current_turn]

        if pos is not None:

            while True:
                pos = input(f"{current_player.name} it is your turn, what tile do you want to play? ").strip()
                if pos.isnumeric():
                    result = self.game_board.makeMove(pos, current_player.tile_piece)

                    if result == -1:
                        print("Please input a number in the valid range")

                    elif result == -2:
                        print("Please input a cell number that is vacant")

                    else:
                        print()
                        self.game_board.printBoard()
                        break

                else:
                    print("Please input a number")

        else:
            self.game_board.makeMove(pos, current_player.tile_piece)
            print(f"{current_player.name} played their piece on tile {pos}")
            print()
            self.game_board.printBoard()

        # checking if the move is a winning move
        if self.game_board.checkHorizontalWinCase(pos) or \
                self.game_board.checkVerticalWinCase(pos) or \
                self.game_board.checkUpperRightDiagonal(pos) or \
                self.game_board.checkUpperLeftDiagonal(pos):
            print("GG we have a winner!")
            self.gameRunning = False

        # TODO if the player wins that info should be sent to other clients
        # TODO if not then send the position that was played

        self.current_turn = (self.current_turn + 1) % len(self.players)
