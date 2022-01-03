import math

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
        self.allowed__version = 2.0

        # All the cells that are fill with borders. This variable will store a list of (x, y) pairs
        self.allowed__border_cells = borders_cells

        # First direction to return
        self.allowed__direction_to_return = Direction.RIGHT

        # The pos of map edge (col, row)
        self.allowed__map_edge = borders_cells[-1]

    def allowed__get_future_location(self):
        # Reture [col, row] future location based on the location that we will return
        seted_location = self.allowed__direction_to_return
        snake_head = super().allowed__body_position()[0]

        if seted_location == Direction.RIGHT:
            future_col = int(snake_head[0] + 1)
            future_row = int(snake_head[1] + 0)
        elif seted_location == Direction.LEFT:
            future_col = int(snake_head[0] - 1)
            future_row = int(snake_head[1] + 0)
        elif seted_location == Direction.UP:
            future_col = int(snake_head[0] + 0)
            future_row = int(snake_head[1] - 1)
        elif seted_location == Direction.DOWN:
            future_col = int(snake_head[0] + 0)
            future_row = int(snake_head[1] + 1)
        ##print("nowr", snake_head[0], "nowc", snake_head[1])
        ##print("fr", future_row, "fc", future_col)
        #return [future_row, future_col]
        return [future_col, future_row]

    def allowed__get_future_location_by_first_direction(self):
        # Return [col, row] future location based on the location that we will return
        first_direction = self.direction
        snake_head = super().allowed__body_position()[0]

        if first_direction == Direction.RIGHT:
            future_col = int(snake_head[0] + 1)
            future_row = int(snake_head[1] + 0)
        elif first_direction == Direction.LEFT:
            future_col = int(snake_head[0] - 1)
            future_row = int(snake_head[1] + 0)
        elif first_direction == Direction.UP:
            future_col = int(snake_head[0] + 0)
            future_row = int(snake_head[1] - 1)
        elif first_direction == Direction.DOWN:
            future_col = int(snake_head[0] + 0)
            future_row = int(snake_head[1] + 1)
        ##print("nowr", snake_head[0], "nowc", snake_head[1])
        ##print("fr", future_row, "fc", future_col)
        #return [future_row, future_col]
        return [future_col, future_row]

    def allowed__dont_crush_into_border(self):
        last_row = self.allowed__map_edge[1]
        last_col = self.allowed__map_edge[0]
        # future_col, future_row = self.allowed__get_future_location_by_first_direction()
        future_col, future_row = self.allowed__get_future_location()

        ##print(future_col, future_row)
        ##print(last_col, last_row)
        # Top - going up
        if future_row <= 0:
            # Default to return
            self.allowed__direction_to_return = Direction.RIGHT
            # Right
            if future_col >= last_col - 1:
                self.allowed__direction_to_return = Direction.LEFT
            # Left
            elif future_col <= 1:
                self.allowed__direction_to_return = Direction.RIGHT
        # Bottom - going down
        elif future_row >= last_row:
            # Default to return
            self.allowed__direction_to_return = Direction.LEFT
            # Right
            if future_col >= last_col - 1:
                self.allowed__direction_to_return = Direction.LEFT
            # Left
            elif future_col <= 1:
                self.allowed__direction_to_return = Direction.RIGHT
        # Right - going right
        elif future_col >= last_col:
            #print(future_row)
            # Default to return
            self.allowed__direction_to_return = Direction.UP
            # Top
            if future_row <= 1:
                self.allowed__direction_to_return = Direction.DOWN
            # Bottom
            elif future_row >= last_row - 1:
                self.allowed__direction_to_return = Direction.UP
        # Left - going left
        elif future_col <= 0:
            #print(future_row)
            # Default to return
            self.allowed__direction_to_return = Direction.UP
            # Top
            if future_row <= 1:
                self.allowed__direction_to_return = Direction.DOWN
            # Bottom
            elif future_row >= last_row - 1:
                self.allowed__direction_to_return = Direction.UP

        future_col, future_row = self.allowed__get_future_location_by_first_direction()
        if (self.direction == Direction.LEFT and self.allowed__direction_to_return == Direction.RIGHT)\
                or (self.direction == Direction.RIGHT and self.allowed__direction_to_return == Direction.LEFT):
            if future_row <= 1:
                self.allowed__direction_to_return = Direction.DOWN
            elif future_row >= last_row - 1:
                self.allowed__direction_to_return = Direction.UP
        elif (self.direction == Direction.UP and self.allowed__direction_to_return == Direction.DOWN)\
                or (self.direction == Direction.DOWN and self.allowed__direction_to_return == Direction.UP):
            if future_col <= 1:
                self.allowed__direction_to_return = Direction.RIGHT
            elif future_col >= last_col - 1:
                self.allowed__direction_to_return = Direction.LEFT


    def allowed__avoid_skel(self, board_state):
        all_skels = []
        for skel in board_state["fruits"]:
            if skel.kind == FruitKind.SKULL:
                all_skels.append(skel.pos)

        if self.allowed__get_future_location() in all_skels:
            if self.allowed__direction_to_return == Direction.DOWN:
                # Going left
                if self.direction == Direction.LEFT:
                    self.allowed__direction_to_return = Direction.UP
                # Going right
                elif self.direction == Direction.RIGHT:
                    self.allowed__direction_to_return = Direction.UP
                # Going down
                elif self.direction == Direction.DOWN:
                    self.allowed__direction_to_return = Direction.RIGHT
            elif self.allowed__direction_to_return == Direction.UP:
                # Going left
                if self.direction == Direction.LEFT:
                    self.allowed__direction_to_return = Direction.UP
                elif self.direction == Direction.RIGHT:
                    self.allowed__direction_to_return = Direction.UP
                elif self.direction == Direction.UP:
                    self.allowed__direction_to_return = Direction.RIGHT
            elif self.allowed__direction_to_return == Direction.RIGHT:
                if self.direction == Direction.UP:
                    self.allowed__direction_to_return = Direction.RIGHT
                elif self.direction == Direction.DOWN:
                    self.allowed__direction_to_return = Direction.RIGHT
                elif self.direction == Direction.RIGHT:
                    self.allowed__direction_to_return = Direction.UP
            elif self.allowed__direction_to_return == Direction.LEFT:
                if self.direction == Direction.UP:
                    self.allowed__direction_to_return = Direction.RIGHT
                elif self.direction == Direction.DOWN:
                    self.allowed__direction_to_return = Direction.RIGHT
                # Going left
                elif self.direction == Direction.LEFT:
                    self.allowed__direction_to_return = Direction.UP

    def allowed__go_there(self, something):
        pos = super().allowed__body_position()
        if pos[0][0] > something[0]:
            if (self.direction == Direction.RIGHT):
                self.allowed__direction_to_return = Direction.UP
            else:
                self.allowed__direction_to_return = Direction.LEFT

        if pos[0][0] < something[0]:
            if (self.direction == Direction.LEFT):
                self.allowed__direction_to_return = Direction.UP
            else:
                self.allowed__direction_to_return = Direction.RIGHT

        if pos[0][0] == something[0]:

            if pos[0][1] < something[1]:
                if (self.direction == Direction.UP):
                    self.allowed__direction_to_return = Direction.RIGHT
                else:
                    self.allowed__direction_to_return = Direction.DOWN

            if pos[0][1] > something[1]:
                if (self.direction == Direction.DOWN):
                    self.allowed__direction_to_return = Direction.RIGHT
                else:
                    self.allowed__direction_to_return = Direction.UP

    def allowed__go_to_fruit(self, fruit):

        pos = super().allowed__body_position()
        if pos[0][0] > fruit.pos[0]:
            if (self.direction == Direction.RIGHT):
                self.allowed__direction_to_return = Direction.UP
            else:
                self.allowed__direction_to_return = Direction.LEFT

        if pos[0][0] < fruit.pos[0]:
            if (self.direction == Direction.LEFT):
                self.allowed__direction_to_return = Direction.UP
            else:
                self.allowed__direction_to_return = Direction.RIGHT

        if pos[0][0] == fruit.pos[0]:

            if pos[0][1] < fruit.pos[1]:
                if (self.direction == Direction.UP):
                    self.allowed__direction_to_return = Direction.RIGHT
                else:
                    self.allowed__direction_to_return = Direction.DOWN

            if pos[0][1] > fruit.pos[1]:
                if (self.direction == Direction.DOWN):
                    self.allowed__direction_to_return = Direction.RIGHT
                else:
                    self.allowed__direction_to_return = Direction.UP

    def allowed_bad_locations(self):
        snake_head = super().allowed__body_position()[0]
        my_row, my_col = snake_head
        bad_locations = []

    def allowed__get_best_fruit(self, board_state):
        fruits = []
        for fruit in board_state["fruits"]:
            if fruit.kind == FruitKind.DRAGON_FRUIT:
                fruits.append(fruit.pos)
            elif fruit.kind == FruitKind.STRAWBERRY:
                fruits.append(fruit.pos)

        return self.allowed__clost_loc(fruits)

    def allowed__clost_loc(self, arr_locs):
        distance = 100000
        snake_head = super().allowed__body_position()[0]
        close_loc = None
        for loc in arr_locs:
            if math.dist(loc, snake_head) < distance:
            #if math.sqrt((loc[0] - snake_head[0])**2 + (loc[1] - snake_head[0])**2) < distance:
                distance = math.dist(loc, snake_head)
                close_loc = loc
        return close_loc

    def allowed__get_best_knife(self, board_state):
        knif = []
        for k in board_state["fruits"]:
            if k.kind == FruitKind.KNIFE:
                knif.append(k.pos)
        return self.allowed__clost_loc(knif)

    def allowed__get_best_shield(self, board_state):
        shields = []
        for sh in board_state["fruits"]:
            if sh.kind == FruitKind.SHIELD:
                shields.append(sh.pos)

        return self.allowed__clost_loc(shields)

    def allowed__attack(self, board_state):
        my_head = super().allowed__body_position()[0]
        enemy_neck = None
        for snake in board_state["snakes"]:
           if not snake.allowed__body_position()[0] == my_head:
               if snake.length > 1:
                enemy_neck = snake.allowed__body_position()[1]
        if enemy_neck:
            self.allowed__go_there(enemy_neck)
            return True
        return False

    def allowed__avoid_me(self, board_state):
        all_poses = super().allowed__body_position()
        if self.allowed__get_future_location() in all_poses:
            ##print(self.allowed__get_future_location())
            ##print(self.allowed__body_position()[0])
            ##print(all_poses)
            if self.allowed__direction_to_return == Direction.DOWN:
                if self.direction == Direction.LEFT:
                    self.allowed__direction_to_return = Direction.UP
                elif self.direction == Direction.RIGHT:
                    self.allowed__direction_to_return = Direction.UP
                elif self.direction == Direction.DOWN:
                    self.allowed__direction_to_return = Direction.RIGHT
            elif self.allowed__direction_to_return == Direction.UP:
                if self.direction == Direction.LEFT:
                    self.allowed__direction_to_return = Direction.DOWN
                elif self.direction == Direction.RIGHT:
                    self.allowed__direction_to_return = Direction.DOWN
                elif self.direction == Direction.UP:
                    self.allowed__direction_to_return = Direction.RIGHT
            elif self.allowed__direction_to_return == Direction.RIGHT:
                if self.direction == Direction.UP:
                    self.allowed__direction_to_return = Direction.LEFT
                elif self.direction == Direction.DOWN:
                    self.allowed__direction_to_return = Direction.LEFT
                elif self.direction == Direction.RIGHT:
                    self.allowed__direction_to_return = Direction.UP
            elif self.allowed__direction_to_return == Direction.LEFT:
                if self.direction == Direction.UP:
                    self.allowed__direction_to_return = Direction.RIGHT
                elif self.direction == Direction.DOWN:
                    self.allowed__direction_to_return = Direction.RIGHT
                elif self.direction == Direction.LEFT:
                    self.allowed__direction_to_return = Direction.UP

            future_loc = self.allowed__get_future_location_by_first_direction()
            if (self.direction == Direction.LEFT and self.allowed__direction_to_return == Direction.RIGHT) \
                    or (self.direction == Direction.RIGHT and self.allowed__direction_to_return == Direction.LEFT):
                if future_loc in all_poses:
                    self.allowed__direction_to_return = Direction.DOWN
            elif (self.direction == Direction.UP and self.allowed__direction_to_return == Direction.DOWN) \
                    or (self.direction == Direction.DOWN and self.allowed__direction_to_return == Direction.UP):
                if future_loc in all_poses:
                    self.allowed__direction_to_return = Direction.RIGHT

    def allowed__avoid_other(self, board_state):
        my_head = super().allowed__body_position()[0]
        enemy_all = None
        for snake in board_state["snakes"]:
           if not snake.allowed__body_position()[0] == my_head:
               enemy_all = snake.allowed__body_position()
        if enemy_all:
            if self.allowed__get_future_location() in enemy_all:
                ##print(self.allowed__get_future_location())
                ##print("enemy", enemy_all)
                ##print("WHAT ENEMY")
                ##print("n", super().allowed__body_position()[0])
                ##print("F", self.allowed__get_future_location())
                ##print("dir", self.allowed_direction_to_return)
                ##print("a", enemy_all)
                if self.allowed__direction_to_return == Direction.DOWN:
                    if self.direction == Direction.LEFT:
                        self.allowed__direction_to_return = Direction.UP
                    elif self.direction == Direction.RIGHT:
                        self.allowed__direction_to_return = Direction.UP
                    elif self.direction == Direction.DOWN:
                        self.allowed__direction_to_return = Direction.RIGHT
                elif self.allowed__direction_to_return == Direction.UP:
                    if self.direction == Direction.LEFT:
                        self.allowed__direction_to_return = Direction.DOWN
                    elif self.direction == Direction.RIGHT:
                        self.allowed__direction_to_return = Direction.DOWN
                    elif self.direction == Direction.UP:
                        self.allowed__direction_to_return = Direction.RIGHT
                elif self.allowed__direction_to_return == Direction.RIGHT:
                    if self.direction == Direction.UP:
                        self.allowed__direction_to_return = Direction.LEFT
                    elif self.direction == Direction.DOWN:
                        self.allowed__direction_to_return = Direction.LEFT
                    elif self.direction == Direction.RIGHT:
                        self.allowed__direction_to_return = Direction.UP
                elif self.allowed__direction_to_return == Direction.LEFT:
                    if self.direction == Direction.UP:
                        self.allowed__direction_to_return = Direction.RIGHT
                    elif self.direction == Direction.DOWN:
                        self.allowed__direction_to_return = Direction.RIGHT
                    elif self.direction == Direction.LEFT:
                        self.allowed__direction_to_return = Direction.UP

                future_loc = self.allowed__get_future_location_by_first_direction()
                if (self.direction == Direction.LEFT and self.allowed__direction_to_return == Direction.RIGHT) \
                        or (self.direction == Direction.RIGHT and self.allowed__direction_to_return == Direction.LEFT):
                    if future_loc in enemy_all:
                        self.allowed__direction_to_return = Direction.DOWN
                elif (self.direction == Direction.UP and self.allowed__direction_to_return == Direction.DOWN) \
                        or (self.direction == Direction.DOWN and self.allowed__direction_to_return == Direction.UP):
                    if future_loc in enemy_all:
                        self.allowed__direction_to_return = Direction.RIGHT

    def make_decision(self, board_state):
        # You can only call methods that starts with the word 'allowed__'. You can't change attrbiutes directly.

        super().allowed__get_direction()  # This function takes no arguments and returns the direction of the snake.
        super().allowed__body_position()  # This function takes no arguments and returns a list with all cells (x,y) that are filled with your snake.
        super().allowed__is_king()  # returns True if your snake is king else returns False
        super().allowed__is_knife()  # returns True if your snake has a knife else returns False.
        super().allowed__is_shield()  # returns True if your snake is shielded else returns False.

        # list_of_pos_you_cant_go = self.allowed__dont_crush_border()
        # self.allowed__dont_crush_border()
        # self.allowed_can_i_go_there(self.allowed_where_i_cant_go())

        # for fruit in board_state["fruits"]:
        #    if fruit.kind == FruitKind.DRAGON_FRUIT:
        #        return Direction.DOWN()

        # for snake in board_state["snakes"]:
        #    #print(snake.allowed__get_direction)
        #print("s", self.direction)
        if not self.allowed__is_shield():
            #print("no shield")
            shield = self.allowed__get_best_shield(board_state)
            if shield:
                self.allowed__go_there(shield)
            else:
                #print("yes fruit")
                fruit = self.allowed__get_best_fruit(board_state)
                if fruit:
                    self.allowed__go_there(fruit)
                    #self.allowed__go_to_fruit(fruit)
                    #print("fcant", self.allowed__direction_to_return)
        elif not self.allowed__is_knife():
            knife = self.allowed__get_best_knife(board_state)
            if knife:
                self.allowed__go_there(knife)
            else:
                fruit = self.allowed__get_best_fruit(board_state)
                if fruit:
                    self.allowed__go_there(fruit)
                    # self.allowed__go_to_fruit(fruit)
                    #print("fcant", self.allowed__direction_to_return)
        elif self.allowed__is_knife() and len(board_state["snakes"]) > 1:
            can_i = self.allowed__attack(board_state)
            #print("a", self.allowed__direction_to_return)
            if not can_i:
                fruit = self.allowed__get_best_fruit(board_state)
                if fruit:
                    self.allowed__go_there(fruit)
                    #self.allowed__go_to_fruit(fruit)
                    #print("fcant", self.allowed__direction_to_return)
        else:
            fruit = self.allowed__get_best_fruit(board_state)
            if fruit:
                self.allowed__go_there(fruit)
                #self.allowed__go_to_fruit(fruit)
                #print(fruit)
                #print("f", self.allowed__direction_to_return)


        self.allowed__avoid_me(board_state)
        #print("m", self.allowed__direction_to_return)
        self.allowed__avoid_me(board_state)
        #print("m", self.allowed__direction_to_return)
        if not self.allowed__is_knife():
            self.allowed__avoid_other(board_state)
            #print("o", self.allowed__direction_to_return)
            self.allowed__avoid_other(board_state)
            #print("o", self.allowed__direction_to_return)
            self.allowed__dont_crush_into_border()
        #print("b", self.allowed__direction_to_return)
        self.allowed__avoid_skel(board_state)

        #print("final", self.allowed__direction_to_return)
        #print("-----------------")
        return self.allowed__direction_to_return

    """    
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
        """