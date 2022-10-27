from snakes_battle.snake import Snake, Direction
import random

class RandomSnake(Snake):
    def __init__(self, borders_cells, color, name) -> None:
        super().__init__(color, name)

        self.version = 1.0
        self.border_cells = borders_cells

        self.my_direction = self.direction
        self.counter = 1


    def make_decision(self, board_state):

        self.counter += 1
        
        if self.counter % 3 == 0: # Changes direction every three frames
            self.my_direction = random.randint(0,3)
            self.counter = 1
        
        return self.my_direction