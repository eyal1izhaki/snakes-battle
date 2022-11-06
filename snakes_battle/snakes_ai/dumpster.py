import random

import numpy as np
import copy
from snakes_battle.snake import Snake, Direction
from snakes_battle.fruit import FruitKind


def get_distances_to_fruit(snake_head, fruit_list_pos):
    return [abs(snake_head[0] - fruit_pos[0]) + abs(snake_head[1] - fruit_pos[1]) for fruit_pos in fruit_list_pos]


class Dumpster(Snake):
    def __init__(self, borders_cells, color, name) -> None:
        super().__init__(color, name)

        self.version = 1.0
        self.border_cells = borders_cells

    def make_decision(self, board_state):
        direction_dict_code_key = {0: "RIGHT", 1: "LEFT", 2: "UP", 3: "DOWN", 4: "CONTINUE"}
        direction_dict_decision_key = {"RIGHT": 0, "LEFT": 1, "UP": 2, "DOWN": 3, "CONTINUE": 4}
        decision = Direction.CONTINUE
        head = self.head
        fruits = board_state["fruits"]
        snakes = board_state["snakes"]
        enemy_snake = None
        enemy_snake_head = None
        if len(snakes) > 1:
            enemy_snake = snakes[1]
            enemy_snake_head = snakes[1].head
        boarder_cell_list = [list(elem) for elem in self.border_cells]
        skull_pos = [-11, -11]
        for fruit in fruits:
            if fruit.kind['name'] == 'SKULL':
                skull_pos[0] = fruit.pos[0]
                skull_pos[1] = fruit.pos[1]

        beneficial_fruits = [fruit for fruit in fruits if fruit.kind['name'] in ["STRAWBERRY", "DRAGON_FRUIT"]]
        beneficial_fruits_pos = [fruit.pos for fruit in beneficial_fruits]
        harmful_fruits = [fruit for fruit in fruits if fruit.kind['name'] == "BOMB"]
        harmful_fruits_pos = [fruit.pos for fruit in harmful_fruits]

        available_directions = [Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT]
        # make sure not to do full turn since snake will collide
        if self.direction == Direction.UP:
            available_directions.remove(Direction.DOWN)
        elif self.direction == Direction.DOWN:
            available_directions.remove(Direction.UP)
        elif self.direction == Direction.LEFT:
            available_directions.remove(Direction.RIGHT)
        elif self.direction == Direction.RIGHT:
            available_directions.remove(Direction.LEFT)

        # make sure not to collide with border cells and skull
        # top

        if ([head[0], head[1] - 1] in boarder_cell_list) or (head[0] == skull_pos[0] and head[1] - 1 == skull_pos[1]):
            if Direction.UP in available_directions:
                available_directions.remove(Direction.UP)
        # right
        if ([head[0] + 1, head[1]] in boarder_cell_list) or (head[0] + 1 == skull_pos[0] and head[1] == skull_pos[1]):
            if Direction.RIGHT in available_directions:
                available_directions.remove(Direction.RIGHT)
        # bottom
        if ([head[0], head[1] + 1] in boarder_cell_list) or (head[0] == skull_pos[0] and head[1] + 1 == skull_pos[1]):
            if Direction.DOWN in available_directions:
                available_directions.remove(Direction.DOWN)
        # left
        if ([head[0] - 1, head[1]] in boarder_cell_list) or (head[0] - 1 == skull_pos[0] and head[1] == skull_pos[1]):
            if Direction.LEFT in available_directions:
                available_directions.remove(Direction.LEFT)

        for snake in snakes:
            # todo attack if have knife, crown, only I have shield or both no shields but I have bigger length

            # avoid insta-losing decisions (snakes collision)
            for snake_pos in snake.body_position:
                if snake_pos[0] == head[0] and snake_pos[1] == head[1]:
                    continue
                if head[0] - 1 == snake_pos[0] and head[1] == snake_pos[1]:
                    if Direction.LEFT in available_directions:
                        available_directions.remove(Direction.LEFT)
                if head[0] + 1 == snake_pos[0] and head[1] == snake_pos[1]:
                    if Direction.RIGHT in available_directions:
                        available_directions.remove(Direction.RIGHT)
                if head[0] == snake_pos[0] and head[1] - 1 == snake_pos[1]:
                    if Direction.UP in available_directions:
                        available_directions.remove(Direction.UP)
                if head[0] == snake_pos[0] and head[1] + 1 == snake_pos[1]:
                    if Direction.DOWN in available_directions:
                        available_directions.remove(Direction.DOWN)
        target = self.get_target(board_state, available_directions)
        ally_destination = target
        ally_distance_to_fruit = [abs(head[0] - fruit_pos[0]) + abs(head[1] - fruit_pos[1]) for fruit_pos in
                                  beneficial_fruits_pos]

        # ally_destination = beneficial_fruits_pos[np.argmin(ally_distance_to_fruit)]  # todo abort if closest to enemy
        # todo combat tactics and target selection:
        # todo trap near food when length 14, 3 way block a fruit (only non-special fruits)
        '''
        6- 5|x| 1-14 
        7- 4-3-2-13
        8-9-10-11-12
        '''
        # todo attack if have knife, crown, only I have shield or both no shields but I have bigger length
        # todo grow by eating fruit - find closest fruit to enemy and self, if fruit closer to self, go.
        # todo if fruit closer to enemy - find one closer to self. if none exist, go to furthest away from enemy
        '''
        if fruit closest to enemy is closer to ally, set destination to that fruit. 
        if fruit closest to ally is closer to enemy, go for the max distance fruit from enemy.
        if one closer to ally and one closer to enemy, go to closer to ally
        if enemy has knife, go to furthermost fruit until can reach shield or crown, then sprint there. 
        '''
        # special_items = [fruit for fruit in fruits if fruit.kind['name'] in ["SHIELD", "KING", "KNIFE"]]
        #
        # shield_pos_list = [fruit.pos for fruit in special_items if fruit.kind['name'] == "SHIELD"]
        # shield_lifespan_list = [fruit.lifespan for fruit in fruits if fruit.kind['name'] == "SHIELD"]
        #
        # king_lifespan_list = [fruit.lifespan for fruit in fruits if fruit.kind['name'] == "KING"]
        # king_pos_list = [fruit.pos for fruit in special_items if fruit.kind['name'] == "KING"]
        #
        # knife_lifespan_list = [fruit.lifespan for fruit in fruits if fruit.kind['name'] == "KNIFE"]
        # knife_pos_list = [fruit.pos for fruit in special_items if fruit.kind['name'] == "KNIFE"]
        # if len(snakes) > 1:
        #     if not self.king:
        #         ally_distance_to_king = [abs(head[0] - king_pos[0]) + abs(head[1] - king_pos[1]) for king_pos in
        #                                  king_pos_list]
        #         enemy_distance_to_king = None
        #         if enemy_snake is not None:
        #             enemy_distance_to_king = [
        #                 abs(enemy_snake_head[0] - king_pos[0]) + abs(enemy_snake_head[1] - king_pos[1]) for king_pos in
        #                 king_pos_list]
        #         for i in range(len(ally_distance_to_king)):
        #             if ally_distance_to_king[i] > king_lifespan_list[i]:
        #                 continue
        #             if enemy_snake is not None:
        #                 # if ally_distance_to_king[i] > enemy_distance_to_king[i]:
        #                 continue
        #             else:
        #                 if self.length > 20 or ally_distance_to_king[
        #                     i] <= 7:  # todo alter when switch targets because enemy closer
        #                     ally_destination = king_pos_list[i]
        #     if ally_destination not in king_pos_list and not self.shield:
        #
        #         ally_distance_to_shield = [abs(head[0] - shield_pos[0]) + abs(head[1] - shield_pos[1]) for shield_pos in
        #                                    shield_pos_list]
        #         enemy_distance_to_shield = None
        #         if enemy_snake is not None and enemy_snake_head is not None:
        #             enemy_distance_to_shield = [
        #                 abs(enemy_snake_head[0] - shield_pos[0]) + abs(enemy_snake_head[1] - shield_pos[1]) for
        #                 shield_pos in shield_pos_list]
        #         for i in range(len(ally_distance_to_shield)):
        #             if ally_distance_to_shield[i] > shield_lifespan_list[i]:
        #                 continue
        #             if enemy_snake is not None:
        #                 pass
        #                 # if ally_distance_to_shield[i] > enemy_distance_to_shield[i]:
        #                 #     continue
        #             else:
        #                 ally_destination = shield_pos_list[i]
        #     if ally_destination not in king_pos_list and not self.knife and ally_destination not in shield_pos_list:
        #         ally_distance_to_knife = [abs(head[0] - knife_pos[0]) + abs(head[1] - knife_pos[1]) for knife_pos in
        #                                   knife_pos_list]
        #         enemy_distance_to_knife = None
        #         if enemy_snake is not None and enemy_snake_head is not None:
        #             enemy_distance_to_knife = [
        #                 abs(enemy_snake_head[0] - knife_pos[0]) + abs(enemy_snake_head[1] - knife_pos[1]) for knife_pos
        #                 in
        #                 knife_pos_list]
        #         for i in range(len(ally_distance_to_knife)):
        #             if ally_distance_to_knife[i] > knife_lifespan_list[i]:
        #                 continue
        #             if enemy_snake is not None:
        #                 if ally_distance_to_knife[i] > enemy_distance_to_knife[i]:
        #                     continue
        #             else:
        #                 ally_destination = knife_pos_list[i]
        possible_steps = {
            "up": [head[0], head[1] - 1],
            "down": [head[0], head[1] + 1],
            "right": [head[0] + 1, head[1]],
            "left": [head[0] - 1, head[1]]
        }
        if head[0] < ally_destination[0]:
            if Direction.RIGHT in available_directions:
                decision = Direction.RIGHT
            # todo add workaround for right blocked
        if head[0] > ally_destination[0]:
            if Direction.LEFT in available_directions:
                decision = Direction.LEFT
            # todo add workaround for left blocked
        if head[1] < ally_destination[1]:
            if Direction.DOWN in available_directions:
                decision = Direction.DOWN
            # todo add workaround for down blocked
        if head[1] > ally_destination[1]:
            if Direction.UP in available_directions:
                decision = Direction.UP
            # todo add workaround for up blocked
        if head[0] == ally_destination[0]:
            if head[1] > ally_destination[1]:
                if Direction.UP in available_directions:
                    decision = Direction.UP
                # todo add workaround for up blocked
            if head[1] < ally_destination[1]:
                if Direction.DOWN in available_directions:
                    decision = Direction.DOWN

        if decision == Direction.CONTINUE:
            if len(available_directions) >= 1:
                decision = random.choice(available_directions)
                # todo if decision goes to bomb look try another move that doesn't insta lose
        else:
            if possible_steps[direction_dict_code_key[decision].lower()] in harmful_fruits_pos:
                keys = possible_steps.keys()
                for k in keys:
                    option = possible_steps[k]
                    if option not in harmful_fruits_pos \
                            and option not in boarder_cell_list \
                            and option != skull_pos \
                            and option not in [snake.body_position[0:] for snake in snakes]:
                        return direction_dict_decision_key[k.upper()]
        return decision

    def get_target(self, board_state, available_directions):
        fruits = board_state["fruits"]
        snakes = board_state["snakes"]
        head = self.head
        is_alone_on_board = len(snakes) == 1
        beneficial_fruits = [fruit for fruit in fruits if fruit.kind['name'] in ["STRAWBERRY", "DRAGON_FRUIT"]]
        beneficial_fruits_pos = [fruit.pos for fruit in beneficial_fruits]
        if is_alone_on_board:
            ally_distance_to_fruit = get_distances_to_fruit(head, beneficial_fruits_pos)
            ally_destination = beneficial_fruits_pos[np.argmin(ally_distance_to_fruit)]
            # print("is alone", is_alone_on_board)
            return ally_destination

        enemy_snake = snakes[1]
        enemy_snake_head = snakes[1].head

        ally_distance_to_fruit = get_distances_to_fruit(head, beneficial_fruits_pos)
        ally_min_distance = min(ally_distance_to_fruit)
        ally_destination = beneficial_fruits_pos[np.argmin(ally_distance_to_fruit)]

        enemy_distance_to_fruit = get_distances_to_fruit(enemy_snake_head, beneficial_fruits_pos)
        enemy_min_distance = min(enemy_distance_to_fruit)
        enemy_destination = beneficial_fruits_pos[np.argmin(enemy_distance_to_fruit)]

        if ally_destination == enemy_destination:
            if ally_min_distance > enemy_min_distance:
                ally_destination = beneficial_fruits_pos[np.argmin(ally_distance_to_fruit) - 1]
        if abs(head[0] - enemy_destination[0]) + abs(head[1] - enemy_destination[1]) < enemy_min_distance:
            ally_destination = enemy_destination

        enemy_target_bank = []
        special_items = [fruit for fruit in fruits if fruit.kind['name'] in ["SHIELD", "KING", "KNIFE"]]

        shield_pos_list = [fruit.pos for fruit in special_items if fruit.kind['name'] == "SHIELD"]
        shield_lifespan_list = [fruit.lifespan for fruit in fruits if fruit.kind['name'] == "SHIELD"]

        king_lifespan_list = [fruit.lifespan for fruit in fruits if fruit.kind['name'] == "KING"]
        king_pos_list = [fruit.pos for fruit in special_items if fruit.kind['name'] == "KING"]

        knife_lifespan_list = [fruit.lifespan for fruit in fruits if fruit.kind['name'] == "KNIFE"]
        knife_pos_list = [fruit.pos for fruit in special_items if fruit.kind['name'] == "KNIFE"]
        if not self.king and len(snakes) > 1:
            if len(king_pos_list) >= 1:
                for i in range(len(king_pos_list)):
                    # if self.is_can_get_there(king_pos_list[i], king_lifespan_list[i]):
                    if self.is_can_get_there_before_enemy(enemy_snake_head, king_pos_list[i]):
                        ally_destination = king_pos_list[i]
                    return ally_destination
        if (self.knife or self.king) and not (enemy_snake.shield or enemy_snake.king):
            ally_distance_to_target = get_distances_to_fruit(head, enemy_snake.body_position)
            target = enemy_snake.body_position[np.argmin(ally_distance_to_fruit)]
            ally_destination = target
            if enemy_snake.length >= 3:
                return ally_destination

        if not self.knife and len(snakes) > 1 and self.length > 12:
            if len(knife_pos_list) >= 1:
                for i in range(len(knife_pos_list)):
                    if self.is_can_get_there(knife_pos_list[i], knife_lifespan_list[i]):
                        # print("looking for knife")
                        if self.is_can_get_there_before_enemy(enemy_snake_head, knife_pos_list[i]):
                            ally_destination = knife_pos_list[i]
                            return ally_destination

        if not self.shield and len(snakes) > 1 and self.length > 12:
            if len(shield_pos_list) >= 1:
                # print("looking for shield")
                for i in range(len(shield_pos_list)):
                    # if self.is_can_get_there(shield_pos_list[i], shield_lifespan_list[i]):
                    if self.is_can_get_there_before_enemy(enemy_snake_head, shield_pos_list[i]):
                        ally_destination = shield_pos_list[i]
                        return ally_destination

        return ally_destination

    def is_can_get_there(self, pos, lifespan):
        head = self.head
        return abs(head[0] - pos[0]) + abs(head[1] - pos[1]) < lifespan

    def is_can_get_there_before_enemy(self, enemy_head, pos):
        head = self.head
        return abs(head[0] - pos[0]) + abs(head[1] - pos[1]) < abs(enemy_head[0] - pos[0]) + abs(enemy_head[1] - pos[1])
