from random import randint, choice
import settings
import copy
import math

class Direction:
    RIGHT = 0
    LEFT = 1
    UP = 2
    DOWN = 3

class Snake:
    all_snakes_start_position = []
    all_available_colors = settings.SNAKES_COLORS

    def __init__(self) -> None:

        # Picking a random color
        self.color = choice(self.all_available_colors)

        # Removing the picked color so other snakes won't be in this color.
        self.all_available_colors.remove(self.color)
        
        self.direction = randint(0,3) # Only 4 directions - will pick one of them
        self.length = 1

        # Generating random and unique position to the head of the snake, that will not collide with other snake's tail
        generate_position = True
        random_head_position = self.generate_random_position()
        while (generate_position == True):
            random_head_position = self.generate_random_position()
            too_close = False
            for position in Snake.all_snakes_start_position:
                if (math.dist(position, random_head_position) < settings.STARTING_SNAKE_LENGTH):
                    too_close = True
                    break
            generate_position = too_close
        self.body_pos = [ random_head_position ]

        for i in range(settings.STARTING_SNAKE_LENGTH-1):
            self._grow_in_one_unit()
        
        # Making sure the snake's positions will not be generated again
        for position in self.body_pos:
            Snake.all_snakes_start_position.append(position)

    def generate_random_position(self):
        return [
                randint(settings.BORDER_THICKNESS, settings.BOARD_SIZE[0]-settings.BORDER_THICKNESS-1),
                randint(settings.BORDER_THICKNESS, settings.BOARD_SIZE[1]-settings.BORDER_THICKNESS-1)
            ]

    def _grow_in_one_unit(self):
        # Makes the snake one cell longer. Will be called when a snake eats a fruit for example

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


    def eat(self, fruit):
        # The snake eats a fruit, it grows as the fruit value.

        for i in range(fruit.value):
            self._grow_in_one_unit()
