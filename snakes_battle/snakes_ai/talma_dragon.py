from os import close
from snakes_battle.fruit import Fruit, FruitKind
from snakes_battle.snake import Snake, Direction


AINT_ACTIVATE  = 0
ACTIVE = -1

DIRECTION_FIELD = "direction"
FRUIT_FIELD = "fruit"

class TalmaDragon(Snake):
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

    
    def make_decision(self, board_state):
        # You can only call methods that starts with the word 'allowed__'. You can't change attrbiutes directly.


        '''super().allowed__get_direction() # This function takes no arguments and returns the direction of the snake.
        super().allowed__body_position() # This function takes no arguments and returns a list with all cells (x,y) that are filled with your snake.
        super().allowed__is_king() # returns True if your snake is king else returns False
        super().allowed__is_knife() # returns True if your snake has a knife else returns False.
        super().allowed__is_shield() # returns True if your snake is shielded else returns False.'''
        #self.print_something(super().allowed__body_position())
        possible_directions = [Direction.RIGHT, Direction.LEFT, Direction.UP, Direction.DOWN]
        self.allowed__is_hit_border(possible_directions)
        #self.print_something(possible_directions)
        # Finds the fruit I wanna eat 
        target_fruit = self.allowed__find_target_fruit(board_state['fruits'], possible_directions)
        if target_fruit[FRUIT_FIELD] == None:
            print("fucking shit")
            return possible_directions[0]
        # If safe ignores the enemy and self hit
        if (self.allowed__is_safe() != AINT_ACTIVATE):
            return self.allowed__calculates_direction(target_fruit[FRUIT_FIELD].pos, possible_directions)

        # Checks self hit 
        self.allowed__dangerous_targets_iterate \
            (super().allowed__body_position(), possible_directions)
        #self.print_something(possible_directions)
        # If can attack enemy not dangerous
        if (self.allowed__is_attack() != AINT_ACTIVATE):
            return self.allowed__calculates_direction(target_fruit[FRUIT_FIELD].pos, possible_directions)

        # Checks enemy hit 
        for enemy in board_state['snakes']:
            self.allowed__dangerous_targets_iterate \
                (enemy.allowed__body_position(), possible_directions)
        #self.print_something(possible_directions)
         
        decision = self.allowed__calculates_direction(target_fruit[FRUIT_FIELD].pos, possible_directions)
        #self.print_something(decision)
        return decision


    def allowed__find_target_fruit(self, fruits, possible_directions):

        close_strawberry_dist:int = 100
        close_dragon_fruit_dist:int = 100
        close_shield_dist:int = 100
        close_king_dist:int = 100
        close_knife_dist:int = 100

        close_strawberry:Fruit = None
        close_dragon_fruit:Fruit = None
        close_shield:Fruit = None
        close_king:Fruit = None
        close_knife:Fruit = None

        for fruit in fruits:
            curr_distance = self.allowed__get_distance(fruit.pos)
            if fruit.kind == FruitKind.DRAGON_FRUIT and curr_distance < close_dragon_fruit_dist:
                close_dragon_fruit = fruit
                close_dragon_fruit_dist = curr_distance
            elif fruit.kind == FruitKind.STRAWBERRY and curr_distance < close_strawberry_dist:
                close_strawberry = fruit
                close_strawberry_dist = curr_distance
            elif fruit.kind == FruitKind.SHIELD and curr_distance < close_shield_dist:
                close_shield = fruit
                close_shield_dist = curr_distance
            elif fruit.kind == FruitKind.KING and curr_distance < close_king_dist:
                close_king = fruit
                close_king_dist = curr_distance
            elif fruit.kind == FruitKind.KNIFE and curr_distance < close_knife_dist:
                close_knife = fruit
                close_king_dist = curr_distance
            elif fruit.kind == FruitKind.SKULL or fruit.kind == FruitKind.BOMB:
                bad_direction = self.allowed__is_hit(fruit.pos)
                if(bad_direction != AINT_ACTIVATE):
                    possible_directions.remove(bad_direction)

        fruits = [{DIRECTION_FIELD: close_strawberry_dist, FRUIT_FIELD: close_strawberry},\
                    {DIRECTION_FIELD: close_dragon_fruit_dist, FRUIT_FIELD: close_dragon_fruit},\
                    {DIRECTION_FIELD: close_shield_dist, FRUIT_FIELD: close_shield},\
                    {DIRECTION_FIELD: close_king_dist, FRUIT_FIELD: close_king},\
                    {DIRECTION_FIELD: close_knife_dist, FRUIT_FIELD: close_knife}]

        closest_dist = [fruit[DIRECTION_FIELD] for fruit in fruits if fruit != None]
        closest_dist.sort()
        
        return [fruit for fruit in fruits if fruit[DIRECTION_FIELD] == closest_dist[0]][0]


    def allowed__dangerous_targets_iterate(self, iter_targets, possible_directions):
        for pos in iter_targets:
            is_hit = self.allowed__is_hit(pos)
            if is_hit != AINT_ACTIVATE and is_hit in possible_directions:
                possible_directions.remove(is_hit)


    def allowed__is_hit(self, target):
        my_x, my_y = super().allowed__body_position()[0] 
        target_x, target_y = target
        if my_x + 1 == target_x and my_y == target_y:
            return Direction.RIGHT
        if my_x - 1 == target_x and my_y == target_y:
            return Direction.LEFT
        if my_x == target_x and my_y + 1 == target_y:
            return Direction.DOWN
        if my_x == target_x and my_y - 1 == target_y:
            return Direction.UP
        return AINT_ACTIVATE


    def allowed__get_distance(self, target):
        my_x, my_y = super().allowed__body_position()[0]
        target_x, target_y = target

        return abs(my_x - target_x) + abs(my_y - target_y)


    def allowed__calculates_direction(self, target, possible_directions) -> int:
        my_x, my_y = super().allowed__body_position()[0] 
        target_x, target_y = target

        if(my_x >= target_x and my_y >= target_y):
            favorite_direction = Direction.UP if my_x == target_x else Direction.LEFT
            if favorite_direction in possible_directions:
                #print("target up and left")
                return favorite_direction
            favorite_direction = Direction.UP if favorite_direction == Direction.LEFT else Direction.LEFT
            if favorite_direction in possible_directions:
                #print("target up and left")
                return favorite_direction
            return possible_directions[0]
        
        if(my_x >= target_x and my_y <= target_y):
            favorite_direction = Direction.UP if my_x == target_x else Direction.RIGHT
            if favorite_direction in possible_directions:
                #print("target up and right")
                return favorite_direction
            favorite_direction = Direction.UP if favorite_direction == Direction.RIGHT else Direction.RIGHT
            if favorite_direction in possible_directions:
                #print("target up and right")
                return favorite_direction
            return possible_directions[0]

        if(my_x <= target_x and my_y >= target_y):
            favorite_direction = Direction.DOWN if my_x == target_x else Direction.LEFT
            if favorite_direction in possible_directions:
                #print("target down and left")
                return favorite_direction
            favorite_direction = Direction.DOWN if favorite_direction == Direction.LEFT else Direction.LEFT
            if favorite_direction in possible_directions:
                #print("target down and left")
                return favorite_direction
            return possible_directions[0]
        
        if(my_x <= target_x and my_y >= target_y):
            favorite_direction = Direction.DOWN if my_x == target_x else Direction.RIGHT
            if favorite_direction in possible_directions:
                #print("target down and right")
                return favorite_direction
            favorite_direction = Direction.DOWN if favorite_direction == Direction.RIGHT else Direction.RIGHT
            if favorite_direction in possible_directions:
                #print("target down and right")
                return favorite_direction
            return possible_directions[0]

        return possible_directions[0]
        
    
    def allowed__is_safe(self) -> int:
        if super().allowed__is_king():
            return super().allowed__get_king_remaining_effection()
        elif super().allowed__is_shield():
            return ACTIVE
        return AINT_ACTIVATE


    def allowed__is_attack(self) -> int:
        if super().allowed__is_king():
            return super().allowed__get_king_remaining_effection()
        elif super().allowed__is_knife():
            return ACTIVE
        return AINT_ACTIVATE


    def allowed__is_hit_border(self, possible_directions):
        my_x, my_y = super().allowed__body_position()[0]
        border_x, bordar_y = self.allowed__border_cells[-1]
        if my_x + 1 == border_x:
            possible_directions.remove(Direction.RIGHT)
        if my_x - 1 == 0:
            possible_directions.remove(Direction.LEFT)
        if my_y + 1 == bordar_y:
            possible_directions.remove(Direction.DOWN)
        if my_y - 1 == 0:
            possible_directions.remove(Direction.UP)


    def print_something(self, something):
        print("--------------------")
        print(something)
        print("--------------------")