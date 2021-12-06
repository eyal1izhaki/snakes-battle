
# All the rules of the game should be defined here.
# For example, If snake eats a fruit, we grows. If a snake hit a border a loses and so on...

import random
import sys
import time
import settings
from snakes_battle.fruit import Fruit

def apply_rules(board):
    for snake in board.snakes:

        # Rule: Snake eat a fruit
        for fruit in board.fruits:
            if snake.body_pos[0] == fruit.pos: # if head of snake in the same position of the fruit

                snake.eat(fruit)

                board.fruit_eaten(fruit)

                board.add_fruit(Fruit(get_new_fruit_position(board)))


        # Rule: Snake hitted a border
        if snake.body_pos[0][0] == settings.BORDER_THICKNESS-1: # Hitted left border
            snake_lost(snake)

        if snake.body_pos[0][0] == settings.BOARD_SIZE[0] - settings.BORDER_THICKNESS: # Hitted right border
            snake_lost(snake)

        if snake.body_pos[0][1] == settings.BORDER_THICKNESS-1: # Hitted upper border
            snake_lost(snake)

        if snake.body_pos[0][1] == settings.BOARD_SIZE[1] - settings.BORDER_THICKNESS: # Hitted bottom border
            snake_lost(snake)


        # Rule: Snake hitted itself or other snakes
        for _snake in board.snakes:

            if snake == _snake: # snake hitted itself.
                if snake.body_pos[0] in _snake.body_pos[1:]:
                    snake_lost(snake)

            elif snake.body_pos[0] in _snake.body_pos: # snake hitted other snakes
                snake_lost(snake)

def snake_lost(snake):
    time.sleep(5)
    sys.exit(0)


def get_new_fruit_position(board):
    # Returns an empty cell so a fruit can be placed there
    
    board._update_empty_cells()
    return list(random.choice(board.empty_cells))

