from snakes_battle.snake import Snake, Direction
from snakes_battle.fruit import FruitKind

class YoavSnake(Snake):
    def __init__(self, borders_cells, color, name) -> None:
        super().__init__(color, name)

        self.version = 1.0
        self.border_cells = borders_cells

    def is_harmful(self, fruits, x_val, y_val):
        pos = self.body_position
        for item in fruits:
            curr_fruit = item.kind["name"]
            if curr_fruit == "BOMB" or curr_fruit == "SKULL":
                if item.pos[0] == pos[0][0] + x_val and item.pos[1] == pos[0][1] + y_val:
                    return True
        return False

    def is_snake(self, snakes, x, y):
        pos = self.body_position
        curr_snake = snakes[0].body_position
        for body_part in curr_snake:
            if body_part[0] == pos[0][0] + x and body_part[1] == pos[0][1] + y:
                return True
        return False

    def get_next_fruit(self, fruits):
        for fruit in fruits:
            if fruit.kind in FruitKind.harmful_fruits:
                continue
            else:
                return fruit
    
    def make_decision(self, board_state):
        fruits = board_state["fruits"]
        snakes = board_state["snakes"]
        fruit = self.get_next_fruit(fruits)
        pos = self.body_position
        if pos[0][0] > fruit.pos[0]:
            if self.direction == Direction.RIGHT:
                if (not self.is_harmful(fruits, 0, -1) and not self.is_snake(snakes, 0, -1)):  # If the position I want to go to has a harmful item, don't go there.
                    return Direction.UP
                elif(not self.is_snake(snakes, 0, 1)):
                    return Direction.DOWN
            else:
                if (not self.is_harmful(fruits, -1, 0) and not self.is_snake(snakes, -1, 0)):
                    return Direction.LEFT
                elif(not self.is_snake(snakes, 0, -1)):
                    return Direction.UP
        
        if pos[0][0] < fruit.pos[0]:
            if self.direction == Direction.LEFT:
                if (not self.is_harmful(fruits, 0, -1) and not self.is_snake(snakes, 0, -1)):
                    return Direction.UP
                elif(not self.is_snake(snakes, 0, 1)):
                    return Direction.DOWN
            else:
                if (not self.is_harmful(fruits, 1, 0) and not self.is_snake(snakes, 1, 0)):
                    return Direction.RIGHT
                elif(not self.is_snake(snakes, 0, 1)):
                    return Direction.DOWN
        
        if pos[0][0] == fruit.pos[0]:

            if pos[0][1] < fruit.pos[1]:
                if self.direction == Direction.UP:
                    if (not self.is_harmful(fruits, 1, 0) and not self.is_snake(snakes, 1, 0)):
                        return Direction.RIGHT
                    elif(not self.is_snake(snakes, -1, 0)):
                        return Direction.LEFT
                else:
                    if (not self.is_harmful(fruits, 0, 1) and not self.is_snake(snakes, 0, 1)):
                        return Direction.DOWN
                    elif(not self.is_snake(snakes, 1, 0)):
                        return Direction.RIGHT

            if pos[0][1] > fruit.pos[1]:
                if self.direction == Direction.DOWN:
                    if (not self.is_harmful(fruits, 1, 0) and not self.is_snake(snakes, 1, 0)):
                        return Direction.RIGHT
                    elif(not self.is_snake(snakes, -1, 0)):
                        return Direction.LEFT
                else:
                    if (not self.is_harmful(fruits, 0, -1) and not self.is_snake(snakes, 0, -1)):
                        return Direction.UP
                    elif(not self.is_snake(snakes, -1, 0)):
                        return Direction.LEFT
    
        return Direction.CONTINUE
    



