class FruitKind:
    STRAWBERRY = {
        "name": "STRAWBERRY",
        "color": (255, 62, 97),
        "image": "snakes_battle\\images\\fruits\\strawberry.png",
        "score": 1,
        "lifespan": -1
        }

    DRAGON_FRUIT = {
        "name": "DRAGON_FRUIT",
        "color": (145, 67, 114),
        "image": "snakes_battle\\images\\fruits\\dragonfruit.png",
        "score": 2,
        "lifespan": -1
    }
    BOMB = {
        "name": "BOMB",
        "color": (114, 114, 114),
        "image": "snakes_battle\\images\\fruits\\bomb.png",
        "score": -2,
        "creation_probability": 1/100, # Will create a bomb roughly every 20 frames.
        "lifespan": 80, # How many frames will the bomb be on the board
    }
    SHIELD = {
        "name": "SHIELD",
        "color": (68, 79, 231),
        "image": "snakes_battle\\images\\fruits\\shield.png",
        "creation_probability": 1/500, # Will create a bomb roughly every 20 frames.
        "lifespan": 30, # How many frames will the bomb be on the board
    }
    
    SKULL = {
        "name": "SKULL",
        "color": (38, 38, 38),
        "image": "snakes_battle\\images\\fruits\\skull.png",
        "creation_probability": 1/600, # Will create a bomb roughly every 20 frames.
        "lifespan": 15, # How many frames will the bomb be on the board
    }
    KING = {
        "name": "KING",
        "color": (254, 212, 2),
        "image": "snakes_battle\\images\\fruits\\king.png",
        "creation_probability": 1/600, # Will create a bomb roughly every 20 frames.
        "lifespan": 30, # How many frames will the bomb be on the board
    }
    KNIFE = {
        "name": "KNIFE",
        "color": (255, 107, 107),
        "image": "snakes_battle\\images\\fruits\\knife.png",
        "creation_probability": 1/600, # Will create a bomb roughly every 20 frames.
        "lifespan": 30, # How many frames will the bomb be on the board
    }

    beneficial_fruits = [STRAWBERRY, DRAGON_FRUIT]
    harmful_fruits = [BOMB, SKULL]
    special_fruits = [SHIELD, KING, KNIFE]
    fruits = beneficial_fruits + harmful_fruits + special_fruits


class Fruit:
    def __init__(self, fruitKind, position) -> None:
        self.kind = fruitKind
        self.pos = position
        self.lifespan = fruitKind["lifespan"]