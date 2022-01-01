from snakes_battle.snake import Snake, Direction

class YourBotName(Snake):
    def __init__(self, borders_cells, color, name) -> None:
        super().__init__(color, name)
        self.init()
        
        self.borders_cells = borders_cells      
        self.version = 1.0


    ##############################
    # You can edit only the code below. You can't change methods names.
    ##############################

    def init(self):
        # Your bot initializations will be here.
        pass

    
    def make_decision(self, board_state):
        # You can only call methods that starts with the word 'allowed__'. You can't change attrbiutes directly.

        super().allowed__change_direction() # Changes the direction of the snake. You can pass Direction.UP, Direction.DOWN. Returns nothing
        super().allowed__get_direction() # This function takes no arguments and returns the direction of the snake.
        super().allowed__body_position() # This function takes no arguments and returns a list with all cells (x,y) that are filled with your snake.
        super().allowed__is_king() # returns True if your snake is king else returns False
        super().allowed__is_knife() # returns True if your snake has a knife else returns False.
        super().allowed__is_shield() # returns True if your snake is shielded else returns False.

        # You can't ca

