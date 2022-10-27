from random import randint
import copy


class Direction:
    RIGHT = 0
    LEFT = 1
    UP = 2
    DOWN = 3
    CONTINUE = 4


class Snake:

    def __init__(self, color, name) -> None:

        self._name = name
        self._color = color

        # Only 4 directions - will pick one of them
        self._direction = randint(0, 3)
        self._length = 1
        self._lost = False # If True, snake will be removed from game
        self._lived_x_frames = 0 # Number of frames the snake lived.

        self._body_position = None
        self._version = "0.0"

        # All the special fruits that can be active in this snake.
        self._shield = False
        self._knife = False
        self._king = False
        self._king_remaining_time = 0

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, value):
        self._version = value

    @property
    def body_position(self):
        return copy.deepcopy(self._body_position)

    @body_position.setter
    def body_position(self, value):
        pass  # Player can't change body_position value

    @property
    def head(self):
        return copy.copy(self._body_position[0])
    
    @head.setter
    def head(self, value):
        pass # Player can't change head value

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value):
        pass  # Player can't change direction value

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self):
        pass  # Player can't change length value

    @property
    def king(self):
        return self._king

    @king.setter
    def king(self, value):
        pass  # Player can't change king value

    @property
    def knife(self):
        return self._knife

    @knife.setter
    def knife(self, value):
        pass  # Player can't change knife value

    @property
    def shield(self):
        return self._shield

    @shield.setter
    def shield(self, value):
        pass  # Player can't change shield value

    @property
    def king_remaining_time(self):
        return self._king_remaining_time

    @king_remaining_time.setter
    def king_remaining_time(self, value):
        pass  # Player can't change 'king_remaining_time' value

    def _grow(self, growth_amount):
        # Makes the snake <growth_amount> cells longer. Will be called when a snake eats a fruit for example

        for _ in range(growth_amount):
            # Gets the tail position
            tail_x, tail_y = self._body_position[-1]

            if self._length > 1:

                tail_neighbor_x, tail_neighbor_y = self._body_position[-2]

                # Adding the new cell above the tail cell.
                if tail_y < tail_neighbor_y:
                    self._body_position.append([tail_x, tail_y-1])

                # Adding the new cell under the tail cell.
                elif tail_y > tail_neighbor_y:
                    self._body_position.append([tail_x, tail_y+1])

                # Adding the new cell right to the tail cell
                elif tail_x > tail_neighbor_x:
                    self._body_position.append([tail_x+1, tail_y])

                # Adding the new cell left to the tail cell
                elif tail_x < tail_neighbor_x:
                    self._body_position.append([tail_x-1, tail_y])

            # In case the length of the snake is 1.  This piece of code runs only once - when the snake is created.
            else:
                if self._direction == Direction.DOWN:
                    self._body_position.append([tail_x, tail_y-1])

                elif self._direction == Direction.UP:
                    self._body_position.append([tail_x, tail_y+1])

                elif self._direction == Direction.LEFT:
                    self._body_position.append([tail_x+1, tail_y])

                elif self._direction == Direction.RIGHT:
                    self._body_position.append([tail_x-1, tail_y])

            self._length += 1

    def _change_direction(self, direction: int):
        # Changes the direction of the snake.

        if direction == Direction.LEFT:
            if self._direction == Direction.UP or self._direction == Direction.DOWN:
                self._direction = Direction.LEFT

        elif direction == Direction.RIGHT:
            if self._direction == Direction.UP or self._direction == Direction.DOWN:
                self._direction = Direction.RIGHT

        elif direction == Direction.UP:
            if self._direction == Direction.RIGHT or self._direction == Direction.LEFT:
                self._direction = Direction.UP

        elif direction == Direction.DOWN:
            if self._direction == Direction.RIGHT or self._direction == Direction.LEFT:
                self._direction = Direction.DOWN
        
        elif direction == Direction.CONTINUE or direction is None:
            pass # Continue in the same direction

    def _move_one_cell(self):
        # Changes the position of the snake's head.

        head = copy.copy(self._body_position[0])

        if self._direction == Direction.DOWN:
            head[1] += 1
        elif self._direction == Direction.UP:
            head[1] -= 1
        elif self._direction == Direction.LEFT:
            head[0] -= 1
        elif self._direction == Direction.RIGHT:
            head[0] += 1

        self._body_position.pop() # Removing tail
        self._body_position.insert(0, head) # Inserting new head
        

    def _shrink(self, shrinking_amount):
        self._length -= min(self._length, shrinking_amount)
        if self._length == 0:
            self._body_position = []
            return

        # Removing nodes from the snake
        self._body_position = self._body_position[:self._length]
    
    def __repr__(self) -> str:
        return f"{self._name}"
