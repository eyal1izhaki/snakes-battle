
# All the rules of the game should be defined here.
# For example, If snake eats a fruit, we grows. If a snake hit a border a loses and so on...

import random
import math
import settings
from snakes_battle.board import Board
from snakes_battle.fruit import Fruit, FruitKind

def apply_logic(board):

    for snake in board.snakes:

        # Rule: Snake eats a fruit
        for fruit in board.fruits:
            if snake.body_pos[0] == fruit.pos: # if head of snake in the same position of the fruit
                snake.eat(fruit)
                board.fruit_eaten(fruit)

                if fruit.kind in FruitKind.beneficial_fruits:
                    new_fruit = Fruit(random.choice(FruitKind.beneficial_fruits), get_new_fruit_position(board))
                    board.add_fruit(new_fruit)

                break


        # Rule - Snake must have a length of 1 at least (can be lower if the snake was hit by a bomb and it's length was reduced too much)
        if (snake.length == 0):
            snake_lost(snake, board)
            continue

        # Rule: Snake hitted a border
        if snake.body_pos[0][0] == settings.BORDER_THICKNESS-1: # Hitted left border
            snake_lost(snake,board)
            continue

        if snake.body_pos[0][0] == board.board_size[0] - settings.BORDER_THICKNESS: # Hitted right border
            snake_lost(snake,board)
            continue

        if snake.body_pos[0][1] == settings.BORDER_THICKNESS-1: # Hitted upper border
            snake_lost(snake,board)
            continue

        if snake.body_pos[0][1] == board.board_size[1] - settings.BORDER_THICKNESS: # Hitted bottom border
            snake_lost(snake,board)
            continue

        # Rule: Snake hitted itself or other snakes
        for _snake in board.snakes:

            if snake == _snake: # snake hitted itself.

                headless = _snake.body_pos[1:] # Snake body position without the head

                for i in range(len(headless)):
                    if snake.body_pos[0] == headless[i]:
                        if snake.super_power["SHIELD"]: # If snake is shielded then it won't shrink
                            snake.super_power["SHIELD"] = False
                        else:
                            snake.shrink(len(headless) - i) # Snake is not shielded so it will be shrinked. Snake cuts itself.
                            break

            elif snake.body_pos[0] in _snake.body_pos: # snake hitted other snakes

                if snake.super_power["SHIELD"]: # Snake can hit other snakes without lose if it shielded
                        snake.super_power["SHIELD"] = False

                else: # Snake not shielded so it loses.
                    snake_lost(snake,board)
                    break
        
    # Rule - generate a bomb randomly.
    if (random.random() < FruitKind.BOMB["creation_probability"]):
        new_bomb = Fruit(FruitKind.BOMB, get_new_fruit_position(board))
        board.add_fruit(new_bomb)
    
    # Rule - generate a special fruit randomly.
    if random.random() < FruitKind.SHIELD["creation_probability"]:
        new_special_fruit = Fruit(random.choice(FruitKind.special_fruits), get_new_fruit_position(board))
        board.add_fruit(new_special_fruit)

    # Rule - subtract lifespan in 1. when lifespan is zero, remove the fruit from board.
    if fruit.lifespan > 0:
        fruit.lifespan -= 1
    
    if fruit.lifespan == 0:
        board.fruit_eaten(fruit)



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



