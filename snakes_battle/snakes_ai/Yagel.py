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
        snakes = board_state["snakes"]
        pos = super().allowed__body_position()

        bombs = []
        bombs = [x.pos for x in fruits if x.kind in FruitKind.harmful_fruits]
        fruits = [x for x in fruits if not x.kind in FruitKind.harmful_fruits]
        snakes_pos = [x.body_pos for x in snakes]

        fruits = allowed__bubbleSort(fruits,pos[0])
        
        # print("fruits[0].pos")
        # print(fruits[0].pos[0])
        # print("snakes_pos")
        # print(snakes_pos)
        # print(board_state["snakes"][1].body_pos[0][0])
        
        if super().allowed__is_king() or super().allowed__is_knife():
            if len(board_state["snakes"]) > 1:
                for snake in board_state["snakes"]:
                    if snake.name != self.name:
                        print(snake.body_pos[0][0])
                        fruits[0].pos[0] = snake.body_pos[0][0]
                        print(snake.body_pos[0][1])
                        fruits[0].pos[0] = snake.body_pos[0][1]
        #     fruits[0].pos[0] = snakes_pos[0][0][0]
        #     fruits[0].pos[1] = snakes_pos[0][0][1]

        if len(fruits) != 0:
            x = pos[0][0]
            y = pos[0][1]
            if x > fruits[0].pos[0]:
                if (self.direction == Direction.RIGHT):
                    if ([x,y-1] not in super().allowed__body_position() and [x,y-1] not in bombs and [x,y-1] not in self.allowed__border_cells and [x,y-1] not in snakes_pos):
                            return Direction.UP
                    else:
                        return allowed__check_ifhithimself(x,y,"UP","RIGHT",super().allowed__body_position(),bombs,snakes_pos)
                elif ([x-1,y] not in super().allowed__body_position() and [x-1,y] not in bombs and [x-1,y] not in self.allowed__border_cells and [x-1,y] not in snakes_pos):
                    return Direction.LEFT
                else:
                    return allowed__check_ifhithimself(x,y,"LEFT","LEFT",super().allowed__body_position(),bombs,snakes_pos)


            if x < fruits[0].pos[0]:
                if (self.direction == Direction.LEFT):
                    if ([x,y-1] not in super().allowed__body_position() and [x,y-1] not in bombs and [x,y-1] not in self.allowed__border_cells and [x,y-1] not in snakes_pos):
                        return Direction.UP
                    else:
                        return allowed__check_ifhithimself(x,y,"UP","LEFT",super().allowed__body_position(),bombs,snakes_pos)
                elif ([x+1,y] not in super().allowed__body_position() and [x+1,y] not in bombs and [x+1,y] not in self.allowed__border_cells and [x+1,y] not in snakes_pos):
                    return Direction.RIGHT
                else:
                    return allowed__check_ifhithimself(x,y,"RIGHT","RIGHT",super().allowed__body_position(),bombs,snakes_pos)


            if x == fruits[0].pos[0]:

                if y < fruits[0].pos[1]:
                    if (self.direction == Direction.UP):
                        if ([x+1,y] not in super().allowed__body_position() and [x+1,y] not in bombs and [x+1,y] not in self.allowed__border_cells and [x+1,y] not in snakes_pos):
                            return Direction.RIGHT
                        else:
                            return allowed__check_ifhithimself(x,y,"RIGHT","UP",super().allowed__body_position(),bombs,snakes_pos)
                    elif ([x,y+1] not in super().allowed__body_position() and [x,y+1] not in bombs and [x,y+1] not in self.allowed__border_cells and [x,y+1] not in snakes_pos):
                        return Direction.DOWN
                    else:
                        return allowed__check_ifhithimself(x,y,"DOWN","DOWN",super().allowed__body_position(),bombs,snakes_pos)

                if y > fruits[0].pos[1]:
                    if (self.direction == Direction.DOWN):
                        if ([x+1,y] not in super().allowed__body_position() and [x+1,y] not in bombs and [x+1,y] not in self.allowed__border_cells and [x+1,y] not in snakes_pos):
                            return Direction.RIGHT
                        else:
                            return allowed__check_ifhithimself(x,y,"RIGHT","DOWN",super().allowed__body_position(),bombs,snakes_pos)
                    elif ([x,y-1] not in super().allowed__body_position() and [x,y-1] not in bombs and [x,y-1] not in self.allowed__border_cells and [x,y-1] not in snakes_pos):
                        return Direction.UP
                    else:
                        return allowed__check_ifhithimself(x,y,"UP","UP",super().allowed__body_position(),bombs,snakes_pos)

        super().allowed__get_direction() # This function takes no arguments and returns the direction of the snake.
        super().allowed__body_position() # This function takes no arguments and returns a list with all cells (x,y) that are filled with your snake.
        super().allowed__is_king() # returns True if your snake is king else returns False
        super().allowed__is_knife() # returns True if your snake has a knife else returns False.
        super().allowed__is_shield() # returns True if your snake is shielded else returns False.

        # for fruit in board_state["fruits"]:
        #     if fruit.kind == FruitKind.DRAGON_FRUIT:
        #         # do_something()

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

