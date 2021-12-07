from snakes_battle.fruits.BaseFruit import BaseFruit, FruitKind

class DragonFruit(BaseFruit):
    def __init__(self, position) -> None:
        super().__init__(position)

        self.kind = FruitKind.DRAGON_FRUIT
    
    def eaten(self, snake):
        for _ in range(self.kind["score"]):
            self.grow_snake_length(snake)
