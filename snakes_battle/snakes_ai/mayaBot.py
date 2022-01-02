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
    
    # decide which directin to go based on my snake position and other object position
    def allowed__calcDirection(self, snakePosition, snakeDirection, objectPosition):
        if (snakePosition[0] > objectPosition[0]):
            if (snakeDirection == Direction.RIGHT):
                return Direction.UP
            else:
                return Direction.LEFT
        elif (snakePosition[0] < objectPosition[0]):
            if (snakeDirection == Direction.LEFT):
                return Direction.UP
            else:
                return Direction.RIGHT
        elif (snakePosition[1] > objectPosition[1]):
            if (snakeDirection == Direction.DOWN):
                return Direction.RIGHT
            else:
                return Direction.UP
        elif (snakePosition[1] < objectPosition[1]):
            if (snakeDirection == Direction.UP):
                return Direction.RIGHT
            else:
                return Direction.DOWN

    # calculate the distance between my snake and other object on board
    def allowed__calcDistance(self, snake, otherObject):
        pass


    
    def make_decision(self, board_state):
        myPosition = super().allowed__body_position()
        isKing = super().allowed__is_king()
        isKnife = super().allowed__is_knife()
        isSheild = super().allowed__is_shield()
        myDirection = super().allowed__get_direction()

        if isKnife:
            for snake in board_state["snakes"]:


        # TODO - PROIRITZE BETWEEN FRUITS
        for fruit in board_state["fruits"]:
            if fruit.kind not in FruitKind.harmful_fruits:
                return self.allowed__calcDirection(myPosition[0], myDirection, fruit.pos)
 
        




    
