import sys
import numpy as np
from snakes_battle.snake import Snake, Direction
from scipy.spatial.distance import cityblock
from snakes_battle.board import Board
from snakes_battle.graphics import GameGraphics
from snakes_battle.snakes_ai.manual_control_snake import ManualSnake
from snakes_battle.snakes_ai.manual_control_snake_wasd import ManualSnakeWASD
from snakes_battle.snakes_ai.random_snake import RandomSnake
from snakes_battle.snakes_ai.simple_snake import SimpleSnake


class SnakySnake(Snake):
    def __init__(self, borders_cells, color, name) -> None:
        super().__init__(color, name)

        self.version = 1.0
        self.border_cells = borders_cells

    def make_decision(self, board_state):
        temp_ai_classes_available = [
            {"class": SnakySnake, "should_play": False}
        ]
        graphics = GameGraphics(temp_ai_classes_available)
        my_board = Board(graphics.board_size)
        boarder_cells_as_tuples = my_board.get_border_cells()
        boarder_cells_as_2D_list = [list(ele) for ele in boarder_cells_as_tuples]

        pos = self.body_position
        fruits = board_state["fruits"]
        nearest_good_fruit_pos = None
        city_block_dis_list = []
        good_fruits_pos = []
        bad_fruits_pos = []
        for fruit in fruits:
            print(fruit.pos, fruit.kind["name"])
            if fruit.kind["name"] is "BOMB" or fruit.kind["name"] is "SKULL":
                bad_fruits_pos.append(fruit.pos)
            else:
                city_block_dis_list.append(cityblock(pos[0], fruit.pos))
                good_fruits_pos.append(fruit.pos)

        for border_cell in boarder_cells_as_2D_list:
            bad_fruits_pos.append(border_cell)
        # print(bad_fruits_pos)
        # print(boarder_cells_as_2D_list)
        min_index = np.argmin(city_block_dis_list)
        nearest_good_fruit_pos = good_fruits_pos[min_index]
        # print(nearest_good_fruit_pos)
        # print("head at:", pos[0])
        for bad_fruit in bad_fruits_pos:
            if self.direction == Direction.RIGHT:

                if pos[0][0]+1 == bad_fruit[0] and pos[0][1] == bad_fruit[1]:
                    print("1", bad_fruit)
                    if pos[0][0] < 5:
                        return Direction.UP
                    else:
                        return Direction.DOWN
            if self.direction == Direction.LEFT:
                if pos[0][0] - 1 == bad_fruit[0] and pos[0][1] == bad_fruit[1]:
                    print("2", bad_fruit)
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
                    print("4", bad_fruit)
                    if pos[0][1] < 5:
                        return Direction.RIGHT
                    else:
                        return Direction.LEFT

        if pos[0][0] > nearest_good_fruit_pos[0]:
            if self._direction == Direction.RIGHT:
                for bad_fruit in bad_fruits_pos:
                    if pos[0][0] == bad_fruit[0] and pos[0][1] + 1 == bad_fruit[1]:
                        return Direction.DOWN
                return Direction.UP
            else:
                return Direction.LEFT

        if pos[0][0] < nearest_good_fruit_pos[0]:
            if self._direction == Direction.LEFT:
                for bad_fruit in bad_fruits_pos:
                    if pos[0][0] == bad_fruit[0] and pos[0][1] + 1 == bad_fruit[1]:
                        return Direction.DOWN
                return Direction.UP
            else:
                return Direction.RIGHT

        if pos[0][0] == nearest_good_fruit_pos[0]:
            if pos[0][1] < nearest_good_fruit_pos[1]:
                if self._direction == Direction.UP:
                    for bad_fruit in bad_fruits_pos:
                        if pos[0][0] + 1 == bad_fruit[0] and pos[0][1] == bad_fruit[1]:
                            return Direction.LEFT
                    return Direction.RIGHT
                else:
                    return Direction.DOWN

            if pos[0][1] > nearest_good_fruit_pos[1]:
                if self._direction == Direction.DOWN:
                    for bad_fruit in bad_fruits_pos:
                        if pos[0][0] + 1 == bad_fruit[0] and pos[0][1] + 1 == bad_fruit[1]:
                            return Direction.DOWN
                    return Direction.RIGHT
                else:
                    return Direction.UP

        return Direction.CONTINUE
