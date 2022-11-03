import math
from snakes_battle.snake import Snake, Direction
from snakes_battle.fruit import *


class AriSnake(Snake):
    def __init__(self, borders_cells, color, name) -> None:
        super().__init__(color, name)

        self.version = 1.0
        self.border_cells = borders_cells

    def make_decision(self, board_state):
        # kind of fruit
        # fruits[0].kind in FruitKind.harmful_fruits
        # self.body_position is list of 2 items list of coordinates [x,y]
        # fruits is all objects fruits in board
        # pos it is all my positions
        # print(not_harmful_fruits[0].kind['name'])
        # print(self.distance(not_harmful_fruits[0]))

        # for i in harmful_fruits:
        #     print(i.kind['name'], end = ' ')

        # print(self.head)
        # fruits[0].fr
        # print()
        # for i in h:
        #     print(i.kind['name'], end = ' ')
        # print('hi',fruits[0].kind  not in FruitKind.harmful_fruits)
        # print('pos',board_state["snakes"][0].body_position)

        # dont eat harmful_fruits and dont hit on yourself
        # need to check if in your direction have harmful fruits
        # try:
        fruits = board_state["fruits"]
        pos = self.body_position

        not_harmful_fruits = self.remove_harmful_fruits(fruits)
        harmful_fruits = self.get_harmful_fruits(fruits)

        for fruit in not_harmful_fruits:
            print(fruit.kind['name'],end= ' ')
        print()

        limit_x = self.border_cells[-1][0]
        limit_y = self.border_cells[-1][1]
        left_pos = [self.head[0] - 1, self.head[1]]
        right_pos = [self.head[0] + 1, self.head[1]]
        up_pos = [self.head[0], self.head[1] - 1]
        down_pos = [self.head[0], self.head[1] + 1]

        self.find_closest_fruit(not_harmful_fruits)
        self.find_closest_fruit(fruits)

        snakes = board_state["snakes"]
        enemy_snakes = self.find_closet_enemy_snakes(snakes)

        # if enemy_snakes >

        target = not_harmful_fruits[0].pos
        if enemy_snakes:
            if self.king or self.knife:
                target = enemy_snakes[0].head

                if enemy_snakes[0].length > self.length:
                    target = enemy_snakes[0].body_position[1]

        if pos[0][0] > target[0]:
            if self._direction == Direction.RIGHT:
                if self.is_up(board_state):
                    return Direction.UP
                elif self.is_down(board_state):
                    return Direction.DOWN
            else:
                if self.is_left(board_state):
                    return Direction.LEFT

                if self._direction != Direction.DOWN and self.is_up(board_state):
                    return Direction.UP
                elif self._direction != Direction.UP and self.is_down(board_state):
                    return Direction.DOWN
                elif self._direction != Direction.LEFT and self.is_right(board_state):
                    return Direction.RIGHT

        if pos[0][0] < target[0]:
            if self._direction == Direction.LEFT:
                if self.is_up(board_state):
                    return Direction.UP
                elif self.is_down(board_state):
                    return Direction.DOWN
            else:
                if self.is_right(board_state):
                    return Direction.RIGHT
                elif self._direction != Direction.DOWN and self.is_up(board_state):
                    return Direction.UP
                elif self._direction != Direction.UP and self.is_down(board_state):
                    return Direction.DOWN
                elif self._direction != Direction.RIGHT and self.is_left(board_state):
                    return Direction.LEFT

        if pos[0][0] == target[0]:

            if pos[0][1] < target[1]:
                if self._direction == Direction.UP:
                    if self.is_right(board_state):
                        return Direction.RIGHT
                    elif self.is_left(board_state):
                        return Direction.LEFT
                else:
                    if self.is_down(board_state):
                        return Direction.DOWN
                    elif self._direction != Direction.LEFT and self.is_right(board_state):
                        return Direction.RIGHT
                    elif self._direction != Direction.RIGHT and self.is_left(board_state):
                        return Direction.LEFT
                    elif self._direction != Direction.DOWN and self.is_up(board_state):
                        return Direction.UP

            if pos[0][1] > target[1]:
                if self._direction == Direction.DOWN:
                    if self.is_right(board_state):
                        return Direction.RIGHT
                    elif self.is_left(board_state):
                        return Direction.LEFT
                else:
                    if self.is_up(board_state):
                        return Direction.UP
                    elif self._direction != Direction.LEFT and self.is_right(board_state):
                        return Direction.RIGHT
                    elif self._direction != Direction.RIGHT and self.is_left(board_state):
                        return Direction.LEFT
                    elif self._direction != Direction.UP and self.is_down(board_state):
                        return Direction.DOWN

        if left_pos == fruits[0].pos and fruits[0].kind == FruitKind.BOMB:
            if self.direction != Direction.RIGHT:
                return Direction.LEFT

        if right_pos == fruits[0].pos and fruits[0].kind == FruitKind.BOMB:
            if self.direction != Direction.LEFT:
                return Direction.RIGHT

        if up_pos == fruits[0].pos and fruits[0].kind == FruitKind.BOMB:
            if self.direction != Direction.DOWN:
                return Direction.UP

        if down_pos == fruits[0].pos and fruits[0].kind == FruitKind.BOMB:
            if self.direction != Direction.UP:
                return Direction.DOWN

        if left_pos == 0:
            if self.direction == Direction.LEFT:
                if self.is_up(board_state):
                    return Direction.UP
                else:
                    return Direction.DOWN
            if self.direction == Direction.UP:
                if self.is_right(board_state):
                    return Direction.RIGHT
                else:
                    return Direction.UP

            if self.direction == Direction.DOWN:
                if self.is_right(board_state):
                    return Direction.RIGHT
                else:
                    return Direction.DOWN

        return Direction.CONTINUE
        # except:
        #     return Direction.CONTINUE

    def distance(self, fruit):
        head_pos = self.head
        fruit_pos = fruit.pos
        return abs(head_pos[0] - fruit_pos[0]) + abs(head_pos[1] - fruit_pos[1])

    def find_closest_fruit(self, fruits):
        fruits.sort(key=self.distance)

    def remove_harmful_fruits(self, fruits):
        ret_fruits = []
        for fruit in fruits:
            if fruit.kind in FruitKind.special_fruits and self.arrive_in_time(fruit):
                ret_fruits.append(fruit)
            if fruit.kind in FruitKind.beneficial_fruits:
                ret_fruits.append(fruit)
        return ret_fruits

    def get_harmful_fruits(self, fruits):
        ret_fruits = []
        for fruit in fruits:
            if fruit.kind in FruitKind.harmful_fruits:
                ret_fruits.append(fruit)
        return ret_fruits

    def is_left(self, board_state):
        pos = self.body_position
        fruits = board_state["fruits"]
        snakes = board_state["snakes"]
        enemy_snakes = self.find_closet_enemy_snakes(snakes)

        harmful_fruits = self.get_harmful_fruits(fruits)
        left_pos = [self.head[0] - 1, self.head[1]]
        bad_pos = [left_pos, [self.head[0] - 2, self.head[1]],
                   [self.head[0] - 1, self.head[1] + 1],
                   [self.head[0] - 1, self.head[1] - 1]]

        for fruit in harmful_fruits:
            if left_pos == fruit.pos:
                return False

        if self.knife == False and self.king == False:

            for snake in enemy_snakes:
                for bad in bad_pos:
                    if bad == snake.head:
                        return False

            for snake in enemy_snakes:
                if left_pos in snake.body_position[1:]:
                    return False

        if left_pos in pos or left_pos[0] == 0:
            return False
        return True

    def is_right(self, board_state):
        pos = self.body_position
        fruits = board_state["fruits"]
        snakes = board_state["snakes"]
        enemy_snakes = self.find_closet_enemy_snakes(snakes)

        limit_x = self.border_cells[-1][0]
        harmful_fruits = self.get_harmful_fruits(fruits)
        right_pos = [self.head[0] + 1, self.head[1]]
        bad_pos = [right_pos,
                   [self.head[0] + 2, self.head[1]],
                   [self.head[0] + 1, self.head[1] + 1],
                   [self.head[0] + 1, self.head[1] - 1]
                   ]
        for fruit in harmful_fruits:
            if right_pos == fruit.pos:
                return False

        if self.knife == False and self.king == False:
            for snake in enemy_snakes:
                for bad in bad_pos:
                    if bad == snake.head:
                        return False

        for snake in enemy_snakes:
            if right_pos in snake.body_position[1:]:
                return False

        if right_pos in pos or right_pos[0] == limit_x:
            return False
        return True

    def is_up(self, board_state):
        pos = self.body_position
        snakes = board_state["snakes"]
        fruits = board_state["fruits"]
        harmful_fruits = self.get_harmful_fruits(fruits)
        enemy_snakes = self.find_closet_enemy_snakes(snakes)
        up_pos = [self.head[0], self.head[1] - 1]

        bad_pos = [up_pos, [self.head[0], self.head[1] - 2],
                   [self.head[0] - 1, self.head[1] - 1],
                   [self.head[0] + 1, self.head[1] - 1]]

        for fruit in harmful_fruits:
            if up_pos == fruit.pos:
                return False

        if self.knife == False and self.king == False:

            for snake in enemy_snakes:
                for bad in bad_pos:
                    if bad == snake.head:
                        return False

            for snake in enemy_snakes:
                if up_pos in snake.body_position[1:]:
                    return False

        if up_pos in pos or up_pos[1] == 0:
            return False
        return True

    def is_down(self, board_state):
        pos = self.body_position
        fruits = board_state["fruits"]
        snakes = board_state["snakes"]
        limit_y = self.border_cells[-1][1]
        harmful_fruits = self.get_harmful_fruits(fruits)
        enemy_snakes = self.find_closet_enemy_snakes(snakes)

        down_pos = [self.head[0], self.head[1] + 1]

        bad_pos = [down_pos, [self.head[0], self.head[1] + 2],
                   [self.head[0] - 1, self.head[1] + 1],
                   [self.head[0] + 1, self.head[1] + 1]]
        for fruit in harmful_fruits:
            if down_pos == fruit.pos:
                return False

        if self.knife == False and self.king == False:

            for snake in enemy_snakes:
                for bad in bad_pos:
                    if bad == snake.head:
                        return False
                        
            for snake in enemy_snakes:
                if down_pos in snake.body_position[1:]:
                            return False



        if down_pos in pos or down_pos[1] == limit_y:
            return False
        return True

    def find_closet_enemy_snakes(self, snakes):
        ret_snakes = []
        for snake in snakes:
            if snake is not self:
                ret_snakes.append(snake)

        ret_snakes.sort(key=self.dist)
        return ret_snakes

    def dist(self, snake):
        head_pos = self.head
        snake_pos = snake.head
        return math.floor(((head_pos[0] - snake_pos[0])**2 + (head_pos[1] - snake_pos[1])**2)**0.5)

    def arrive_in_time(self, fruit):
        pos_fruit = fruit.pos
        x_steps = abs(self.head[0] - pos_fruit[0])
        y_steps = abs(self.head[1] - pos_fruit[1])

        return x_steps+y_steps <= fruit.lifespan
