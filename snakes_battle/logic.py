
# All the rules of the game should be defined here.
# For example, If snake eats a fruit, it grows. If a snake hits a border it loses and so on...

import random
import math
import copy
import settings
from snakes_battle.board import Board
from snakes_battle.fruit import Fruit, FruitKind
from snakes_battle.snakes_ai.manual_control_snake import ManualSnake
from snakes_battle.snakes_ai.manual_control_snake_wasd import ManualSnakeWASD


def apply_snake_logic(board, snake):

    if snake._lost == True:
        return

    for fruit in board.fruits:

        # Rule: Snake eats a fruit
        # if head of snake in the same position of the fruit
        if snake._body_position[0] == fruit.pos:

            if fruit.kind == FruitKind.KING:
                board.is_there_a_king = True

            snake_eats(snake, fruit)
            board.fruit_eaten(fruit)

            if fruit.kind in FruitKind.beneficial_fruits:
                new_fruit = Fruit(random.choice(
                    FruitKind.beneficial_fruits), get_new_fruit_position(board))
                board.add_fruit(new_fruit)

            break

    # Rules: subtract king remaining effection by 1 every frame.
    if snake._king:
        snake._king_remaining_time -= 1

        if snake._king_remaining_time == 0:
            snake._king = False # Not a king anymore
            board.is_there_a_king = False

    # Rule: Snake must have a length of 1 at least (can be lower if the snake ate a bomb and it's length was reduced too much)
    if snake._length == 0:
        snake._lost = True
        return 

    # Rule: Snake hits a border

    # Hits left border
    if snake._body_position[0][0] == settings.BORDER_THICKNESS-1:  
        snake._lost = True
        return

    # Hits right border
    if snake._body_position[0][0] == board.board_size[0] - settings.BORDER_THICKNESS:
        snake._lost = True
        return

    # Hits upper border
    if snake._body_position[0][1] == settings.BORDER_THICKNESS-1:  
        snake._lost = True
        return

    # Hits bottom border
    if snake._body_position[0][1] == board.board_size[1] - settings.BORDER_THICKNESS:
        snake._lost = True
        return

    # Rule: Snake hits itself or other snakes
    for _snake in board.snakes:

        if snake == _snake:  # snake hits itself.

            # Snake body position without the head
            headless = _snake._body_position[1:]

            for i in range(len(headless)):
                if snake._body_position[0] == headless[i]: # Head is in the same position of one of the nodes in the body

                    if snake._king:  # King can cross itself
                        break

                    if snake._shield:  # If snake is shielded then it won't shrink
                        snake._shield = False
                        break

                    else:
                        snake._lost = True
                        break

        else:  # snake hits other snakes

            for i in range(len(_snake._body_position) - 1):

                if snake._body_position[0] == _snake._body_position[i]:

                    # When a snake hits other snake head to head.
                    if snake._body_position[0] == _snake._body_position[0]:

                        if snake._king == True:
                            _snake._lost = True
                            return
                        
                        elif _snake._king == True:
                            snake._lost = True
                            return
                        
                        else: # Non of them is a king
                            snake._lost = True
                            _snake._lost = True
                            return

                    else:  # Snake hits other snake but not in its head.

                        if snake._knife or snake._king:
                            snake._knife = False

                            if _snake._shield:
                                _snake._shield = False
                                break

                            _snake._shrink(len(_snake._body_position) - i)
                            break

                        elif snake._shield:  # Snake can hit other snakes without lose if it shielded
                            snake._shield = False
                            break

                        else:  # Snake not shielded so it loses.
                            snake._lost = True
                            return


