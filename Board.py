class Board:
    def __init__(self, board_size=3):
        self.default_piece = 0
        self.board_size = board_size
        self.board = None
        self.clearBoard()

    def clearBoard(self):
        """ When called will reset the board to a 3x3 """
        self.board = [[self.default_piece] * self.board_size for _ in range(self.board_size)]

        # TODO if called tell the other clients

    def cellNumberToArrayCoords(self, cellNumber):
        return cellNumber // self.board_size, cellNumber % self.board_size

    def makeMove(self, cell, tile_piece):
        """ When called it will attempt to make a move on a certain tile
            if the position is out of bounds or taken already will return a negative number """

        xPos, yPos = self.cellNumberToArrayCoords(cell)

        if xPos < 0 or xPos >= self.board_size or yPos < 0 or yPos >= self.board_size:
            return -1

        if self.board[xPos][yPos] != self.default_piece:
            return -2

        self.board[xPos][yPos] = tile_piece
        return 1

    def checkUpperLeftDiagonal(self, pos):
        """ When called will check if a player has won on the upper left bottom right diagonal
            :param pos the position of the tile played
            :returns Boolean """

        xPos, yPos = pos

        # checking if the tile played was even a diagonal
        if xPos != yPos:
            return False

        upper_left_corner = self.board[0][0]
        if upper_left_corner == self.default_piece:
            return False

        for i in range(1, self.board_size):
            if self.board[i][i] != upper_left_corner:
                return False

        return True

    def checkUpperRightDiagonal(self, pos):
        """ When called will check if a player has won on the upper left bottom right diagonal
            :param pos the position of the tile played
            :returns Boolean """

        xPos, _ = pos

        # checking if the tile played was even a diagonal
        if xPos != self.board_size - xPos - 1:
            return False

        upper_right_corner = self.board[0][self.board_size - 1]
        if upper_right_corner == self.default_piece:
            return False

        for i in range(1, self.board_size):
            if self.board[i][self.board_size - i - 1] != upper_right_corner:
                return False

        return True

    def checkHorizontalWinCase(self, pos):
        """ When called will check if a player has won on the horizontal
            :param pos the position of the tile played
            :return Boolean """

        _, yPos = pos

        top_of_horizontal = self.board[0][yPos]
        for i in range(1, self.board_size):
            if self.board[i][yPos] != top_of_horizontal:
                return False

        return True

    def checkVerticalWinCase(self, pos):
        """ When call will check if a player has won on the vertical
            :param pos the position of the tile played
            :return Boolean """

        xPos, _ = pos

        leftmost_of_vertical = self.board[xPos][0]
        for i in range(1, self.board_size):
            if self.board[xPos][i] != leftmost_of_vertical:
                return False

        return True

    def printBoard(self):
        """ Prints the board"""
        # example
        #    | O |
        # ---+---+---
        #  O | X |
        # ---+---+---
        #    | X | O

        print(self.__str__())

        # example
        #  1 | O | 3
        # ---+---+---
        #  O | X | 6
        # ---+---+---
        #  7 | X | O
        print(self.__str__(withCellNumbers=True))

    def __str__(self, withCellNumbers=False):
        """ Converts the board into a printable string
            :param withCellNumbers True if the cell numbers should be displayed in empty cells"""

        i = 0
        row_divider = "---" + "+---" * (self.board_size - 1)
        base = []
        for row_index, row in enumerate(self.board, 1):
            row_string = ""
            for tile_index, tile in enumerate(row, 1):
                cell_content = str(i if withCellNumbers and self.default_piece == tile else tile)
                if tile_index != self.board_size:
                    row_string += " " + cell_content + " |"
                else:
                    row_string += " " + cell_content + " "
                i += 1
            base.append(row_string)
            if row_index != self.board_size:
                base.append(row_divider)

        return '\n'.join(base)