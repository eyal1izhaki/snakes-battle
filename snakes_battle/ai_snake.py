from snakes_battle.snake import Snake, Direction

class AISnake(Snake):
    def __init__(self, borders_cells,name="test") -> None:
        super().__init__()
        #player name
        self.name = name
        # All the cells that are fill with borders. This variable will store a list of (x, y) pairs
        self.border_cells = borders_cells

    def change_direction(self, board_state):
        # .... #
        # borad_state = {
        #   "snakes": [snake1, snake2, ...],            "snakes" contains a list of Snake objects.
        #   "fruits": [fruit1, fruit2, fruit3, ....]    "fruits" contains a list of Fruit objects.
        #

        
        # You need to make a decision based on the board state.
        fruits = board_state["fruits"]
        pos = super().get_body_position()

        if pos[0][0] > fruits[0].pos[0]:
            if (self.direction == Direction.RIGHT):
                super().change_direction(Direction.UP)
            else:
                super().change_direction(Direction.LEFT)
        
        if pos[0][0] < fruits[0].pos[0]:
            if (self.direction == Direction.LEFT):
                super().change_direction(Direction.UP)
            else:
                super().change_direction(Direction.RIGHT)
        
        if pos[0][0] == fruits[0].pos[0]:

            if pos[0][1] < fruits[0].pos[1]:
                if (self.direction == Direction.UP):
                    super().change_direction(Direction.RIGHT)
                else:
                    super().change_direction(Direction.DOWN)

            if pos[0][1] > fruits[0].pos[1]:
                if (self.direction == Direction.DOWN):
                    super().change_direction(Direction.RIGHT)
                else:
                    super().change_direction(Direction.UP)


        

        # super.change_direction(Direction.RIGHT)

        # super.change_direction(Direction.UP)

        # super.change_direction(Direction.DOWN)
