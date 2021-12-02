from snakes_battle.snake import Snake, Direction

class AISnake(Snake):
    def __init__(self, borders_cells) -> None:
        super().__init__()

        # All the cells that are fill with borders. This variable will store a list of (x, y) pairs
        self.border_cells = borders_cells

    def change_direction(self, board_state):
        # .... #

        # 'board_state' will contain a dict in this format:
        # {
        #     "snakes": [[x1,y1],[x2,y2]...[...]] 'snakes' key contains a list of all cells that are filled with snakes.
        #     "fruits": [[fruit1_x, fruit1_y], [fruit2_x, fruit2_y] ... ] 'fruits' key contains a list of all cells that are files with fruits. One fruit fills one cell.
        # }

        # You need to make a decision based on the board state.
        super.change_direction(Direction.LEFT)

        # super.change_direction(Direction.RIGHT)

        # super.change_direction(Direction.UP)

        # super.change_direction(Direction.DOWN)
