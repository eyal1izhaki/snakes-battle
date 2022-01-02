from snakes_battle.fruit import FruitKind
from snakes_battle.snake import Snake, Direction

class MayaWins(Snake):
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
    
    def allowed__getHead(self):
        return super().allowed__body_position()[0]
    
    def allowed__calcDirectionForFruit(self, snakePosition, fruitPosition):
        if (snakePosition[0] > fruitPosition[0]):
            return Direction.LEFT
        elif (snakePosition[0] < fruitPosition[0]):
            return Direction.RIGHT
        elif (snakePosition[1] < fruitPosition[1]):
            return Direction.UP
        else:
            return Direction.DOWN


    
    def make_decision(self, board_state):
        # You can only call methods that starts with the word 'allowed__'. You can't change attrbiutes directly.

        # super().allowed__get_direction() # This function takes no arguments and returns the direction of the snake.
        # super().allowed__body_position() # This function takes no arguments and returns a list with all cells (x,y) that are filled with your snake.
        # super().allowed__is_king() # returns True if your snake is king else returns False
        # super().allowed__is_knife() # returns True if your snake has a knife else returns False.
        # super().allowed__is_shield() # returns True if your snake is shielded else returns False.

        myPosition = super().allowed__body_position()

        for fruit in board_state["fruits"]:
            if fruit.kind not in FruitKind.harmful_fruits:
                return allowed__calcDirectionForFruit(myPosition, fruit.pos) 

        return Direction.DOWN


    
