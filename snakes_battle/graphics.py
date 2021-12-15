import pygame
import os
import settings
from snakes_battle.board import Board

init = True

title_font, subtitle_font, score_font, SCOREBOARD_STARTING_POSITION = None, None, None, (0, 0)

left_border_coordinates = []

right_border_coordinates = []

upper_border_coordinates = []

bottom_border_coordinates = []

dead_snake_image = None

def intiailize_game_constants():
    global left_border_coordinates, right_border_coordinates, upper_border_coordinates, bottom_border_coordinates, \
            dead_snake_image, title_font, subtitle_font, score_font, SCOREBOARD_STARTING_POSITION

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

    title_font = pygame.font.SysFont('Arial Black', settings.SCOREBOARD_TITLE_FONT_SIZE)
    subtitle_font = pygame.font.SysFont('Arial Black', 10)
    score_font = pygame.font.SysFont('Arial Black', settings.SCOREBOARD_TEXT_FONT_SIZE)

    SCOREBOARD_STARTING_POSITION = ((settings.BOARD_SIZE[0] + settings.BORDER_THICKNESS * (2 + settings.SCOREBOARD_TITLE_TEXT_SEPERATION)) * settings.CELL_SIZE,
                                     settings.SCOREBOARD_TITLE_TEXT_SEPERATION * settings.CELL_SIZE)
    
    dead_snake_image = pygame.image.load(os.path.join(settings.DEAD_SNAKE_IMAGE_PATH))
    dead_snake_image = pygame.transform.scale(dead_snake_image, (40, 40))


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
        end_pos = ((column + settings.BORDER_THICKNESS)*settings.CELL_SIZE, (settings.BOARD_SIZE[1] + settings.BORDER_THICKNESS) * settings.CELL_SIZE)

        pygame.draw.line(surface, settings.BACKGROUND_LINES_COLOR, start_pos, end_pos)

    for row in range(settings.BOARD_SIZE[1] + 1):
        start_pos = (settings.BORDER_THICKNESS * settings.CELL_SIZE, (row + settings.BORDER_THICKNESS)*settings.CELL_SIZE)
        end_pos = ((settings.BOARD_SIZE[0] + settings.BORDER_THICKNESS) * settings.CELL_SIZE, (row + settings.BORDER_THICKNESS) * settings.CELL_SIZE)

        pygame.draw.line(surface, settings.BACKGROUND_LINES_COLOR, start_pos, end_pos)

def create_surface():
    surface = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    return surface

def _draw_scoreboard(board, surface):
    score_title_surface = title_font.render("Scoreboard:", False, (0, 0, 0))
    score_subtitle_surface = subtitle_font.render("aka the best game made by the best team alpha's scoreboard:", False, (0, 0, 0))
    surface.blit(score_title_surface, SCOREBOARD_STARTING_POSITION)
    surface.blit(score_subtitle_surface, (SCOREBOARD_STARTING_POSITION[0], SCOREBOARD_STARTING_POSITION[1] + 60))

    all_snakes = board.snakes + board.lost_snakes
    for i in range(len(all_snakes)):
        snake = all_snakes[i]
        score_position = (SCOREBOARD_STARTING_POSITION[0], SCOREBOARD_STARTING_POSITION[1] + (i + 2) * settings.CELL_SIZE * settings.SCOREBOARD_TITLE_SCORE_SEPERATION)
        score_text_surface = score_font.render(f"{snake.name}: {snake.length}", False, (0, 0, 0))
        surface.blit(score_text_surface, score_position)
        if (snake in board.lost_snakes):
            surface.blit(dead_snake_image, score_position)

def update_screen(surface, board :Board):
    global init

    # Cleaning the board
    surface.fill(settings.BACKGROUND_COLOR)

    if (init == True):
        init = False
        settings.CELL_SIZE = int(pygame.display.get_window_size()[0] / 100)
        intiailize_game_constants()

    _draw_borders(surface)
    _draw_background_lines(surface)
    # Drawing snakes and fruits

    for snake in board.snakes:
        _draw_snake(snake, surface)
    
    for fruit in board.fruits:
        _draw_fruit(fruit, surface)
    
    # Draw the scoreboard
    _draw_scoreboard(board, surface)

    # Displaying draws
    pygame.display.flip()