def apply_logic(board, events):

    for fruit in board.fruits:

        # Rule - subtract 1 lifespan. when lifespan is zero, remove the fruit from board.
        if fruit.lifespan > 0:
            fruit.lifespan -= 1

        if fruit.lifespan == 0:
            board.fruit_eaten(fruit)
            if fruit.kind == FruitKind.KING:
                board.is_there_a_king = False

    for snake in copy.copy(board.snakes):
        apply_snake_logic(board, snake)

        if snake._king:
            try:
                if snake.__class__ in [ManualSnake, ManualSnakeWASD]:
                    new_direction = snake.make_decision(
                        board.get_board_state(), events)
                else:
                    new_direction = snake.make_decision(
                        board.get_board_state())

            except Exception as e:
                print(e)

            if new_direction in [0, 1, 2, 3, 4, None]:
                snake._change_direction(new_direction)

            else:
                print(snake._name, "was removed from the game: ",
                      "snake not returned a valid direction", f"({new_direction})")
                snake._lost = True

            if snake._lost != True:
                snake._move_one_cell()

            apply_snake_logic(board, snake)

    for snake in copy.copy(board.snakes):
        if snake._lost == True:
            remove_snake(snake, board) # Removing lost snakes
        else:
            snake._lived_x_frames += 1

    # Creates randomly created fruits in their creation_probability.
    for randomly_created_fruit in FruitKind.randomly_created:
        if random.random() < randomly_created_fruit["creation_probability"]:

            if randomly_created_fruit == FruitKind.KING:
                if board.is_there_a_king:
                    continue

                board.is_there_a_king = True

            new_fruit = Fruit(randomly_created_fruit,
                              get_new_fruit_position(board))
            board.add_fruit(new_fruit)


def snake_eats(snake, fruit):
    # What's happen when the snake eats a fruit.

    # If the snake is a king so every fruit the snake eats, the snake grows in 'FruitKind.KING["fruits_score"]' units. even bomb.
    if snake._king:
        snake._grow(FruitKind.KING["fruits_score"])
        return

    if fruit.kind in FruitKind.beneficial_fruits: # Snake ate a beneficial fruit
        snake._grow(fruit.kind["score"])

    elif fruit.kind in FruitKind.harmful_fruits: # Snake ate an harmful fruit
        if snake._shield or snake._king:
            snake._shield = False 
            return

        if fruit.kind == FruitKind.BOMB:
            snake._shrink(-fruit.kind["score"])

        elif fruit.kind == FruitKind.SKULL:
            snake._shrink(snake._length)

    elif fruit.kind in FruitKind.special_fruits: # Snake ate a special fruit
        if fruit.kind == FruitKind.SHIELD:
            snake._shield = True

        elif fruit.kind == FruitKind.KNIFE:
            snake._knife = True

        elif fruit.kind == FruitKind.KING:
            snake._knife = False
            snake._shield = False
            snake._king = True
            snake._king_remaining_time = FruitKind.KING["effection_duration"]

def remove_snake(snake, board):
    if snake._king:
        board.is_there_a_king = False

    board.lost_snakes.append(snake)
    board.snakes.remove(snake)


def get_new_fruit_position(board):
    # Returns an empty cell so a fruit can be placed there

    board.update_empty_cells()
    return list(random.choice(board.empty_cells))


def get_unique_snake_head_position(board: Board):

    # Generating random and unique position to the head of the snake, that will not collide with other snake's tail
    generate_position = True
    while generate_position == True:
        random_head_position = list(random.choice(board.all_cells_pos))
        too_close = False
        for snake in board.snakes:
            if math.dist(snake._body_position[0], random_head_position) < settings.STARTING_SNAKE_LENGTH:
                too_close = True
                break
        generate_position = too_close

    return random_head_position


def get_first_place(board):
    
    
    snakes = board.snakes + board.lost_snakes

    highest = snakes[0]
    tie_with_highest = []

    for snake in snakes:

        if snake is highest:
            continue

        if snake._length > highest._length:
            highest = snake
            tie_with_highest = []
        
        elif snake._length == highest._length:
            if snake._lived_x_frames > highest._lived_x_frames:
                highest = snake
                tie_with_highest = []
            
            elif snake._lived_x_frames == highest._lived_x_frames:
                tie_with_highest.append(snake)
        
    return [highest] + tie_with_highest