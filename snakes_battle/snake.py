from random import randint
import copy

from snakes_battle.fruit import FruitKind

class Direction:
    RIGHT = 0
    LEFT = 1
    UP = 2
    DOWN = 3

class Snake:

    def __init__(self, color, name) -> None:

        self.name = name
        self.color = color
        
        self.direction = randint(0,3) # Only 4 directions - will pick one of them
        self.length = 1
        self.body_pos = None

        # All the special fruits that active in this snake.
        self.super_power = {
            "SHIELD": False,
            "KING": False,
            "KNIFE": False
        }


    def grow(self, growth_amount):
        # Makes the snake <growth_amount> cells longer. Will be called when a snake eats a fruit for example

        for _ in range(growth_amount):
            # Gets the tail position
            tail_x, tail_y = self.body_pos[-1]

            if self.length > 1:

                tail_neighbor_x, tail_neighbor_y = self.body_pos[-2]

                # Adding the new cell above the tail cell.
                if  tail_y < tail_neighbor_y:
                    self.body_pos.append([tail_x, tail_y-1])

                # Adding the new cell under the tail cell.
                elif tail_y > tail_neighbor_y:
                    self.body_pos.append([tail_x, tail_y+1])

                # Adding the new cell right to the tail cell
                elif tail_x > tail_neighbor_x:
                    self.body_pos.append([tail_x+1, tail_y])

                # Adding the new cell left to the tail cell
                elif tail_x < tail_neighbor_x:
                    self.body_pos.append([tail_x-1, tail_y])

            # In case the length of the snake is 1.  This pieace of code runs only once - when the snake is created.
            else:
                if self.direction == Direction.DOWN:
                    self.body_pos.append([tail_x, tail_y-1])

                elif self.direction == Direction.UP:
                    self.body_pos.append([tail_x, tail_y+1])

                elif self.direction == Direction.LEFT:
                    self.body_pos.append([tail_x+1, tail_y])

                elif self.direction == Direction.RIGHT:
                    self.body_pos.append([tail_x-1, tail_y])


            self.length += 1

    def _update_body_pos(self):
        # updates the position of the rest of the snake's body. The position of the head changes in the continuse_movement method.

        for i in reversed(range(1, self.length)):
            self.body_pos[i][0] = self.body_pos[i-1][0]
            self.body_pos[i][1] = self.body_pos[i-1][1]

    def get_body_position(self):
        return copy.deepcopy(self.body_pos)

    def change_direction(self, direction: int):
        # Changes the direcation of the snake.

        if direction == Direction.LEFT:
            if self.direction == Direction.UP or self.direction == Direction.DOWN:
                self.direction = Direction.LEFT

        elif direction == Direction.RIGHT:
            if self.direction == Direction.UP or self.direction == Direction.DOWN:
                self.direction = Direction.RIGHT

        elif direction == Direction.UP:
            if self.direction == Direction.RIGHT or self.direction == Direction.LEFT:
                self.direction = Direction.UP

        elif direction == Direction.DOWN:
            if self.direction == Direction.RIGHT or self.direction == Direction.LEFT:
                self.direction = Direction.DOWN

    def move_one_cell(self):
        # Changes the position of the snake's head. The position of each block in the snake's body
        # varies depending on the position of the neighboring block.

        self._update_body_pos()
        
        if self.direction == Direction.DOWN:
            self.body_pos[0][1] += 1
        elif self.direction == Direction.UP:
            self.body_pos[0][1] -= 1
        elif self.direction == Direction.LEFT:
            self.body_pos[0][0] -= 1
        elif self.direction == Direction.RIGHT:
            self.body_pos[0][0] += 1

    def shrink(self, shrinking_amount):
        self.length -= min(self.length, shrinking_amount)
        if (self.length == 0):
            self.body_pos = []
            return
        
        self.body_pos = self.body_pos[:self.length] # Removing nodes from the snake

    def eat(self, fruit):
        if fruit.kind in FruitKind.beneficial_fruits:
            self.grow(fruit.kind["score"])

        elif fruit.kind in FruitKind.harmful_fruits:
            if self.super_power["SHIELD"]:
                self.super_power["SHIELD"] = False
                return
            
            if fruit.kind == FruitKind.BOMB:
                self.shrink(-fruit.kind["score"])
            elif fruit.kind == FruitKind.SKULL:
                self.shrink(self.length)
        
        elif fruit.kind in FruitKind.special_fruits:
            if fruit.kind == FruitKind.SHIELD:
                self.super_power["SHIELD"] = True
            elif fruit.kind == FruitKind.KING:
                self.super_power["KING"] = True
            elif fruit.kind == FruitKind.KNIFE:
                self.super_power["KNIFE"] = True
