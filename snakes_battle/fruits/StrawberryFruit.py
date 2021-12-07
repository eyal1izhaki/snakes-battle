from snakes_battle.fruits.BaseFruit import BaseFruit, FruitKind

class StrawberryFruit(BaseFruit):
    def __init__(self, position) -> None:
        super().__init__(position)

        self.kind = FruitKind.STRAWBERRY
    
    def eaten(self, snake):
        self.grow_snake_length(snake)
