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
        print(self.harmful_fruits)

    def is_fruit_up_ok(self, fruit):
        if self.direction == Direction.UP and self.head[1]-1 == fruit.pos[1] and fruit.kind['name'] in self.harmful_fruits:
            return False
        # elif self.direction==Direction.DOWN and self.head[1]-1 == fruit.pos[1] and fruit.kind['name'] in self.harmful_fruits:
        #     return False
        return True

    def is_fruit_down_ok(self, fruit):
        if self.direction == Direction.DOWN and self.head[1]+1 == fruit.pos[1] and fruit.kind['name'] in self.harmful_fruits:
            return False
        return True

    def is_fruit_right_ok(self, fruit):
        if self.direction == Direction.RIGHT and self.head[0]+1 == fruit.pos[0] and fruit.kind['name'] in self.harmful_fruits:
            return False
        return True

    def is_fruit_left_ok(self, fruit):
        if self.direction == Direction.LEFT and self.head[0]-1 == fruit.pos[0] and fruit.kind['name'] in self.harmful_fruits:
            return False
        return True

    def is_snake_up_ok(self, snakes):
        for snake in snakes:
            for snake_pos in snake.body_position:
                if self.direction == Direction.UP and self.head[1]-1 == snake_pos[1] and self.head[0] == snake_pos[0]:
                    return "up"
                elif self.direction == Direction.UP and self.head[0]+1 == snake_pos[0] and self.head[1] == snake_pos[1]:
                    return "right"
                elif self.direction == Direction.UP and self.head[0]-1 == snake_pos[0] and self.head[1] == snake_pos[1]:
                    return "left"  
        return True

    def is_snake_down_ok(self, snakes):
        for snake in snakes:
            for snake_pos in snake.body_position:
                if self.direction == Direction.DOWN and self.head[1]+1 == snake_pos[1] and self.head[0] == snake_pos[0]:
                    return "down"
                elif self.direction == Direction.UP and self.head[0]+1 == snake_pos[0] and self.head[1] == snake_pos[1]:
                    return "right"
                elif self.direction == Direction.UP and self.head[0]-1 == snake_pos[0] and self.head[1] == snake_pos[1]:
                    return "left"  
        return True

    def is_snake_right_ok(self, snakes):
        for snake in snakes:
            for snake_pos in snake.body_position:
                if self.direction == Direction.RIGHT and self.head[0]+1 == snake_pos[0] and self.head[1] == snake_pos[1]:
                    return "right"
                elif self.direction == Direction.RIGHT and self.head[1]-1 == snake_pos[1] and self.head[0] == snake_pos[0]:
                    return "up"
                elif self.direction == Direction.RIGHT and self.head[0]+1 == snake_pos[0] and self.head[0] == snake_pos[0]:
                    return "down"
        return True

    def is_snake_left_ok(self, snakes):
        for snake in snakes:
            for snake_pos in snake.body_position:
                if self.direction == Direction.LEFT and self.head[0]-1 == snake_pos[0] and self.head[1] == snake_pos[1]:
                    return 'left'
                elif self.direction == Direction.RIGHT and self.head[1]-1 == snake_pos[1] and self.head[0] == snake_pos[0]:
                    return "up"
                elif self.direction == Direction.RIGHT and self.head[0]+1 == snake_pos[0] and self.head[0] == snake_pos[0]:
                    return "down"
        return True

    def make_decision(self, board_state):
        # print(board_state['snakes'][0].head)

        # print(beneficial_fruits)
        # print(self.body_position)
        # print(self_head)
        # print(self_head[0])
        # print(self.direction)
        fruits = board_state["fruits"]
        pos = self.body_position
        # print(fruits[0].kind['name'] in beneficial_fruits)

        all_snakes = board_state['snakes']

        up = right = left = down = True
        
        if self.is_snake_up_ok(all_snakes)=='up':
            print("up false")
            up = False
        elif self.is_snake_up_ok(all_snakes)=='right':
            print("right false")
            right = False
        elif self.is_snake_up_ok(all_snakes)=='left':
            print("left false")
            left = False
        
        
        
        if self.is_snake_down_ok(all_snakes)=='down':
            print("down false")
            down = False
        elif self.is_snake_down_ok(all_snakes)=='right':
            print("right false")
            right = False
        elif self.is_snake_down_ok(all_snakes)=='left':
            print("left false")
            left = False
        
        
        if self.is_snake_right_ok(all_snakes)=='right':
            print("right false")
            right = False
        elif self.is_snake_right_ok(all_snakes)=='up':
            print("up false")
            up = False
        elif self.is_snake_right_ok(all_snakes)=='down':
            print("down false")
            down = False
        
        
        if self.is_snake_left_ok(all_snakes)=='left':
            print("left false")
            left = False
        elif self.is_snake_left_ok(all_snakes)=='up':
            print("up false")
            up = False
        elif self.is_snake_left_ok(all_snakes)=='down':
            print("down false")
            down = False

        for fruit in fruits:
            if not self.is_fruit_up_ok(fruit):
                # return Direction.RIGHT
                up= False
            elif not self.is_fruit_down_ok(fruit):
                # return Direction.RIGHT
                down=False
            elif not self.is_fruit_right_ok(fruit):
                # return Direction.RIGHT
                right=False
            elif not self.is_fruit_left_ok(fruit):
                # return Direction.RIGHT
                left=False

            # if fruit.pos[]:

            # print(fruit.kind['name'])
            if fruit.kind['name'] in self.beneficial_fruits:

                # print(fruits[0].pos)
                # print(fruits[0].pos[0])
                # print(fruits[0].kind['name'])
                if self.head[0] > fruit.pos[0]:
                    if self.direction == Direction.RIGHT:
                        if up: 
                            return Direction.UP
                        # elif down:
                        #     return Direction.DOWN
                    else:
                        if left: 
                            return Direction.LEFT
                        # else:
                        #     return Direction.RIGHT
                        

                if self.head[0] < fruit.pos[0]:
                    if self.direction == Direction.LEFT:
                        if up: 
                            return Direction.UP
                        # else:
                        #     return Direction.DOWN
                    else:
                        if right: 
                            return Direction.RIGHT
                        # else:
                        #     return Direction.LEFT

                if self.head[0] == fruit.pos[0]:

                    if self.head[1] < fruit.pos[1]:
                        if self.direction == Direction.UP:
                            if right: 
                                return Direction.RIGHT
                            # else:
                            #     return Direction.LEFT
                        else:
                            if down: 
                                return Direction.DOWN
                            # else:
                            #     return Direction.UP

                    if self.head[1] > fruit.pos[1]:
                        if self.direction == Direction.DOWN:
                            if right: 
                                return Direction.RIGHT
                        else:
                            if up: 
                                return Direction.UP

        return Direction.CONTINUE
