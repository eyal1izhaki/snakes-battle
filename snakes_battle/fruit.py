class FruitKind:

    # creation_probability: The probability that the fruit will be created on the board every frame.
    # lifespan: How many frames will the bomb be on the board

    STRAWBERRY = {
        "name": "STRAWBERRY",
        "color": (255, 62, 97),
        "image": "snakes_battle/images/fruits/strawberry.png",
        "score": 1,
        "lifespan": -1
    }

    DRAGON_FRUIT = {
        "name": "DRAGON_FRUIT",
        "color": (145, 67, 114),
        "image": "snakes_battle/images/fruits/dragonfruit.png",
        "score": 2,
        "lifespan": -1
    }
    BOMB = {
        "name": "BOMB",
        "color": (114, 114, 114),
        "image": "snakes_battle/images/fruits/bomb.png",
        "score": -2,
        "creation_probability": 1/50,
        "lifespan": 80,
    }
    SHIELD = {
        "name": "SHIELD",
        "color": (68, 79, 231),
        "image": "snakes_battle/images/fruits/shield.png",
        "creation_probability": 1/80,
        "lifespan": 50,
    }

    SKULL = {
        "name": "SKULL",
        "color": (38, 38, 38),
        "image": "snakes_battle/images/fruits/skull.png",
        "creation_probability": 1/200,
        "lifespan": 30,
    }
    KING = {
        "name": "KING",
        "color": (254, 212, 2),
        "image": "snakes_battle/images/fruits/king.png",
        "creation_probability": 1/200,
        "lifespan": 50,
        "effection_duration": 30,
        "fruits_score": 1
    }
    KNIFE = {
        "name": "KNIFE",
        "color": (255, 107, 107),
        "image": "snakes_battle/images/fruits/knife.png",
        "creation_probability": 1/100,
        "lifespan": 40,
    }

    beneficial_fruits = [STRAWBERRY, DRAGON_FRUIT]
    harmful_fruits = [BOMB, SKULL]
    special_fruits = [SHIELD, KING, KNIFE]
    randomly_created = [BOMB, SKULL, SHIELD, KING, KNIFE]
    fruits = beneficial_fruits + harmful_fruits + special_fruits


class Fruit:
    def __init__(self, fruit_kind, position) -> None:
        self.kind = fruit_kind
        self.pos = position
        self.lifespan = fruit_kind["lifespan"]
