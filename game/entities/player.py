import json

from engine import entity, filehandler, animation


# if we want different types of characters in our game we can use this
player_specs = {}


class PlayerType:
    def __init__(self, path):
        """Creates new playertype object - stores data on different characters"""
        self.path = path
        # load the data from the json
        # format.txt in assets/playertypes/
        self.animations = {}
        with open(path, 'r') as file:
            data = json.load(file)
            file.close()
        self.name = data["name"]
        self.health = data["stats"]["health"]
        self.speed = data["stats"]["speed"]
        self.strength = data["stats"]["strength"]
        # load animations
        for ani in data["animation"]:
            self.animations[ani] = animation.AnimationData(data["animation"][ani]["frames"], 
                        data["animation"][ani]["size"], data["animation"][ani]["frame_time"])


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


