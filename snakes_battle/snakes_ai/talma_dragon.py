from os import close
from snakes_battle.fruit import FruitKind
from snakes_battle.snake import Snake, Direction


AINT_ACTIVATE  = 0
ACTIVE = -1

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

        possible_directions = [Direction.RIGHT, Direction.LEFT, Direction.UP, Direction.DOWN]
        possible_directions = self.allowed__is_hit_border(possible_directions)
        '''super().allowed__get_direction() # This function takes no arguments and returns the direction of the snake.
        super().allowed__body_position() # This function takes no arguments and returns a list with all cells (x,y) that are filled with your snake.
        super().allowed__is_king() # returns True if your snake is king else returns False
        super().allowed__is_knife() # returns True if your snake has a knife else returns False.
        super().allowed__is_shield() # returns True if your snake is shielded else returns False.'''

        favorite_direction = Direction.DOWN

        

        close_strawberry_dist = 100
        close_dragon_fruit_dist = 100
        close_shield_dist = 100
        close_king_dist = 100
        close_knife_dist = 100


        close_strawberry = None
        close_dragon_fruit = None
        close_shield = None
        close_king = None
        close_knife = None

        for fruit in board_state["fruits"]:
            curr_distance = self.allowed__get_distance(fruit.pos)
            if fruit.kind == FruitKind.DRAGON_FRUIT and curr_distance < close_dragon_fruit:
                close_dragon_fruit = fruit
                close_dragon_fruit_dist = curr_distance
            elif fruit.kind == FruitKind.STRAWBERRY and curr_distance < close_strawberry:
                close_strawberry = fruit
                close_strawberry_dist = curr_distance
            elif fruit.kind == FruitKind.SHIELD and curr_distance < close_shield:
                close_shield = fruit
                close_shield_dist = curr_distance
            elif fruit.kind == FruitKind.KING and curr_distance < close_king:
                close_king = fruit
                close_king_dist = curr_distance
            elif fruit.kind == FruitKind.KNIFE and curr_distance < close_knife:
                close_knife = fruit
                close_king_dist = curr_distance
        
        fruits = {close_strawberry_dist: close_strawberry, close_dragon_fruit_dist: close_dragon_fruit, close_shield_dist: close_shield, close_king_dist:close_king, close_knife_dist:close_knife}
        favorite_direction = fruits.keys().sort()[0]
        
        if (self.allowed__is_safe() != AINT_ACTIVATE):
            return self.allowed__calculates_direction(fruits[favorite_direction], possible_directions)

        for enemy in board_state['snakes']:
            ''' Checks enemy hit '''
            for pos in enemy.allowed__body_position():
                hit = self.allowed__check_if_direction_hits(pos)
                if hit != AINT_ACTIVATE:
                    possible_directions.remove(hit)

        return self.allowed__calculates_direction(fruits[favorite_direction], possible_directions)


    def allowed__check_if_direction_hits(self, target):
        my_x, my_y = super().allowed__body_position()[0] 
        target_x, target_y = target
        if my_x + 1 == target_x and my_y == target_y:
            return Direction.DOWN
        if my_x - 1 == target_x and my_y == target_y:
            return Direction.UP
        if my_x == target_x and my_y + 1 == target_y:
            return Direction.RIGHT
        if my_x == target_x and my_y - 1 == target_y:
            return Direction.LEFT
        return AINT_ACTIVATE


    def allowed__get_distance(self, target):
        my_x, my_y = super().allowed__body_position()[0]
        target_x, target_y = target

        return abs(my_x - target_x) + abs(my_y - target_y)

    def allowed__calculates_direction(self, target, possible_directions) -> int:
        my_x, my_y = super().allowed__body_position()[0] 
        target_x, target_y = target

        if(my_x >= target_x and my_y >= target_y):
            if Direction.LEFT in possible_directions:
                return Direction.LEFT
            elif Direction.UP in possible_directions:
                return Direction.UP
            elif Direction.RIGHT in possible_directions:
                return Direction.RIGHT
            return Direction.DOWN
        
        if(my_x >= target_x and my_y <= target_y):
            if Direction.RIGHT in possible_directions:
                return Direction.RIGHT
            elif Direction.UP in possible_directions:
                return Direction.UP
            elif Direction.LEFT in possible_directions:
                return Direction.LEFT
            return Direction.DOWN

        if(my_x <= target_x and my_y >= target_y):
            if Direction.LEFT in possible_directions:
                return Direction.LEFT
            elif Direction.DOWN in possible_directions:
                return Direction.DOWN
            elif Direction.RIGHT in possible_directions:
                return Direction.RIGHT
            return Direction.UP
        
        if(my_x <= target_x and my_y >= target_y):
            if Direction.RIGHT in possible_directions:
                return Direction.RIGHT
            elif Direction.DOWN in possible_directions:
                return Direction.DOWN
            elif Direction.LEFT in possible_directions:
                return Direction.LEFT
            return Direction.UP

        return Direction.DOWN
        
    
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
        border_x, border_y = self.allowed__border_cells[-1]
        if my_x + 1 == border_x:
            possible_directions.remove(Direction.RIGHT)
        if my_x - 1 == border_x:
            possible_directions.remove(Direction.LEFT)
        if my_y + 1 == border_y:
            possible_directions.remove(Direction.DOWN)
        if my_y - 1 == border_y:
            possible_directions.remove(Direction.UP)
        return possible_directions