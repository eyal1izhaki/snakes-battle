from snakes_battle.fruit import FruitKind
from snakes_battle.snake import Snake, Direction
import math

class Tehila(Snake):
    def __init__(self, borders_cells, color, name) -> None:
        super().__init__(color, name)
        self.init(borders_cells)
        

    ##############################
    # You can edit only the code below. You can't change methods names.
    ##############################


    def init(self, borders_cells):
        # Your bot initializations will be here.
        self.allowed__version = 1.0

        # All the cells that are fill with borders. This variable will store a list of (x, y) pairs
        self.allowed__border_cells = borders_cells


    def check_if_position_in_snake(self, snake_pos, direction):
        pos_to_check=snake_pos[0]
        for snake_node in snake_pos:
            if direction == Direction.UP:
                if (pos_to_check[0] , pos_to_check[1]-1) == (snake_node[0],snake_node[1]) or (pos_to_check[0] , pos_to_check[1]-1) in self.allowed__border_cells:
                    return True
            if direction == Direction.RIGHT:
                if (pos_to_check[0]+1 , pos_to_check[1]) == (snake_node[0],snake_node[1]) or (pos_to_check[0]+1 , pos_to_check[1]) in self.allowed__border_cells:
                    return True
            if direction == Direction.DOWN:
                if (pos_to_check[0] , pos_to_check[1]+1) == (snake_node[0],snake_node[1]) or (pos_to_check[0] , pos_to_check[1]+1) in self.allowed__border_cells:
                    return True
            if direction == Direction.LEFT:
                if (pos_to_check[0]-1 , pos_to_check[1]) == (snake_node[0],snake_node[1]) or  (pos_to_check[0]-1 , pos_to_check[1]) in self.allowed__border_cells:
                    return True
        return False
    
    def allowed__change_direction(self, pos, fruit_to_follow):
        if pos[0][0] > fruit_to_follow.pos[0]:
            if (self.direction == Direction.RIGHT):
                if self.check_if_position_in_snake(pos, Direction.UP):
                    return Direction.RIGHT
                return Direction.UP
            else:
                if self.check_if_position_in_snake(pos, Direction.LEFT):
                    return Direction.RIGHT
                return Direction.LEFT
        
        if pos[0][0] < fruit_to_follow.pos[0]:
            if (self.direction == Direction.LEFT):
                if self.check_if_position_in_snake(pos, Direction.UP):
                    return Direction.LEFT
                return Direction.UP
            else:
                if self.check_if_position_in_snake(pos, Direction.RIGHT):
                    return Direction.LEFT
                return Direction.RIGHT
        
        if pos[0][0] == fruit_to_follow.pos[0]:

            if pos[0][1] < fruit_to_follow.pos[1]:
                if (self.direction == Direction.UP):
                    if self.check_if_position_in_snake(pos,  Direction.RIGHT):
                        return Direction.UP
                    return Direction.RIGHT
                else:
                    if self.check_if_position_in_snake(pos,Direction.DOWN):
                        return Direction.UP
                    return Direction.DOWN

            if pos[0][1] > fruit_to_follow.pos[1]:
                if (self.direction == Direction.DOWN):
                    if self.check_if_position_in_snake(pos,Direction.RIGHT):
                        return Direction.DOWN
                    return Direction.RIGHT
                else:
                    if self.check_if_position_in_snake(pos,Direction.UP):
                        return Direction.DOWN
                    return Direction.UP

    def get_distance(self, pos_1, pos_2):
        x = abs(pos_2[0] - pos_1[0])
        y = abs(pos_2[1] - pos_1[1])
        return x+y
    
    

    def make_decision(self, board_state):
        # You can only call methods that starts with the word 'allowed__'. You can't change attrbiutes directly.

        # super().allowed__get_direction() # This function takes no arguments and returns the direction of the snake.
        # super().allowed__body_position() # This function takes no arguments and returns a list with all cells (x,y) that are filled with your snake.
        # super().allowed__is_king() # returns True if your snake is king else returns False
        # super().allowed__is_knife() # returns True if your snake has a knife else returns False.
        # super().allowed__is_shield() # returns True if your snake is shielded else returns False.

        pos = super().allowed__body_position()
        fruits = board_state["fruits"]

        for fruit in fruits:
            min_distance = self.get_distance(pos[0], fruit.pos)
            if fruit.kind not in FruitKind.harmful_fruits:
                if  self.get_distance(pos[0], fruit.pos) <=  min_distance:
                    fruit_to_follow = fruit

        return self.allowed__change_direction(pos, fruit_to_follow)

            

