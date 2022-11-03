import random
import sys
import numpy as np
from snakes_battle.snake import Snake, Direction
from scipy.spatial.distance import cityblock



class SnakySnake(Snake):
    def __init__(self, borders_cells, color, name) -> None:
        super().__init__(color, name)

        self.version = 1.0
        self.border_cells = borders_cells

    def make_decision(self, board_state):

        boarder_cell_list = [list(elem) for elem in self.border_cells]
        snakes = board_state["snakes"]
        fruits = board_state["fruits"]
        skull_pos = [-11, -11]
        for fruit in fruits:
            if fruit.kind['name'] == 'SKULL':
                skull_pos[0] = fruit.pos[0]
                skull_pos[1] = fruit.pos[1]
        ally_head = self.head
        head_x = ally_head[0]
        head_y = ally_head[1]
        available_directions = [Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT]
        # make sure not to do full turn since snake will collide
        if self.direction == Direction.UP:
            available_directions.remove(Direction.DOWN)
        elif self.direction == Direction.DOWN:
            available_directions.remove(Direction.UP)
        elif self.direction == Direction.LEFT:
            available_directions.remove(Direction.RIGHT)
        elif self.direction == Direction.RIGHT:
            available_directions.remove(Direction.LEFT)

        if ([head_x, head_y - 1] in boarder_cell_list) or (head_x == skull_pos[0] and head_y - 1 == skull_pos[1]):
            if Direction.UP in available_directions:
                available_directions.remove(Direction.UP)
        # right
        if [head_x + 1, head_y] in boarder_cell_list or (head_x + 1 == skull_pos[0] and head_y == skull_pos[1]):
            if Direction.RIGHT in available_directions:
                available_directions.remove(Direction.RIGHT)
        # bottom
        if [head_x, head_y + 1] in boarder_cell_list or (head_x == skull_pos[0] and head_y + 1 == skull_pos[1]):
            if Direction.DOWN in available_directions:
                available_directions.remove(Direction.DOWN)
        # left
        if [head_x - 1, head_y] in boarder_cell_list or (head_x - 1 == skull_pos[0] and head_y == skull_pos[1]):
            if Direction.LEFT in available_directions:
                available_directions.remove(Direction.LEFT)
        # first iteration of not to collide with other snakes
        for snake in snakes:
            # todo attack if have knife, crown, only I have shield or both no shields but I have bigger length

            # avoid insta-losing decisions (snakes collision)
            for snake_pos in snake.body_position:
                if snake_pos[0] == head_x and snake_pos[1] == head_y:
                    continue
                if head_x - 1 == snake_pos[0] and head_y == snake_pos[1]:
                    if Direction.LEFT in available_directions:
                        available_directions.remove(Direction.LEFT)
                if head_x + 1 == snake_pos[0] and head_y == snake_pos[1]:
                    if Direction.RIGHT in available_directions:
                        available_directions.remove(Direction.RIGHT)
                if head_x == snake_pos[0] and head_y - 1 == snake_pos[1]:
                    if Direction.UP in available_directions:
                        available_directions.remove(Direction.UP)
                if head_x == snake_pos[0] and head_y + 1 == snake_pos[1]:
                    if Direction.DOWN in available_directions:
                        available_directions.remove(Direction.DOWN)

        pos = self.body_position
        fruits = board_state["fruits"]
        nearest_good_fruit_pos = None
        city_block_dis_list = []
        beneficial_fruits_pos = []
        bad_fruits_pos = []
        for fruit in fruits:
            # print(fruit.pos, fruit.kind["name"])
            if fruit.kind["name"] == "BOMB":
                bad_fruits_pos.append(fruit.pos)
            elif fruit.kind["name"] in ["STRAWBERRY", "DRAGON_FRUIT"]:
                city_block_dis_list.append(cityblock(ally_head, fruit.pos))
                beneficial_fruits_pos.append(fruit.pos)

        for border_cell in boarder_cell_list:
            bad_fruits_pos.append(border_cell)
        # print(bad_fruits_pos)
        # print(boarder_cells_as_2D_list)
        min_index = np.argmin(city_block_dis_list)
        nearest_good_fruit_pos = beneficial_fruits_pos[min_index]
        # print(nearest_good_fruit_pos)
        # print("head at:", pos[0])
        for bad_fruit in bad_fruits_pos:
            if self.direction == Direction.RIGHT:

                if pos[0][0]+1 == bad_fruit[0] and pos[0][1] == bad_fruit[1]:
                    # print("1", bad_fruit)
                    if pos[0][0] < 5:
                        return Direction.UP
                    else:
                        return Direction.DOWN
            if self.direction == Direction.LEFT:
                if pos[0][0] - 1 == bad_fruit[0] and pos[0][1] == bad_fruit[1]:
                    # print("2", bad_fruit)
                    if pos[0][0] < 5:
                        return Direction.UP
                    else:
                        return Direction.DOWN
            if self.direction == Direction.UP:
                if pos[0][0] == bad_fruit[0] and pos[0][1] + 1 == bad_fruit[1]:
                    print("3", bad_fruit)
                    if pos[0][1] < 5:
                        return Direction.RIGHT
                    else:
                        return Direction.LEFT
            if self.direction == Direction.DOWN:
                if pos[0][0] == bad_fruit[0] and pos[0][1] - 1 == bad_fruit[1]:
                    # print("4", bad_fruit)
                    if pos[0][1] < 5:
                        return Direction.RIGHT
                    else:
                        return Direction.LEFT

        if pos[0][0] > nearest_good_fruit_pos[0]:
            if self._direction == Direction.RIGHT:
                for bad_fruit in bad_fruits_pos:
                    if pos[0][0] == bad_fruit[0] and pos[0][1] + 1 == bad_fruit[1]:
                        if Direction.DOWN in available_directions:
                            return Direction.DOWN
                if Direction.UP in available_directions:
                    return Direction.UP
            elif Direction.LEFT in available_directions:
                return Direction.LEFT

        if pos[0][0] < nearest_good_fruit_pos[0]:
            if self._direction == Direction.LEFT:
                for bad_fruit in bad_fruits_pos:
                    if pos[0][0] == bad_fruit[0] and pos[0][1] + 1 == bad_fruit[1]:
                        if Direction.DOWN in available_directions:
                            return Direction.DOWN
                if Direction.UP in available_directions:
                    return Direction.UP
            else:
                if Direction.RIGHT in available_directions:
                    return Direction.RIGHT

        if pos[0][0] == nearest_good_fruit_pos[0]:
            if pos[0][1] < nearest_good_fruit_pos[1]:
                if self._direction == Direction.UP:
                    for bad_fruit in bad_fruits_pos:
                        if pos[0][0] + 1 == bad_fruit[0] and pos[0][1] == bad_fruit[1]:
                            if Direction.LEFT in available_directions:
                                return Direction.LEFT
                    if Direction.RIGHT in available_directions:
                        return Direction.RIGHT
                else:
                    if Direction.DOWN in available_directions:
                        return Direction.DOWN

            if pos[0][1] > nearest_good_fruit_pos[1]:
                if self._direction == Direction.DOWN:
                    for bad_fruit in bad_fruits_pos:
                        if pos[0][0] + 1 == bad_fruit[0] and pos[0][1] + 1 == bad_fruit[1]:
                            if Direction.DOWN in available_directions:
                                return Direction.DOWN
                    if Direction.RIGHT in available_directions:
                        return Direction.RIGHT
                else:
                    if Direction.UP in available_directions:
                        return Direction.UP

        if len(available_directions) >= 1:
            return random.choice(available_directions)
        return Direction.CONTINUE
