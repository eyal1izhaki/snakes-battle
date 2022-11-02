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
        

        fruits = board_state["fruits"]
        pos = self.body_position
        

        # print(fruits[0].pos[0])
        not_harmful_fruits = self.remove_harmful_fruits(fruits)
        harmful_fruits = self.get_harmful_fruits(fruits)
        
        # fruits[0].fr
        # print()
        # for i in h:
        #     print(i.kind['name'], end = ' ')
        # print('hi',fruits[0].kind  not in FruitKind.harmful_fruits)
        # print('pos',board_state["snakes"][0].body_position)

        # dont eat harmful_fruits and dont hit on yourself
        # need to check if in your direction have harmful fruits
        self.find_closest_fruit(not_harmful_fruits)
        
        
        # print(not_harmful_fruits[0].kind['name'])
        # print(self.distance(not_harmful_fruits[0]))
        
        # for i in harmful_fruits:
        #     print(i.kind['name'], end = ' ')
        
        
        
        if pos[0][0] > not_harmful_fruits[0].pos[0]:
            if self._direction == Direction.RIGHT:
                return Direction.UP
            else:
                return Direction.LEFT

        if pos[0][0] < not_harmful_fruits[0].pos[0]:
            if self._direction == Direction.LEFT:
                return Direction.UP
            else:
                return Direction.RIGHT
        
        if pos[0][0] == not_harmful_fruits[0].pos[0]:

            if pos[0][1] < not_harmful_fruits[0].pos[1]:
                if self._direction == Direction.UP:
                    return Direction.RIGHT
                else:
                    return Direction.DOWN

            if pos[0][1] > fruits[0].pos[1]:
                if self._direction == Direction.DOWN:
                    return Direction.RIGHT
                else:
                    return Direction.UP

        return Direction.CONTINUE

    def distance(self, fruit):
        head_pos = self.head
        fruit_pos = fruit.pos
        return math.floor(((head_pos[0] - fruit_pos[0])**2 + (head_pos[1] - fruit_pos[1])**2)**0.5)

    def find_closest_fruit(self,fruits):
        fruits.sort(key=self.distance)

    def remove_harmful_fruits(self, fruits):
        ret_fruits = []
        for fruit in fruits:
            if fruit.kind in FruitKind.beneficial_fruits or fruit.kind in FruitKind.special_fruits:
                ret_fruits.append(fruit)
        return ret_fruits

    def get_harmful_fruits(self,fruits):
        ret_fruits = []
        for fruit in fruits:
            if fruit.kind in FruitKind.harmful_fruits:
                ret_fruits.append(fruit)
        return ret_fruits
