from math import sqrt
from random import triangular
from snakes_battle.fruit import FruitKind, Fruit
from snakes_battle.snake import Snake, Direction
from pprint import pprint
import random
import time
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
        self.distanceToTarget = 999
        self.timesLost = 0
        print(self.name)

        # All the cells that are fill with borders. This variable will store a list of (x, y) pairs
        self.allowed__border_cells = borders_cells

    
    def make_decision(self, board_state):
        # print(self.allowed__border_cells)
        # time.sleep(0.1)
        # You can only call methods that starts with the word 'allowed__'. You can't change attrbiutes directly.

        direction = super().allowed__get_direction() # This function takes no arguments and returns the direction of the snake.
        body_pos = super().allowed__body_position() # This function takes no arguments and returns a list with all cells (x,y) that are filled with your snake.
        is_king = super().allowed__is_king() # returns True if your snake is king else returns False
        is_knife = super().allowed__is_knife() # returns True if your snake has a knife else returns False.
        is_shield = super().allowed__is_shield() # returns True if your snake is shielded else returns False.
        # print("hello")
        head = body_pos[0]
        allowedNextPositions = get_allowedNextPositions(head, direction)
        # print("1111")
        interestingFruits = getInterestingFruits(board_state["fruits"])
        # print("222")
        heads_of_other = getHeadsOfOthers(board_state["snakes"], self.name)
        bestFruit_length = get_closestFruit(body_pos[0], interestingFruits, heads_of_other, self)
        nexDir =  getDirToGoToGivenPosition(head, direction, bestFruit_length.pos)
        # if(len(heads_of_other)>0):  
        #     nexDir =  getDirToGoToGivenPosition(head, direction, (heads_of_other[0][0]+3, heads_of_other[0][1]))
        
        # previousDist = self.distanceToTarget
        # self.distanceToTarget = calculateDistance(head, bestFruit_length.pos)
        # if(previousDist<=self.distanceToTarget):
        #     self.timesLost += 1
        # else:
        #     self.timesLost=0
        # if(self.timesLost>2):
        #     nexDir =  getDirToGoToGivenPosition(head, direction, random.choice(interestingFruits))
        #     self.timesLost = 0
        if(self.knife):
            if(len(board_state["snakes"])>1):
                target = getOpenentHead(board_state["snakes"], self.name)
                if(self.knife):
                    nexDir = getDirToGoToGivenPosition(head, direction, target)
        if(self.king):
            if(len(board_state["snakes"])>1):
                target = getOpenentNeck(board_state["snakes"], self.name)
                if((self.king and calculateDistance(head, target)<15)):
                    nexDir = getDirToGoToGivenPosition(head, direction, target)

        # if(self.shield):
        #     if(len(board_state["snakes"])>1):
        #         target = getOpenentHead(board_state["snakes"], self.name)
        #         if(self.shield):
        #             nexDir = getDirToGoToGivenPosition(head, direction, target)
        nextPos = calcNextPos(head, nexDir)

        #we have a wish, check it now

        notGoodFruits = getNotGoodFruits(board_state["fruits"])
        allOtherSnakes = getAllOtherSnakes(board_state["snakes"], self.name)
        notDiePositions = []
        # for allowedNext in allowedNextPositions:
        #     if(not willDie(allowedNext, body_pos, notGoodFruits, self.allowed__border_cells, allOtherSnakes)):
        #         notDiePositions.append(allowedNext)
        allowed_directions = [Direction.RIGHT, Direction.LEFT, Direction.UP, Direction.DOWN]
        allowed_directions.remove(getopositeDir(direction))
        if(willDie(nextPos, body_pos, notGoodFruits, self.allowed__border_cells, allOtherSnakes)):
            allowed_directions.remove(nexDir)
            print(allowed_directions, "allowed_directions")
            print("I WILL ALMOST DIE from ", nexDir)
            nexDir = random.choice(allowed_directions)
            if(direction in allowed_directions):
                nexDir = direction
            nextPos = calcNextPos(head, nexDir)
            if(willDie(nextPos, body_pos, notGoodFruits, self.allowed__border_cells, allOtherSnakes)):
                print("@@@I WILL ALMOST DIE@@@")
                allowed_directions.remove(nexDir)
                nexDir = random.choice(allowed_directions)
                if(direction in allowed_directions):
                    nexDir = direction
                nextPos = calcNextPos(head, nexDir)
                if(willDie(nextPos, body_pos, notGoodFruits, self.allowed__border_cells, allOtherSnakes)):
                    print("###@@@I WILL ALMOST DIE@@@###")
                    allowed_directions.remove(nexDir)
                    nexDir = random.choice(allowed_directions)
                    if(direction in allowed_directions):
                        nexDir = direction
                    nextPos = calcNextPos(head, nexDir)
                else:
                    print(nextPos, "WAS CHOSEN level3")
                    return nexDir
            else:
                print(nextPos, "WAS CHOSEN level2")
                return nexDir
        else:
            # print(nextPos, "WAS CHOSEN level3")
            return nexDir

        # print("nextPos", nextPos)
        # print("currentPosition", head)
        # print("notDiePositions", notDiePositions)
        # while(nextPos not in notDiePositions):
        #     if(len(notDiePositions)>=1):
        #         # nextPos = notDiePositions[0]
        #         nextPos = random.choice(notDiePositions)
        #         nexDir = getDirToGoToGivenPosition(head, direction, nextPos)
        #         return nexDir
        #     return nexDir

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

        # while(willDie(nextPos, body_pos, notGoodFruits, self.allowed__border_cells, allOtherSnakes)):
        #     nexDir = checkPos(nextPos, direction, nexDir, body_pos, notGoodFruits, self.allowed__border_cells, allOtherSnakes)
        #     nextPos = calcNextPos(head, nexDir)

        # nexDir = checkPos(nextPos, direction, nexDir, body_pos, notGoodFruits, self.allowed__border_cells, allOtherSnakes)
        # nextPos = calcNextPos(head, nexDir)
        # nexDir = checkPos(nextPos, direction, nexDir, body_pos, notGoodFruits, self.allowed__border_cells, allOtherSnakes)
        # nextPos = calcNextPos(head, nexDir)
        # nexDir = checkPos(nextPos, direction, nexDir, body_pos, notGoodFruits, self.allowed__border_cells, allOtherSnakes)        
        # nextPos = calcNextPos(head, nexDir)
        # nexDir = checkPos(nextPos, direction, nexDir, body_pos, notGoodFruits, self.allowed__border_cells, allOtherSnakes)
        # nexDir = checkPos(nextPos, direction, nexDir, body_pos, notGoodFruits, self.allowed__border_cells, allOtherSnakes)
        # nextPos = calcNextPos(head, nexDir)
        # nexDir = checkPos(nextPos, direction, nexDir, body_pos, notGoodFruits, self.allowed__border_cells, allOtherSnakes)
        # print("turning ", nexDir)
        return nexDir



        # print(bestFruit_length.pos, bestFruit_length.kind)
        # return Direction.DOWN
        # for fruit in board_state["fruits"]:
        #     pprint(fruit.pos)
        #     if fruit.kind == FruitKind.DRAGON_FRUIT:
        #         # self.do_something()
        #         print("jon")
