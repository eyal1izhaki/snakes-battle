
# All the rules of the game should be defined here.
# For example, If snake eats a fruit, we grows. If a snake hit a border a loses and so on...

import random

import settings

def apply_rules(board):
    for snake in board.snakes:

        # Checks if this snake eat a fruit
        for fruit in board.fruits:
            if snake.body_pos[0] == fruit.pos: # if head of snake in the same position of the fruit
                snake.eat(fruit)
                board.fruit_eaten(fruit)

        # checks if the snake hitted a border
        if snake.body_pos[0][0] == settings.BORDER_THICKNESS-1: # Hitted left border
            return False
        if snake.body_pos[0][0] == settings.BOARD_SIZE[0] - settings.BORDER_THICKNESS: # Hitted right border
            return False
        if snake.body_pos[0][1] == settings.BORDER_THICKNESS-1: # Hitted upper border
            return False
        if snake.body_pos[0][1] == settings.BOARD_SIZE[1] - settings.BORDER_THICKNESS: # Hitted bottom border
            return False
        
        return True

        # Checks if the snake hitted itself or other snakes



def get_new_fruit_position(board):
    board._update_empty_cells()
    return list(random.choice(board.empty_cells))

