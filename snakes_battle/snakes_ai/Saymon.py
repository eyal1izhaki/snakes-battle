from snakes_battle.fruit import FruitKind
from snakes_battle.snake import Snake, Direction

class Saymon(Snake):
    def __init__(self, borders_cells, color, name) -> None:
        super().__init__(color, name)
        self.init(borders_cells)
        

    ##############################
    # You can edit only the code below. You can't change methods names.
    ##############################


    def init(self, borders_cells):
        # Your bot initializations will be here.
        self.allowed__version = 1.0

        # All the cells that are fill with borders. This variable will store a list of (x, y) pairs
        self.allowed__border_cells = borders_cells

        # Direction to return
        self.allowed_direction_to_return = Direction.UP


    def allowed__can_i_make_it(self):
        pass

    def allowed__get_enemy_global_quarter(self):
        # Get enemy quarter
        # + | +
        # -----
        # + | +
        pass

    def allowed__emergency(self):
        # Avoid bomb if possible
        # Avoid skeleton MUST!
        pass

    def allowed__get_close_fruit(self):
        pass

    def allowed__should_i_use_king(self):
        pass

    def allowed__is_direction_upside_down(self):
        pass

    def allowed__go_to_fruit(self, fruit):

        pos = super().allowed__body_position()
        if pos[0][0] > fruit.pos[0]:
            if (self.direction == Direction.RIGHT):
                self.allowed_direction_to_return = Direction.UP
            else:
                self.allowed_direction_to_return = Direction.LEFT

        if pos[0][0] < fruit.pos[0]:
            if (self.direction == Direction.LEFT):
                self.allowed_direction_to_return = Direction.UP
            else:
                self.allowed_direction_to_return = Direction.RIGHT

        if pos[0][0] == fruit.pos[0]:

            if pos[0][1] < fruit.pos[1]:
                if (self.direction == Direction.UP):
                    self.allowed_direction_to_return = Direction.RIGHT
                else:
                    self.allowed_direction_to_return = Direction.DOWN

            if pos[0][1] > fruit.pos[1]:
                if (self.direction == Direction.DOWN):
                    self.allowed_direction_to_return = Direction.RIGHT
                else:
                    self.allowed_direction_to_return = Direction.UP

    def allowed__dont_crush_into_border(self):
        last_row = int(self.allowed__border_cells[-1][0] - 1)
        last_col = int(self.allowed__border_cells[-1][1] - 1)

        my_direction_now = self.allowed_direction_to_return
        snake_head = super().allowed__body_position()[0]

        if my_direction_now == Direction.RIGHT:
            future_row = int(snake_head[0] + 1)
            future_col = int(snake_head[1] + 0)
        elif my_direction_now == Direction.LEFT:
            future_row = int(snake_head[0] - 1)
            future_col = int(snake_head[1] + 0)
        elif my_direction_now == Direction.UP:
            future_row = int(snake_head[0] + 0)
            future_col = int(snake_head[1] - 1)
        elif my_direction_now == Direction.DOWN:
            future_row = int(snake_head[0] + 0)
            future_col = int(snake_head[1] + 1)
        print("s")
        print(snake_head)
        print("row", future_row, "col", future_col)
        print(last_row, last_col)
        # Top
        if future_col <= 0:
            # Left
            if future_row <= 0:
                if self.allowed_direction_to_return == Direction.LEFT:
                    self.allowed_direction_to_return = Direction.RIGHT
                elif self.allowed_direction_to_return == Direction.UP:
                    self.allowed_direction_to_return = Direction.DOWN
            # Right
            elif future_col > last_col:
                if self.allowed_direction_to_return == Direction.RIGHT:
                    self.allowed_direction_to_return = Direction.LEFT
                elif self.allowed_direction_to_return == Direction.UP:
                    self.allowed_direction_to_return = Direction.DOWN
            else:
                self.allowed_direction_to_return = Direction.RIGHT

        # Bottom
        elif future_row > last_row:
            # Left
            if future_col <= 0:
                if self.allowed_direction_to_return == Direction.LEFT:
                    self.allowed_direction_to_return = Direction.RIGHT
                elif self.allowed_direction_to_return == Direction.DOWN:
                    self.allowed_direction_to_return = Direction.UP
            # Right
            elif future_col > last_col:
                if self.allowed_direction_to_return == Direction.RIGHT:
                    self.allowed_direction_to_return = Direction.LEFT
                elif self.allowed_direction_to_return == Direction.DOWN:
                    self.allowed_direction_to_return = Direction.UP
            else:
                self.allowed_direction_to_return = Direction.RIGHT

        # Left
        elif future_row <= 0:
            # Top
            if future_col <= 0:
                if self.allowed_direction_to_return == Direction.UP:
                    self.allowed_direction_to_return = Direction.DOWN
                elif self.allowed_direction_to_return == Direction.LEFT:
                    self.allowed_direction_to_return = Direction.RIGHT
            # Bottom
            elif future_row > last_row:
                if self.allowed_direction_to_return == Direction.DOWN:
                    self.allowed_direction_to_return = Direction.UP
                elif self.allowed_direction_to_return == Direction.LEFT:
                    self.allowed_direction_to_return = Direction.RIGHT
            else:
                self.allowed_direction_to_return = Direction.UP
        # Right
        elif future_col > last_col:
            print("AAA")
            # Top
            if future_row <= 0:
                if self.allowed_direction_to_return == Direction.UP:
                    self.allowed_direction_to_return = Direction.DOWN
                elif self.allowed_direction_to_return == Direction.RIGHT:
                    self.allowed_direction_to_return = Direction.LEFT
            # Bottom
            elif future_row > last_row:
                if self.allowed_direction_to_return == Direction.DOWN:
                    self.allowed_direction_to_return = Direction.UP
                elif self.allowed_direction_to_return == Direction.RIGHT:
                    self.allowed_direction_to_return = Direction.LEFT
            else:
                self.allowed_direction_to_return = Direction.UP


    def allowed__change_direction(self):
        if self.allowed_direction_to_return == Direction.DOWN:
            self.allowed_direction_to_return = Direction.UP
        elif self.allowed_direction_to_return == Direction.UP:
            self.allowed_direction_to_return = Direction.DOWN
        elif self.allowed_direction_to_return == Direction.LEFT:
            self.allowed_direction_to_return = Direction.RIGHT
        elif self.allowed_direction_to_return == Direction.RIGHT:
            self.allowed_direction_to_return = Direction.LEFT


    def allowed_can_i_go_there(self, cant_go):
        snake_head = super().allowed__body_position()[0]
        my_row, my_col = snake_head
        if snake_head in cant_go:
            self.allowed__change_direction()

    def allowed__dont_crush_border(self):
        last_row = self.allowed__border_cells[-1][0]
        last_col = self.allowed__border_cells[-1][1]

        snake_head = super().allowed__body_position()[0]
        my_row, my_col = snake_head

        if self.allowed_direction_to_return == Direction.DOWN:
            new_row = my_row + 0
            new_col = my_col + 1

        elif self.allowed_direction_to_return == Direction.UP:
            new_row = my_row + 0
            new_col = my_col - 1

        elif self.allowed_direction_to_return == Direction.RIGHT:
            new_row = my_row + 1
            new_col = my_col + 0

        elif self.allowed_direction_to_return == Direction.LEFT:
            new_row = my_row - 1
            new_col = my_col + 0

        # Going Right
        if new_row >= last_row:
            if new_col < last_col:
                self.allowed_direction_to_return = Direction.DOWN
        # Going Down
        elif new_col >= last_col:
            self.allowed_direction_to_return = Direction.RIGHT
        # Going Left
        elif new_row < 0:
            self.allowed_direction_to_return = Direction.DOWN
        # Going Up
        elif new_col < 0:
            self.allowed_direction_to_return = Direction.RIGHT

    def allowed__get_clost_fruit(self, board_state):
        for fruit in board_state["fruits"]:
            if fruit.kind == FruitKind.DRAGON_FRUIT:
                return fruit
            elif fruit.kind == FruitKind.STRAWBERRY:
                return fruit


    def allowed_close_pos(self, pos1, poses):
        m = pos1
        for p in poses:
            if pos1 < m:
                m = pos1
        return m


    def make_decision(self, board_state):
        # You can only call methods that starts with the word 'allowed__'. You can't change attrbiutes directly.

        super().allowed__get_direction() # This function takes no arguments and returns the direction of the snake.
        super().allowed__body_position() # This function takes no arguments and returns a list with all cells (x,y) that are filled with your snake.
        super().allowed__is_king() # returns True if your snake is king else returns False
        super().allowed__is_knife() # returns True if your snake has a knife else returns False.
        super().allowed__is_shield() # returns True if your snake is shielded else returns False.


        #list_of_pos_you_cant_go = self.allowed__dont_crush_border()
        #self.allowed__dont_crush_border()
        #self.allowed_can_i_go_there(self.allowed_where_i_cant_go())

        #for fruit in board_state["fruits"]:
        #    if fruit.kind == FruitKind.DRAGON_FRUIT:
        #        return Direction.DOWN()

        #for snake in board_state["snakes"]:
        #    print(snake.allowed__get_direction)
        fruit = self.allowed__get_clost_fruit(board_state)
        self.allowed__go_to_fruit(fruit)
        #for fruit in board_state["fruits"]:
        #    if fruit.kind == FruitKind.DRAGON_FRUIT:
        #        self.allowed__go_to_fruit(fruit)
        #    if fruit.kind == FruitKind.STRAWBERRY:
        #        self.allowed__go_to_fruit(fruit)

        self.allowed__dont_crush_into_border()

        #return self.allowed_direction_to_return
        return self.allowed_direction_to_return
