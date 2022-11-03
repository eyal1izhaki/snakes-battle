from snakes_battle.snake import Snake, Direction
from snakes_battle.fruit import FruitKind
76
class ElitzSnake(Snake):
    def __init__(self, borders_cells, color, name) -> None:
        super().__init__(color, name)
        self.version = 1.0
        self.border_cells = borders_cells
        
    def its_bad(self , frutis, next_index):
        for fruit in frutis:
            if fruit.kind in FruitKind.harmful_fruits and next_index == fruit.pos:
                return False
            else:
                return True


    
    def make_decision(self, board_state):
        min_distance = 100000
        fruits = board_state["fruits"]
        pos = self.body_position
        head = pos[0] 

        for item in fruits:
            dic = abs(item.pos[0] - pos[0][0]) + abs(item.pos[1] - pos[0][1])
            if dic > min_distance:
                continue
            else:
                if item.kind not in FruitKind.harmful_fruits:
                    the_fruit = item
                    if item.kind in FruitKind.special_fruits:
                        break

        if self.direction == 0:
                if  [head[0]+1,head[1]] in pos:
                    if [head[0],head[1]-1] in pos or head[1]-1 == 0:
                        return Direction.DOWN

        if self.direction == 1:
            if  [head[0]-1,head[1]] in pos  or head[0]-1 == 0:
                if [head[0],head[1]-1] in pos or head[1]-1 == 0:
                    return Direction.DOWN
                

        if self.direction == 2:
            if  [head[0],head[1]-1] in pos or head[1]-1 == 0 :
                if [head[0]-1,head[1]] in pos or head[0]-1 == 0:
                    return Direction.RIGHT

        if self.direction == 3:
            if  [head[0],head[1]+1] in pos :
                if [head[0]-1,head[1]] in pos or head[0]-1 == 0:
                    return Direction.RIGHT

        
        if pos[0][0] > the_fruit.pos[0]:
            if self.direction == Direction.RIGHT:
                if [head[0], head[1]-1] not in pos and head[1]-1 != 0:
                    if self.its_bad(fruits, [head[0],head[1]+1]):
                        return Direction.UP
                else:
                    return Direction.DOWN
            else:
                return Direction.LEFT
        
        if pos[0][0] < the_fruit.pos[0]:
            if self.direction == Direction.LEFT:
                if [head[0], head[1]-1] not in pos and head[1]-1 != 0:
                    if self.its_bad(fruits, [head[0],head[1]+1]):
                        return Direction.UP
                else:
                    return Direction.DOWN
            else:
                return Direction.RIGHT
        
        if pos[0][0] == the_fruit.pos[0]:
            if pos[0][1] < the_fruit.pos[1]:
                if self.direction == Direction.UP:
                    if [head[0]+1, head[1]] not in pos and head[1]+1 !=39:
                        if self.its_bad(fruits , [head[0]+1, head[1]]):
                            return Direction.RIGHT
                    else:
                        return Direction.LEFT
                else:
                    return Direction.DOWN

            if pos[0][1] > the_fruit.pos[1]:
                if self.direction == Direction.DOWN:
                    if [head[0]+1, head[1]] not in pos and head[1]+1 !=39:
                        if self.its_bad(fruits , [head[0]+1, head[1]]):
                            return Direction.RIGHT
                    else:
                        return Direction.LEFT
                else:
                    return Direction.UP
    
        return Direction.CONTINUE