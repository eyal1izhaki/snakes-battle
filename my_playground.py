#########################################################
#  I test the code here so the run.py file stays clean. #
#########################################################

import pygame
import sys
from time import sleep


from snakes_battle.board import Board
from snakes_battle.fruit import Fruit
from snakes_battle.ai_snake import AISnake
from snakes_battle import graphics,rules

import settings

# Initialization for pygame
pygame.init()

# Creating the surface that we going to print and draw on.
surface = graphics.create_surface()

# Creating the board object. board will hold all the snakes and fruit objects. 
board = Board()


# Creating snakes from the AISnake class. In the competition, players will need to implement their own AISnake class.
snake_a = AISnake(board.get_border_cells())
snake_b = AISnake(board.get_border_cells())

# Adding the snakes to the board
board.add_snake(snake_a)
board.add_snake(snake_b)

# Creating and adding initial fruits on the board.
fruit_a = Fruit(rules.get_new_fruit_position(board))

board.add_fruit(fruit_a)


while True:

    sleep(settings.DELAY_BETWEEN_SCREEN_UPDATES)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    # The AI Snake Should make a decision in which direction to go.
    snake_a.change_direction(board.get_board_state())
    snake_b.change_direction(board.get_board_state())

    snake_a.move_one_cell()
    snake_b.move_one_cell()
    
    rules.apply_rules(board)

    graphics.update_screen(surface, board)
    