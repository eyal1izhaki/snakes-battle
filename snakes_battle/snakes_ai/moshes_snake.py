import random
from snakes_battle.snake import Snake, Direction
from snakes_battle.fruit import FruitKind


class MoshesSnake(Snake):
    def __init__(self, borders_cells, color, name) -> None:
        super().__init__(color, name)

        self.version = 2.0
        self.border_cells = borders_cells

    def make_decision(self, board_state):
        fruits = board_state["fruits"]
        pos = self.body_position

        current_x, current_y = pos[0]
        min_dist = 10000
        closest_fruit = fruits[0]

        # choosing the closest fruit
        for fruit in fruits:
            fruit_x, fruit_y = fruit.pos

            if fruit.kind in FruitKind.harmful_fruits:
                continue
            else:
                if closest_fruit in FruitKind.harmful_fruits:
                    closest_fruit = fruit

            distance = abs(current_x - fruit_x) + abs(current_y - fruit_y)
            if (distance < min_dist):
                # and ((fruit.lifespan > distance))
                if fruit.kind['name'] != "STRAWBERRY" and fruit.kind['name'] != "DRAGON_FRUIT":
                    if fruit.lifespan > distance:
                        continue
                min_dist = distance
                closest_fruit = fruit
                if fruit.kind['name'] == "KING":
                    break

        new_direction = Direction.CONTINUE
        not_available_directions = self.check_next_step(board_state, 1)
        # not_available_directions3 = self.check_next_step(board_state, 3)
        available_directions = [Direction.DOWN,
                                Direction.UP, Direction.LEFT, Direction.RIGHT]
        available_directions = list(
            set(available_directions) - set(not_available_directions))

        if len(available_directions) == 0:
            return Direction.CONTINUE

        # First chance
        ############################    
        if current_x > closest_fruit.pos[0]:
            if self.direction == Direction.RIGHT:
                if Direction.UP in available_directions:
                    new_direction = Direction.UP
                else:
                    new_direction = Direction.DOWN
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
                    if Direction.RIGHT in available_directions:
                        new_direction = Direction.RIGHT
                    else:
                        if Direction.LEFT in available_directions:
                            new_direction = Direction.LEFT
                        else:
                            new_direction = Direction.CONTINUE
                else:
                    new_direction = Direction.DOWN

            if current_y > closest_fruit.pos[1]:
                if self.direction == Direction.DOWN:
                    if Direction.RIGHT in available_directions:
                        new_direction = Direction.RIGHT
                    else:
                        if Direction.LEFT in available_directions:
                            new_direction = Direction.LEFT
                        else:
                            new_direction = Direction.CONTINUE
                else:
                    new_direction = Direction.UP
        ############################
        
        # Second chance
        ############################
        # if current_x > closest_fruit.pos[0]:
        #     if self.direction == Direction.RIGHT:
        #         if current_x == closest_fruit.pos[0]:
        #             if current_y < closest_fruit.pos[1]:
        #                 new_direction = Direction.DOWN
        #             else:
        #                 new_direction = Direction.UP
        #         else:
        #             new_direction = Direction.RIGHT
        #     else:
        #         new_direction = Direction.LEFT

        # elif current_x < closest_fruit.pos[0]:
        #     if self.direction == Direction.LEFT:
        #         if current_x == closest_fruit.pos[0]:
        #             if current_y < closest_fruit.pos[1]:
        #                 new_direction = Direction.DOWN
        #             else:
        #                 new_direction = Direction.UP
        #         else:
        #             new_direction = Direction.LEFT
        #     else:
        #         new_direction = Direction.RIGHT

        # elif current_x == closest_fruit.pos[0]:
        #     if current_y < closest_fruit.pos[1]:

        #         if self.direction == Direction.UP:
        #             if Direction.RIGHT in available_directions:
        #                 new_direction = Direction.RIGHT
        #             else:
        #                 new_direction = Direction.LEFT
        #         else:
        #             new_direction = Direction.DOWN

        #     if current_y > closest_fruit.pos[1]:
        #         if self.direction == Direction.DOWN:
        #             if Direction.RIGHT in available_directions:
        #                 new_direction = Direction.RIGHT
        #             else:
        #                 new_direction = Direction.LEFT
        #         else:
        #             new_direction = Direction.UP

        ############################

        if new_direction in available_directions:

            return new_direction
        else:
            if Direction.CONTINUE in available_directions:
                return Direction.CONTINUE
            else:
                return random.choice(available_directions)

        return Direction.CONTINUE

    def check_next_step(self, board_state, i=1):
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
                if fruit.pos == [head_x + i, head_y]:
                    if Direction.RIGHT not in not_available_directions:
                        not_available_directions.append(Direction.RIGHT)
                elif fruit.pos == [head_x - i, head_y]:
                    if Direction.LEFT not in not_available_directions:
                        not_available_directions.append(Direction.LEFT)
                elif fruit.pos == [head_x, head_y + i]:
                    if Direction.DOWN not in not_available_directions:
                        not_available_directions.append(Direction.DOWN)
                elif fruit.pos == [head_x, head_y - i]:
                    if Direction.UP not in not_available_directions:
                        not_available_directions.append(Direction.UP)

        for snake in board_state["snakes"]:
            snake_pos = snake.body_position
            for cell in snake_pos:
                if cell == [head_x + i, head_y]:
                    if Direction.RIGHT not in not_available_directions:
                        not_available_directions.append(Direction.RIGHT)
                elif cell == [head_x - i, head_y]:
                    if Direction.LEFT not in not_available_directions:
                        not_available_directions.append(Direction.LEFT)
                elif cell == [head_x, head_y + i]:
                    if Direction.DOWN not in not_available_directions:
                        not_available_directions.append(Direction.DOWN)
                elif cell == [head_x, head_y - i]:
                    if Direction.UP not in not_available_directions:
                        not_available_directions.append(Direction.UP)

            # if snake_pos[0] == self.body_position[0]:
            #     for cell in snake_pos:
            #         if cell == [head_x + i + 1, head_y]:
            #             if Direction.RIGHT not in not_available_directions:
            #                 not_available_directions.append(Direction.RIGHT)
            #         elif cell == [head_x - i - 1, head_y]:
            #             if Direction.LEFT not in not_available_directions:
            #                 not_available_directions.append(Direction.LEFT)
            #         elif cell == [head_x, head_y + i + 1]:
            #             if Direction.DOWN not in not_available_directions:
            #                 not_available_directions.append(Direction.DOWN)
            #         elif cell == [head_x, head_y - i -1]:
            #             if Direction.UP not in not_available_directions:
            #                 not_available_directions.append(Direction.UP)


        for cell in self.border_cells:
            if head_x + i >= 39:
                if Direction.RIGHT not in not_available_directions:
                    not_available_directions.append(Direction.RIGHT)
            elif head_x - i <= 0:
                if Direction.LEFT not in not_available_directions:
                    not_available_directions.append(Direction.LEFT)
            elif head_y + i >= 35:
                if Direction.DOWN not in not_available_directions:
                    not_available_directions.append(Direction.DOWN)
            elif head_y - i <= 0:
                if Direction.UP not in not_available_directions:
                    not_available_directions.append(Direction.UP)

        return not_available_directions
