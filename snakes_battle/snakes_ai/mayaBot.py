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
    
    # find the closest fruit to my snake
    def allowed__findClosestFruitPosition(self, snakePosition, fruits):
        minDistance = self.allowed__calcDistance(snakePosition, fruits[0].pos)
        closestFruitPoisiton = fruits[0].pos
        for f in fruits:
            currentDistance = self.allowed__calcDistance(snakePosition, f.pos)
            if currentDistance < minDistance:
                minDistance = currentDistance
                closestFruitPoisiton = f.pos
        return closestFruitPoisiton
    
    # find the closest snakes to my snake
    def allowed__findClosestSnake(self, snakePosition, snakes):
        minDistance = self.allowed__calcDistance(snakePosition, snakes[0].body_pos[0])
        closestSnake = snakes[0]
        for s in snakes:
            currentDistance = self.allowed__calcDistance(snakePosition, s.body_pos[0])
            if currentDistance < minDistance:
                minDistance = currentDistance
                closestSnake = s
        return closestSnake
    
    # get a direction and return the opposite direction
    def allowed__calcOppositeDirectionFromOtherSnake(self, otherSnakeDirection, myDirection):
        if otherSnakeDirection == Direction.RIGHT:
            if myDirection == Direction.RIGHT:
                return Direction.UP
            else:
                return Direction.LEFT
        elif otherSnakeDirection == Direction.LEFT:
            if myDirection == Direction.LEFT:
                return Direction.UP
            else:
                return Direction.RIGHT
        elif otherSnakeDirection == Direction.UP:
            if myDirection == Direction.UP:
                return Direction.RIGHT
            else:
                return Direction.DOWN
        elif otherSnakeDirection == Direction.DOWN:
            if myDirection == Direction.DOWN:
                return Direction.RIGHT
            else:
                return Direction.UP

    # check if my head is close to any part of other snake and if yes return this snake part. if not return none      
    def allowed__findOtherSnakeClosestBodyPart(self, myHead, otherSnakePosition):
        for i in range(0, len(otherSnakePosition)):
            if self.allowed__calcDistance(myHead, otherSnakePosition[i]) == 1:
                return otherSnakePosition[i]
        return None

    # if the next cell is safe return true and false if not 
    def allowed__isCellSafe(self, allSnakesPositions, wantedCell):
        # make sure the snake is not killing itself or touching other snakes 
        #for pos in myPosition:
            # if myDirection == Direction.RIGHT and [myHead[0] + 1, myHead[1]] == pos:
            #     return False
            # elif myDirection == Direction.LEFT and [myHead[0] - 1, myHead[1]] == pos:
            #     return False
            # elif myDirection == Direction.UP and [myHead[0], myHead[1] + 1] == pos:
            #     return False
            # elif myDirection == Direction.DOWN and [myHead[0], myHead[1] - 1] == pos:
            #     return False
                # elif pos in self.allowed__border_cells:
                #     return False
        for snakePosition in allSnakesPositions:
            if wantedCell in snakePosition:
                return False
            if wantedCell in self.allowed__border_cells:
                return False
        return True
          
    # checks all options and finds a safe cell to go 
    def allowed__findSafeCell(self, currentCell, allSnakePositions, direction):
        newCell = [currentCell[0] + 1, currentCell[1]]
        if direction == Direction.RIGHT and self.allowed__isCellSafe(allSnakePositions, newCell):
            return newCell
        newCell = [currentCell[0] - 1, currentCell[1]]
        if direction == Direction.LEFT and self.allowed__isCellSafe(allSnakePositions, newCell):
            return newCell
        newCell = [currentCell[0], currentCell[1] + 1]
        if direction == Direction.UP and self.allowed__isCellSafe(allSnakePositions, newCell):
            return newCell
        newCell = [currentCell[0], currentCell[1] - 1]
        if direction == Direction.DOWN and self.allowed__isCellSafe(allSnakePositions, newCell):
            return newCell
        # newCell = [currentCell[0] + 1, currentCell[1]]
        # if self.allowed__isCellSafe(newCell, positions, direction):
        #     return newCell
        # newCell = [currentCell[0] - 1, currentCell[1]]
        # if self.allowed__isCellSafe(newCell, positions, direction):
        #     return newCell
        # newCell = [currentCell[0], currentCell[1] + 1]
        # if self.allowed__isCellSafe(newCell, positions, direction):
        #     return newCell
        # newCell = [currentCell[0], currentCell[1] -1]
        # if self.allowed__isCellSafe(newCell, positions, direction):
        #     return newCell
        return None
            
    def make_decision(self, board_state):
        myPosition = super().allowed__body_position()
        myHead = myPosition[0]
        isKing = super().allowed__is_king()
        isKnife = super().allowed__is_knife()
        isSheild = super().allowed__is_shield()
        myDirection = super().allowed__get_direction()

        snakesWithoutMe = [s for s in board_state["snakes"] if type(s)!=MayaWins]
        allSnakesPositions = [s.body_pos for s in board_state["snakes"]]
        closestSnake = self.allowed__findClosestSnake(myHead, snakesWithoutMe)
        closestSnakeBodyPart = self.allowed__findOtherSnakeClosestBodyPart(myHead, closestSnake.body_pos)

        # if another snake is close to me - distance is 1 
        if closestSnakeBodyPart:
            if isKing or isKnife:
                if self.allowed__isCellSafe(allSnakesPositions, closestSnakeBodyPart) or isSheild or isKing:
                    return self.allowed__calcDirection(myHead, myDirection, closestSnakeBodyPart)
                else:
                    safeCell = self.allowed__findSafeCell(myHead, allSnakesPositions, myDirection)
                    return self.allowed__calcDirection(myHead, myDirection, safeCell)
            else:
                if self.allowed__isCellSafe(allSnakesPositions, closestSnakeBodyPart) or isSheild or isKing:
                    return self.allowed__calcOppositeDirectionFromOtherSnake(closestSnake.direction, myDirection)
                else:
                    safeCell = self.allowed__findSafeCell(myHead, allSnakesPositions, myDirection)
                    return self.allowed__calcDirection(myHead, myDirection, safeCell)
        else:
            non_harmful_fruits = [f for f in board_state["fruits"] if f.kind not in FruitKind.harmful_fruits]
            closestFruitPosition = self.allowed__findClosestFruitPosition(myHead, non_harmful_fruits)
            if self.allowed__isCellSafe(allSnakesPositions, closestFruitPosition) or isSheild or isKing:
                return self.allowed__calcDirection(myHead, myDirection, closestFruitPosition)
            else:
                safeCell = self.allowed__findSafeCell(myHead, allSnakesPositions, myDirection)
                return self.allowed__calcDirection(myHead, myDirection, safeCell)

 
        




    
