from random import choice
import pygame
import os
import settings
from snakes_battle.board import Board
import math

from snakes_battle.fruit import Fruit, FruitKind




class GameGraphics:
    def __init__(self) -> None:

        pygame.init()
        self.surface = self._create_surface()

        cell_size, board_height, board_width = self._get_cell_and_board_size()
        
        self.cell_size = cell_size

        self.board_size = (board_width ,board_height)

        self.borders = {
            "left": [
            (0,0),
            (settings.BORDER_THICKNESS*self.cell_size - 1, 0),
            (settings.BORDER_THICKNESS*self.cell_size - 1, self.board_size[1] * self.cell_size - 1),
            (0, self.board_size[1] * self.cell_size - 1)
            ],

            "right": [
            ((self.board_size[0] - settings.BORDER_THICKNESS) * self.cell_size - 1, 0),
            (self.board_size[0] * self.cell_size - 1, 0),
            (self.board_size[0] * self.cell_size - 1, self.board_size[1] * self.cell_size - 1),
            ((self.board_size[0] - settings.BORDER_THICKNESS) * self.cell_size - 1, self.board_size[1] * self.cell_size - 1)
            ],

            "top": [
            (0,0),
            (self.board_size[0] * self.cell_size - 1, 0),
            (self.board_size[0] * self.cell_size - 1, settings.BORDER_THICKNESS * self.cell_size - 1),
            (0, settings.BORDER_THICKNESS * self.cell_size - 1 )
            ],

            "bottom": [
            (0, (self.board_size[1] - settings.BORDER_THICKNESS) * self.cell_size - 1),
            (self.board_size[0] * self.cell_size - 1 , (self.board_size[1] - settings.BORDER_THICKNESS) * self.cell_size - 1),
            (self.board_size[0] * self.cell_size - 1, self.board_size[1] * self.cell_size - 1),
            (0, self.board_size[1] * self.cell_size - 1)
            ]
        }

        self.images = {}

        for kind in FruitKind.fruits:
            name = kind["name"]
            image_path = kind["image"]
            image = self._load_and_scale_image(image_path)
            self.images[name] = image


        self.title_font = pygame.font.SysFont('Arial Black', settings.SCOREBOARD_TITLE_FONT_SIZE)
        self.subtitle_font = pygame.font.SysFont('Arial Black', 10)
        self.score_font = pygame.font.SysFont('Arial Black', settings.SCOREBOARD_TEXT_FONT_SIZE)

    
        self.SCOREBOARD_STARTING_POSITION = ((self.board_size[0] + settings.SCOREBOARD_TITLE_TEXT_SEPERATION) * self.cell_size,
                                        settings.SCOREBOARD_TITLE_TEXT_SEPERATION * self.cell_size)
        
        self.dead_snake_image = pygame.image.load(os.path.join(settings.DEAD_SNAKE_IMAGE_PATH))
        self.dead_snake_image = pygame.transform.scale(self.dead_snake_image, (40, 40))

        self.token_snakes_colors = []

    def _get_cell_and_board_size(self):
        screen_size = self.surface.get_size()
        ratio = screen_size[0]/screen_size[1]*0.7
        num_cells = settings.NUMBER_OF_CELLS

        board_height_pixels = screen_size[1]

        board_height = int(math.sqrt(num_cells/ratio))

        cell_size = int(board_height_pixels/board_height)

        board_height = int(board_height_pixels/cell_size)

        board_width = int(board_height*ratio)

        return cell_size, board_height, board_width

    def _get_cell_coordinates(self, cell_pos, margin=0):

        top_left = (cell_pos[0]*self.cell_size,
                    cell_pos[1]*self.cell_size)
        top_right = (cell_pos[0]*self.cell_size +
                        self.cell_size, cell_pos[1]*self.cell_size)
        bottom_left = (cell_pos[0]*self.cell_size,
                        cell_pos[1]*self.cell_size+self.cell_size)
        bottom_right = (cell_pos[0]*self.cell_size+self.cell_size,
                        cell_pos[1]*self.cell_size+self.cell_size)

        return [top_left, bottom_left, bottom_right, top_right]

    def _draw_snake(self, snake):
        for square in snake.body_pos:
            pygame.draw.polygon(self.surface, snake.color, self._get_cell_coordinates(square))

    def _draw_fruit(self, fruit):
        self.surface.blit(self.images[fruit.kind["name"]], self._get_cell_coordinates(fruit.pos)[0])

    def _draw_borders(self):
        pygame.draw.polygon(self.surface, settings.BORDER_COLOR,self.borders["left"])
        pygame.draw.polygon(self.surface, settings.BORDER_COLOR,self.borders["right"])
        pygame.draw.polygon(self.surface, settings.BORDER_COLOR,self.borders["top"])
        pygame.draw.polygon(self.surface, settings.BORDER_COLOR,self.borders["bottom"])

    def _draw_background_lines(self):

        for column in range(self.board_size[0] - settings.BORDER_THICKNESS * 2 + 1):
            start_pos = ((column + settings.BORDER_THICKNESS)*self.cell_size-1, settings.BORDER_THICKNESS * self.cell_size-1)
            end_pos = ((column + settings.BORDER_THICKNESS)*self.cell_size-1, (self.board_size[1] - settings.BORDER_THICKNESS) * self.cell_size-1)

            pygame.draw.line(self.surface, settings.BACKGROUND_LINES_COLOR, start_pos, end_pos)

        for row in range(self.board_size[1] - settings.BORDER_THICKNESS * 2 + 1):
            start_pos = (settings.BORDER_THICKNESS * self.cell_size - 1, (row + settings.BORDER_THICKNESS)*self.cell_size-1)
            end_pos = ((self.board_size[0] - settings.BORDER_THICKNESS)* self.cell_size-1, (row + settings.BORDER_THICKNESS) * self.cell_size-1)

            pygame.draw.line(self.surface, settings.BACKGROUND_LINES_COLOR, start_pos, end_pos)

    def _create_surface(self):
        surface = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        return surface

    def _draw_scoreboard(self, board):
        score_title_surface = self.title_font.render("Scoreboard:", False, (0, 0, 0))
        score_subtitle_surface = self.subtitle_font.render("aka the best game made by the best team alpha's scoreboard:", False, (0, 0, 0))
        self.surface.blit(score_title_surface, self.SCOREBOARD_STARTING_POSITION)
        self.surface.blit(score_subtitle_surface, (self.SCOREBOARD_STARTING_POSITION[0], self.SCOREBOARD_STARTING_POSITION[1] + 60))

        all_snakes = board.snakes + board.lost_snakes
        for i, snake in enumerate(all_snakes):
            score_position = (self.SCOREBOARD_STARTING_POSITION[0], self.SCOREBOARD_STARTING_POSITION[1] + (i + 2) * self.cell_size * settings.SCOREBOARD_TITLE_SCORE_SEPERATION)
            score_text_surface = self.score_font.render(f"{snake.name}: {snake.length}", False, (0, 0, 0))
            self.surface.blit(score_text_surface, score_position)
            if (snake in board.lost_snakes):
                self.surface.blit(self.dead_snake_image, score_position)

    def _load_and_scale_image(self, image_path):
        image = pygame.image.load(image_path)

        ratio_width_height = image.get_width()/image.get_height()

        if ratio_width_height > 1:
            scale_width = self.cell_size
            scale_height= scale_width/ratio_width_height
        else:
            scale_height = self.cell_size
            scale_width = scale_height*ratio_width_height

        return pygame.transform.smoothscale(image, (scale_width, scale_height))

    def get_unique_snake_color(self):
        not_a_unique_color = True
        while not_a_unique_color:
            color = choice(settings.SNAKES_COLORS)
            not_a_unique_color = color in self.token_snakes_colors
            self.token_snakes_colors.append(color)
        
        return color

    def update_screen(self, board :Board):

        # Cleaning the board
        self.surface.fill(settings.BACKGROUND_COLOR)

        self._draw_borders()
        self._draw_background_lines()
        # Drawing snakes and fruits

        for snake in board.snakes:
            self._draw_snake(snake)
        
        for fruit in board.fruits:
            self._draw_fruit(fruit)
        
        # Draw the scoreboard
        self._draw_scoreboard(board)

        # Displaying draws
        pygame.display.flip()