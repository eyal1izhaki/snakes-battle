#########################################################
#  I test the code here so the run.py file stays clean. #
#########################################################

import pygame
import sys
import time

from snakes_battle.board import Board
from snakes_battle.fruits.StrawberryFruit import StrawberryFruit
from snakes_battle.ai_snake import AISnake
from snakes_battle import rules
from snakes_battle.graphics import GameGraphics
from tkinter import messagebox
import settings

graphics = GameGraphics()
board = Board(graphics.board_size)

snake_a = AISnake(board.border_cells, color=graphics.get_unique_snake_color(), name="Yagel")
snake_b = AISnake(board.border_cells, color=graphics.get_unique_snake_color(), name="David")

snakes_array = [snake_a, snake_b]

for snake in snakes_array:
    # The position of the head is determined by the rules and the board state.
    head_pos = rules.get_unique_snake_head_position(board)
    snake.body_pos = [head_pos]
    for _ in range(settings.STARTING_SNAKE_LENGTH - 1):
        snake._grow_in_one_unit()

    board.add_snake(snake)

board.add_fruit(StrawberryFruit(rules.get_new_fruit_position(board)))
time_pass = time.time()

while time.time() - time_pass <= settings.GAME_TIME_LENGTH and len(board.snakes) > 0:
    time.sleep(settings.DELAY_BETWEEN_SCREEN_UPDATES)

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

    graphics.update_screen(board)

    rules.apply_rules(board)

combined_snakes = board.snakes + board.lost_snakes
snakes_win = [combined_snakes[0]]

for snake in combined_snakes[1:]:
    if snakes_win[0].length == snake.length:
        snakes_win.append(snake)
    elif snakes_win[0].length < snake.length:
        snakes_win = [snake]

messagebox.showinfo("winner", snakes_win[0].name + " is the winner!!!")
