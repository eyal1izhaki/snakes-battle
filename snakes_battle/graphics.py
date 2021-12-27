from random import choice
import pygame
import os
import settings
from snakes_battle.board import Board
import math

from snakes_battle.fruit import Fruit, FruitKind
from snakes_battle.snake import Direction




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

        # Loads all snakes heads
        for color in settings.SNAKES_COLORS:
            self.images[f"HEAD_{str(color)}"] = self._load_and_scale_image(f"snakes_battle\\images\\snake_heads\snake_head{str(color)}.png", fit_width=True, fit_height=False)

        self.title_font = pygame.font.SysFont('Arial Black', settings.SCOREBOARD_TITLE_FONT_SIZE)
        self.subtitle_font = pygame.font.SysFont('Arial Black', 10)
        self.score_font = pygame.font.SysFont('Arial Black', settings.SCOREBOARD_TEXT_FONT_SIZE)

    
        self.SCOREBOARD_STARTING_POSITION = ((self.board_size[0] + settings.SCOREBOARD_TITLE_TEXT_SEPERATION) * self.cell_size,
                                        settings.SCOREBOARD_TITLE_TEXT_SEPERATION * self.cell_size)
        
        self.dead_snake_image = pygame.image.load(os.path.join(settings.DEAD_SNAKE_IMAGE_PATH))
        self.dead_snake_image = pygame.transform.scale(self.dead_snake_image, (40, 40))

        self.snakes_colors_in_use = []

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

    def _get_cell_coordinates(self, cell_pos):

        top_left = (cell_pos[0]*self.cell_size-1,
                    cell_pos[1]*self.cell_size-1)
        top_right = (cell_pos[0]*self.cell_size +
                        self.cell_size-1, cell_pos[1]*self.cell_size-1)
        bottom_left = (cell_pos[0]*self.cell_size-1,
                        cell_pos[1]*self.cell_size+self.cell_size-1)
        bottom_right = (cell_pos[0]*self.cell_size+self.cell_size-1,
                        cell_pos[1]*self.cell_size+self.cell_size-1)

        return [top_left, bottom_left, bottom_right, top_right]

    def _draw_snake(self, snake, margin=4):

        snake_head_offset_to_body = 2
        head_image = self.images[f"HEAD_{str(snake.color)}"]


        # Creating the turn block surface. We will rotate it as needed.
        snake_turn_block = pygame.Surface((self.cell_size + 1, self.cell_size + 1))
        snake_turn_block.set_colorkey((0,0,0))
        x1 = (margin, margin)
        x2 = (self.cell_size, margin)
        x3 = (self.cell_size, self.cell_size - margin)
        x4 = (self.cell_size - margin, self.cell_size - margin)
        x5 = (self.cell_size - margin ,self.cell_size)
        x6 = (margin, self.cell_size)

        # The turn block is in a position of: form up direction turn right.
        pygame.draw.polygon(snake_turn_block, snake.color, [x1,x2,x3,x4,x5,x6])

        # Drawing the head and the rest of the snakes body.
        head=True
        for i in range(len(snake.body_pos)):

            if head:    
                head = False
    
                if snake.direction == Direction.UP:
                    head_image = pygame.transform.rotate(head_image, 180)
                    head_x_y = self._get_cell_coordinates(snake.body_pos[i])[1]
                    head_x_y = (head_x_y[0], head_x_y[1] - head_image.get_height() + snake_head_offset_to_body)

                elif snake.direction == Direction.LEFT:
                    head_image = pygame.transform.rotate(head_image, 270)
                    head_x_y = self._get_cell_coordinates(snake.body_pos[i])[3]
                    head_x_y = (head_x_y[0] - head_image.get_width() + snake_head_offset_to_body, head_x_y[1])

                elif snake.direction == Direction.RIGHT:
                    head_image = pygame.transform.rotate(head_image, 90)
                    head_x_y = self._get_cell_coordinates(snake.body_pos[i])[0]
                    head_x_y = (head_x_y[0] - snake_head_offset_to_body, head_x_y[1])
                
                else:
                    head_x_y = self._get_cell_coordinates(snake.body_pos[i])[0]
                    head_x_y = (head_x_y[0], head_x_y[1] - snake_head_offset_to_body)

                self.surface.blit(head_image, head_x_y)


            # Drawing the rest of the body.
            else:

                coordinates = self._get_cell_coordinates(snake.body_pos[i])

                # Checking if this block in the snake body is a turn block.
                if i < len(snake.body_pos) - 1 and snake.body_pos[i-1][1] != snake.body_pos[i+1][1] and snake.body_pos[i-1][0] != snake.body_pos[i+1][0]:

                    turn_block_top_left = coordinates[0]
                    # Up and left or right.
                    if snake.body_pos[i+1][1] > snake.body_pos[i][1]:
                        # Left
                        if snake.body_pos[i][0] > snake.body_pos[i-1][0]:
                            self.surface.blit(pygame.transform.rotate(snake_turn_block, -90), turn_block_top_left)
                        
                        # Right
                        else:
                            self.surface.blit(snake_turn_block, turn_block_top_left)
                    
                    # Down and left ot right.
                    elif snake.body_pos[i+1][1] < snake.body_pos[i][1]:
                        # Left
                        if snake.body_pos[i][0] > snake.body_pos[i-1][0]:
                            self.surface.blit(pygame.transform.rotate(snake_turn_block, 180), turn_block_top_left)
                        # Right
                        else:
                            self.surface.blit(pygame.transform.rotate(snake_turn_block, 90), turn_block_top_left)
                        
                    # Right and up or down.
                    elif snake.body_pos[i][0] < snake.body_pos[i+1][0]:
                        # Up
                        if snake.body_pos[i][1] > snake.body_pos[i-1][1]:
                            self.surface.blit(pygame.transform.rotate(snake_turn_block, 90), turn_block_top_left)
                        # Down
                        else:
                            self.surface.blit(snake_turn_block, turn_block_top_left)

                    # Left and up or down
                    elif snake.body_pos[i][0] > snake.body_pos[i+1][0]:
                        # Up
                        if snake.body_pos[i][1] > snake.body_pos[i-1][1]:
                            self.surface.blit(pygame.transform.rotate(snake_turn_block, 180), turn_block_top_left)
                        # Down
                        else:
                            self.surface.blit(pygame.transform.rotate(snake_turn_block, -90), turn_block_top_left)

                # Square is horizontal (The block is in right or left direction).
                elif  snake.body_pos[i][1] == snake.body_pos[i-1][1]:

                    top_left, bottom_left, bottom_right, top_right = coordinates
                    top_left = (top_left[0], top_left[1] + margin)
                    top_right = (top_right[0], top_right[1] + margin)
                    bottom_left = (bottom_left[0],bottom_left[1] - margin)
                    bottom_right = (bottom_right[0], bottom_right[1] - margin)

                                        
                    coordinates = [top_left, bottom_left, bottom_right, top_right]

                    pygame.draw.polygon(self.surface, snake.color, coordinates)

                # Square is vertical (The block is in up or down direction).
                elif snake.body_pos[i][0] == snake.body_pos[i-1][0]:
                    top_left, bottom_left, bottom_right, top_right =  coordinates
                    top_left = (top_left[0] + margin, top_left[1])
                    top_right = (top_right[0] - margin, top_right[1])
                    bottom_left = (bottom_left[0] + margin, bottom_left[1])
                    bottom_right = (bottom_right[0] - margin, bottom_right[1])

                    coordinates = [top_left, bottom_left, bottom_right, top_right]

                    pygame.draw.polygon(self.surface, snake.color, coordinates)

                

    def _draw_fruit(self, fruit, draw_background=True):
        
        if draw_background:
            top_left = self._get_cell_coordinates((fruit.pos[0]-1,fruit.pos[1]-1))[0]

            fruit_background = pygame.Surface((self.cell_size*3,self.cell_size*3))
            fruit_background.set_alpha(40)
            fruit_background.fill(fruit.kind["color"])    

            self.surface.blit(fruit_background, top_left)

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
        time_left_surface = self.score_font.render(f"Time left: {board.game_time_left()}", False, (0, 0, 0))
        self.surface.blit(score_title_surface, self.SCOREBOARD_STARTING_POSITION)
        self.surface.blit(score_subtitle_surface, (self.SCOREBOARD_STARTING_POSITION[0], self.SCOREBOARD_STARTING_POSITION[1] + 60))
        self.surface.blit(time_left_surface, (self.SCOREBOARD_STARTING_POSITION[0], 0))

        all_snakes = board.snakes + board.lost_snakes
        for i, snake in enumerate(all_snakes):
            score_position = (self.SCOREBOARD_STARTING_POSITION[0], self.SCOREBOARD_STARTING_POSITION[1] + (i + 2) * self.cell_size * settings.SCOREBOARD_TITLE_SCORE_SEPERATION)
            score_text_surface = self.score_font.render(f"{snake.name}: {snake.length}", False, (0, 0, 0))
            self.surface.blit(score_text_surface, score_position)
            if (snake in board.lost_snakes):
                self.surface.blit(self.dead_snake_image, score_position)

    def _load_and_scale_image(self, image_path, fit_width=True, fit_height=True):
        # Loads the image and scales it to fit the cell width, height or both will keeping the image proportion.

        image = pygame.image.load(image_path)

        ratio_width_height = image.get_width()/image.get_height()

        if fit_width and fit_height:
            if ratio_width_height > 1:
                scale_width = self.cell_size
                scale_height= scale_width/ratio_width_height
            else:
                scale_height = self.cell_size
                scale_width = scale_height*ratio_width_height

        elif fit_width and not fit_height:
            scale_width = self.cell_size
            scale_height = scale_width/ratio_width_height

        elif fit_height and not fit_width:
            scale_height = self.cell_size
            scale_width = scale_height*ratio_width_height
        
        else:
            return image
        
        return pygame.transform.smoothscale(image, (scale_width, scale_height))

    def get_unique_snake_color(self):
        not_a_unique_color = True
        while not_a_unique_color:
            color = choice(settings.SNAKES_COLORS)
            not_a_unique_color = color in self.snakes_colors_in_use
            self.snakes_colors_in_use.append(color)
        
        return color

    def update_screen(self, board :Board):

        # Cleaning the board
        self.surface.fill(settings.BACKGROUND_COLOR)

        
        self._draw_background_lines()

        # Drawing snakes and fruits
        
        for fruit in board.fruits:
            self._draw_fruit(fruit, True)
                
        for snake in board.snakes:
            self._draw_snake(snake)


        self._draw_borders()


     
        # Draw the scoreboard
        self._draw_scoreboard(board)

        # Displaying draws
        pygame.display.flip()