def getHeadsOfOthers(snakes, name):
    heads = []
    for snake in snakes:
        if(name != snake.name):
            heads.append(snake.body_pos[0])
    return heads
def get_allowedNextPositions(head, direction):
    x = head[0]
    y = head[1]
    allowed = []
    if(direction==Direction.UP):
        allowed = [[x-1, y], [x,y-1], [x+1, y]]
    if(direction==Direction.DOWN):
        allowed = [[x-1, y], [x,y+1], [x+1, y]]
    if(direction==Direction.RIGHT):
        allowed = [[x, y+1], [x,y-1], [x+1, y]]
    if(direction==Direction.UP):
        allowed = [[x, y+1], [x,y-1], [x-1, y]]
    return allowed
def willDie(nextPos, body_pos, notGoodFruits, borders, allOtherSnakes):
    print(nextPos)
    if(nextPos[0]==0 or nextPos[1]==0 or nextPos[0]==41 or nextPos[1]==41):
        return True
    # print(nextPos in (body_pos + notGoodFruits + borders + allOtherSnakes))
    return nextPos in (body_pos + notGoodFruits + borders + allOtherSnakes)
def checkPos(nextPos, direction, nexDir,  body_pos, notGoodFruits, borders, allOtherSnakes):
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
        if(nextPos in borders):
            print("I WILL DIE FROM WALL")
            changeDir = (nexDir+1)%4
            if(changeDir==direction or changeDir==getopositeDir(direction)):
                return (changeDir+1)%4
        
        if(nextPos in allOtherSnakes):
            print("I WILL DIE FROM OTHER SNAKE")
            changeDir = (nexDir+1)%4
            if(changeDir==direction or changeDir==getopositeDir(direction)):
                return (changeDir+1)%4
        return nexDir
