#########################################################
#  I test the code here so the run.py file stays clean. #
#########################################################

import pygame
import sys
from time import sleep


from snakes_battle.board import Board
from snakes_battle.fruits.StrawberryFruit import StrawberryFruit
from snakes_battle.ai_snake import AISnake
from snakes_battle import graphics,rules

import settings

pygame.init()

surface = graphics.create_surface()
board = Board()


snake_a = AISnake(board.border_cells)
snake_b = AISnake(board.border_cells)

snakes_array = [snake_a]

for snake in snakes_array:
    board.add_snake(snake)

board.add_fruit(StrawberryFruit(rules.get_new_fruit_position(board)))

while True:

    sleep(settings.DELAY_BETWEEN_SCREEN_UPDATES)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                board.add_fruit(StrawberryFruit(rules.get_new_fruit_position(board)))


    # The AI Snake Should make a decision in which direction to go.
    for snake in snakes_array:
        snake.change_direction(board.get_board_state())
        snake.move_one_cell()
    
    graphics.update_screen(surface, board)

    rules.apply_rules(board)
    