######################################
##         Graphics settings        ##
######################################


# Board
NUMBER_OF_CELLS = 7000 # The number of cells in the board area. The actual number of cells will be close to this number.

BACKGROUND_COLOR = (255, 255, 255) # rgb

BACKGROUND_LINES_COLOR = (218, 218, 218)

BORDER_COLOR = (49, 39, 18)

BORDER_THICKNESS = 2 # Number of cells


# Score Board
SCOREBOARD_TITLE_FONT_SIZE = 50

SCOREBOARD_TEXT_FONT_SIZE = 25

SCOREBOARD_TITLE_TEXT_SEPERATION = 3 # In units of CELL_SIZE

SCOREBOARD_TITLE_SCORE_SEPERATION = 4 # In units of CELL_SIZE


# Snakes And Fruits
SNAKES_COLORS = [(106, 153, 73), (39, 39, 39), (54, 50, 33), (35, 166, 255), (147, 127, 15), (8, 32, 185), (28, 154, 57), (0, 122, 204)]
DEAD_SNAKE_IMAGE_PATH = "snakes_battle\\images\\fruits\\dead_icon.png"


# General
DELAY_BETWEEN_SCREEN_UPDATES = 0.04 # Delay between screen update to another. Snakes move one cell every screen update. 0.07 looks good

######################################




######################################
##         Logic settings           ##
######################################


STARTING_SNAKE_LENGTH = 3

GAME_TIME_LENGTH = 60

BOMB_CREATION_PROBABILITY = 1 / 100 # Will create a bomb roughly every 20 frames.

BOMB_LIFESPAN = 100 # How many frames will the bomb be on the board

######################################
