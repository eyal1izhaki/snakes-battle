
# All the rules of the game should be defined here.
# For example, If snake eats a fruit, we grows. If a snake hit a border a loses and so on...

import random
import sys
import time
import settings
from snakes_battle.fruits.StrawberryFruit import StrawberryFruit
from snakes_battle.fruits.DragonFruit import DragonFruit
from snakes_battle.fruits.Bomb import Bomb

harmfulFruits = (Bomb, ) # List of fruits that should not create new fruits to the board
benefitialFruits = (StrawberryFruit, DragonFruit)

def apply_rules(board):
    for fruit in board.fruits:
        fruit.make_turn(board)

    for snake in board.snakes:
        # Rule: Snake eat a fruit
        for fruit in board.fruits:
            if snake.body_pos[0] == fruit.pos: # if head of snake in the same position of the fruit
                fruit.eaten(snake)

                board.fruit_eaten(fruit)

                # Rule - Snake must have a length of 1 at least (can be lower if the snake was hit by a bomb and it's length was reduced too much)
                if (snake.length == 0):
                    snake_lost(snake,board)

                if (not isinstance(fruit, harmfulFruits)):
                    new_fruit_type = random.choice(benefitialFruits)
                    board.add_fruit(new_fruit_type(get_new_fruit_position(board)))

        # Rule: Snake hitted a border
        if snake.body_pos[0][0] == settings.BORDER_THICKNESS-1: # Hitted left border
            snake_lost(snake,board)

        if snake.body_pos[0][0] == settings.BOARD_SIZE[0] - settings.BORDER_THICKNESS: # Hitted right border
            snake_lost(snake,board)

        if snake.body_pos[0][1] == settings.BORDER_THICKNESS-1: # Hitted upper border
            snake_lost(snake,board)

        if snake.body_pos[0][1] == settings.BOARD_SIZE[1] - settings.BORDER_THICKNESS: # Hitted bottom border
            snake_lost(snake,board)

        # Rule: Snake hitted itself or other snakes
        for _snake in board.snakes:

            if snake == _snake: # snake hitted itself.
                if snake.body_pos[0] in _snake.body_pos[1:]:
                    snake_lost(snake,board)

            elif snake.body_pos[0] in _snake.body_pos: # snake hitted other snakes
                snake_lost(snake,board)
        
        # Rule - generate a bomb randomlly.
        if (random.random() < Bomb.BOMB_CREATION_PROBABILITY):
            board.add_fruit(Bomb(get_new_fruit_position(board)))

def snake_lost(snake,board):
    board.lost_snakes.append(snake)
    board.snakes.remove(snake)

def get_new_fruit_position(board):
    # Returns an empty cell so a fruit can be placed there
    
    board._update_empty_cells()
    return list(random.choice(board.empty_cells))

