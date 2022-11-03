import random
from snakes_battle.snake import Snake, Direction
from snakes_battle.fruit import FruitKind


class MoshesSnake(Snake):
    def __init__(self, borders_cells, color, name) -> None:
        super().__init__(color, name)

        self.version = 1.0
        self.border_cells = borders_cells

    def make_decision(self, board_state):
        fruits = board_state["fruits"]
        pos = self.body_position

        current_x, current_y = pos[0]
        min_dist = 10000
        closest_fruit = fruits[0]

        # choosing the closest fruit
        for fruit in fruits:
            fruit_x = fruit.pos[0]
            fruit_y = fruit.pos[1]

            distance = abs(current_x - fruit_x) + abs(current_y - fruit_y)
            if (distance < min_dist) and (fruit.lifespan > distance) and (fruit.kind not in FruitKind.harmful_fruits):
                min_dist = distance
                closest_fruit = fruit
                if fruit.kind['name'] == "KING":
                    break

        # print(closest_fruit.kind, distance)

        new_direction = Direction.CONTINUE
        not_available_directions = self.check_next_step(board_state)
        available_directions = [Direction.DOWN,
                                Direction.UP, Direction.LEFT, Direction.RIGHT]
        available_directions = list(
            set(available_directions) - set(not_available_directions))

        # print("available: ", available_directions)

        # if x of the snake's head > x of the fruit
        if current_x > closest_fruit.pos[0]:
            if self.direction == Direction.RIGHT:
                if Direction.UP in available_directions:
                    new_direction = Direction.UP
                else:
                    new_direction = Direction.CONTINUE
            else:
                new_direction = Direction.LEFT

        elif current_x < closest_fruit.pos[0]:
            if self.direction == Direction.LEFT:
                if Direction.UP in available_directions:
                    new_direction = Direction.UP
                else:
                    new_direction = Direction.CONTINUE
            else:
                new_direction = Direction.RIGHT

        elif current_x == closest_fruit.pos[0]:

            if current_y < closest_fruit.pos[1]:
                if self.direction == Direction.UP:
                    new_direction = Direction.RIGHT
                else:
                    new_direction = Direction.DOWN

            if current_y > closest_fruit.pos[1]:
                if self.direction == Direction.DOWN:
                    new_direction = Direction.RIGHT
                else:
                    new_direction = Direction.UP

        if len(available_directions) == 0:
            return Direction.CONTINUE
            
        if new_direction in available_directions:
            return new_direction
        else:
            if Direction.CONTINUE in available_directions:
                return Direction.CONTINUE
            else:
                return random.choice(available_directions)

        return Direction.CONTINUE

    def check_next_step(self, board_state):
        not_available_directions = []
        head_x, head_y = self.body_position[0]

        if self.direction == Direction.UP:
            not_available_directions.append(Direction.DOWN)
        elif self.direction == Direction.DOWN:
            not_available_directions.append(Direction.UP)
        elif self.direction == Direction.RIGHT:
            not_available_directions.append(Direction.LEFT)
        elif self.direction == Direction.LEFT:
            not_available_directions.append(Direction.RIGHT)

        for fruit in board_state["fruits"]:
            if fruit.kind in FruitKind.harmful_fruits:
                # print("Fruit pos",fruit.pos)
                if fruit.pos == [head_x + 1, head_y]:
                    if Direction.RIGHT not in not_available_directions:
                        not_available_directions.append(Direction.RIGHT)
                elif fruit.pos == [head_x - 1, head_y]:
                    if Direction.LEFT not in not_available_directions:
                        not_available_directions.append(Direction.LEFT)
                elif fruit.pos == [head_x, head_y + 1]:
                    if Direction.DOWN not in not_available_directions:
                        not_available_directions.append(Direction.DOWN)
                elif fruit.pos == [head_x, head_y - 1]:
                    if Direction.UP not in not_available_directions:
                        not_available_directions.append(Direction.UP)

        for snake in board_state["snakes"]:
            snake_pos = snake.body_position
            for cell in snake_pos:
                # print("cell",cell)
                if cell == [head_x + 1, head_y]:
                    if Direction.RIGHT not in not_available_directions:
                        not_available_directions.append(Direction.RIGHT)
                elif cell == [head_x - 1, head_y]:
                    if Direction.LEFT not in not_available_directions:
                        not_available_directions.append(Direction.LEFT)
                elif cell == [head_x, head_y + 1]:
                    if Direction.DOWN not in not_available_directions:
                        not_available_directions.append(Direction.DOWN)
                elif cell == [head_x, head_y - 1]:
                    if Direction.UP not in not_available_directions:
                        not_available_directions.append(Direction.UP)

        # print("border cells",self.border_cells)

        for cell in self.border_cells:
            if cell[0] == 0 or cell[0] == 39 or cell[1] == 0 or cell[1] == 35:
                if cell == (head_x + 1, head_y):
                    if Direction.RIGHT not in not_available_directions:
                        not_available_directions.append(Direction.RIGHT)
                elif cell == (head_x - 1, head_y):
                    if Direction.LEFT not in not_available_directions:
                        not_available_directions.append(Direction.LEFT)
                elif cell == (head_x, head_y + 1):
                    if Direction.DOWN not in not_available_directions:
                        not_available_directions.append(Direction.DOWN)
                elif cell == (head_x, head_y - 1):
                    if Direction.UP not in not_available_directions:
                        not_available_directions.append(Direction.UP)

        return not_available_directions