def getOpenentNeck(snakes, name):
    for snake in snakes:
        if(snake.name != name):
            return snake.body_pos[1]

def getOpenentHead(snakes, name):
    for snake in snakes:
        if(snake.name != name):
            return snake.body_pos[0]
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
            # print(snake.name)
            allSnakes = allSnakes + snake.body_pos
    # print(allSnakes)
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

def get_closestFruit(MyPosition, fruits, headsOfOthers, me):
    if(len(fruits)==0):
        jonas = Fruit(pos = [20, 20], fruitKind="jonas") 
        return jonas 
    min_dist = 999
    bestFruitPosition = (-1,-1)
    for fruit in fruits:
        currentDist = calculateDistance(MyPosition, fruit.pos)
        if(fruit.kind == FruitKind.KING and len(headsOfOthers)!=0):
            if(fruit.lifespan>currentDist):
                # if(iAmTheClosestSnakeToFruit(MyPosition, fruit.pos, headsOfOthers)):
                #     print("king")
                return fruit
        if(fruit.kind == FruitKind.SHIELD and not me.shield and len(headsOfOthers)!=0):
            if(fruit.lifespan>currentDist):
                print("shield")
                return fruit
                
                # if(iAmTheClosestSnakeToFruit(MyPosition, fruit.pos, headsOfOthers)):
                #     print("shield")
                #     return fruit
        if(fruit.kind == FruitKind.KNIFE and len(headsOfOthers)!=0):
            if(fruit.lifespan>currentDist):
                # if(iAmTheClosestSnakeToFruit(MyPosition, fruit.pos, headsOfOthers)):
                    # print("knife")
                return fruit
        # print(currentDist, fruit.kind["name"])
        if(currentDist<min_dist):
        #     min_dist = currentDist
        #     bestFruitPosition = fruit

            if(not iAmTheClosestSnakeToFruit(MyPosition, fruit.pos, headsOfOthers)):
                # bestFruitPosition = fruit
                if(bestFruitPosition == (-1,-1)):
                    min_dist = currentDist
                    bestFruitPosition = fruit
            else:
                # if(bestFruitPosition == (-1,-1)):
                min_dist = currentDist
                bestFruitPosition = fruit
        else:
            if(bestFruitPosition == (-1,-1)):
                    min_dist = currentDist
                    bestFruitPosition = fruit

    # print(fruit.kind["name"])
    return bestFruitPosition

def iAmTheClosestSnakeToFruit(myPosition, fruit, headOfOthers):
    # print("IN")
    if(len(headOfOthers)>0):
        return(calculateDistance(myPosition, fruit)>=calculateDistance(headOfOthers[0],fruit)) 
    else:
        return True
    # print("OUT")             
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
    
