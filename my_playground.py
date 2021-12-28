#########################################################
#  I test the code here so the run.py file stays clean. #
#########################################################

import pygame
import sys
import time

from snakes_battle.board import Board
from snakes_battle.snakes_ai.simple_snake import SimpleSnake
from snakes_battle import logic
from snakes_battle.graphics import GameGraphics
from tkinter import messagebox,Tk
import settings
from snakes_battle.fruit import FruitKind, Fruit

graphics = GameGraphics()
board = Board(graphics.board_size)

snake_a = SimpleSnake(board.border_cells, color=graphics.get_unique_snake_color(), name="Yagel")
snake_b = SimpleSnake(board.border_cells, color=graphics.get_unique_snake_color(), name="David")


snakes_array = [snake_a, snake_b]

for snake in snakes_array:
    # The position of the head is determined by the rules and the board state.
    head_pos = logic.get_unique_snake_head_position(board)
    snake.body_pos = [head_pos]

    snake.grow(settings.STARTING_SNAKE_LENGTH - 1)

    board.add_snake(snake)

board.add_fruit(Fruit(FruitKind.STRAWBERRY, logic.get_new_fruit_position(board)))

while not board.is_game_timed_out() and len(board.snakes) > 0:
    time.sleep(settings.DELAY_BETWEEN_SCREEN_UPDATES)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                pass
    # The AI Snake Should make a decision in which direction to go.
    for snake in board.snakes:
        snake.change_direction(board.get_board_state())
        snake.move_one_cell()


    logic.apply_logic(board)

    graphics.update_screen(board)


combined_snakes = board.snakes + board.lost_snakes
snakes_win = [combined_snakes[0]]

for snake in combined_snakes[1:]:
    if snakes_win[0].length == snake.length:
        snakes_win.append(snake)
    elif snakes_win[0].length < snake.length:
        snakes_win = [snake]

# I added this root object to hide the root window that io displayed when we call the messagebox info.
root = Tk()
root.withdraw()
messagebox.showinfo("winner", snakes_win[0].name + " is the winner!!!")
root.destroy()
