
class FruitKind:
    STRAWBERRY = {
        "name": "STRAWBERRY",
        "color": (222, 84, 72),
        "image": "",
        "score": 1
        }
    DRAGON_FRUIT = {
        "name": "DRAGON_FRUIT",
        "color": (90, 90, 90),
        "image": "",
        "score": 2
        }
    BOMB = {
        "name": "BOMB",
        "color": (20, 20, 20),
        "image": "",
        "score":  -2
        }
    EMPTY = { # A fruit type that does nothing. Just the default one before overriding.
        "name": "EMPTY",
        "color": (144, 144, 144),
        "image": "",
        "score": 0
        }

# Just a base class to be inherited - will not really be used.
class BaseFruit:
    def __init__(self, position) -> None:
        self.pos = position
        self.kind = FruitKind.EMPTY
    
    def eaten(self, snake):
        pass

    def grow_snake_length(self, snake):
        for _ in range(self.kind["score"]):
            snake._grow_in_one_unit()

    def make_turn(self, board):
        pass
