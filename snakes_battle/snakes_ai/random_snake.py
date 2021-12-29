import random
from snakes_battle.snake import Snake, Direction

class RandomSnake(Snake):
    def __init__(self, borders_cells, color, name) -> None:
        super().__init__(color, name)

        # All the cells that are fill with borders. This variable will store a list of (x, y) pairs
        self.border_cells = borders_cells
    
    def change_direction(self, board_state):
        super().change_direction(random.randint(0,3))
