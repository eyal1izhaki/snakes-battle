class FruitKind:
    STRAWBERRY = {
        "name": "STRAWBERRY",
        "color": (255, 62, 97),
        "image": "snakes_battle\\images\\fruits\\strawberry.png",
        "score": 1,
        }

    DRAGON_FRUIT = {
        "name": "DRAGON_FRUIT",
        "color": (145, 67, 114),
        "image": "snakes_battle\\images\\fruits\\dragonfruit.png",
        "score": 2,
    }
    BOMB = {
        "name": "BOMB",
        "color": (114, 114, 114),
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
