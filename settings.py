
# NOT THE REAL VALUE OF CELL_SIZE! IS DEFINED AGAIN RELATIVE TO THE SCREEN (could not do that here because the screen is not initialized)
# For the real value look at the graphics file
CELL_SIZE = 20 # px

BOARD_WIDTH = 75
BOARD_HEIGHT = 55
BOARD_SIZE = (BOARD_WIDTH,BOARD_HEIGHT) # number of cells, not pixels. Size includes borders

BACKGROUND_COLOR = (255, 255, 255) # rgb

BACKGROUND_LINES_COLOR = (218, 218, 218)

BORDER_COLOR = (49, 39, 18)

BORDER_THICKNESS = 1 # Number of cells

# Delay between screen update to another. Snakes move one cell every screen update. 0.07 looks good
DELAY_BETWEEN_SCREEN_UPDATES = 0.04 # second

STARTING_SNAKE_LENGTH = 3

SNAKES_COLORS = [(106, 153, 73), (39, 39, 39), (54, 50, 33), (35, 166, 255), (147, 127, 15), (8, 32, 185)]

SCOREBOARD_TITLE_FONT_SIZE = 50

SCOREBOARD_TEXT_FONT_SIZE = 25

SCOREBOARD_TITLE_TEXT_SEPERATION = 3 # In units of CELL_SIZE

SCOREBOARD_TITLE_SCORE_SEPERATION = 4 # In units of CELL_SIZE

DEAD_SNAKE_IMAGE_PATH = "snakes_battle\\fruits\\images\\dead_icon.png"

GAME_TIME_LENGTH = 60
