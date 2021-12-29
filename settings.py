######################################
##         Graphics settings        ##
######################################


# Board
NUMBER_OF_CELLS = 1500 # The number of cells in the board area. The actual number of cells will be close to this number.

BACKGROUND_COLOR = (255, 255, 255) # rgb

BACKGROUND_LINES_COLOR = (218, 209, 209)

BORDER_COLOR = (49, 39, 18)

BORDER_THICKNESS = 1 # Number of cells


# Score Board
SCOREBOARD_TITLE_FONT_SIZE = 50

SCOREBOARD_TEXT_FONT_SIZE = 25

SCOREBOARD_TITLE_TEXT_SEPERATION = 3 # In units of CELL_SIZE

SCOREBOARD_TITLE_SCORE_SEPERATION = 4 # In units of CELL_SIZE

SCOREBOARD_SCORE_POWERUPS_SEPERATOR = 7 # In units of CELL_SIZE

# Snakes And Fruits
SNAKES_COLORS = [(160, 196, 50) ,(106, 153, 73), (55, 40, 40), (120, 100, 19), (35, 166, 255), (225, 191, 0), (8, 32, 185), (28, 154, 57), (0, 97, 162)]
DEAD_SNAKE_IMAGE_PATH = "snakes_battle/images/dead_icon.png"



# General
DELAY_BETWEEN_SCREEN_UPDATES = 0.04 # Delay between screen update to another. Snakes move one cell every screen update. 0.07 looks good

######################################




######################################
##         Logic settings           ##
######################################


STARTING_SNAKE_LENGTH = 15

GAME_TIME_LENGTH = 10000

######################################
