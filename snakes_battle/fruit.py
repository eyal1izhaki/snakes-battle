
# class FruitKind:
#     STRAWBERRY = 0

class Fruit:
    def __init__(self, position) -> None:
        self.pos = position
        self.value = 1
        self.color = (222, 84, 72)
        # self.kind = FruitKind.STRAWBERRY