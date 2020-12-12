class Player:
    def __init__(self, name="", tile_piece=""):
        self.name = name
        self.tile_piece = tile_piece

        # maybe add the client address here to save it?

    def load_from_string(self, player_string):
        """ Unpacks a serialized Player object and
        saves it as the current instance's player """
        player_info = player_string.split(",")

        if player_info != len(2):
            return False

        self.name = player_info[0]
        self.tile_piece = player_info[1]

        return True

    def __str__(self):
        """ Converts the player into a string useful when
         sending player information to all other clients """

        return f"{self.name},{self.tile_piece}"
