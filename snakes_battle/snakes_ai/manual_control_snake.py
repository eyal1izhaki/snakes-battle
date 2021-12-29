import pygame
from snakes_battle.snake import Snake, Direction

class ManualSnake(Snake):
    def __init__(self, borders_cells, color, name) -> None:
        super().__init__(color, name)

        # All the cells that are fill with borders. This variable will store a list of (x, y) pairs
        self.border_cells = borders_cells
    
    def change_direction(self, board_state, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    super().change_direction(Direction.LEFT)
                elif event.key == pygame.K_RIGHT:
                    super().change_direction(Direction.RIGHT)
                elif event.key == pygame.K_UP:
                    super().change_direction(Direction.UP)
                elif event.key == pygame.K_DOWN:
                    super().change_direction(Direction.DOWN)
