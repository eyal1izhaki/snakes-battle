
# All the rules of the game should be defined here.
# For example, If snake eats a fruit, we grows. If a snake hit a border a loses and so on...

import random
import math
import settings
from snakes_battle.board import Board
from snakes_battle.fruit import Fruit, FruitKind
from snakes_battle.snakes_ai.manual_control_snake import ManualSnake
from snakes_battle.snakes_ai.manual_control_snake_wasd import ManualSnakeWASD

def apply_snake_logic(board, snake):
    for fruit in board.fruits:

        # Rule: Snake eats a fruit
        if snake.body_pos[0] == fruit.pos: # if head of snake in the same position of the fruit

            if fruit.kind == FruitKind.KING:
                board.is_there_a_king = True

            snake_eats(snake, fruit)
            board.fruit_eaten(fruit)

            if fruit.kind in FruitKind.beneficial_fruits:
                new_fruit = Fruit(random.choice(FruitKind.beneficial_fruits), get_new_fruit_position(board))
                board.add_fruit(new_fruit)

            break

    # Rules - subtract king remaining effection by 1 every frame.
    if snake.king:
        snake.king_remaining_effection -=1

        if snake.king_remaining_effection == 0:
            snake.king = False
            board.is_there_a_king = False
        

    # Rule - Snake must have a length of 1 at least (can be lower if the snake was hit by a bomb and it's length was reduced too much)
    if (snake.length == 0):
        snake_lost(snake, board)
        return

    # Rule: Snake hitted a border
    if snake.body_pos[0][0] == settings.BORDER_THICKNESS-1: # Hitted left border
        snake_lost(snake,board)
        return

    if snake.body_pos[0][0] == board.board_size[0] - settings.BORDER_THICKNESS: # Hitted right border
        snake_lost(snake,board)
        return

    if snake.body_pos[0][1] == settings.BORDER_THICKNESS-1: # Hitted upper border
        snake_lost(snake,board)
        return

    if snake.body_pos[0][1] == board.board_size[1] - settings.BORDER_THICKNESS: # Hitted bottom border
        snake_lost(snake,board)
        return

    # Rule: Snake hitted itself or other snakes
    for _snake in board.snakes:

        if snake == _snake: # snake hitted itself.

            headless = _snake.body_pos[1:] # Snake body position without the head

            for i in range(len(headless)):
                if snake.body_pos[0] == headless[i]:

                    if snake.king: # King can cross itself
                        break

                    if snake.shield: # If snake is shielded then it won't shrink
                        snake.shield = False
                    else:
                        # Snake is not shielded so it will be shrinked. Snake cuts itself.
                        # snake.shrink(len(headless) - i)
                        
                        snake_lost(snake, board)
                        break

        else: # snake hitted other snakes

            for i in range(len(_snake.body_pos) - 1):

                if snake.body_pos[0] == _snake.body_pos[i]:

                    if snake.knife or snake.king:
                        snake.knife = False
                        _snake.shrink(len(_snake.body_pos) - i)
                        break

                    elif snake.shield: # Snake can hit other snakes without lose if it shielded
                            snake.shield = False
                    
                    else: # Snake not shielded so it loses.
                        snake_lost(snake,board)
                        break

def apply_logic(board,events):

    for fruit in board.fruits:
                    
        # Rule - subtract 1 lifespan. when lifespan is zero, remove the fruit from board.
        if fruit.lifespan > 0:
            fruit.lifespan -= 1

        if fruit.lifespan == 0:
            board.fruit_eaten(fruit)
            if fruit.kind == FruitKind.KING:
                board.is_there_a_king = False
                
            continue

    for snake in board.snakes:
        apply_snake_logic(board,snake)
        
        if snake.king:
            if (snake.__class__ in [ManualSnake, ManualSnakeWASD] ):
                snake.change_direction(board.get_board_state(), events)
            else:
                snake.change_direction(board.get_board_state())            
            snake.move_one_cell()
            apply_snake_logic(board, snake)

        
    # Creates randomly created fruits in their creation_probability.
    for randomly_created_fruit in FruitKind.randomly_created:
        if random.random() < randomly_created_fruit["creation_probability"]:
            if (randomly_created_fruit == FruitKind.KING and board.is_there_a_king):
                continue
            else:
                board.is_there_a_king = True

            new_fruit= Fruit(randomly_created_fruit, get_new_fruit_position(board))    
            board.add_fruit(new_fruit)



def snake_eats(snake, fruit):
    # What's happen when the snake eats a fruit.


    if snake.king: # If the snake is a king so every fruit the snake eats, the snake grows in 'FruitKind.KING["fruits_score"]' units. even bomb.
        snake.grow(FruitKind.KING["fruits_score"])
        return


    if fruit.kind in FruitKind.beneficial_fruits:
        snake.grow(fruit.kind["score"])

    elif fruit.kind in FruitKind.harmful_fruits:
        if snake.shield or snake.king:
            snake.shield = False
            return
        
        if fruit.kind == FruitKind.BOMB:
            snake.shrink(-fruit.kind["score"])
            
        elif fruit.kind == FruitKind.SKULL:
            snake.shrink(snake.length)
    
    elif fruit.kind in FruitKind.special_fruits:
        if fruit.kind == FruitKind.SHIELD:
            snake.shield = True

        elif fruit.kind == FruitKind.KNIFE:
            snake.knife = True

        elif fruit.kind == FruitKind.KING:
            snake.knife = False
            snake.shield = False
            snake.king = True
            snake.king_remaining_effection = FruitKind.KING["effection_duration"]


def snake_lost(snake,board):
    if snake.king:
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
    while (generate_position == True):
        random_head_position = list(random.choice(board.all_cells_pos))
        too_close = False
        for snake in board.snakes:
            if (math.dist(snake.body_pos[0], random_head_position) < settings.STARTING_SNAKE_LENGTH):
                too_close = True
                break
        generate_position = too_close

    return random_head_position



