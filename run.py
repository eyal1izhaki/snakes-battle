import sys
import time
import pygame

from snakes_battle.graphics import Board
import settings


def main():

    board = Board()


    ###################################
    ## ## ##  ~  Main loop  ~  ## ## ##
    ###################################

    while True:
        time.sleep(settings.DELAY_BETWEEN_SCREEN_UPDATES)

        # "Listening" for events
        for event in pygame.event.get():

            # Quit game event has "raised"
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        board.update_screen()

if __name__ == "__main__":
    main()