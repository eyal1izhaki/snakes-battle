from snakes_battle.fruit import FruitKind
from snakes_battle.snake import Snake, Direction
import pygame

class shlomo809(Snake):
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

    
    def make_decision(self, board_state):
        # You can only call methods that starts with the word 'allowed__'. You can't change attrbiutes directly.

        super().allowed__get_direction() # This function takes no arguments and returns the direction of the snake.
        super().allowed__body_position() # This function takes no arguments and returns a list with all cells (x,y) that are filled with your snake.
        super().allowed__is_king() # returns True if your snake is king else returns False
        super().allowed__is_knife() # returns True if your snake has a knife else returns False.
        super().allowed__is_shield() # returns True if your snake is shielded else returns False.
        max_dis=999
        for fruit in board_state["fruits"]:
            if fruit.kind in FruitKind.harmful_fruits :
                continue
            
            
            my_pos = super().allowed__body_position()
            my_head=my_pos[0]
            new_dest_x= my_head[0] - fruit.pos[0]
            new_dest_y= my_head[1]- fruit.pos[1]
            new_dest = new_dest_x + new_dest_y
            new_dest *= -1
            
            
            if (new_dest <max_dis):
                
                best_dest_x=new_dest_x
                best_dest_y = new_dest_y
                new_dest = max_dis
                f_x=fruit.pos[0]
                f_y=fruit.pos[1]
            
        direct=self.allowed_nearest_fruit(best_dest_x,best_dest_y)
        is_bad=self.check_for_bad(my_head,board_state,direct)
        if direct==0:
            return Direction.RIGHT
        if direct ==1:
            return Direction.LEFT    
        if direct ==2:
            return Direction.UP   
        if direct ==3:
            return Direction.DOWN   




    def allowed_nearest_fruit(self,x_pos,y_pos):
        if x_pos != 0 and x_pos < 0:
            
            if super().allowed__get_direction()==1:
                
                return 2
            return 0
        if x_pos != 0 and x_pos > 0:
            
            if super().allowed__get_direction()==0:
                return 2
            return 1
        if y_pos != 0 and y_pos > 0:
            
            if super().allowed__get_direction()==3:
                return 0
            return 2    
        if y_pos != 0 and y_pos < 0:
            
            if super().allowed__get_direction()==2:
                return 0
            return 3


    def check_for_bad(self,head,state,original_direct):
        
        
        new_head_x =head[0]+1
        new_head_y = head[1]+1
        
        
        for snake_bad in state["snakes"]:
            
            if new_head_x in snake_bad.allowed__body_position():
                return 2
            if new_head_y in   snake_bad.allowed__body_position():
                return 0

        return original_direct
