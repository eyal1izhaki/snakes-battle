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

    def is_fruit_up_ok(self, fruits):
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
        # if len(snakes)==1:
        #     for snake_pos in snakes[0].body_position:
        #         if self.head[1]-1 == snake_pos[1] and self.head[0]+1 == snake_pos[0] and self.head[0]-1 == snake_pos[0]:
        #             return ["up"]
            
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

    def try_to_go(self, first, second, third, fourth):
        if first:
            return Direction.UP
        elif second:
            return Direction.DOWN
        elif third:
            return Direction.LEFT
        elif fourth:
            return Direction.RIGHT
        else:
            return Direction.CONTINUE

    def fruits_to_go(self, fruit, up, down, left, right):
        if self.head[0] > fruit.pos[0]:
            # added
            # if self.head[1] < fruit.pos[1]:
            #     if self.direction == Direction.RIGHT:
            #         if down:
            #             return Direction.DOWN
            #         else:
            #             return self.try_to_go(up, down, left, right)
            # added

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
    
    def snake_to_go(self, snake_point, up, down, left, right):
        if abs(self.head[0]-snake_point[0]) > abs(self.head[1]-snake_point[1]):
    
            
            if self.head[0] > snake_point[0]:
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

            if self.head[0] < snake_point[0]:
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

        # if self.head[0] == snake_point[0]:
        else:
            if self.head[1] < snake_point[1]:
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

            if self.head[1] > snake_point[1]:
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


    def check_snake_head(self, other_snakes):
        arr_return = []
        for snake in other_snakes:
            if self.head[1]-1 == snake.body_position[0][1] and self.head[0] == snake.body_position[0][0] and snake.direction == Direction.DOWN:
                arr_return.append("up")
            if self.head[1]+1 == snake.body_position[0][1] and self.head[0] == snake.body_position[0][0] and snake.direction == Direction.UP:
                arr_return.append("down")
            if self.head[0]+1 == snake.body_position[0][0] and self.head[1] == snake.body_position[0][1] and snake.direction == Direction.LEFT:
                arr_return.append("right")
            if self.head[0]-1 == snake.body_position[0][0] and self.head[1] == snake.body_position[0][1] and snake.direction == Direction.RIGHT:
                arr_return.append("left")
            if self.head[1]+1 == snake.body_position[0][1]:
                if self.head[0]+1 == snake.body_position[0][0] and snake.direction == Direction.LEFT or snake.direction == Direction.UP:
                    arr_return.append('right')
                    arr_return.append("down")
                elif self.head[0]-1 == snake.body_position[0][0] and snake.direction == Direction.RIGHT or snake.direction == Direction.UP:
                    arr_return.append('left')
                    arr_return.append("down")
            if self.head[1]-1 == snake.body_position[0][1]:
                if self.head[0]+1 == snake.body_position[0][0] and snake.direction == Direction.LEFT or snake.direction == Direction.DOWN:
                    arr_return.append('right')
                    arr_return.append("up")
                elif self.head[0]-1 == snake.body_position[0][0] and snake.direction == Direction.RIGHT or snake.direction == Direction.DOWN:
                    arr_return.append("up")
                    arr_return.append('left')
            if self.head[0]+1 == snake.body_position[0][0]:
                if self.head[1]+1 == snake.body_position[0][1] and snake.direction == Direction.UP or snake.direction == Direction.LEFT:
                    arr_return.append('down')
                    arr_return.append("right")
                elif self.head[1]-1 == snake.body_position[0][1] and snake.direction == Direction.DOWN or snake.direction == Direction.LEFT:
                    arr_return.append('up')
                    arr_return.append("right")
            if self.head[0]-1 == snake.body_position[0][0]:
                if self.head[1]+1 == snake.body_position[0][1] and snake.direction == Direction.UP or snake.direction == Direction.RIGHT:
                    arr_return.append("left")
                    arr_return.append('down')
                elif self.head[1]-1 == snake.body_position[0][1] and snake.direction == Direction.DOWN or snake.direction == Direction.RIGHT:
                    arr_return.append('up')
                    arr_return.append("left")
        return arr_return
    
    def check_other_snake_length(self, other_snakes):
        for snake in other_snakes:
            if ((len(snake.body_position) - len(self.body_position) > 1 and len(self.body_position) > 13) or len(snake.body_position)>9):
                return True
            
    def the_longest_snake(self, other_snakes):
        max_snake = other_snakes[0]
        for snake in other_snakes:
            if len(snake.body_position) > len(max_snake.body_position):
                max_snake=snake
        return max_snake
    
                
            
        

    def make_decision(self, board_state):

        all_fruits = board_state["fruits"]
        fruits = [f for f in all_fruits if f.kind['name']
                  in self.beneficial_fruits or f.kind['name'] in self.special_fruits]
        # ben_fruits = []
        pos = self.body_position
        index_to_go = 0
        all_snakes = board_state['snakes']
        my_snake = [s for s in all_snakes if self == s]
        other_snakes = [s for s in all_snakes if self != s]

        min_far = fruits[0]
        up = right = left = down = True
        # print(len(self.body_position))
        
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

        # check other snake head
        if len(all_snakes)<4:
            if 'up' in self.check_snake_head(other_snakes):
                up = False
            if 'right' in self.check_snake_head(other_snakes):
                right = False
            if 'left' in self.check_snake_head(other_snakes):
                left = False
            if 'down' in self.check_snake_head(other_snakes):
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

        if (self.knife or self.king) and len(all_snakes)<3:
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

        # check the fruit before the snake
        if not self.is_fruit_up_ok(all_fruits):
            up = False
        if not self.is_fruit_down_ok(all_fruits):
            down = False
        if not self.is_fruit_right_ok(all_fruits):
            right = False
        if not self.is_fruit_left_ok(all_fruits):
            left = False

        # if no other snakes
        if len(all_snakes) == 1:
            for index in range(len(fruits)):
                # if fruits[index].kind['name']=='KNIFE' and self.knife or :
                if abs(self.head[0]-fruits[index].pos[0]+self.head[1]-fruits[index].pos[1]) < abs(self.head[0]-min_far.pos[0]+self.head[1]-min_far.pos[1]):
                    if fruits[index].kind['name'] == 'DRAGON_FRUIT':
                        min_far = fruits[index]
                    elif fruits[index].kind['name'] == 'STRAWBERRY' and abs(self.head[0]-fruits[index].pos[0]+self.head[1]-fruits[index].pos[1]) < 2:
                        min_far = fruits[index]
                        

                    elif fruits[index].kind['name'] == 'KNIFE':
                        pass
                    elif fruits[index].kind['name'] == 'KING':
                        pass
                    elif fruits[index].kind['name'] == 'SHIELD' and abs(self.head[0]-fruits[index].pos[0]+self.head[1]-fruits[index].pos[1]) < 10:
                        if not self.shield and len(self.body_position) > 20:
                            min_far = fruits[index]
                        else:
                            pass
                    else:
                        if fruits[index].kind['name'] == 'STRAWBERRY':
                            min_far = fruits[index]

            return self.fruits_to_go(min_far, up, down, left, right)
        
            
            
        elif len(self.body_position) < 13:

            for index in range(len(fruits)):
                if fruits[index].kind['name'] == 'KING':
                    if abs(self.head[0]-fruits[index].pos[0]+self.head[1]-fruits[index].pos[1]) < 10:
                        index_to_go = index
                        return self.fruits_to_go(fruits[index_to_go], up, down, left, right)
                elif fruits[index].kind['name'] == 'SHIELD':
                    if abs(self.head[0]-fruits[index].pos[0]+self.head[1]-fruits[index].pos[1]) < 10 and not self.shield:
                        index_to_go = index
                        return self.fruits_to_go(fruits[index_to_go], up, down, left, right)
                elif fruits[index].kind['name'] == 'KNIFE':
                    if abs(self.head[0]-fruits[index].pos[0]+self.head[1]-fruits[index].pos[1]) < 15 and not self.knife:
                        index_to_go = index
                        return self.fruits_to_go(fruits[index_to_go], up, down, left, right)

                elif abs(self.head[0]-fruits[index].pos[0]+self.head[1]-fruits[index].pos[1]) < abs(self.head[0]-min_far.pos[0]+self.head[1]-min_far.pos[1]) and (fruits[index].kind['name'] == 'STRAWBERRY' or fruits[index].kind['name'] == 'DRAGON_FRUIT'):
                    if fruits[index].kind['name'] == 'DRAGON_FRUIT':
                        min_far = fruits[index]
                    elif fruits[index].kind['name'] == 'STRAWBERRY' and abs(self.head[0]-fruits[index].pos[0]+self.head[1]-fruits[index].pos[1]) < 2:
                        min_far = fruits[index]
                        
                    # min_far = fruits[index]

            # for index in range(len(fruits)):
            #     if abs(self.head[0]-fruits[index].pos[0]+self.head[1]-fruits[index].pos[1]) < abs(self.head[0]-min_far.pos[0]+self.head[1]-min_far.pos[1]):
            #         if fruits[index].kind['name']=='KNIFE' and self.knife:
            #             pass
            #         elif fruits[index].kind['name']=='SHIELD' and self.shield:
            #             pass
            #         else:
            #             min_far = fruits[index]

            # if min_far.kind['name'] in self.beneficial_fruits or min_far.kind['name'] in self.special_fruits:
            return self.fruits_to_go(min_far, up, down, left, right)

        elif (self.knife or self.king) and self.check_other_snake_length(other_snakes):
            return self.snake_to_go(self.the_longest_snake(other_snakes).body_position[1], up, down, left, right)
        else:
            for index in range(len(fruits)):
                if fruits[index].kind['name'] == 'KING':
                    if abs(self.head[0]-fruits[index].pos[0]+self.head[1]-fruits[index].pos[1]) < 15:
                        index_to_go = index
                        return self.fruits_to_go(fruits[index_to_go], up, down, left, right)
                elif fruits[index].kind['name'] == 'SHIELD':
                    if abs(self.head[0]-fruits[index].pos[0]+self.head[1]-fruits[index].pos[1]) < 10 and not self.shield:
                        index_to_go = index
                        return self.fruits_to_go(fruits[index_to_go], up, down, left, right)
                elif fruits[index].kind['name'] == 'KNIFE':
                    if abs(self.head[0]-fruits[index].pos[0]+self.head[1]-fruits[index].pos[1]) < 10 and not self.knife:
                        index_to_go = index
                        return self.fruits_to_go(fruits[index_to_go], up, down, left, right)

                elif abs(self.head[0]-fruits[index].pos[0]+self.head[1]-fruits[index].pos[1]) < abs(self.head[0]-min_far.pos[0]+self.head[1]-min_far.pos[1]) and (fruits[index].kind['name'] == 'STRAWBERRY' or fruits[index].kind['name'] == 'DRAGON_FRUIT'):
                    # min_far = fruits[index]
                    if fruits[index].kind['name'] == 'DRAGON_FRUIT':
                        min_far = fruits[index]
                    elif fruits[index].kind['name'] == 'STRAWBERRY' and abs(self.head[0]-fruits[index].pos[0]+self.head[1]-fruits[index].pos[1]) < 2:
                        min_far = fruits[index]
                        

            # for index in range(len(fruits)):
            #     if abs(self.head[0]-fruits[index].pos[0]+self.head[1]-fruits[index].pos[1]) < abs(self.head[0]-min_far.pos[0]+self.head[1]-min_far.pos[1]):
            #         if fruits[index].kind['name']=='KNIFE' and self.knife:
            #             pass
            #         elif fruits[index].kind['name']=='SHIELD' and self.shield:
            #             pass
            #         else:
            #             min_far = fruits[index]
            # if min_far.kind['name'] in self.beneficial_fruits or min_far.kind['name'] in self.special_fruits:
            return self.fruits_to_go(min_far, up, down, left, right)