def allowed__check_ifhithimself(x,y,nextStep,headSide,allSnake,bomb,snakes_pos):
    if nextStep == "UP" and headSide == "RIGHT":
        if [x,y+1] not in allSnake and [x,y+1] not in bomb and [x,y+1] not in snakes_pos:
            return Direction.DOWN
        elif [x+1,y] not in allSnake and [x+1,y] not in bomb and [x+1,y] not in snakes_pos:
            return Direction.RIGHT   
    elif nextStep == "UP" and headSide == "LEFT":
        if [x,y+1] not in allSnake and [x,y+1] not in bomb and [x,y+1] not in snakes_pos:
            return Direction.DOWN
        elif [x-1,y] not in allSnake and [x-1,y] not in bomb and [x-1,y] not in snakes_pos:
            return Direction.LEFT

    elif nextStep == "DOWN" and headSide == "DOWN":
        if [x+1,y] not in allSnake and [x+1,y] not in bomb and [x+1,y] not in snakes_pos:
            return Direction.RIGHT
        elif [x-1,y] not in allSnake and [x-1,y] not in bomb and [x-1,y] not in snakes_pos:
            return Direction.LEFT
    elif nextStep == "LEFT" and headSide == "LEFT":
        if [x,y-1] not in allSnake and [x,y-1] not in bomb and [x,y-1] not in snakes_pos:
            return Direction.UP
        elif [x,y+1] not in allSnake and [x,y+1] not in bomb and [x,y+1] not in snakes_pos:
            return Direction.DOWN


    elif nextStep == "RIGHT" and headSide == "DOWN":
        if [x,y+1] not in allSnake and [x,y+1] not in bomb and [x,y+1] not in snakes_pos:
            return Direction.DOWN
        elif [x-1,y] not in allSnake and [x-1,y] not in bomb and [x-1,y] not in snakes_pos:
            return Direction.LEFT

    elif nextStep == "RIGHT" and headSide == "UP":
        if [x-1,y] not in allSnake and [x-1,y] not in bomb and [x-1,y] not in snakes_pos:
            return Direction.LEFT
        elif [x,y-1] not in allSnake and [x,y-1] not in bomb and [x,y-1] not in snakes_pos:
            return Direction.UP
    
    elif nextStep == "UP" and headSide == "UP":
        if [x+1,y] not in allSnake and [x+1,y] not in bomb and [x+1,y] not in snakes_pos:
            return Direction.RIGHT
        elif [x-1,y] not in allSnake and [x-1,y] not in bomb and [x-1,y] not in snakes_pos:
            return Direction.LEFT

    elif nextStep == "RIGHT" and headSide == "RIGHT":
        if [x,y-1] not in allSnake and [x,y-1] not in bomb and [x,y-1] not in snakes_pos:
            return Direction.UP
        elif [x,y+1] not in allSnake and [x,y+1] not in bomb and [x,y+1] not in snakes_pos:
            return Direction.DOWN