from snakes_battle.snake import Snake, Direction
from snakes_battle.fruit import FruitKind

class Yakov(Snake):
    def __init__(self, borders_cells, color, name) -> None:
        super().__init__(color, name)

        self.version = 1.0
        self.border_cells = borders_cells

    def get_best(self,fruits, head, bads=[], direction = -1):
        best  = [0,0]
        distance = 10000000000
        for fruit in fruits:
            dis = abs(head[0]-fruit.pos[0])+ abs(head[1]-fruit.pos[1])
            if fruit.kind in FruitKind.beneficial_fruits or fruit.kind in FruitKind.special_fruits:
                if dis< distance and fruit.pos not in bads:
                    distance = dis
                    best = fruit.pos

        if distance == 10000000000:
            if direction == Direction.RIGHT:
                best = [head[0]-1,head[1]]
            elif direction == Direction.LEFT:
                best = [head[0]+1,head[1]]
            elif direction == Direction.UP:
                best = [head[0],head[1]+1]
            elif direction == Direction.DOWN:
                best = [head[0]-1,head[1]-1]

        return best

    def bad_next(self,direction,head,snakes, my_snake , fruits):
        next = [0,0]
        if direction == Direction.RIGHT:
            next = [head[0]+1,head[1]]
        elif direction == Direction.LEFT:
            next = [head[0]-1,head[1]]
        elif direction == Direction.UP:
            next = [head[0],head[1]-1]
        elif direction == Direction.DOWN:
            next = [head[0]-1,head[1]+1]

        bad_cells = []
        for snake in snakes:
            body = snake.body_position
            for i in body:
                if i not in my_snake:
                    bad_cells.append(i)
        
        for fruit in fruits:
            if fruit.kind in FruitKind.harmful_fruits:
                bad_cells.append(fruit.pos)
        
        for cell in bad_cells:
            if [next[0]+1,next[1]] == cell or [next[0]-1,next[1]]== cell or [next[0],next[1]-1]== cell or [next[0],next[1]+1]== cell:
                return True
        
        if next in my_snake:
            return True

        return False

    def make_decision(self, board_state):

        fruits = board_state["fruits"]
        snakes = board_state["snakes"]

        my_position = self.body_position
        close = self.get_best(fruits, my_position[0])
        bads = []
        direction = Direction.CONTINUE

        if my_position[0][0] > close[0]:
            if self.direction == Direction.RIGHT:
                direction = Direction.UP
            else:
                direction = Direction.LEFT
        
        if my_position[0][0] < close[0]:
            if self.direction == Direction.LEFT:
                direction = Direction.UP
            else:
                direction = Direction.RIGHT
        
        if my_position[0][0] == close[0]:

            if my_position[0][1] < close[1]:
                if self.direction == Direction.UP:
                    direction = Direction.RIGHT
                else:
                    direction = Direction.DOWN

            if my_position[0][1] > close[1]:
                if self._direction == Direction.DOWN:
                    direction = Direction.RIGHT
                else:
                    direction = Direction.UP
        
        times = 0
        while self.bad_next(direction, my_position[0], snakes, my_position , fruits ) or times > 10: 
            times+=1
            bads.append(close)
            close = self.get_best(fruits, my_position[0],bads, direction)

            if my_position[0][0] > close[0]:
                if self.direction == Direction.RIGHT:
                    direction = Direction.UP
                else:
                    direction = Direction.LEFT
        
            if my_position[0][0] < close[0]:
                if self.direction == Direction.LEFT:
                    direction = Direction.UP
                else:
                    direction = Direction.RIGHT
            
            if my_position[0][0] == close[0]:

                if my_position[0][1] < close[1]:
                    if self.direction == Direction.UP:
                        direction = Direction.RIGHT
                    else:
                        direction = Direction.DOWN

                if my_position[0][1] > close[1]:
                    if self._direction == Direction.DOWN:
                        direction = Direction.RIGHT
                    else:
                        direction = Direction.UP
    
        return direction