from snakes_battle.fruit import FruitKind
from snakes_battle.snake import Snake, Direction
import math

class Tehila(Snake):
    def __init__(self, borders_cells, color, name) -> None:
        super().__init__(color, name)
        self.init(borders_cells)

    def init(self, borders_cells):
        # Your bot initializations will be here.
        self.allowed__version = 1.2

        # All the cells that are fill with borders. This variable will store a list of (x, y) pairs
        self.allowed__border_cells = borders_cells


    def is_pos_snake(self,pos_to_check, snake_pos):
        for snake_node in snake_pos:
            if pos_to_check == snake_node:
                return True
        return False
    
    
    def is_pos_harmful_fruit(self,pos_to_check, fruits):
        for fruit in fruits:
            if fruit.kind in FruitKind.harmful_fruits and pos_to_check == fruit.pos:
                    return True
        return False
    
        
    def is_pos_other_snake(self,pos_to_check, snakes):
        for snake in snakes:
            for pos in snake.get_body_position():
                if pos_to_check == pos:
                    return True
        return False


    def get_pos_to_check(self, direction, pos):
        if direction == Direction.UP:
            pos_to_check = [pos[0] , pos[1]-1]
        if direction == Direction.RIGHT:
            pos_to_check = [pos[0]+1 , pos[1]]
        if direction == Direction.DOWN:
            pos_to_check = [pos[0] , pos[1]+1]
        if direction == Direction.LEFT:
            pos_to_check = [pos[0]-1 , pos[1]]
        return pos_to_check

    def check_if_position_in_snake(self, snake_pos, direction, fruits, snakes, pos_to_check=None):

        if not pos_to_check:
            pos_to_check = snake_pos[0]
        pos_to_check = self.get_pos_to_check(direction,pos_to_check)
        
        
        if self.is_pos_snake(pos_to_check, snake_pos):
                return True
        
        if self.is_pos_harmful_fruit(pos_to_check, fruits):
                return True
        
        if self.is_pos_other_snake(pos_to_check, snakes):
            return True
        
        if (pos_to_check[0],pos_to_check[1]) in self.allowed__border_cells:
            return True
        
        return False
    
    def allowed__change_direction(self, pos, fruit_to_follow, fruits, snakes,pos_to_check):
        if pos[0][0] > fruit_to_follow.pos[0]:
            if (self.direction == Direction.RIGHT):
                if not self.check_if_position_in_snake(pos,Direction.UP,fruits, snakes,pos_to_check):
                    return Direction.DOWN
                return Direction.UP
            else:
                return Direction.LEFT
        
        if pos[0][0] < fruit_to_follow.pos[0]:
            if (self.direction == Direction.LEFT):
                if not self.check_if_position_in_snake(pos,Direction.UP,fruits, snakes,pos_to_check):
                    return Direction.DOWN
                return Direction.UP
            else:
                return Direction.RIGHT
        
        if pos[0][0] == fruit_to_follow.pos[0]:

            if pos[0][1] <fruit_to_follow.pos[1]:
                if (self.direction == Direction.UP):
                    if not self.check_if_position_in_snake(pos,Direction.RIGHT,fruits, snakes):
                        return Direction.LEFT
                    return Direction.RIGHT
                else:
                    return Direction.DOWN

            if pos[0][1] > fruit_to_follow.pos[1]:
                if (self.direction == Direction.DOWN):
                    if not self.check_if_position_in_snake(pos,Direction.RIGHT,fruits, snakes):
                        return Direction.LEFT
                    return Direction.RIGHT
                else:
                    return Direction.UP


    def get_distance(self, pos_1, pos_2):
        x = abs(pos_2[0] - pos_1[0])
        y = abs(pos_2[1] - pos_1[1])
        return x+y
    

    def get_direction_after_clear_way(self, direction, pos, fruits, snakes, pos_to_check):
        if direction == Direction.UP and self.check_if_position_in_snake(pos,Direction.UP,fruits, snakes,pos_to_check):
            if not self.check_if_position_in_snake(pos,Direction.DOWN,fruits, snakes):
                return Direction.DOWN
            if not self.check_if_position_in_snake(pos,Direction.LEFT,fruits, snakes):
                return Direction.LEFT
            return Direction.RIGHT  


        if direction == Direction.DOWN and self.check_if_position_in_snake(pos,Direction.DOWN,fruits, snakes):
            if not self.check_if_position_in_snake(pos,Direction.UP,fruits, snakes,pos_to_check):
                return Direction.UP
            if not self.check_if_position_in_snake(pos,Direction.LEFT,fruits, snakes):
                return Direction.LEFT
            return Direction.RIGHT  
        
        
        if direction == Direction.RIGHT and self.check_if_position_in_snake(pos,Direction.RIGHT,fruits, snakes):
            if not self.check_if_position_in_snake(pos,Direction.LEFT,fruits, snakes):
                return Direction.LEFT
            if not self.check_if_position_in_snake(pos,Direction.UP,fruits, snakes,pos_to_check):
                return Direction.UP
            return Direction.DOWN

        if direction == Direction.LEFT and self.check_if_position_in_snake(pos,Direction.LEFT,fruits, snakes):
            if not self.check_if_position_in_snake(pos,Direction.RIGHT,fruits, snakes):
                return Direction.RIGHT
            if not self.check_if_position_in_snake(pos,Direction.UP,fruits, snakes,pos_to_check):
                return Direction.UP
            return Direction.DOWN
        else: 
            return direction
    

    def make_decision(self, board_state):

        pos = super().allowed__body_position()
        fruits = board_state["fruits"]
        snakes = board_state["snakes"]
         
        not_harmful_fruits = [fruit for fruit in fruits if fruit.kind not in FruitKind.harmful_fruits]
              
                
        other_snakes = [snake for snake in snakes if snake.__class__  != Tehila]
        if other_snakes == []:
            not_harmful_fruits = [fruit for fruit in fruits if fruit.kind  in FruitKind.beneficial_fruits]
        
        fruit_to_follow =  not_harmful_fruits[0]
        min_fruit_dis =  self.get_distance(pos[0], not_harmful_fruits[0].pos)
        for snake in snakes:
            for fruit in not_harmful_fruits:
                snake_dis = self.get_distance(snake.get_body_position()[0], fruit.pos)
                fruit_dis = self.get_distance(pos[0], fruit.pos)
                if fruit_dis <= min_fruit_dis and (snake.__class__  == Tehila  or fruit_dis < snake_dis):
                    min_fruit_dis = fruit_dis
                    fruit_to_follow = fruit
        
        direction = self.allowed__change_direction(pos, fruit_to_follow, fruits, snakes, pos[0])
        direction2 = self.get_direction_after_clear_way(direction, pos, fruits, snakes,pos[0])        
        return direction2