import settings
import random
import copy

class Board:
    def __init__(self, board_size) -> None:

        self.board_size = board_size

        self.snakes = []
        self.lost_snakes = []
        self.fruits = []
        self.empty_cells = [] # Current empty cells. You have to call _update_empty_cells function every time before accessing this variable.
        self.all_cells_pos = [] # All potentially empty cells.
        self.border_cells = []
        
        # Initilazing the 'border_cells' list.
        for x in range( self.board_size[0]):
            for y in range( self.board_size[1]):
                if x < settings.BORDER_THICKNESS or x >=  self.board_size[0] - settings.BORDER_THICKNESS or y < settings.BORDER_THICKNESS or y >= board_size[1] - settings.BORDER_THICKNESS:
                    self.border_cells.append((x,y))

        # Initilazing the 'all_cells_pos' with all the cells on the board except the borders cells.
        for x in range(settings.BORDER_THICKNESS, self.board_size[0]-settings.BORDER_THICKNESS-1):
            for y in range(settings.BORDER_THICKNESS, self.board_size[1]-settings.BORDER_THICKNESS-1):
                self.all_cells_pos.append((x,y))

    def _update_empty_cells(self):
        self.empty_cells = self.all_cells_pos.copy()
        for snake in self.snakes:
            for cell_pos in snake.body_pos:
                for cell in self.empty_cells:
                    if cell[0] == cell_pos[0] and cell[1] == cell_pos[1]:
                        self.empty_cells.remove(cell)

        for fruit in self.fruits:
            for cell in self.empty_cells:
                if cell[0] == fruit.pos[0] and cell[1] == fruit.pos[1]:
                    self.empty_cells.remove(cell)

    def add_snake(self, snake):
        self.snakes.append(snake)

    def add_fruit(self, fruit):
        self.fruits.append(fruit)

    def fruit_eaten(self, fruit):
        self.fruits.remove(fruit)

    def get_border_cells(self):
        return copy.deepcopy(self.border_cells)

    def get_board_state(self):
        return {
            "snakes": copy.deepcopy(self.snakes),
            "fruits": copy.deepcopy(self.fruits)
            }
