from multiprocessing import current_process
from xml.dom.xmlbuilder import Options
from snakes_battle.snake import Snake, Direction
from snakes_battle.fruit import FruitKind


class Yakov(Snake):
    def __init__(self, borders_cells, color, name) -> None:
        super().__init__(color, name)

        self.version = 1.0
        self.border_cells = borders_cells
        self.MAX_DISTANCE = 100000

    def find_not_die(self,head, fruits,his_snake):
        my_snake = self.body_position
        snakes = his_snake+ my_snake
        if([head[0]+1,head[1]] not in snakes):
            for fruit in fruits:
                if fruit.kind not in FruitKind.harmful_fruits:
                    return [head[0]+1,head[1]]
                if fruit.kind['name']!='SKULL':
                    return [head[0]+1,head[1]]
        elif([head[0]-1,head[1]] not in snakes):
            for fruit in fruits:
                if fruit.kind not in FruitKind.harmful_fruits:
                    return [head[0]-1,head[1]]
                if fruit.kind['name']!='SKULL':
                    return [head[0]-1,head[1]]
        elif([head[0],head[1]-1] not in snakes):
            for fruit in fruits:
                if fruit.kind not in FruitKind.harmful_fruits:
                    return [head[0],head[1]-1]
                if fruit.kind['name']!='SKULL':
                    return [head[0],head[1]-1]
        elif([head[0],head[1]+1] not in snakes):
            for fruit in fruits:
                if fruit.kind not in FruitKind.harmful_fruits:
                    return [head[0],head[1]+1]
                if fruit.kind['name']!='SKULL':
                    return [head[0],head[1]+1]
                    
    def get_direction(self, head, close):
        direction = 1
        if head[0] > close[0]:
            direction = Direction.LEFT

        if head[0] < close[0]:
            direction = Direction.RIGHT

        if head[0] == close[0]:

            if head[1] < close[1]:
                direction = Direction.DOWN

            if head[1] > close[1]:
                direction = Direction.UP

        return direction

    def bad_next(self, his_snake, fruits, direction):
        my_snake = self.body_position
        head = my_snake[0]

        next = [0, 0]
        if direction == Direction.RIGHT:
            next = [head[0]+1, head[1]]
        elif direction == Direction.LEFT:
            next = [head[0]-1, head[1]]
        elif direction == Direction.UP:
            next = [head[0], head[1]-1]
        elif direction == Direction.DOWN:
            next = [head[0]-1, head[1]+1]

        for fruit in fruits:
            if fruit.kind in FruitKind.harmful_fruits and next == fruit.pos:
                return True

        for place in his_snake[1:]:
            if next == place:
                return True

        if [next[0]+1, next[1]] == his_snake[0] or [next[0]-1, next[1]] == his_snake[0] or [next[0], next[1]-1] == his_snake[0] or [next[0], next[1]+1] == his_snake[0]:
            return True

        if next in my_snake:
            return True

        return False

    def get_best_plain(self, the_max,my_options, fruits, his_snake):
        head = self.body_position[0]
        for option in my_options:
            if option["value"] == the_max:
                current_best = option['place'][0]
                print(current_best)
                print(head)
                print(self.get_direction(head, current_best))
                if self.bad_next(his_snake, fruits, self.get_direction(head, current_best)):
                    print("in bad next")
                    my_options2 = [optio for optio in my_options if option['value']!=optio["value"] ]
                    if len(my_options2)==0:
                        self.get_best_plain(the_max,my_options2, fruits, his_snake)
                    else:
                        return self.find_not_die(head,fruits,his_snake)
                else:
                    return current_best

    def closest(self, kind, fruits):
        my_snake = self.body_position
        head = my_snake[0]
        best = [-1, -1]
        distance = self.MAX_DISTANCE

        for fruit in fruits:
            dis = abs(head[0]-fruit.pos[0]) + abs(head[1]-fruit.pos[1])
            if fruit.kind['name'] == kind and (dis < distance):
                distance = dis
                best = fruit.pos

        return best, distance

    def get_best(self, fruits, snakes):
        shield = self.shield
        knife = self.knife
        king = self.king

        his_snake = []
        snakes = snakes

        for snake in snakes:
            if snake != self:
                for cell in snake.body_position:
                    his_snake.append(cell)

        my_options = []
        if not king:
            close_king = {"place": self.closest(
                'KING', fruits), "name": 'KING'}
            close_king["value"] = close_king["place"][1]*3
            if close_king["place"][1] != self.MAX_DISTANCE:
                my_options.append(close_king)
        if not shield:
            close_shield = {"place": self.closest(
                'SHIELD', fruits), "name": 'SHIELD'}
            close_shield["value"] = close_shield["place"][1]*2.5
            if close_shield["place"][1] != self.MAX_DISTANCE:
                my_options.append(close_shield)
        if not knife:
            close_knife = {"place": self.closest(
                'KNIFE', fruits), "name": 'KNIFE'}
            close_knife["value"] = close_knife["place"][1]*2
            if close_knife["place"][1] != self.MAX_DISTANCE:
                my_options.append(close_knife)

        close_strawberry = {"place": self.closest(
            'STRAWBERRY', fruits), "name": 'STRAWBERRY'}
        close_dragon_fruit = {"place": self.closest(
            'DRAGON_FRUIT', fruits), "name": 'DRAGON_FRUIT'}

        close_strawberry["value"] = close_strawberry["place"][1]
        close_dragon_fruit["value"] = close_dragon_fruit["place"][1]*1.2

        if close_strawberry["place"][1] != self.MAX_DISTANCE:
            my_options.append(close_strawberry)
        if close_dragon_fruit["place"][1] != self.MAX_DISTANCE:
            my_options.append(close_dragon_fruit)

        if not king and not knife and not shield:
            the_max = max(option["value"] for option in my_options)
            return self.get_best_plain(the_max,my_options,fruits,his_snake)

    
        return [25,25]

    def make_decision(self, board_state):

        fruits = board_state["fruits"]
        snakes = board_state["snakes"]

        my_position = self.body_position
        best = self.get_best(fruits, snakes)
        direction = self.get_direction(my_position[0], best)

        return direction
