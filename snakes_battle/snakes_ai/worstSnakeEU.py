import sys

from snakes_battle.snake import Snake, Direction
import random


class WorstSnakeEU(Snake):
    def __init__(self, borders_cells, color, name) -> None:
        super().__init__(color, name)

        self.version = 1.0
        self.border_cells = borders_cells
        self.my_direction = self.direction

    def make_decision(self, board_state):
        snakes = board_state["snakes"]
        fruits = board_state["fruits"]

        for snake in snakes:
            temp = vars(snake)
            print(', '.join("%s: %s" % item for item in temp.items()))
        sys.exit(0)



        return self.my_direction
