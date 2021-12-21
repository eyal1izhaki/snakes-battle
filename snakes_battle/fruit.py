class FruitKind:
    STRAWBERRY = {
        "name": "STRAWBERRY",
        "color": (222, 84, 72),
        "image": "snakes_battle\\images\\fruits\\strawberry.png",
        "score": 1,
        }

    DRAGON_FRUIT = {
        "name": "DRAGON_FRUIT",
        "color": (90, 90, 90),
        "image": "snakes_battle\\images\\fruits\\dragonfruit.png",
        "score": 2,
    }
    BOMB = {
        "name": "BOMB",
        "color": (20, 20, 20),
        "image": "snakes_battle\\images\\fruits\\bomb.png",
        "score": -2
    }
    
    beneficial_fruits = [STRAWBERRY, DRAGON_FRUIT]
    harmful_fruits = [BOMB]
    fruits = beneficial_fruits + harmful_fruits


class Fruit:
    def __init__(self, fruitKind, position) -> None:
        self.kind = fruitKind
        self.pos = position
        self.score = fruitKind["score"]
