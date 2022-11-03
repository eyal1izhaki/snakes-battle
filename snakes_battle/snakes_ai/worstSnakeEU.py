import sys

import numpy as np

from snakes_battle.snake import Snake, Direction
from scipy.spatial.distance import cityblock
import random


class WorstSnakeEU(Snake):
    def __init__(self, borders_cells, color, name) -> None:
        super().__init__(color, name)

        self.version = 1.0
        self.border_cells = borders_cells
        self.my_direction = self.direction

    def make_decision(self, board_state):
        direction_dict = {0: "RIGHT", 1: "LEFT", 2: "UP", 3: "DOWN", 4: "CONTINUE"}
        ally_head = self.head
        head_x = ally_head[0]
        head_y = ally_head[1]
        skull_pos = [-10, -10]
        snakes = board_state["snakes"]
        fruits = board_state["fruits"]
        border_cells = [list(elem) for elem in snakes[0].border_cells]
        enemy_snake_head = [-1000, -1000]
        if len(snakes) > 1:
            enemy_snake = snakes[1]
            enemy_snake_head = enemy_snake.head

        beneficial_fruits = [fruit for fruit in fruits if fruit.kind['name'] in ["STRAWBERRY", "DRAGON_FRUIT"]]
        beneficial_fruits_pos = []
        fruit_score = []
        ally_city_block_distance_to_food = []
        enemy_city_block_distance_to_food = []

        harmful_fruits = [fruit for fruit in fruits if fruit.kind['name'] == "BOMB"]
        harmful_fruits_pos = []
        special_fruits = [fruit for fruit in fruits if fruit.kind['name'] in ["SHIELD", "KING", "KNIFE"]]
        special_fruits_pos = []

        for food in beneficial_fruits:
            beneficial_fruits_pos.append(food.pos)
            # ally_city_block_distance_to_food.append(cityblock(ally_head, food.pos))
            ally_city_block_distance_to_food.append(abs(ally_head[0] - food.pos[0]) + abs(ally_head[1] - food.pos[1]))
            if len(snakes) > 1:
                enemy_city_block_distance_to_food.append(cityblock(enemy_snake_head, food.pos))
            fruit_score.append(food.kind['score'])

        for bomb in harmful_fruits:
            harmful_fruits_pos.append(bomb.pos)

        for fruit in fruits:
            if fruit.kind['name'] == 'SKULL':
                skull_pos[0] = fruit.pos[0]
                skull_pos[1] = fruit.pos[1]
        # for snake in snakes:
        #     temp = vars(snake)
        #     for item in temp.items():
        #         print(item)
        #
        # for fruit in fruits:
        #     temp = vars(fruit)
        #     print(temp)

        available_directions = [Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT]

        # make sure not to do full turn since snake will collide
        if self.my_direction == Direction.UP:
            available_directions.remove(Direction.DOWN)
        elif self.my_direction == Direction.DOWN:
            available_directions.remove(Direction.UP)
        elif self.my_direction == Direction.LEFT:
            available_directions.remove(Direction.RIGHT)
        elif self.my_direction == Direction.RIGHT:
            available_directions.remove(Direction.LEFT)

        # make sure not to collide with border cells and skull
        # top
        if ([head_x, head_y - 1] in border_cells) or (head_x == skull_pos[0] and head_y - 1 == skull_pos[1]):
            if Direction.UP in available_directions:
                available_directions.remove(Direction.UP)
        # right
        if ([head_x + 1, head_y] in border_cells) or (head_x + 1 == skull_pos[0] and head_y == skull_pos[1]):
            if Direction.RIGHT in available_directions:
                available_directions.remove(Direction.RIGHT)
        # bottom
        if ([head_x, head_y + 1] in border_cells) or (head_x == skull_pos[0] and head_y + 1 == skull_pos[1]):
            if Direction.DOWN in available_directions:
                available_directions.remove(Direction.DOWN)
        # left
        if ([head_x - 1, head_y] in border_cells) or (head_x - 1 == skull_pos[0] and head_y == skull_pos[1]):
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

        if len(available_directions) >= 1:
            # debug_text = ""
            # for i in range(len(available_directions)):
            #     debug_text += direction_dict[available_directions[i]]
            #     debug_text += ", "
            # print(debug_text)
            decision = random.choice(available_directions)

            if len(snakes) <= 1:
                # print("possible moves:", len(available_directions))
                possible_steps = [
                    [ally_head[0], ally_head[1] - 1],
                    [ally_head[0], ally_head[1] + 1],
                    [ally_head[0] + 1, ally_head[1]],
                    [ally_head[0] - 1, ally_head[1]]
                ]

                temptemp = ""
                # for i in range(len(available_directions)):
                #     temptemp += direction_dict[available_directions[i]] + ", "
                # print(temptemp)
                allay_min_index = np.argmin(ally_city_block_distance_to_food)
                ally_min_distance = ally_city_block_distance_to_food[allay_min_index]
                ally_dest = beneficial_fruits_pos[allay_min_index]
                print("dest:", ally_dest, len(available_directions))
                best_step = min([cityblock(step, ally_dest) for step in possible_steps])
                # print(ally_dest)
                if cityblock([ally_head[0], ally_head[1] - 1], ally_head) == best_step:
                    # print("1")
                    if Direction.UP in available_directions:
                        return Direction.UP
                if cityblock([ally_head[0], ally_head[1] + 1], ally_head) == best_step:
                    # print("2")
                    if Direction.DOWN in available_directions:
                        return Direction.DOWN
                if cityblock([ally_head[0] + 1, ally_head[1]], ally_head) == best_step:
                    # print("3")
                    if Direction.RIGHT in available_directions:
                        return Direction.RIGHT
                if cityblock([ally_head[0] - 1, ally_head[1]], ally_head) == best_step:
                    # print("4")
                    if Direction.LEFT in available_directions:
                        return Direction.LEFT

            else:
                ally_dest = random.choice(beneficial_fruits_pos)
                ally_min_index = np.argmin(ally_city_block_distance_to_food)
                ally_min_distance = ally_city_block_distance_to_food[ally_min_index]
                enemy_min_index = np.argmin(enemy_city_block_distance_to_food)
                enemy_min_distance = enemy_city_block_distance_to_food[enemy_min_index]
                if ally_min_index == enemy_min_index:
                    if ally_min_distance < enemy_min_distance:
                        ally_dest = beneficial_fruits_pos[ally_min_index]
                    elif ally_min_distance > enemy_min_distance:
                        ally_dest = beneficial_fruits_pos[np.argmax(enemy_city_block_distance_to_food)]
                    elif ally_min_distance == enemy_min_distance:
                        if self.length > enemy_snake.length:
                            ally_dest = beneficial_fruits_pos[ally_min_index]
                if enemy_min_distance > ally_city_block_distance_to_food[enemy_min_index]:
                    ally_dest = beneficial_fruits_pos[enemy_min_index]
                if enemy_min_index != ally_min_index and enemy_min_distance < ally_city_block_distance_to_food[
                    enemy_min_index]:
                    ally_dest = beneficial_fruits_pos[ally_min_index]

            if ally_head[0] < ally_dest[0]:
                if self.direction != Direction.LEFT:  # todo add bomb check
                    if Direction.RIGHT in available_directions:
                        return Direction.RIGHT
                if self.direction == Direction.LEFT:
                    if Direction.UP in available_directions and Direction.DOWN in available_directions:
                        if [ally_head[0], ally_head[1] - 1] in harmful_fruits_pos:
                            if Direction.DOWN in available_directions:
                                return Direction.DOWN
                        if [ally_head[0], ally_head[1] - 1] not in harmful_fruits_pos:
                            if Direction.UP in available_directions:
                                return Direction.UP
            if ally_head[1] == ally_dest[1]:
                if ally_head[0] < ally_dest[0]:
                    if self.direction != Direction.LEFT:
                        if Direction.RIGHT in available_directions:
                            return Direction.RIGHT
                        else:
                            if [ally_head[0], ally_head[1]-1] in harmful_fruits_pos:
                                if Direction.DOWN in available_directions:
                                    return Direction.DOWN
                            else:
                                if Direction.UP in available_directions:
                                    return Direction.UP
                if ally_head[0] > ally_dest[0]:
                    if self.direction != Direction.RIGHT:
                        if Direction.LEFT in available_directions:
                            return Direction.LEFT
                        else:
                            if [ally_head[0], ally_head[1]-1] in harmful_fruits_pos:
                                if Direction.DOWN in available_directions:
                                    return Direction.DOWN
                            else:
                                if Direction.UP in available_directions:
                                    return Direction.UP

            if ally_head[0] > ally_dest[0]:
                if self.direction != Direction.RIGHT:  # todo add bomb check
                    if Direction.LEFT in available_directions:
                        return Direction.LEFT
                if self.direction == Direction.RIGHT:
                    if Direction.UP in available_directions and Direction.DOWN in available_directions:
                        if [ally_head[0], ally_head[1] - 1] in harmful_fruits_pos:
                            if Direction.DOWN in available_directions:
                                return Direction.DOWN
                        if [ally_head[0], ally_head[1] - 1] not in harmful_fruits_pos:
                            if Direction.UP in available_directions:
                                return Direction.UP

            if ally_head[0] == ally_dest[0]:

                if ally_head[1] < ally_dest[1]:
                    if self.direction != Direction.UP:  # todo add bomb check
                        if Direction.DOWN in available_directions:
                            return Direction.DOWN
                    if self.direction == Direction.UP:
                        if [ally_head[0] + 1, ally_head[1]] in harmful_fruits_pos:
                            if Direction.LEFT in available_directions:
                                return Direction.LEFT
                        if [ally_head[0] + 1, ally_head[1]] not in harmful_fruits_pos:
                            if Direction.RIGHT in available_directions:
                                return Direction.RIGHT

                if ally_head[1] > ally_dest[1]:
                    if self.direction != Direction.DOWN:  # todo add bomb check
                        if Direction.UP in available_directions:
                            return Direction.UP
                    if self.direction == Direction.DOWN:
                        if [ally_head[0] + 1, ally_head[1]] in harmful_fruits_pos:
                            if Direction.LEFT in available_directions:
                                return Direction.LEFT
                        if [ally_head[0] + 1, ally_head[1]] not in harmful_fruits_pos:
                            if Direction.RIGHT in available_directions:
                                return Direction.RIGHT

            # if ally_head[1] == ally_dest[1] and self.direction in [Direction.UP, Direction.DOWN]:
            #     if ally_head[0] > ally_dest[0]:
            #         if Direction.LEFT in available_directions:
            #             return Direction.LEFT
            #         # todo add logic to where left is blocked
            #     if ally_head[0] < ally_dest[0]:
            #         if Direction.RIGHT in available_directions:
            #             return Direction.RIGHT

            self.my_direction = decision
            # print("head at", head)
            # print("Final: ", direction_dict[decision])
            return random.choice(available_directions)
        # print("head at", head)
        # print("Default", direction_dict[self.my_direction])
        self.my_direction = Direction.CONTINUE
        return self.my_direction
