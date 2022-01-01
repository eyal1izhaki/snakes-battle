import random
from snakes_battle.snake import Snake, Direction

class RandomSnake(Snake):
    def __init__(self, borders_cells, color, name) -> None:
        super().__init__(color, name)
        self.init()

        # All the cells that are fill with borders. This variable will store a list of (x, y) pairs
        self.border_cells = borders_cells
        self.version = 1.0
    
    def init(self):
        # Your bot initializations will be here.
        pass


    def make_decision(self, board_state):
        super().allowed__change_direction(random.randint(0,3))
