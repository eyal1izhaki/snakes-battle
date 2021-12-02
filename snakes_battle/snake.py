import settings

class Direction:
    RIGHT = 0
    LEFT = 1
    UP = 2
    DOWN = 3

class Snake:

    def __init__(self) -> None:
        self.color = (53, 117, 58)
        self.direction = Direction.DOWN
        self.length = 3
        self.body_pos = [25,10]

        for i in range(settings.STARTING_SNAKE_SIZE-1):
            self._grow_in_one_unit()


    def _grow_in_one_unit(self):
        # Makes the snake one cell longer. Will be called when a snake eats a fruit for example


        # TODO: Fix the growth of the snake, the new unit should be added in the previous position of the tail
        tail_x, tail_y = self.body_pos[-1]

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
