from math import log
import pygame
import os
import settings
from snakes_battle.board import Board

init = True

left_border_coordinates = []

right_border_coordinates = []

upper_border_coordinates = []

bottom_border_coordinates = []

def update_border_coordinates():
    global left_border_coordinates, right_border_coordinates, upper_border_coordinates, bottom_border_coordinates

    left_border_coordinates = [
        (0,0),
        (settings.BORDER_THICKNESS*settings.CELL_SIZE,0),
        (settings.BORDER_THICKNESS*settings.CELL_SIZE, (settings.BOARD_SIZE[1] + settings.BORDER_THICKNESS * 2) * settings.CELL_SIZE),
        (0, (settings.BOARD_SIZE[1] + settings.BORDER_THICKNESS * 2) * settings.CELL_SIZE)
    ]

    right_border_coordinates = [
        ((settings.BOARD_SIZE[0] + settings.BORDER_THICKNESS) * settings.CELL_SIZE, 0),
        ((settings.BOARD_SIZE[0] + settings.BORDER_THICKNESS * 2) * settings.CELL_SIZE, 0),
        ((settings.BOARD_SIZE[0] + settings.BORDER_THICKNESS * 2) * settings.CELL_SIZE, (settings.BOARD_SIZE[1] + settings.BORDER_THICKNESS * 2) * settings.CELL_SIZE),
        ((settings.BOARD_SIZE[0] + settings.BORDER_THICKNESS) * settings.CELL_SIZE, (settings.BOARD_SIZE[1] + settings.BORDER_THICKNESS * 2) * settings.CELL_SIZE)
        ]

    upper_border_coordinates = [
        (0,0),
        ((settings.BOARD_SIZE[0] + settings.BORDER_THICKNESS * 2) * settings.CELL_SIZE, 0),
        ((settings.BOARD_SIZE[0] + settings.BORDER_THICKNESS * 2) * settings.CELL_SIZE, settings.BORDER_THICKNESS * settings.CELL_SIZE),
        (0, settings.BORDER_THICKNESS * settings.CELL_SIZE)
        ]

    bottom_border_coordinates = [
        (0, (settings.BOARD_SIZE[1] + settings.BORDER_THICKNESS) * settings.CELL_SIZE),
        ((settings.BOARD_SIZE[0] + settings.BORDER_THICKNESS * 2) * settings.CELL_SIZE, (settings.BOARD_SIZE[1] + settings.BORDER_THICKNESS) * settings.CELL_SIZE),
        ((settings.BOARD_SIZE[0] + settings.BORDER_THICKNESS * 2) * settings.CELL_SIZE, (settings.BOARD_SIZE[1] + settings.BORDER_THICKNESS * 2) * settings.CELL_SIZE),
        (0, (settings.BOARD_SIZE[1] + settings.BORDER_THICKNESS * 2) * settings.CELL_SIZE)
    ]


def _get_cell_coordinates(cell_pos):

    top_left = (cell_pos[0]*settings.CELL_SIZE,
                cell_pos[1]*settings.CELL_SIZE)
    top_right = (cell_pos[0]*settings.CELL_SIZE +
                    settings.CELL_SIZE, cell_pos[1]*settings.CELL_SIZE)
    bottom_left = (cell_pos[0]*settings.CELL_SIZE,
                    cell_pos[1]*settings.CELL_SIZE+settings.CELL_SIZE)
    bottom_right = (cell_pos[0]*settings.CELL_SIZE+settings.CELL_SIZE,
                    cell_pos[1]*settings.CELL_SIZE+settings.CELL_SIZE)

    return [top_left, bottom_left, bottom_right, top_right]

def _draw_snake(snake, surface):
    for square in snake.body_pos:
        pygame.draw.polygon(surface, snake.color, _get_cell_coordinates(square))

def _draw_fruit(fruit,surface):
    surface.blit(pygame.image.load(os.path.join(fruit.kind["image"])), _get_cell_coordinates(fruit.pos)[0])

def _draw_borders(surface):
    pygame.draw.polygon(surface, settings.BORDER_COLOR,left_border_coordinates)
    pygame.draw.polygon(surface, settings.BORDER_COLOR,right_border_coordinates)
    pygame.draw.polygon(surface, settings.BORDER_COLOR,upper_border_coordinates)
    pygame.draw.polygon(surface, settings.BORDER_COLOR,bottom_border_coordinates)

def _draw_background_lines(surface):

    for column in range(settings.BOARD_SIZE[0] + 1):
        start_pos = ((column + settings.BORDER_THICKNESS)*settings.CELL_SIZE, settings.BORDER_THICKNESS * settings.CELL_SIZE)
        end_pos = ((column + settings.BORDER_THICKNESS)*settings.CELL_SIZE, (settings.BOARD_SIZE[1] + settings.BORDER_THICKNESS)*settings.CELL_SIZE)

        pygame.draw.line(surface, settings.BACKGROUND_LINES_COLOR, start_pos, end_pos)

    for row in range(settings.BOARD_SIZE[1] + 1):
        start_pos = (settings.BORDER_THICKNESS * settings.CELL_SIZE, (row + settings.BORDER_THICKNESS)*settings.CELL_SIZE)
        end_pos = ((settings.BOARD_SIZE[0] + settings.BORDER_THICKNESS) * settings.CELL_SIZE, (row + settings.BORDER_THICKNESS)*settings.CELL_SIZE)

        pygame.draw.line(surface, settings.BACKGROUND_LINES_COLOR, start_pos, end_pos)

def create_surface():
    x_size = settings.BOARD_SIZE[0]*settings.CELL_SIZE
    y_size = settings.BOARD_SIZE[1]*settings.CELL_SIZE

    # surface = pygame.display.set_mode((x_size, y_size))
    surface = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

    return surface

def update_screen(surface, board :Board):
    global init

    # Cleaning the board
    surface.fill(settings.BACKGROUND_COLOR)

    if (init == True):
        init = False
        settings.CELL_SIZE=int(pygame.display.get_window_size()[0] / 100)
        update_border_coordinates()

    _draw_borders(surface)
    _draw_background_lines(surface)
    # Drawing snakes and fruits


    for snake in board.snakes:
        _draw_snake(snake, surface)
    
    for fruit in board.fruits:
        _draw_fruit(fruit, surface)

    # Displaying draws
    pygame.display.flip()