from snakes_battle.snake import Snake, Direction
from snakes_battle.fruit import FruitKind


class ChaimSnake(Snake):
    def __init__(self, borders_cells, color, name) -> None:
        super().__init__(color, name)

        self.version = 1.0
        self.border_cells = borders_cells
        self.beneficial_fruits = [fruit['name']
                                  for fruit in FruitKind.beneficial_fruits]
        self.harmful_fruits = [fruit['name']
                               for fruit in FruitKind.harmful_fruits]
        self.special_fruits = [fruit['name']
                               for fruit in FruitKind.special_fruits]

    def is_fruit_up_ok(self,fruits):
        for fruit in fruits:
            if self.head[1]-1 == fruit.pos[1] and self.head[0] == fruit.pos[0] and fruit.kind['name'] in self.harmful_fruits:
                # print('up yes')
                return False
        return True

    def is_fruit_down_ok(self, fruits):
        for fruit in fruits:
            if self.head[1]+1 == fruit.pos[1] and self.head[0] == fruit.pos[0] and fruit.kind['name'] in self.harmful_fruits:
                # print('down yes')
                return False
        return True

    def is_fruit_right_ok(self, fruits):
        for fruit in fruits:
            if self.head[0]+1 == fruit.pos[0] and self.head[1] == fruit.pos[1] and fruit.kind['name'] in self.harmful_fruits:
                # print('right yes')
                return False
        return True

    def is_fruit_left_ok(self, fruits):
        for fruit in fruits:
            if self.head[0]-1 == fruit.pos[0] and self.head[1] == fruit.pos[1] and fruit.kind['name'] in self.harmful_fruits:
                # print('left yes')
                return False
        return True
    # check snake not in another

    def is_snake_up_ok(self, snakes):
        for snake in snakes:
            for snake_pos in snake.body_position:
                if self.head[1]-1 == snake_pos[1] and self.head[0] == snake_pos[0]:
                    if self.head[0]+1 == snake_pos[0] and self.head[1] == snake_pos[1]:
                        return ['up', "right"]
                    if self.head[0]-1 == snake_pos[0] and self.head[1] == snake_pos[1]:
                        return ["up", "left"]
                    return ["up"]
        return []

    def is_snake_down_ok(self, snakes):
        for snake in snakes:
            for snake_pos in snake.body_position:
                if self.head[1]+1 == snake_pos[1] and self.head[0] == snake_pos[0]:
                    if self.head[0]+1 == snake_pos[0] and self.head[1] == snake_pos[1]:
                        return ["down", "right"]
                    if self.head[0]-1 == snake_pos[0] and self.head[1] == snake_pos[1]:
                        return ["down", "left"]
                    return ["down"]
        return []

    def is_snake_right_ok(self, snakes):
        for snake in snakes:
            for snake_pos in snake.body_position:
                if self.head[0]+1 == snake_pos[0] and self.head[1] == snake_pos[1]:
                    if self.head[1]-1 == snake_pos[1] and self.head[0] == snake_pos[0]:
                        return ["right", "up"]
                    if self.head[1]+1 == snake_pos[1] and self.head[0] == snake_pos[0]:
                        return ["right", "down"]
                    return ["right"]
        return []

    def is_snake_left_ok(self, snakes):
        for snake in snakes:
            for snake_pos in snake.body_position:
                if self.head[0]-1 == snake_pos[0] and self.head[1] == snake_pos[1]:
                    if self.head[1]-1 == snake_pos[1] and self.head[0] == snake_pos[0]:
                        return ['left', "up"]
                    if self.head[1]+1 == snake_pos[1] and self.head[0] == snake_pos[0]:
                        return ['left', "down"]
                    return ['left']
        return []

    def is_snake_both_ok(self, snakes):
        for snake in snakes:
            for snake_pos in snake.body_position:
                if self.head[0]-1 == snake_pos[0] and self.head[1] == snake_pos[1]:
                    if self.head[1]-1 == snake_pos[1] and self.head[0] == snake_pos[0]:
                        return ['left', "up"]
                    if self.head[0]+1 == snake_pos[0] and self.head[0] == snake_pos[0]:
                        return ['left', "down"]
                    return ['left']
        return []

    def try_to_go(self, up, down, left, right):
        if up:
            return Direction.UP
        elif down:
            return Direction.DOWN
        elif left:
            return Direction.LEFT
        elif right:
            return Direction.RIGHT

    def fruits_to_go(self, fruit, up, down, left, right):
        if self.head[0] > fruit.pos[0]:
            if self.direction == Direction.RIGHT:
                if up:
                    return Direction.UP
                else:
                    return self.try_to_go(up, down, left, right)

            else:
                if left:
                    return Direction.LEFT
                else:
                    return self.try_to_go(up, down, left, right)

        if self.head[0] < fruit.pos[0]:
            if self.direction == Direction.LEFT:
                if up:
                    return Direction.UP
                else:
                    return self.try_to_go(up, down, left, right)

            else:
                if right:
                    return Direction.RIGHT
                else:
                    return self.try_to_go(up, down, left, right)

        if self.head[0] == fruit.pos[0]:

            if self.head[1] < fruit.pos[1]:
                if self.direction == Direction.UP:
                    if right:
                        return Direction.RIGHT
                    else:
                        return self.try_to_go(up, down, left, right)

                else:
                    if down:
                        return Direction.DOWN
                    else:
                        return self.try_to_go(up, down, left, right)

            if self.head[1] > fruit.pos[1]:
                if self.direction == Direction.DOWN:
                    if right:
                        return Direction.RIGHT
                    else:
                        return self.try_to_go(up, down, left, right)
                else:
                    if up:
                        return Direction.UP
                    else:
                        return self.try_to_go(up, down, left, right)

    def check_cells(self):
        for cell in self.border_cells:
            if self.head[1]-1 == cell[1] and self.head[0] == cell[0]:
                # if self.head[0]+1 == cell[0]:
                #     return ['up',"right"]
                # if self.head[0]-1 == cell[0]:
                #     return ["up","left"]
                return ["up"]

            elif self.head[1]+1 == cell[1] and self.head[0] == cell[0]:
                # if self.head[0]+1 == cell[0]:
                #     return ['down',"right"]
                # if self.head[0]-1 == cell[0]:
                #     return ["down","left"]
                return ["down"]
            elif self.head[0]+1 == cell[0] and self.head[1] == cell[1]:
                # if self.head[0]+1 == cell[0]:
                #     return ['down',"right"]
                # if self.head[0]-1 == cell[0]:
                #     return ["down","left"]
                return ["right"]
            elif self.head[0]-1 == cell[0] and self.head[1] == cell[1]:
                # if self.head[0]+1 == cell[0]:
                #     return ['down',"right"]
                # if self.head[0]-1 == cell[0]:
                #     return ["down","left"]
                return ["left"]
        return []

    def make_decision(self, board_state):

        all_fruits = board_state["fruits"]
        fruits = [f for f in all_fruits if f.kind['name']
                  in self.beneficial_fruits or f.kind['name'] in self.special_fruits]
        # ben_fruits = []
        pos = self.body_position
        index_to_go = 0
        all_snakes = board_state['snakes']
        my_snake = [s for s in all_snakes if self == s]
        
        min_far = fruits[0]
        up = right = left = down = True

        # check celss
        if 'up' in self.check_cells():
            up = False
        if 'right' in self.check_cells():
            right = False
        if 'left' in self.check_cells():
            left = False
        if 'down' in self.check_cells():
            down = False
        # /////////////////////////////

        # dont go from up to down
        if self.direction == Direction.UP:
            down = False
        elif self.direction == Direction.DOWN:
            up = False
        elif self.direction == Direction.RIGHT:
            left = False
        elif self.direction == Direction.LEFT:
            right = False
        # /////////////////////////////


        if self.knife or self.king:
            if 'up' in self.is_snake_up_ok(my_snake):
                up = False
            if 'right' in self.is_snake_up_ok(my_snake):
                right = False
            if 'left' in self.is_snake_up_ok(my_snake):
                left = False

            if 'down' in self.is_snake_down_ok(my_snake):
                down = False
            if 'right' in self.is_snake_down_ok(my_snake):
                right = False
            if 'left' in self.is_snake_down_ok(my_snake):
                left = False

            if 'right' in self.is_snake_right_ok(my_snake):
                right = False
            if 'up' in self.is_snake_right_ok(my_snake):
                up = False
            if 'down' in self.is_snake_right_ok(my_snake):
                down = False

            if 'left' in self.is_snake_left_ok(my_snake):
                left = False
            if 'up' in self.is_snake_left_ok(my_snake):
                up = False
            if 'down' in self.is_snake_left_ok(my_snake):
                down = False
        
        else:    
            if 'up' in self.is_snake_up_ok(all_snakes):
                up = False
            if 'right' in self.is_snake_up_ok(all_snakes):
                right = False
            if 'left' in self.is_snake_up_ok(all_snakes):
                left = False

            if 'down' in self.is_snake_down_ok(all_snakes):
                down = False
            if 'right' in self.is_snake_down_ok(all_snakes):
                right = False
            if 'left' in self.is_snake_down_ok(all_snakes):
                left = False

            if 'right' in self.is_snake_right_ok(all_snakes):
                right = False
            if 'up' in self.is_snake_right_ok(all_snakes):
                up = False
            if 'down' in self.is_snake_right_ok(all_snakes):
                down = False

            if 'left' in self.is_snake_left_ok(all_snakes):
                left = False
            if 'up' in self.is_snake_left_ok(all_snakes):
                up = False
            if 'down' in self.is_snake_left_ok(all_snakes):
                down = False

        

        
        if not self.is_fruit_up_ok(all_fruits):
            # return Direction.RIGHT
            up = False
        if not self.is_fruit_down_ok(all_fruits):
            # return Direction.RIGHT
            down = False
        if not self.is_fruit_right_ok(all_fruits):
            # return Direction.RIGHT
            right = False
        if not self.is_fruit_left_ok(all_fruits):
            # return Direction.RIGHT
            left = False
        
        
            
        for index in range(len(fruits)):
            if fruits[index].kind['name'] == 'KING':
                if abs(self.head[0]+self.head[1]-fruits[index].pos[0]+fruits[index].pos[1]) < 15:
                    index_to_go = index
                    return self.fruits_to_go(fruits[index_to_go], up, down, left, right)
            if fruits[index].kind['name'] == 'SHIELD':
                if abs(self.head[0]+self.head[1]-fruits[index].pos[0]+fruits[index].pos[1]) < 25 and not self.shield:
                    index_to_go = index
                    return self.fruits_to_go(fruits[index_to_go], up, down, left, right)    
            
        
        for fruit in fruits:
            for index in range(len(fruits)):
                if abs(self.head[0]+self.head[1]-fruits[index].pos[0]+fruits[index].pos[1]) < abs(self.head[0]+self.head[1]-min_far.pos[0]+min_far.pos[1]):
                    if fruits[index].kind['name']=='KNIFE' and self.knife:
                        pass
                    elif fruits[index].kind['name']=='SHIELD' and self.shield:
                        pass
                    else:
                        min_far = fruits[index]
        # if min_far.kind['name'] in self.beneficial_fruits or min_far.kind['name'] in self.special_fruits:
        return self.fruits_to_go(min_far, up, down, left, right)

        
        return Direction.CONTINUE
