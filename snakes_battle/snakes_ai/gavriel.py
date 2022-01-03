from snakes_battle import fruit
from snakes_battle.fruit import FruitKind
from snakes_battle.snake import Snake, Direction

class Gavriel(Snake):
    def __init__(self, borders_cells, color, name) -> None:
        super().__init__(color, name)
        self.init(borders_cells)

    def init(self, borders_cells):
        # Your bot initializations will be here.
        self.allowed__version = 0.0
        # All the cells that are fill with borders. This variable will store a list of (x, y) pairs
        self.allowed__border_cells = borders_cells

    def dont_eat_your(self,board_state):
        direction =super().allowed__get_direction() # This function takes no arguments and returns the direction of the snake.
       
        # print("dirction:",direction)
        # board_state["snakes"][0]
        # print("board_state[snakes]:",board_state["snakes"][0])
        


    def good_fruits(self,fruits,board_state):
        fruits = board_state["fruits"]
        for fruit in fruits: 
            if fruit.kind in FruitKind.harmful_fruits :
                i = 0
                if fruit.kind in FruitKind.harmful_fruits :
                    i=1
                    if fruit.kind in FruitKind.harmful_fruits :
                       i=2
            else:
                i = 0
            return i 
    
    def make_decision(self, board_state):

        fruits = board_state["fruits"]
        # print("fruits",fruits)
        # print("fruits",fruit)
        # self.dont_eat_your(board_state)
        # direction =super().allowed__get_direction() # This function takes no arguments and returns the direction of the snake.


        action = self.good_fruits(fruits,board_state)
        # print ("action",action)       
        pos = super().allowed__body_position()
        
        if pos[0][0] > fruits[0+action].pos[0]:
            if (self.direction == Direction.RIGHT):
                return Direction.UP
            else:
                return Direction.LEFT
        
        if pos[0][0] < fruits[0+action].pos[0]:
            if (self.direction == Direction.LEFT):
                return Direction.UP
            else:
                return Direction.RIGHT
        
        if pos[0][0] == fruits[0+action].pos[0]:

            if pos[0][1] < fruits[0].pos[1]:
                if (self.direction == Direction.UP):
                    return Direction.RIGHT
                else:
                    return Direction.DOWN

            if pos[0][1] > fruits[0].pos[1]:
                if (self.direction == Direction.DOWN):
                    return Direction.RIGHT
                else:
                    return Direction.UP
