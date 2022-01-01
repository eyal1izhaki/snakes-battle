from snakes_battle.snake import Snake, Direction

class SimpleSnake(Snake):
    def __init__(self, borders_cells, color, name) -> None:
        super().__init__(color, name)
        self.init(borders_cells)



    def init(self, borders_cells):
        # Your bot initializations will be here.
        self.allowed__version = 1.0
        # All the cells that are fill with borders. This variable will store a list of (x, y) pairs
        self.allowed__border_cells = borders_cells

    
    def make_decision(self, board_state):
        # .... #
        # borad_state = {
        #   "snakes": [snake1, snake2, ...],            "snakes" contains a list of Snake objects.
        #   "fruits": [fruit1, fruit2, fruit3, ....]    "fruits" contains a list of Fruit objects.
        #

        
        # You need to make a decision based on the board state.
        fruits = board_state["fruits"]
        pos = super().allowed__body_position()

        if pos[0][0] > fruits[0].pos[0]:
            if (self.direction == Direction.RIGHT):
                return Direction.UP
            else:
                return Direction.LEFT
        
        if pos[0][0] < fruits[0].pos[0]:
            if (self.direction == Direction.LEFT):
                return Direction.UP
            else:
                return Direction.RIGHT
        
        if pos[0][0] == fruits[0].pos[0]:

            if pos[0][1] < fruits[0].pos[1]:
                if (self.direction == Direction.UP):
                    return Direction.RIGHT
                else:
                    return Direction.DOWN

            if pos[0][1] > fruits[0].pos[1]:
                if (self.direction == Direction.DOWN):
                    return Direction.RIGHT
                else:
                    return Direction.UP


        

        # super.allowed__change_direction(Direction.RIGHT)

        # super.allowed__change_direction(Direction.UP)

        # super.allowed__change_direction(Direction.DOWN)
