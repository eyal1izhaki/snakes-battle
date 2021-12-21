
# All the rules of the game should be defined here.
# For example, If snake eats a fruit, we grows. If a snake hit a border a loses and so on...

import random
import math
import settings
from snakes_battle.board import Board
from snakes_battle.fruit import Fruit, FruitKind

def apply_logic(board):

    for snake in board.snakes:
        # Rule: Snake eat a fruit
        for fruit in board.fruits:
            if snake.body_pos[0] == fruit.pos: # if head of snake in the same position of the fruit

                snake.eat(fruit)
                board.fruit_eaten(fruit)

                # Rule - Snake must have a length of 1 at least (can be lower if the snake was hit by a bomb and it's length was reduced too much)
                if (snake.length == 0):
                    snake_lost(snake, board)

                if fruit.score > 0:
                    new_fruit = Fruit(random.choice(FruitKind.beneficial_fruits), get_new_fruit_position(board))
                    board.add_fruit(new_fruit)

        # Rule: Snake hitted a border
        if snake.body_pos[0][0] == settings.BORDER_THICKNESS-1: # Hitted left border
            snake_lost(snake,board)

        if snake.body_pos[0][0] == board.board_size[0] - settings.BORDER_THICKNESS: # Hitted right border
            snake_lost(snake,board)

        if snake.body_pos[0][1] == settings.BORDER_THICKNESS-1: # Hitted upper border
            snake_lost(snake,board)

        if snake.body_pos[0][1] == board.board_size[1] - settings.BORDER_THICKNESS: # Hitted bottom border
            snake_lost(snake,board)

        # Rule: Snake hitted itself or other snakes
        for _snake in board.snakes:

            if snake == _snake: # snake hitted itself.
                if snake.body_pos[0] in _snake.body_pos[1:]:
                    snake_lost(snake,board)

            elif snake.body_pos[0] in _snake.body_pos: # snake hitted other snakes
                snake_lost(snake,board)
        
        # Rule - generate a bomb randomly.
        if (random.random() < settings.BOMB_CREATION_PROBABILITY):
            new_bomb = Fruit(FruitKind.BOMB, get_new_fruit_position(board))
            board.add_fruit(new_bomb)

def snake_lost(snake,board):
    board.lost_snakes.append(snake)
    board.snakes.remove(snake)

def get_new_fruit_position(board):
    # Returns an empty cell so a fruit can be placed there
    
    board.update_empty_cells()
    return list(random.choice(board.empty_cells))

def get_unique_snake_head_position(board: Board):

    # Generating random and unique position to the head of the snake, that will not collide with other snake's tail
    generate_position = True
    while (generate_position == True):
        random_head_position = list(random.choice(board.all_cells_pos))
        too_close = False
        for snake in board.snakes:
            if (math.dist(snake.body_pos[0], random_head_position) < settings.STARTING_SNAKE_LENGTH):
                too_close = True
                break
        generate_position = too_close

    return random_head_position



