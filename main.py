#########################################################
#  I test the code here so the run.py file stays clean. #
#########################################################

from random import choice, random
import pygame
import sys
import time

from snakes_battle.board import Board
from snakes_battle.exceptions import InvalidDirection
from snakes_battle.snakes_ai.random_snake import RandomSnake
from snakes_battle.snakes_ai.simple_snake import SimpleSnake
from snakes_battle.snakes_ai.moshes_snake import MoshesSnake
from snakes_battle.snakes_ai.manual_control_snake import ManualSnake
from snakes_battle.snakes_ai.manual_control_snake_wasd import ManualSnakeWASD
from snakes_battle.snakes_ai.snakysnake import SnakySnake
from snakes_battle.snakes_ai.worstSnakeEU import WorstSnakeEU
from snakes_battle.snakes_ai.dumpster import Dumpster
from snakes_battle.snakes_ai.yoav_snake import YoavSnake
from snakes_battle.snakes_ai.elitz_snake import ElitzSnake
from snakes_battle.snakes_ai.chaim_snake import ChaimSnake
from snakes_battle.snakes_ai.ari_snake import AriSnake
from snakes_battle.snakes_ai.yakov_snake import Yakov
from snakes_battle import logic
from snakes_battle.graphics import GameGraphics
import settings
from snakes_battle.fruit import FruitKind, Fruit


def main():
    ai_classes_available = [
        {"class": Dumpster, "should_play": False},
        # {"class": RandomSnake, "should_play": False},
        {"class": YoavSnake, "should_play": False},
        # {"class": SimpleSnake, "should_play": False},
        # {"class": ManualSnake, "should_play": False},
        # {"class": ManualSnakeWASD, "should_play": False},
        {"class": MoshesSnake, "should_play": False},
        {"class": SnakySnake, "should_play": False},
        # {"class": WorstSnakeEU, "should_play": False},
        {"class": ElitzSnake , "should_play": False},
        {"class": ChaimSnake, "should_play": False},
        {"class": AriSnake, "should_play": False},
        {"class": Yakov, "should_play": False},
    ]

    should_exit = False
    game_running = False
    game_menus = True
    run_num = 0

    graphics = GameGraphics(ai_classes_available)

    while should_exit == False:
        if game_running == True:
            playing_classes = [x['class']
                               for x in ai_classes_available if x["should_play"] == True]
            if len(playing_classes) > 0:
                run_num += 1
                print(
                    f"\n\n######################### Game Number {run_num} #########################\n")
                run_game(playing_classes, ai_classes_available)
                print(
                    f"\n#################################################################")

            game_menus = True
            game_running = False

        elif game_menus == True:
            menus_return = run_menus(graphics, ai_classes_available)
            if menus_return['action'] == "Exit":
                pygame.quit()
                should_exit = True
            elif menus_return['action'] == "Play":
                game_menus = False
                game_running = True


def run_menus(graphics, ai_classes_available):
    menu_running = True

    main_menu = True
    snake_picker = False

    while menu_running == True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return "Exit"
            if event.type == pygame.KEYDOWN:
                for index, class_dict in enumerate(ai_classes_available):
                    if event.key == settings.PYGAME_START_NUMBER_PRESS_VALUE + index:
                        class_dict['should_play'] = not class_dict['should_play']

        if main_menu == True:
            menu_action = graphics.draw_menu(ai_classes_available, events)
            if menu_action == 'Exit':
                return {"action": menu_action, "args": ""}
            elif menu_action == 'Play':
                return {"action": menu_action, "args": ""}

        elif snake_picker == True:
            pass


def run_game(playing_classes, ai_classes_available):

    graphics = GameGraphics(ai_classes_available)
    board = Board(graphics.board_size)

    frames_delay = settings.DELAY_BETWEEN_SCREEN_UPDATES

    snakes_array = []

    for snake_class in playing_classes:
        snakes_array.append(snake_class(
            board.border_cells, color=graphics.get_unique_snake_color(), name=snake_class.__name__))

    for snake in snakes_array:
        # The position of the head is determined by the rules and the board state.
        head_pos = logic.get_unique_snake_head_position(board)
        snake._body_position = [head_pos]

        snake._grow(settings.STARTING_SNAKE_LENGTH - 1)

        board.add_snake(snake)

    for _ in range(settings.NUMBER_OF_BENEFICIAL_FRUITS_ON_BOARD):
        board.add_fruit(Fruit(choice(FruitKind.beneficial_fruits),
                        logic.get_new_fruit_position(board)))

    while not board.is_game_timed_out() and len(board.snakes) > 0:
        time.sleep(frames_delay)

        should_exit = False
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                should_exit = True

            if event.type == pygame.KEYDOWN:
                if event.unicode == "+":
                    frames_delay *= 0.9
                if event.unicode == "-":
                    frames_delay *= 1.1

        if should_exit == True:
            break

        # The AI Snake Should make a decision in which direction to go.
        for snake in board.snakes:
            try:

                if snake.__class__ in [ManualSnake, ManualSnakeWASD]:
                    new_direction = snake.make_decision(
                        board.get_board_state(), events)

                else:
                    new_direction = snake.make_decision(
                        board.get_board_state())

            except Exception as e:
                print(snake._name, "was removed from the game: ", e)
                snake._lost = True
                
                if settings.DEBUG == True:
                    raise e
                    
                continue

            if new_direction in [0, 1, 2, 3, 4, None]:
                snake._change_direction(new_direction)

            else:
                print(snake._name, "was removed from the game: ",
                      "snake not returned a valid direction", f"({new_direction})")
                snake._lost = True

                if settings.DEBUG == True:
                    raise InvalidDirection(f'Snake not returned a valid direction ({new_direction})')

        for snake in board.snakes:
            snake._move_one_cell()

        logic.apply_logic(board, events)
        graphics.update_screen(board)

    winners = logic.get_first_place(board)

    if len(winners) == 1:
        print(winners[0]._name + " is the winner!!!")

    else:
        print("There is a tie between", winners, "!!!")

    time.sleep(2)


if __name__ == "__main__":
    main()