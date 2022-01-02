from math import sqrt
from random import triangular
from snakes_battle.fruit import FruitKind, Fruit
from snakes_battle.snake import Snake, Direction
from pprint import pprint

class Jonas(Snake):
    def __init__(self, borders_cells, color, name) -> None:
        super().__init__(color, name)
        self.init(borders_cells)
        

    ##############################
    # You can edit only the code below. You can't change methods names.
    ##############################


    def init(self, borders_cells):
        # Your bot initializations will be here.
        self.allowed__version = 1.0
        self.isWinnerForTheMoment = False
        print(self.name)

        # All the cells that are fill with borders. This variable will store a list of (x, y) pairs
        self.allowed__border_cells = borders_cells

    
    def make_decision(self, board_state):
        # You can only call methods that starts with the word 'allowed__'. You can't change attrbiutes directly.

        direction = super().allowed__get_direction() # This function takes no arguments and returns the direction of the snake.
        body_pos = super().allowed__body_position() # This function takes no arguments and returns a list with all cells (x,y) that are filled with your snake.
        is_king = super().allowed__is_king() # returns True if your snake is king else returns False
        is_knife = super().allowed__is_knife() # returns True if your snake has a knife else returns False.
        is_shield = super().allowed__is_shield() # returns True if your snake is shielded else returns False.
        print("hello")
        head = body_pos[0]
        interestingFruits = getInterestingFruits(board_state["fruits"])
        bestFruit_length = get_closestFruit(body_pos[0], interestingFruits)
        nexDir =  getDirToGoToGivenPosition(head, direction, bestFruit_length.pos)
        if(self.king or self.knife):
            if(len(board_state["snakes"])>1):
                target = getOpenentNeck(board_state["snakes"], self.name)
                nexDir = getDirToGoToGivenPosition(head, direction, target)
        nextPos = calcNextPos(head, nexDir)
        notGoodFruits = getNotGoodFruits(board_state["fruits"])
        allOtherSnakes = getAllOtherSnakes(board_state["snakes"], self.name)
        # self.isWinnerForTheMoment = updateIfIAmTheWinner(board_state["snakes"], self.name, self.length)
        # isInSafeMode = len(board_state["snakes"])==1 and self.isWinnerForTheMoment
        # if(isInSafeMode):
            # print("didfonsdfnoinio")
        changeDir = nexDir
        # while(nextPos in body_pos or nextPos in notGoodFruits or nextPos in self.allowed__border_cells):
        #     changeDir = (nexDir+1)%4
        #     if(changeDir==direction or changeDir==getopositeDir(direction)):
        #         (changeDir+1)%4
        #     nextPos = calcNextPos(head, changeDir)
        # return changeDir
        # if(isInSafeMode):
            # return Direction.DOWN
        if(nextPos in body_pos):
            print("I WILL DIE FROM SNAKE")
            changeDir = (nexDir+1)%4
            if(changeDir==direction or changeDir==getopositeDir(direction)):
                return (changeDir+1)%4
            return changeDir
        if(nextPos in notGoodFruits):
            print("I WILL DIE FROM BOMB")
            changeDir = (nexDir+1)%4
            if(changeDir==direction or changeDir==getopositeDir(direction)):
                return (changeDir+1)%4
            return changeDir
        if(nextPos in self.allowed__border_cells):
            print("I WILL DIE FROM WALL")
            changeDir = (nexDir+1)%4
            if(changeDir==direction or changeDir==getopositeDir(direction)):
                return (changeDir+1)%4
        
        if(nextPos in self.allowed__border_cells):
            print("I WILL DIE FROM WALL")
            changeDir = (nexDir+1)%4
            if(changeDir==direction or changeDir==getopositeDir(direction)):
                return (changeDir+1)%4
        
        if(nextPos in allOtherSnakes):
            print("I WILL DIE FROM OTHER SNAKE")
            changeDir = (nexDir+1)%4
            if(changeDir==direction or changeDir==getopositeDir(direction)):
                return (changeDir+1)%4
        print("turning ", nexDir)
        return nexDir



        # print(bestFruit_length.pos, bestFruit_length.kind)
        # return Direction.DOWN
        # for fruit in board_state["fruits"]:
        #     pprint(fruit.pos)
        #     if fruit.kind == FruitKind.DRAGON_FRUIT:
        #         # self.do_something()
        #         print("jon")
