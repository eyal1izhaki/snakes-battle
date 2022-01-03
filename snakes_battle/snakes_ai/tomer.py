from snakes_battle.fruit import FruitKind
from snakes_battle.snake import Snake, Direction


class Tomer(Snake):
    def __init__(self, borders_cells, color, name) -> None:
        super().__init__(color, name)
        self.init(borders_cells)

    ##############################
    # You can edit only the code below. You can't change methods names.
    ##############################

    def init(self, borders_cells):
        # Your bot initializations will be here.
        self.allowed__version = 1.0

        # All the cells that are fill with borders. This variable will store a list of (x, y) pairs
        self.allowed__border_cells = borders_cells

    def make_decision(self, board_state):
        # You can only call methods that starts with the word 'allowed__'. You can't change attrbiutes directly.

        # super().allowed__get_direction() # This function takes no arguments and returns the direction of the snake.
        # super().allowed__body_position() # This function takes no arguments and returns a list with all cells (x,y) that are filled with your snake.
        # super().allowed__is_king() # returns True if your snake is king else returns False
        # super().allowed__is_knife() # returns True if your snake has a knife else returns False.
        # super().allowed__is_shield() # returns True if your snake is shielded else returns False.
        fruits = board_state["fruits"]
        snakes = board_state["snakes"]
        pos = super().allowed__body_position()

        x = pos[0][0]
        y = pos[0][1]

        if super().allowed__is_king() or super().allowed__is_knife():
            return self.kill(x, y, self.get_enemy_neck_pos(snakes, fruits), snakes, fruits)

        return self.go_get_it(x, y, self.find_best_fruit(fruits), snakes, fruits)

    def avoid_that(self, snakes, fruits):
        bad_fruits = ["SKULL", "BOMB"]
        snakes_pos = []

        if not super().allowed__is_shield():  # if I don't have a shield, don't crash into snakes
            for s in snakes:
                snakes_pos += s.body_pos
        bad_poses = snakes_pos

        for b in bad_fruits:
            for f in fruits:
                if f.kind["name"] == b:
                    print(f.kind["name"], f.pos)
                    bad_poses.append(f.pos)
        # return list(set(bad_poses))
        return bad_poses

    def kill(self, x, y, neck, snakes, fruits):
        return self.go_get_it(x, y, neck, snakes, fruits)

    def swerve(self, x, y, bad_poses):
        for pos in bad_poses:
            if x == pos[0]:

                if y - pos[1] == 1:  # under the pos
                    if self.direction == Direction.UP:
                        return Direction.RIGHT
                    else:
                        return Direction.DOWN

                elif y - pos[1] == -1:  # above the pos
                    if self.direction == Direction.DOWN:
                        return Direction.RIGHT
                    else:
                        return Direction.UP
                else:
                    return 0

            return 0

    def go_get_it(self, x, y, pos, snakes, fruits):

        # dir = self.swerve(x, y, self.avoid_that(snakes, fruits))
        # if dir:  # if swerve is needed
        #     print(dir)
        #     return dir

        if x > pos[0]:
            if self.direction == Direction.RIGHT:
                return Direction.UP
            else:
                return Direction.LEFT

        if x < pos[0]:
            if self.direction == Direction.LEFT:
                return Direction.UP
            else:
                return Direction.RIGHT

        if x == pos[0]:
            if y < pos[1]:
                if self.direction == Direction.UP:
                    return Direction.RIGHT
                else:
                    return Direction.DOWN

            if y > pos[1]:
                if self.direction == Direction.DOWN:
                    return Direction.RIGHT
                else:
                    return Direction.UP
        return Direction.DOWN

    def get_enemy_neck_pos(self, snakes, fruits):
        for s in snakes:
            if s.name != "Tomer":
                return s.body_pos[1]
        return self.find_best_fruit(fruits)  # if I am the only snake I will go to the fruit

    @staticmethod
    def find_best_fruit(fruits):
        priority = ["KING", "KNIFE", "SHIELD", "DRAGON_FRUIT", "STRAWBERRY"]

        for p in priority:
            for f in fruits:
                if f.kind["name"] == p:
                    return f.pos
