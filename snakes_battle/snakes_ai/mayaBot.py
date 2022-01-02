from snakes_battle.fruit import FruitKind
from snakes_battle.snake import Snake, Direction
import math

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
    def allowed__calcDistance(self, snakePosition, otherObjectPosition):
        return (abs(snakePosition[0] - otherObjectPosition[0]) + abs(snakePosition[1] - otherObjectPosition[1]))
    
    def allowed__findClosestObjectPosition(self, snakePosition, objects):
        minDistance = self.allowed__calcDistance(snakePosition, objects[0].pos)
        closestObjectPosition = objects[0].pos
        for item in objects:
            currentDistance = self.allowed__calcDistance(snakePosition, item.pos)
            if currentDistance < minDistance:
                minDistance = currentDistance
                closestObjectPosition = item.pos
        return closestObjectPosition
            

    def make_decision(self, board_state):
        myPosition = super().allowed__body_position()
        myHead = myPosition[0]
        isKing = super().allowed__is_king()
        isKnife = super().allowed__is_knife()
        isSheild = super().allowed__is_shield()
        myDirection = super().allowed__get_direction()

        if isKnife:
            for snake in board_state["snakes"]:
                pass


        # TODO - PROIRITZE BETWEEN FRUITS
        non_harmful_fruits = [f for f in board_state["fruits"] if f.kind not in FruitKind.harmful_fruits]
        closestFruitPosition = self.allowed__findClosestObjectPosition(myHead, non_harmful_fruits)
        return self.allowed__calcDirection(myHead, myDirection, closestFruitPosition)

 
        




    
