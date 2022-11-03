from snakes_battle.snake import Snake, Direction
from snakes_battle.fruit import FruitKind


class YoavSnake(Snake):
    def __init__(self, borders_cells, color, name) -> None:
        super().__init__(color, name)

        self.version = 1.0
        self.border_cells = borders_cells
        self.directions = [0, -1], [0, 1], [1, 0], [-1, 0]

    def is_harmful(self, fruits, dir):
        x, y = dir
        head = self.body_position[0]
        for fruit in fruits:
            if fruit.kind in FruitKind.harmful_fruits:
                if fruit.pos[0] == head[0] + x and fruit.pos[1] == head[1] + y:
                    return True
        return False

    def is_snake(self, snakes, dir):
        x, y = dir
        head = self.body_position[0]
        for snake in snakes:
            curr_snake = snake.body_position
            for body_part in curr_snake:
                if body_part[0] == head[0] + x and body_part[1] == head[1] + y:
                    return True
        return False

    def is_border(self, dir):
        x_head = self.body_position[0][0]
        y_head = self.body_position[0][1]
        x, y = dir
        my_head = (x_head + x, y_head + y)
        if my_head in self.border_cells:
            return True
        return False

    def get_next_fruit(self, fruits):
        for idx, fruit in enumerate(fruits):
            if fruit.kind in FruitKind.harmful_fruits:
                continue
            elif fruit.kind in FruitKind.special_fruits:
                return fruit
            elif fruits[idx+1].kind in FruitKind.special_fruits:
                return fruits[idx+1]
            else:
                return fruit

    def do_this_move(self, snakes):
        up, down, right, left = self.directions
        if (not self.is_snake(snakes, up) and not self.is_border(up)):
            return Direction.UP
        if (not self.is_snake(snakes, down) and not self.is_border(down)):
            return Direction.DOWN
        if (not self.is_snake(snakes, right) and not self.is_border(right)):
            return Direction.RIGHT
        if (not self.is_snake(snakes, left) and not self.is_border(left)):
            return Direction.LEFT
        return Direction.CONTINUE

    def no_problem_found(self, board_state, cmd):
        fruits = board_state["fruits"]
        snakes = board_state["snakes"]
        if (self.is_harmful(fruits, cmd) or self.is_snake(snakes, cmd) or self.is_border(cmd)):
            return False
        return True

    def make_decision(self, board_state):
        up, down, right, left = self.directions
        fruits = board_state["fruits"]
        snakes = board_state["snakes"]
        fruit = self.get_next_fruit(fruits)
        pos = self.body_position

        if pos[0][0] > fruit.pos[0]:
            if self.direction == Direction.RIGHT:
                if (self.no_problem_found(board_state, up)):
                    return Direction.UP
                elif (self.no_problem_found(board_state, down)):
                    return Direction.DOWN
            else:
                if (self.no_problem_found(board_state, left)):
                    return Direction.LEFT

        if pos[0][0] < fruit.pos[0]:
            if self.direction == Direction.LEFT:
                if (self.no_problem_found(board_state, up)):
                    return Direction.UP
                elif (self.no_problem_found(board_state, down)):
                    return Direction.DOWN
            else:
                if (self.no_problem_found(board_state, right)):
                    return Direction.RIGHT

        if pos[0][0] == fruit.pos[0]:

            if pos[0][1] < fruit.pos[1]:
                if self.direction == Direction.UP:
                    if (self.no_problem_found(board_state, right)):
                        return Direction.RIGHT
                    elif (self.no_problem_found(board_state, left)):
                        return Direction.LEFT
                else:
                    if (self.no_problem_found(board_state, down)):
                        return Direction.DOWN

            if pos[0][1] > fruit.pos[1]:
                if self.direction == Direction.DOWN:
                    if (self.no_problem_found(board_state, right)):
                        return Direction.RIGHT
                    elif (self.no_problem_found(board_state, left)):
                        return Direction.LEFT
                else:
                    if (self.no_problem_found(board_state, up)):
                        return Direction.UP

        return self.do_this_move(snakes)