def getOpenentNeck(snakes, name):
    for snake in snakes:
        if(snake.name != name):
            return snake.body_pos[1]
def updateIfIAmTheWinner(snakes, name, myScore):
    maxScore = 0
    for snake in snakes:
            if(maxScore< snake.length):
                maxScore = snake.length
    return myScore==maxScore
def getAllOtherSnakes(snakes, slefName):
    allSnakes = []
    for snake in snakes:
        if(snake.name != slefName):
            print(snake.name)
            allSnakes = allSnakes + snake.body_pos
    print(allSnakes)
    return allSnakes
            # allSnakes = allSnakes + snake.allowed__body_position()
def getopositeDir(direction):
    if(direction == Direction.RIGHT):
        return Direction.LEFT
    if(direction == Direction.LEFT):
        return Direction.RIGHT
    if(direction == Direction.UP):
        return Direction.DOWN
    if(direction == Direction.DOWN):
        return Direction.UP
def calcNextPos(head, direction):
    x = head[0]
    y = head[1]
    if(direction == Direction.RIGHT):
        x = x+1
    if(direction == Direction.LEFT):
        x = x-1
    if(direction == Direction.UP):
        y = y-1
    if(direction == Direction.DOWN):
        y = y+1
    return [x,y]
    
def getNotGoodFruits(fruits):
    not_interestingFruits = []
    not_interestingFruits = [FruitKind.BOMB, FruitKind.SKULL]
    for fruit in fruits:
        if fruit.kind in not_interestingFruits:
            not_interestingFruits.append([fruit.pos[0], fruit.pos[1]])
    return not_interestingFruits
    
def getInterestingFruits(fruits):
    interestingFruits = []
    interestingTypes = [FruitKind.STRAWBERRY, FruitKind.KING, FruitKind.KNIFE, FruitKind.SHIELD, FruitKind.DRAGON_FRUIT]
    for fruit in fruits:
        if fruit.kind in interestingTypes:
            interestingFruits.append(fruit)
    return interestingFruits

def get_closestFruit(MyPosition, fruits):
    if(len(fruits)==0):
        jonas = Fruit(pos = [20, 20], fruitKind="jonas") 
        return jonas 
    min_dist = 999
    bestFruitPosition : any
    for fruit in fruits:
        currentDist = calculateDistance(MyPosition, fruit.pos)
        if(fruit.kind == FruitKind.KING):
            if(fruit.lifespan>currentDist):
                return fruit
        print(currentDist, fruit.kind["name"])
        if(currentDist<min_dist):
            min_dist = currentDist
            bestFruitPosition = fruit
    return bestFruitPosition
                
def calculateDistance(HeadPosition, ElementPosition):
        return sqrt( 
            (HeadPosition[0]-ElementPosition[0])**2 + (HeadPosition[1]-ElementPosition[1])**2
            )

def getDirToGoToGivenPosition(head_position, snakeDirection, goal):
    if head_position[0] > goal[0]:
            if (snakeDirection == Direction.RIGHT):
                return Direction.UP
            else:
                return Direction.LEFT
        
    if head_position[0] < goal[0]:
        if (snakeDirection == Direction.LEFT):
            return Direction.UP
        else:
            return Direction.RIGHT
    
    if head_position[0] == goal[0]:
        if head_position[1] < goal[1]:
            if (snakeDirection == Direction.UP):
                return Direction.RIGHT
            else:
                return Direction.DOWN

        if head_position[1] > goal[1]:
            if (snakeDirection == Direction.DOWN):
                return Direction.RIGHT
            else:
                return Direction.UP
    
