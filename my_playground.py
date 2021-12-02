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

pygame.init()

surface = graphics.create_surface()
board = Board()


snake_a = AISnake(board.border_cells)

board.add_snake(snake_a)

while True:

    sleep(settings.DELAY_BETWEEN_SCREEN_UPDATES)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

                # if event.key == pygame.K_LEFT:
                #     snake_a.change_direction(Direction.LEFT)
                
                # elif event.key == pygame.K_RIGHT:
                #     snake_a.change_direction(Direction.RIGHT)

                # elif event.key == pygame.K_UP:
                #     snake_a.change_direction(Direction.UP)

                # elif event.key == pygame.K_DOWN:
                #     snake_a.change_direction(Direction.DOWN)

                if event.key == pygame.K_a:
                    board.add_fruit(Fruit((232, 17, 35)))


    # The AI Snake Should make a decision in what direction to go.
    snake_a.change_direction(board.get_board_state())

    snake_a.move_one_cell()

    rules.apply_rules(board)

    graphics.update_screen(surface, board)
    