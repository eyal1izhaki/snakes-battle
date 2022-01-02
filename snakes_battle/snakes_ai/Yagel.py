from snakes_battle.fruit import FruitKind
from snakes_battle.snake import Snake, Direction
import math

class Yagel(Snake):
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
        fruits = board_state["fruits"]
        pos = super().allowed__body_position()

        bombs = []
        bombs = [x for x in fruits if x.kind in FruitKind.harmful_fruits]
        fruits = [x for x in fruits if not x.kind in FruitKind.harmful_fruits]
        
        fruits = allowed__bubbleSort(fruits,pos[0])
        
        if len(fruits) != 0:
            if pos[0][0] > fruits[0].pos[0]:
                if (self.direction == Direction.RIGHT):
                    if [pos[0][0],pos[0][1]+1] not in super().allowed__body_position():
                        return Direction.UP
                    else:
                        return allowed__check_ifhithimself(pos[0][0],pos[0][1],"UP","RIGHT",super().allowed__body_position())
                else:
                    return Direction.LEFT
        
            if pos[0][0] < fruits[0].pos[0]:
                if (self.direction == Direction.LEFT):
                    if [pos[0][0],pos[0][1]+1] not in super().allowed__body_position():
                        return Direction.UP
                    else:
                        return allowed__check_ifhithimself(pos[0][0],pos[0][1],"UP","LEFT",super().allowed__body_position())
                else:
                    return Direction.RIGHT
        
            if pos[0][0] == fruits[0].pos[0]:

                if pos[0][1] < fruits[0].pos[1]:
                    if (self.direction == Direction.UP):
                        if [pos[0][0]+1,pos[0][1]] not in super().allowed__body_position():
                            return Direction.RIGHT
                        else:
                            return allowed__check_ifhithimself([pos[0][0],pos[0][1]],"RIGHT")
                    else:
                        return Direction.DOWN

                if pos[0][1] > fruits[0].pos[1]:
                    if (self.direction == Direction.DOWN):
                        if [pos[0][0]+1,pos[0][1]] not in super().allowed__body_position():
                            return Direction.RIGHT
                        else:
                            return allowed__check_ifhithimself([pos[0][0],pos[0][1]],"RIGHT")
                    else:
                        return Direction.UP

        super().allowed__get_direction() # This function takes no arguments and returns the direction of the snake.
        super().allowed__body_position() # This function takes no arguments and returns a list with all cells (x,y) that are filled with your snake.
        super().allowed__is_king() # returns True if your snake is king else returns False
        super().allowed__is_knife() # returns True if your snake has a knife else returns False.
        super().allowed__is_shield() # returns True if your snake is shielded else returns False.

        for fruit in board_state["fruits"]:
            if fruit.kind == FruitKind.DRAGON_FRUIT:
                do_something()

        return Direction.DOWN

def allowed__bubbleSort(fruits,head):
    n = len(fruits)
    for i in range(n-1):
        for j in range(0, n-i-1):
            if allowed__check_distance(fruits[j],head) > allowed__check_distance(fruits[j+1],head) :
                fruits[j], fruits[j + 1] = fruits[j + 1], fruits[j]
    return fruits

def allowed__check_distance(fruit,head):
    distance = math.pow(head[0]-fruit.pos[0],2) + math.pow(head[1]-fruit.pos[1],2)
    return distance

def allowed__check_ifhithimself(x,y,nextStep,headSide,allSnake):
    if nextStep == "UP" and headSide == "RIGHT":
        if [x,y-1] not in allSnake:
            return Direction.DOWN
        elif [x+1,y] not in allSnake:
            return Direction.RIGHT
    elif nextStep == "UP" and headSide == "LEFT":
        if [x,y-1] not in allSnake:
            return Direction.DOWN
        if [x-1,y] not in allSnake:
            return Direction.LEFT

    elif nextStep == "DOWN" and headSide == "RIGHT":
        if [x+1,y] not in allSnake:
            return Direction.RIGHT
        if [x,y+1] not in allSnake:
            return Direction.UP
    elif nextStep == "DOWN" and headSide == "LEFT":
        if [x-1,y] not in allSnake:
            return Direction.LEFT
        if [x,y+1] not in allSnake:
            return Direction.UP

    # elif nextStep == "RIGHT" and headSide == "DOWN":
    #     if [x,y+1] not in allSnake:
    #         return Direction.UP

    # elif nextStep == "RIGHT" and headSide == "UP":
    #     if [x-1,y] not in allSnake:
    #         return Direction.LEFT
    #     if [x,y+1] not in allSnake:
    #         return Direction.UP
    
    # elif nextStep == "LEFT" and headSide == "DOWN":
    #     if [x+1,y] not in allSnake:
    #         return Direction.RIGHT
    #     if [x,y+1] not in allSnake:
    #         return Direction.UP
    # elif nextStep == "LEFT" and headSide == "UP":
    #     if [x-1,y] not in allSnake:
    #         return Direction.LEFT
    #     if [x,y+1] not in allSnake:
    #         return Direction.UP