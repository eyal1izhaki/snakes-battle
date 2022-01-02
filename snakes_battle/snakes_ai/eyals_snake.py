from random import choice
from snakes_battle.fruit import Fruit, FruitKind
from snakes_battle.snake import Snake, Direction
import math

class Eyal(Snake):
    def __init__(self, borders_cells, color, name) -> None:
        super().__init__(color, name)
        self.init(borders_cells)



    def init(self, borders_cells):
        # Your bot initializations will be here.
        self.allowed__version = "2.0"
        # All the cells that are fill with borders. This variable will store a list of (x, y) pairs
        self.allowed__border_cells = borders_cells

    
    def make_decision(self, board_state):

        self.allowed__board_state = board_state
        self.allowed__body_pos = super().allowed__body_position()
        self.allowed__current_direction = super().allowed__get_direction()


        self.allowed__beneficial_fruits = []
        self.allowed__harmful_fruits = []
        self.allowed__special_fruits = []

        self.allowed_all_snakes = board_state["snakes"]


        # Sorting fruits.
        for fruit in self.allowed__board_state["fruits"]:
            if fruit.kind in FruitKind.beneficial_fruits:
                self.allowed__beneficial_fruits.append(fruit)
            elif fruit.kind in FruitKind.harmful_fruits:
                self.allowed__harmful_fruits.append(fruit)
            elif fruit.kind in FruitKind.special_fruits:
                self.allowed__special_fruits.append(fruit)


        closest_fruit = self.closest_fruit(self.allowed__beneficial_fruits + self.allowed__special_fruits)

        new_direction = self.get_direction_to_a_specific_fruit(closest_fruit, self.allowed__current_direction)


        bad_object = self.get_bad_objects_in_next_cell(new_direction)

        if bad_object != None:
            new_direction = self.make_turn(new_direction)


        return new_direction

       
    def make_turn(self, direction):
        if direction == Direction.DOWN or direction == Direction.UP:
            if self.get_bad_objects_in_next_cell(Direction.RIGHT) == None:
                return Direction.RIGHT
            else:
                return Direction.LEFT
        
        if direction == Direction.LEFT or direction == Direction.RIGHT:
            if self.get_bad_objects_in_next_cell(Direction.DOWN) == None:
                return Direction.DOWN
            else:
                return Direction.UP

    def simulate_turn(self,body_pos, current_direction, new_direction):

        if new_direction == Direction.LEFT:
            if current_direction == Direction.UP or current_direction == Direction.DOWN:
                new_direction =  Direction.LEFT

        elif new_direction == Direction.RIGHT:
            if current_direction == Direction.UP or current_direction == Direction.DOWN:
                new_direction =  Direction.RIGHT

        elif new_direction == Direction.UP:
            if current_direction == Direction.RIGHT or current_direction == Direction.LEFT:
                new_direction =  Direction.UP

        elif new_direction == Direction.DOWN:
            if current_direction == Direction.RIGHT or current_direction == Direction.LEFT:
                new_direction =  Direction.DOWN

        for i in reversed(range(1, super().allowed__get_length())):
            body_pos[i][0] = body_pos[i-1][0]
            body_pos[i][1] = body_pos[i-1][1]

        if new_direction == Direction.DOWN:
            body_pos[0][1] += 1
        elif new_direction == Direction.UP:
            body_pos[0][1] -= 1
        elif new_direction == Direction.LEFT:
            body_pos[0][0] -= 1
        elif new_direction == Direction.RIGHT:
            body_pos[0][0] += 1

        return body_pos

    def simulate_turn_head_only(self, new_direction):
        current_direction = self.allowed__current_direction

        body_pos = self.get_body_position()

        if new_direction == Direction.LEFT:
            if current_direction == Direction.UP or current_direction == Direction.DOWN:
                new_direction =  Direction.LEFT

        elif new_direction == Direction.RIGHT:
            if current_direction == Direction.UP or current_direction == Direction.DOWN:
                new_direction =  Direction.RIGHT

        elif new_direction == Direction.UP:
            if current_direction == Direction.RIGHT or current_direction == Direction.LEFT:
                new_direction =  Direction.UP

        elif new_direction == Direction.DOWN:
            if current_direction == Direction.RIGHT or current_direction == Direction.LEFT:
                new_direction =  Direction.DOWN

        if new_direction == Direction.DOWN:
            body_pos[0][1] += 1
        elif new_direction == Direction.UP:
            body_pos[0][1] -= 1
        elif new_direction == Direction.LEFT:
            body_pos[0][0] -= 1
        elif new_direction == Direction.RIGHT:
            body_pos[0][0] += 1

        return body_pos[0]


    def calculate_distance(self, a, b):
        return math.dist(a,b)


    def closest_fruit(self, fruits):
        closest_fruit = fruits[0]
        closest = 100000

        for fruit in fruits:
            fruit_distance = self.calculate_distance(fruit.pos, self.allowed__body_pos[0])
            if fruit_distance < closest:
                closest = fruit_distance
                closest_fruit = fruit
        
        return closest_fruit
    
    def get_direction_to_a_specific_fruit(self, fruit, current_direction):
        if self.allowed__body_pos[0][0] > fruit.pos[0]:
            if (current_direction == Direction.RIGHT):
                return Direction.UP
            else:
                return Direction.LEFT
        
        if self.allowed__body_pos[0][0] < fruit.pos[0]:
            if (current_direction == Direction.LEFT):
                return Direction.UP
            else:
                return Direction.RIGHT
        
        if self.allowed__body_pos[0][0] == fruit.pos[0]:

            if self.allowed__body_pos[0][1] < fruit.pos[1]:
                if (current_direction == Direction.UP):
                    return Direction.RIGHT
                else:
                    return Direction.DOWN

            if self.allowed__body_pos[0][1] > fruit.pos[1]:
                if (current_direction == Direction.DOWN):
                    return Direction.RIGHT
                else:
                    return Direction.UP

    def get_bad_objects_in_next_cell(self, new_direction):

        new_body_pos = self.simulate_turn(self.allowed__body_pos, self.allowed__current_direction, new_direction)

        for fruit in self.allowed__harmful_fruits:
            if new_body_pos[0] == fruit.pos:
                return fruit
        
        for snake in self.allowed_all_snakes:

            if snake.name == self.name:
                for index, cell in enumerate(snake.body_pos):
                    if index != 0 and cell == new_body_pos[0]:
                        return snake
            
            else:
                for cell in snake.body_pos:
                    if new_body_pos[0] == cell:
                        return snake


    def pass_by_object(self, obj):
        current_direction = self.allowed__current_direction
        body_position = self.allowed__body_position()

        if type(obj) == type(Snake):
            snake = obj

            for index, cell in enumerate(snake.body_pos):
                if cell == body_position[0]:
                    hitting_point = cell
                    hitting_point_index = index
                    break

            # Hitting point to the tail
            for i in range(hitting_point_index, snake.allowed__get_length() - 1):
                new_head_pos = self.simulate_turn_head_only()


            
            # Hitting point to the head
            for j in range(0, hitting_point_index):
                pass


            new_head_pos = self.simulate_turn_head_only()


    def is_this_direction_safe(self, new_direction):
        
        current_direction = self.allowed__current_direction
        next_body_pos = self.simulate_turn(self.allowed__body_pos, current_direction, new_direction)

        next_next_body_pos_right = self.simulate_turn(next_body_pos, current_direction, new_direction)
        next_next_body_pos_left = self.simulate_turn(next_body_pos, current_direction, new_direction)
        next_next_body_pos_up = self.simulate_turn(next_body_pos, current_direction, new_direction)
        next_next_body_pos_down = self.simulate_turn(next_body_pos, current_direction, new_direction)

        right = True
        left = True
        up = True
        down = True


        for index, body_pos in enumerate([next_next_body_pos_right, next_next_body_pos_left, next_next_body_pos_up, next_next_body_pos_down]):
            # Snake is going to hit a bad fruit.
            for fruit in self.allowed__harmful_fruits:
                if body_pos[0] in fruit.pos:

                    if index == 0:
                        right = False
                    elif index == 1:
                        left = False
                    elif index == 2:
                        up = False
                    else:
                        down = False
            
        # Snake is going to hit a border
        for cell in body_pos:
            if body_pos[0] in self.allowed__border_cells:
                if index == 0:
                    right = False
                elif index == 1:
                    left = False
                elif index == 2:
                    up = False
                else:
                    down = False

        # Snake is going to hit itself
        for i_cell, cell in enumerate(body_pos):
            if i_cell != 0 and body_pos[0] == cell:
                if index == 0:
                    right = False
                elif index == 1:
                    left = False
                elif index == 2:
                    up = False
                else:
                    down = False
        
        # Snake is going to hit other snakes
        for snake in  self.allowed__board_state["snakes"]:
            if not self.name == snake.name:
                if body_pos[0] in snake.allowed__body_position():
                    if index == 0:
                        right = False
                    elif index == 1:
                        left = False
                    elif index == 2:
                        up = False
                    else:
                        down = False

        safe_directions = 0
        for i in [right, left, up, down]:
            if i:
                safe_directions += 1


        return safe_directions

