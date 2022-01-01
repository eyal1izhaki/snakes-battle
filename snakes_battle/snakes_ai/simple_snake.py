from snakes_battle.snake import Snake, Direction

class SimpleSnake(Snake):
    def __init__(self, borders_cells, color, name) -> None:
        super().__init__(color, name)
        self.init()

        # All the cells that are fill with borders. This variable will store a list of (x, y) pairs
        self.border_cells = borders_cells
        self.version = 1.0
    

    def init(self):
        # Your bot initializations will be here.
        pass
    
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
                super().allowed__change_direction(Direction.UP)
            else:
                super().allowed__change_direction(Direction.LEFT)
        
        if pos[0][0] < fruits[0].pos[0]:
            if (self.direction == Direction.LEFT):
                super().allowed__change_direction(Direction.UP)
            else:
                super().allowed__change_direction(Direction.RIGHT)
        
        if pos[0][0] == fruits[0].pos[0]:

            if pos[0][1] < fruits[0].pos[1]:
                if (self.direction == Direction.UP):
                    super().allowed__change_direction(Direction.RIGHT)
                else:
                    super().allowed__change_direction(Direction.DOWN)

            if pos[0][1] > fruits[0].pos[1]:
                if (self.direction == Direction.DOWN):
                    super().allowed__change_direction(Direction.RIGHT)
                else:
                    super().allowed__change_direction(Direction.UP)


        

        # super.allowed__change_direction(Direction.RIGHT)

        # super.allowed__change_direction(Direction.UP)

        # super.allowed__change_direction(Direction.DOWN)
