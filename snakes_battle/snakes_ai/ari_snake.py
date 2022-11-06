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

        # print(self.head)
        # fruits[0].fr
        # print()
        # limit_x = self.border_cells[-1][0]
        # limit_y = self.border_cells[-1][1]
        # for i in h:
        #     print(i.kind['name'], end = ' ')
        # print('hi',fruits[0].kind  not in FruitKind.harmful_fruits)
        # print('pos',board_state["snakes"][0].body_position)

        # harmful_fruits = self.get_harmful_fruits(fruits)
        # dont eat harmful_fruits and dont hit on yourself
        # need to check if in your direction have harmful fruits
        try:
            fruits = board_state["fruits"]
            pos = self.body_position

            not_harmful_fruits = self.remove_harmful_fruits(fruits)

            # for fruit in not_harmful_fruits:
            #     print(fruit.kind['name'], end=' ')
            # print()

            left_pos = [self.head[0] - 1, self.head[1]]
            right_pos = [self.head[0] + 1, self.head[1]]
            up_pos = [self.head[0], self.head[1] - 1]
            down_pos = [self.head[0], self.head[1] + 1]

            self.find_closest_fruit(not_harmful_fruits)
            self.find_closest_fruit(fruits)

            snakes = board_state["snakes"]
            enemy_snakes = self.find_closet_enemy_snakes(snakes)

            for fruit in not_harmful_fruits:
                if fruit.kind == FruitKind.SHIELD and self.shield:
                    continue
                if fruit.kind == FruitKind.KNIFE:
                    if self.knife or enemy_snakes == []:
                        continue

                target = fruit.pos
                break
                
            for fruit in not_harmful_fruits:
                if not self.shield:
                    if fruit.kind == FruitKind.SHIELD:
                        target = fruit.pos
                        break
            
            for fruit in not_harmful_fruits:
                if not self.knife and enemy_snakes:
                    if self.length > enemy_snakes[0].length and not enemy_snakes[0].knife:
                        if fruit.kind == FruitKind.KNIFE:
                            target = fruit.pos
                            break
            
            for fruit in not_harmful_fruits:
                if fruit.kind == FruitKind.KING:
                    target = fruit.pos
                    break
                    
                
            if enemy_snakes:
                closest_enemy = enemy_snakes[0]
                len_enemy = closest_enemy.length

                if self.king:
                    if (not closest_enemy.king) or (closest_enemy.king and self.length > len_enemy):
                        if self.dist_snake(closest_enemy) < self.king_remaining_time - 2:
                            target = closest_enemy.head

                if self.knife:
                    if len_enemy >= self.length:
                        if len_enemy >= 6:
                            target = closest_enemy.body_position[2]
                    elif not (closest_enemy.king or closest_enemy.knife) :
                        target = closest_enemy.head

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
            return Direction.CONTINUE
        except:
            return Direction.CONTINUE

    def dist_fruit(self, fruit):
        head_pos = self.head
        fruit_pos = fruit.pos
        return abs(head_pos[0] - fruit_pos[0]) + abs(head_pos[1] - fruit_pos[1])

    def find_closest_fruit(self, fruits):
        fruits.sort(key=self.dist_fruit)

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
        return self.is_good_pos(board_state, Direction.LEFT)

    def is_right(self, board_state):
        return self.is_good_pos(board_state, Direction.RIGHT)

    def is_up(self, board_state):
        return self.is_good_pos(board_state, Direction.UP)

    def is_down(self, board_state):
        return self.is_good_pos(board_state, Direction.DOWN)

    def is_good_pos(self, board_state, direction):
        pos = self.body_position
        fruits = board_state["fruits"]
        snakes = board_state["snakes"]
        harmful_fruits = self.get_harmful_fruits(fruits)
        enemy_snakes = self.find_closet_enemy_snakes(snakes)
        x_head = self.head[0]
        y_head = self.head[1]
        limit_x = self.border_cells[-1][0]
        limit_y = self.border_cells[-1][1]

        mapping_pos = {
            Direction.RIGHT: [x_head + 1, y_head],
            Direction.LEFT: [x_head - 1, y_head],
            Direction.UP: [x_head, y_head - 1],
            Direction.DOWN: [x_head, y_head + 1]
        }

        next_pos = mapping_pos[direction]

        mapping_bad_pos = {
            Direction.RIGHT: [next_pos,
                              [x_head + 2, y_head],
                              [x_head + 1, y_head + 1],
                              [x_head + 1, y_head - 1]],

            Direction.LEFT:  [next_pos,
                              [x_head - 2, y_head],
                              [x_head - 1, y_head + 1],
                              [x_head - 1, y_head - 1]],

            Direction.UP: [next_pos,
                           [x_head, y_head - 2],
                           [x_head - 1, y_head - 1],
                           [x_head + 1, y_head - 1]],

            Direction.DOWN: [next_pos,
                             [x_head, y_head + 2],
                             [x_head - 1, y_head + 1],
                             [x_head + 1, y_head + 1]]
        }


        bad_pos = mapping_bad_pos[direction]
        if tuple(next_pos) in self.border_cells:
            return False

        for fruit in harmful_fruits:
            if next_pos == fruit.pos:
                return False

        if enemy_snakes:
            if (self.knife == False and self.king == False) or (self.knife and self.length < enemy_snakes[0].length):
                for snake in enemy_snakes:
                    for bad in bad_pos:
                        if bad == snake.head:
                            return False

            if (self.knife == False and self.king == False ) or (self.knife and self.length > enemy_snakes[0].length):
                for snake in enemy_snakes:
                    if next_pos in snake.body_position[1:]:
                        return False

        if next_pos in pos:
            return False

        return True

    def find_closet_enemy_snakes(self, snakes):
        ret_snakes = []
        for snake in snakes:
            if snake is not self:
                ret_snakes.append(snake)

        ret_snakes.sort(key=self.dist_snake)
        return ret_snakes

    def dist_snake(self, snake):
        return abs(self.head[0] - snake.head[0]) + abs(self.head[1] - snake.head[1])

    def arrive_in_time(self, fruit):
        pos_fruit = fruit.pos
        x_steps = abs(self.head[0] - pos_fruit[0])
        y_steps = abs(self.head[1] - pos_fruit[1])

        return x_steps+y_steps <= fruit.lifespan
