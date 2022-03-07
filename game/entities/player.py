import json

from engine import entity


# if we want different types of characters in our game we can use this
player_specs = {}


class PlayerType:
    def __init__(self, path):
        """Creates new playertype object - stores data on different characters"""
        self.path = path
        # load the data from the json
        # format.txt in assets/playertypes/


class Player(entity.Entity):
    def __init__(self, x, y, w, h):
        """Player object"""
        super().__init__()


def load_player_spec(path):
    """Loads player specs from json file"""
    PlayerType(path)


def create_player(player_type: str):
    """Creates a new player from playertype string"""
    return Player()


