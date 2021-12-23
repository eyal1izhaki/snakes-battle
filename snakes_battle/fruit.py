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
        "color": (236, 20, 34),
        "image": "snakes_battle\\images\\fruits\\shield.png",
        "creation_probability": 1/500, # Will create a bomb roughly every 20 frames.
        "lifespan": 30, # How many frames will the bomb be on the board
    }
    
    beneficial_fruits = [STRAWBERRY, DRAGON_FRUIT]
    harmful_fruits = [BOMB]
    special_fruits = [SHIELD]
    fruits = beneficial_fruits + harmful_fruits + special_fruits


class Fruit:
    def __init__(self, fruitKind, position) -> None:
        self.kind = fruitKind
        self.pos = position
        self.lifespan = fruitKind["lifespan"]