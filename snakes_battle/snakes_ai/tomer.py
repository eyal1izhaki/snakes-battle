import math
import random
from random import choice

from snakes_battle.fruit import FruitKind
from snakes_battle.snake import Snake, Direction


class Tomer(Snake):

    def __init__(self, borders_cells, color, name) -> None:
        super().__init__(color, name)
        self.init(borders_cells)

    ##############################
    # You can edit only the code below. You can't change methods names.
    ##############################

    def init(self, borders_cells):
        # Your bot initializations will be here.
        self.allowed__version = "ICTORY"

        # All the cells that are fill with borders. This variable will store a list of (x, y) pairs
        self.allowed__border_cells = borders_cells
        self.priority = ["KING", "SHIELD",  "KNIFE", "DRAGON_FRUIT", "STRAWBERRY"]

    def make_decision(self, board_state):
        # You can only call methods that starts with the word 'allowed__'. You can't change attrbiutes directly.

        # super().allowed__get_direction() # This function takes no arguments and returns the direction of the snake.
        # super().allowed__body_position() # This function takes no arguments and returns a list with all cells (x,y) that are filled with your snake.
        # super().allowed__is_king() # returns True if your snake is king else returns False
        # super().allowed__is_knife() # returns True if your snake has a knife else returns False.
        # super().allowed__is_shield() # returns True if your snake is shielded else returns False.
        fruits = board_state["fruits"]
        snakes = board_state["snakes"]
        pos = super().allowed__body_position()
        self.can_kill_me = self.enemy_can_kill_me(snakes)
        self.priority = ["KING", "KNIFE", "SHIELD", "DRAGON_FRUIT", "STRAWBERRY"]

        x = pos[0][0]
        y = pos[0][1]

        if len(snakes) > 1:
            if super().allowed__is_king() or super().allowed__is_knife():
                return self.kill(x, y, self.get_enemy_neck_pos(x, y, snakes, fruits), snakes, fruits)
        where = self.go_get_it_safer(x, y, self.choose_best_fruit_from_array(fruits, x, y), snakes, fruits)
        print(where)
        return where

    def avoid_that(self, snakes, fruits):
        bad_fruits = ["SKULL", "BOMB"]
        my_snake_pos = super().allowed__body_position()
        my_snake_pos = my_snake_pos[2::]  # without head and neck
        snakes_pos, bad_poses = [], []

        if not super().allowed__is_shield:
            bad_poses += my_snake_pos
        # bad_poses += my_snake_pos  # there is no way crashing into myself is good
        bad_poses += self.allowed__border_cells

        for s in snakes:
            if s.name != "Tomer":
                if super().allowed__is_king() or super().allowed__is_knife():
                    print("King Knife")
                else:

                    # if not super().allowed__is_king() or not super().allowed__is_knife():
                    bad_poses += s.body_pos  # if i cant kill him i should avoid him

        for b in bad_fruits:
            for f in fruits:
                if f.kind["name"] == b:
                    # print(f.kind["name"], f.pos)
                    bad_poses.append(f.pos)
        # return super().allowed__body_position()
        return bad_poses

        # return list(set(bad_poses))
        # x = [(20, 0), (20, 1), (20, 2), (20, 3), (20, 4), (20, 5), (20, 6), (20, 7), (20, 8), (20, 9), (20, 10),
        #      (20, 11), (20, 12), (20, 13), (20, 14), (20, 15), (20, 16), (20, 17), (20, 18), (20, 19), (20, 20),
        #      (20, 21), (20, 22), (20, 23), (20, 24), (20, 25), (20, 26), (20, 27), (20, 28), (20, 29), (20, 30),
        #      (20, 31), (20, 32), (20, 33)]
        # y = x + self.allowed__border_cells
        # print(y)
        # return y

    def kill(self, x, y, neck, snakes, fruits):
        return self.go_get_it_safer(x, y, neck, snakes, fruits)

    def go_get_it(self, x, y, pos, snakes, fruits):

        if x > pos[0]:
            if self.direction == Direction.RIGHT:
                return Direction.UP
            else:
                return Direction.LEFT

        if x < pos[0]:
            if self.direction == Direction.LEFT:
                return Direction.UP
            else:
                return Direction.RIGHT

        if x == pos[0]:
            if y < pos[1]:
                if self.direction == Direction.UP:
                    return Direction.RIGHT
                else:
                    return Direction.DOWN

            if y > pos[1]:
                if self.direction == Direction.DOWN:
                    return Direction.RIGHT
                else:
                    return Direction.UP
        return Direction.DOWN

    def get_enemy_neck_pos(self, x, y, snakes, fruits):
        for s in snakes:
            if s.name != "Tomer":
                return s.body_pos[1]
        # return self.find_best_fruit(fruits)  # if I am the only snake I will go to the fruit
        return self.choose_best_fruit_from_array(fruits, x, y)

    def find_best_fruit(self, fruits):
        best_type_of_food_locations = []
        for p in self.can_kill_me:
            for f in fruits:
                if f.kind["name"] == p:
                    best_type_of_food_locations.append(f.pos)
                    # return f.pos

        return best_type_of_food_locations if best_type_of_food_locations else None

    def choose_best_fruit_from_array(self, fruits, x, y):
        arr = self.find_best_fruit(fruits)
        arr = sorted(arr, key=lambda a: math.dist((x, y), a))
        return arr[0]

    def get_opposite_direction(self):
        if self.direction == Direction.DOWN:
            return Direction.UP
        elif self.direction == Direction.UP:
            return Direction.DOWN
        elif self.direction == Direction.LEFT:
            return Direction.RIGHT
        elif self.direction == Direction.RIGHT:
            return Direction.LEFT

    def get_safe_directions(self, x, y, bad_poses):
        a = [Direction.RIGHT, Direction.LEFT, Direction.UP, Direction.DOWN]
        a.remove(self.get_opposite_direction())

        for pos in bad_poses:
            if x + 1 == pos[0] and y == pos[1]:
                try:
                    print(f"({x, y}) -> Removed RIGHT for POS {pos}")
                    a.remove(Direction.RIGHT)
                except:
                    pass

            if x - 1 == pos[0] and y == pos[1]:
                try:
                    print(f"({x, y}) -> Removed LEFT for POS {pos}")
                    a.remove(Direction.LEFT)
                except:
                    pass

            if y - 1 == pos[1] and x == pos[0]:
                try:
                    print(f"({x, y}) -> Removed UP for POS {pos}")
                    a.remove(Direction.UP)
                except:
                    pass

            if y + 1 == pos[1] and x == pos[0]:
                try:
                    print(f"({x, y}) -> Removed DOWN for POS {pos}")
                    a.remove(Direction.DOWN)
                except:
                    pass

        return a

    def enemy_can_kill_me(self, snakes):

        if len(snakes) == 1:  # no enemies
            return ["DRAGON_FRUIT", "STRAWBERRY", "KING", "SHIELD", "KNIFE"]
        for s in snakes:
            if s.name != "Tomer":
                if s.allowed__is_knife() or s.allowed__is_king():
                    return ["KING", "SHIELD", "KNIFE", "DRAGON_FRUIT", "STRAWBERRY"]
        return self.priority

    def go_get_it_safer(self, x, y, pos, snakes, fruits):

        safe_directions = self.get_safe_directions(x, y, self.avoid_that(snakes, fruits))
        print(f"safe {safe_directions}")

        if len(pos) > 1 and isinstance(pos, list):
            if isinstance(pos[0], list):
                pos = pos[0]

        if x > pos[0]:
            if self.direction == Direction.RIGHT:
                if Direction.UP in safe_directions:
                    return Direction.UP
            else:
                if Direction.LEFT in safe_directions:
                    return Direction.LEFT

        if x < pos[0]:
            if self.direction == Direction.LEFT:
                if Direction.UP in safe_directions:
                    return Direction.UP
            else:
                if Direction.RIGHT in safe_directions:
                    return Direction.RIGHT

        if x == pos[0]:
            if y < pos[1]:
                if self.direction == Direction.UP:
                    if Direction.RIGHT in safe_directions:
                        return Direction.RIGHT
                else:
                    if Direction.DOWN in safe_directions:
                        return Direction.DOWN

            if y > pos[1]:
                if self.direction == Direction.DOWN:
                    if Direction.RIGHT in safe_directions:
                        return Direction.RIGHT
                else:
                    if Direction.UP in safe_directions:
                        return Direction.UP
        if Direction.DOWN in safe_directions:
            return Direction.DOWN

        if safe_directions:
            return random.choice(safe_directions)

        return Direction.DOWN
