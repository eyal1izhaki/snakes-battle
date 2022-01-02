from snakes_battle.fruit import Fruit, FruitKind
from snakes_battle.snake import Snake, Direction
import math

class Eyal(Snake):
    def __init__(self, borders_cells, color, name) -> None:
        super().__init__(color, name)
        self.init(borders_cells)



    def init(self, borders_cells):
        # Your bot initializations will be here.
        self.allowed__version = 1.0
        # All the cells that are fill with borders. This variable will store a list of (x, y) pairs
        self.allowed__border_cells = borders_cells

    
    def make_decision(self, board_state):

        self.allowed__board_state = board_state
        self.allowed_body_pos = super().allowed__body_position()
        self.allowed_current_direction = super().allowed__get_direction()


        self.allowed_beneficial_fruits = []
        self.allowed_harmful_fruits = []
        self.allowed_special_fruits = []


        # Sorting fruits.
        for fruit in self.allowed__board_state["fruits"]:
            if fruit.kind in FruitKind.beneficial_fruits:
                self.allowed_beneficial_fruits.append(fruit)
            elif fruit.kind in FruitKind.harmful_fruits:
                self.allowed_harmful_fruits.append(fruit)
            elif fruit.kind in FruitKind.special_fruits:
                self.allowed_special_fruits.append(fruit)

        closest_fruit = self.closest_fruit(self.allowed_beneficial_fruits + self.allowed_special_fruits)

        new_direction = self.get_direction_to_a_specific_fruit(closest_fruit)

        return new_direction

       

    def simulate_turn(self, direction, current_direction):
        new_direction = current_direction

        if direction == Direction.LEFT:
            if current_direction == Direction.UP or current_direction == Direction.DOWN:
                new_direction =  Direction.LEFT

        elif direction == Direction.RIGHT:
            if current_direction == Direction.UP or current_direction == Direction.DOWN:
                new_direction =  Direction.RIGHT

        elif direction == Direction.UP:
            if current_direction == Direction.RIGHT or current_direction == Direction.LEFT:
                new_direction =  Direction.UP

        elif direction == Direction.DOWN:
            if current_direction == Direction.RIGHT or current_direction == Direction.LEFT:
                new_direction =  Direction.DOWN

        for i in reversed(range(1, self.allowed__get_length)):
            self.body_pos[i][0] = self.body_pos[i-1][0]
            self.body_pos[i][1] = self.body_pos[i-1][1]


    def calculate_distance(self, a, b):
        return math.dist(a,b)


    def closest_fruit(self, fruits):
        closest_fruit = fruits[0]
        closest = 100000

        for fruit in fruits:
            fruit_distance = self.calculate_distance(fruit.pos, self.allowed_body_pos[0])
            if fruit_distance < closest:
                closest = fruit_distance
                closest_fruit = fruit
        
        return closest_fruit
    
    def get_direction_to_a_specific_fruit(self, fruit, current_direction):
        if self.allowed_body_pos[0][0] > fruit.pos[0]:
            if (current_direction == Direction.RIGHT):
                return Direction.UP
            else:
                return Direction.LEFT
        
        if self.allowed_body_pos[0][0] < fruit.pos[0]:
            if (current_direction == Direction.LEFT):
                return Direction.UP
            else:
                return Direction.RIGHT
        
        if self.allowed_body_pos[0][0] == fruit.pos[0]:

            if self.allowed_body_pos[0][1] < fruit.pos[1]:
                if (current_direction == Direction.UP):
                    return Direction.RIGHT
                else:
                    return Direction.DOWN

            if self.allowed_body_pos[0][1] > fruit.pos[1]:
                if (current_direction == Direction.DOWN):
                    return Direction.RIGHT
                else:
                    return Direction.UP

    def avoid_dangerous_fruits(self, direction):
        pass