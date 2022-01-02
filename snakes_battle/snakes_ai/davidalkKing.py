from snakes_battle.fruit import FruitKind
from snakes_battle.snake import Snake, Direction

class DavidalkKing(Snake):
    def __init__(self, borders_cells, color, name) -> None:
        super().__init__(color, name)
        self.init(borders_cells)

    def init(self, borders_cells):
        self.allowed__version = 1.0
        self.allowed__border_cells = borders_cells

    def allowed_get_distance(self, position1, position2):
        return abs(position1[0] - position2[0]) + abs(position1[1] - position2[1])
    
    def allowed_get_good_fruits(self, fruits):
        good_fruits = [x for x in fruits if not x in FruitKind.harmful_fruits]
        return good_fruits
    
    def allowed_get_target_fruit(self, board_state):
        fruits = board_state["fruits"]
        print (self.allowed_get_good_fruits(fruits))
    
    def allowed_choose_path(self, target_position):
        body = self.allowed__body_position()
        head = body[0]

        if head[0] > target_position[0]:
            if (self.direction == Direction.RIGHT):
                return Direction.UP
            else:
                return Direction.LEFT
        
        if head[0] < target_position[0]:
            if (self.direction == Direction.LEFT):
                return Direction.UP
            else:
                return Direction.RIGHT
        
        if head[0] == target_position[0]:

            if head[1] < target_position[1]:
                if (self.direction == Direction.UP):
                    return Direction.RIGHT
                else:
                    return Direction.DOWN

            if head[1] > target_position[1]:
                if (self.direction == Direction.DOWN):
                    return Direction.RIGHT
                else:
                    return Direction.UP
    
    def make_decision(self, board_state):
        # Choosing a target fruit
        target_fruit = self.allowed_get_target_fruit(board_state)
        return self.allowed_choose_path(target_fruit.pos)
