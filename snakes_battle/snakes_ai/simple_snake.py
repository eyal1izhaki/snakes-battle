

from snakes_battle.snake import Snake, Direction


class SimpleSnake(Snake):
    def __init__(self, borders_cells, color, name) -> None:
        super().__init__(color, name)

        self.version = 1.0
        self.border_cells = borders_cells

    def make_decision(self, board_state):
        
        fruits = board_state["fruits"]
        snakes = board_state["snakes"]
        pos = self.body_position
        if pos[0][0] > fruits[0].pos[0]:
            if self.direction == Direction.RIGHT:
                return Direction.UP
            else:
                return Direction.LEFT

        if pos[0][0] < fruits[0].pos[0]:
            if self.direction == Direction.LEFT:
                return Direction.UP
            else:
                return Direction.RIGHT

        if pos[0][0] == fruits[0].pos[0]:

            if pos[0][1] < fruits[0].pos[1]:
                if self.direction == Direction.UP:
                    return Direction.RIGHT
                else:
                    return Direction.DOWN

            if pos[0][1] > fruits[0].pos[1]:
                if self.direction == Direction.DOWN:
                    return Direction.RIGHT
                else:
                    return Direction.UP

        return Direction.CONTINUE
