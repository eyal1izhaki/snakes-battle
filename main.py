#########################################################
#  I test the code here so the run.py file stays clean. #
#########################################################

import pygame
import sys
import time

from snakes_battle.board import Board
from snakes_battle.snakes_ai.random_snake import RandomSnake
from snakes_battle.snakes_ai.simple_snake import SimpleSnake
from snakes_battle import logic
from snakes_battle.graphics import GameGraphics
from tkinter import messagebox,Tk
import settings
from snakes_battle.fruit import FruitKind, Fruit

ai_classes_available = [{ "class": RandomSnake, "should_play": False }, { "class": SimpleSnake, "should_play": False }]

def main():
    should_exit = False
    game_running = False
    game_menus = True

    graphics = GameGraphics()

    while (should_exit == False):
        if (game_running == True):
            playing_classes = [x['class'] for x in ai_classes_available if x["should_play"] == True]
            if (len(playing_classes) > 0):
                run_game(graphics, playing_classes)
            else:
                root = Tk()
                root.withdraw()
                messagebox.showinfo("Error", "Cannot play without any snakes chosen!")
                root.destroy()
            game_menus = True
            game_running = False

        elif (game_menus == True):
            menus_return = run_menus(graphics)
            if (menus_return['action'] == "Exit"):
                pygame.quit()
                should_exit = True
            elif(menus_return['action'] == "Play"):
                game_menus = False
                game_running = True



def run_menus(graphics):
    global ai_classes_available # A global just for it to be more accessible

    menu_running = True

    main_menu = True
    snake_picker = False

    while (menu_running == True):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return "Exit"
            if event.type == pygame.KEYDOWN:
                for index, class_dict in enumerate(ai_classes_available):
                    if (event.key == settings.PYGAME_START_NUMBER_PRESS_VALUE + index):
                        class_dict['should_play'] = not class_dict['should_play']


        if (main_menu == True):
            menu_action = graphics.draw_menu(ai_classes_available, events)
            if (menu_action == 'Exit'):
                return {"action": menu_action, "args": ""}
            elif (menu_action == 'Play'):
                return {"action": menu_action, "args": ""}

        elif (snake_picker == True):
            pass

def run_game(graphics, playing_classes):
    board = Board(graphics.board_size)

    snakes_array = []

    for snake_class in playing_classes:
        snakes_array.append(snake_class(board.border_cells, color=graphics.get_unique_snake_color(), name=snake_class.__name__))

    for snake in snakes_array:
        # The position of the head is determined by the rules and the board state.
        head_pos = logic.get_unique_snake_head_position(board)
        snake.body_pos = [head_pos]

        snake.grow(settings.STARTING_SNAKE_LENGTH - 1)

        board.add_snake(snake)

    board.add_fruit(Fruit(FruitKind.STRAWBERRY, logic.get_new_fruit_position(board)))

    while not board.is_game_timed_out() and len(board.snakes) > 0:
        time.sleep(settings.DELAY_BETWEEN_SCREEN_UPDATES)

        should_exit = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                should_exit = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    pass
        
        if (should_exit == True):
            break

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

if (__name__ == "__main__"):
    main()
