import pygame
from snakes_battle.snake import Snake, Direction

class ManualSnakeWASD(Snake):
    def __init__(self, borders_cells, color, name) -> None:
        super().__init__(color, name)

        self.version = 1.0
        self.border_cells = borders_cells

    def make_decision(self, board_state, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    return Direction.LEFT
                elif event.key == pygame.K_d:
                    return Direction.RIGHT
                elif event.key == pygame.K_w:
                    return Direction.UP
                elif event.key == pygame.K_s:
                    return Direction.DOWN
        
        return Direction.CONTINUE
