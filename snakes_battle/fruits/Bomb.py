from snakes_battle.fruits.BaseFruit import BaseFruit, FruitKind

class Bomb(BaseFruit):
    BOMB_CREATION_PROBABILITY = 1 / 100 # Will create a bomb roughly every 20 frames.
    BOMB_LIFESPAN = 100 # How many frames will the bomb be on the board

    def __init__(self, position) -> None:
        super().__init__(position)

        self.kind = FruitKind.BOMB
        self.lifespan = Bomb.BOMB_LIFESPAN
    
    def eaten(self, snake):
        snake.shrink(-self.kind["score"])
    
    def make_turn(self, board):
        self.lifespan -= 1
        if (self.lifespan == 0):
            board.fruit_eaten(self)
