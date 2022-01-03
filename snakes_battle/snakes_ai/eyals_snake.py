import copy
from random import choice
from snakes_battle.fruit import Fruit, FruitKind
from snakes_battle.snake import Snake, Direction
import math

class Node:
    depending_on_a_shield = False
    depending_on_a_knife = False

    def __init__(self, direction, body_pos, parent=None) -> None:
        self.parent = parent

        self.left = None
        self.right = None
        self.up = None
        self.down = None

        self.direction = direction
        self.body_pos = body_pos

        self.is_king = False
        self.king_remaining_effection = 0

        self.number_of_potential_dangerous = 0


    def create_children(self, simulate_turn_func):
        self.left = Node(Direction.LEFT, simulate_turn_func(self.body_pos, self.direction, Direction.LEFT), self)
        self.right = Node(Direction.RIGHT, simulate_turn_func(self.body_pos, self.direction, Direction.RIGHT), self)
        self.up = Node(Direction.UP, simulate_turn_func(self.body_pos, self.direction, Direction.UP), self)
        self.down = Node(Direction.DOWN, simulate_turn_func(self.body_pos, self.direction, Direction.DOWN), self)


    def get_children(self):
        return [self.left, self.right, self.up, self.down]
        
    def get_best_direction(self, harmful_fruits, all_snakes, my_snake, wanted_direction, border_cells):
        
        self.number_of_potential_dangerous = self.calculate_potential_dangerous(harmful_fruits, all_snakes, my_snake, border_cells)
        children = self.get_children()
        sorted_children = sorted(children, key=lambda child: child.number_of_potential_dangerous)
    
        for child in sorted_children:
            if abs(child.direction - my_snake.allowed__current_direction) != 1: # Get the best non opposite direction
                returned_direction = child.direction
                break

        if abs(wanted_direction - my_snake.allowed__current_direction) == 1: # Wanted direction is in the opposite direction so returning safest direction
            for child in sorted_children:
                if abs(child.direction - my_snake.allowed__current_direction) != 1 and abs(wanted_direction-child.direction) != 1: # Get the best non opposite direction
                    returned_direction = child.direction
                    return returned_direction


        for child in sorted_children:
            if child.direction == wanted_direction:
                print(f"wanted({wanted_direction}): {child.number_of_potential_dangerous} safest({sorted_children[0].direction}): {sorted_children[0].number_of_potential_dangerous} worst({sorted_children[-1].direction}): {sorted_children[-1].number_of_potential_dangerous}")

                avg_of_safe_and_worst = (sorted_children[0].number_of_potential_dangerous + sorted_children[-1].number_of_potential_dangerous)/2

                if child.number_of_potential_dangerous <= avg_of_safe_and_worst * 0.9:
                    returned_direction = wanted_direction
        
        print(f"current direction: {my_snake.allowed__current_direction}        next direction: {returned_direction}")
        
        if abs(returned_direction - my_snake.allowed__current_direction) == 1:
            print("Cant go in the opposite direction")
            
        return returned_direction


    def calculate_potential_dangerous(self, harmful_fruits, all_snakes, my_snake, border_cells):

        if self.is_leaf():
            if not self.is_it_a_safe_step(harmful_fruits, all_snakes, my_snake, border_cells):
                self.number_of_potential_dangerous += 1

            return self.number_of_potential_dangerous
            
        for child in self.get_children():
            self.number_of_potential_dangerous += child.calculate_potential_dangerous(harmful_fruits, all_snakes, my_snake, border_cells)
        
        return self.number_of_potential_dangerous

    def is_it_a_safe_step(self, harmful_fruits, all_snakes, my_snake, border_cells):

        # for i in range(len(my_snake.allowed__body_pos)):
        #                 if my_snake.allowed__body_pos[i][0] == self.body_pos[i][0] and my_snake.allowed__body_pos[i][1] == self.body_pos[i][1]:
        #                     raise Exception("Not a different snake")


        for fruit in harmful_fruits:
            if self.body_pos[0][0] == fruit.pos[0] and self.body_pos[0][1] == fruit.pos[1]:
                if not my_snake.allowed__is_shield():
                    return False
        
        for snake in all_snakes:

            if snake.name == my_snake.name: # my snake
                for index, cell in enumerate(snake.body_pos):
                    if index != 0 and self.body_pos[0][0] == cell[0] and self.body_pos[0][1] == cell[1]:
                        if not self.depending_on_a_shield and not my_snake.allowed__is_shield():
                            return False
                        else:
                            self.depending_on_a_shield = True
            
            else: # other snakes
                for cell in snake.body_pos:
                    if self.body_pos[0][0] == cell[0] and self.body_pos[0][1] == cell[1]:
                        if (not self.depending_on_a_shield and not my_snake.allowed__is_shield()):
                            return False
                        else:
                            self.depending_on_a_shield = True
                            self.depending_on_a_knife = True

        for cell in border_cells:
            if self.body_pos[0][0] == cell[0] and self.body_pos[0][1] == cell[1]:
                return True

        return True

    def is_leaf(self):
        if self.left != None:
            return False
        if self.right != None:
            return False
        if self.up != None:
            return False
        if self.down != None:
            return False
        
        return True


class Eyal(Snake):
    def __init__(self, borders_cells, color, name) -> None:
        super().__init__(color, name)
        self.init(borders_cells)



    def init(self, borders_cells):
        # Your bot initializations will be here.
        self.allowed__version = "3.0"
        # All the cells that are fill with borders. This variable will store a list of (x, y) pairs
        self.allowed__border_cells = borders_cells
    
    def make_decision(self, board_state):

        self.allowed__board_state = board_state
        self.allowed__body_pos = super().allowed__body_position()
        self.allowed__current_direction = super().allowed__get_direction()


        self.allowed__beneficial_fruits = []
        self.allowed__harmful_fruits = []
        self.allowed__special_fruits = []

        self.allowed_all_snakes = board_state["snakes"]


        # Sorting fruits.
        for fruit in self.allowed__board_state["fruits"]:
            if fruit.kind in FruitKind.beneficial_fruits:
                self.allowed__beneficial_fruits.append(fruit)
            elif fruit.kind in FruitKind.harmful_fruits:
                self.allowed__harmful_fruits.append(fruit)
            elif fruit.kind in FruitKind.special_fruits:
                self.allowed__special_fruits.append(fruit)


        best_fruit = self.best_fruit(self.allowed__beneficial_fruits + self.allowed__special_fruits)

        new_direction = self.get_direction_to_a_specific_fruit(best_fruit, self.allowed__current_direction)

        final_direction = self.calculate_best_step(new_direction, 3)

        return final_direction


    def calculate_best_step(self, wanted_direction, depth):

        Node.depending_on_a_shield = False
        Node.depending_on_a_knife = False

        root = Node(self.allowed__get_direction(), self.allowed__body_pos)

        root.create_children(self.simulate_turn)

        for child in root.get_children():
            child.create_children(self.simulate_turn)
            for child_of_child in child.get_children():
                child_of_child.create_children(self.simulate_turn)
                # for child_of_child_of_child in child_of_child.get_children():
                #     child_of_child_of_child.create_children(self.simulate_turn)

        return root.get_best_direction(self.allowed__harmful_fruits, self.allowed_all_snakes, self, wanted_direction, self.allowed__border_cells)
            
    def simulate_turn(self,body_pos, current_direction, new_direction):
        new_body_pos = copy.deepcopy(body_pos)
        if new_direction == Direction.LEFT:
            if current_direction == Direction.UP or current_direction == Direction.DOWN:
                new_direction =  Direction.LEFT

        elif new_direction == Direction.RIGHT:
            if current_direction == Direction.UP or current_direction == Direction.DOWN:
                new_direction =  Direction.RIGHT

        elif new_direction == Direction.UP:
            if current_direction == Direction.RIGHT or current_direction == Direction.LEFT:
                new_direction =  Direction.UP

        elif new_direction == Direction.DOWN:
            if current_direction == Direction.RIGHT or current_direction == Direction.LEFT:
                new_direction =  Direction.DOWN

        for i in reversed(range(1, super().allowed__get_length())):
            new_body_pos[i][0] = body_pos[i-1][0]
            new_body_pos[i][1] = body_pos[i-1][1]

        if new_direction == Direction.DOWN:
            new_body_pos[0][1] += 1
        elif new_direction == Direction.UP:
            new_body_pos[0][1] -= 1
        elif new_direction == Direction.LEFT:
            new_body_pos[0][0] -= 1
        elif new_direction == Direction.RIGHT:
            new_body_pos[0][0] += 1

        return new_body_pos

    def simulate_turn_head_only(self,body_pos, current_direction, new_direction):
        new_head_pos = copy.deepcopy(body_pos[0])
        if new_direction == Direction.LEFT:
            if current_direction == Direction.UP or current_direction == Direction.DOWN:
                new_direction =  Direction.LEFT

        elif new_direction == Direction.RIGHT:
            if current_direction == Direction.UP or current_direction == Direction.DOWN:
                new_direction =  Direction.RIGHT

        elif new_direction == Direction.UP:
            if current_direction == Direction.RIGHT or current_direction == Direction.LEFT:
                new_direction =  Direction.UP

        elif new_direction == Direction.DOWN:
            if current_direction == Direction.RIGHT or current_direction == Direction.LEFT:
                new_direction =  Direction.DOWN

        if new_direction == Direction.DOWN:
            new_head_pos[1] += 1
        elif new_direction == Direction.UP:
            new_head_pos[1] -= 1
        elif new_direction == Direction.LEFT:
            new_head_pos[0] -= 1
        elif new_direction == Direction.RIGHT:
            new_head_pos[0] += 1

        return new_head_pos

    def calculate_distance(self, a, b):
        return math.dist(a,b)

    def best_fruit(self, fruits):

        second_close_fruit = fruits[1]
        
        closest_fruit = fruits[0]
        closest = 100000

        for fruit in fruits:
            fruit_distance = self.calculate_distance(fruit.pos, self.allowed__body_pos[0])
            if fruit_distance < closest:
                second_close_fruit = closest_fruit
                closest = fruit_distance
                closest_fruit = fruit
        
        # for cell in self.allowed__border_cells:
        #     if abs(closest_fruit.pos[0] - cell[0]) + abs(closest_fruit.pos[1] - cell[1]) == 1: # Don't take that fruit
        #         return second_close_fruit

        return closest_fruit

    def chose_a_good_direction_when_wants_the_opposite(self, direction1, direction2, fruit):
        head1 = self.simulate_turn_head_only(self.allowed__body_pos, self.allowed__current_direction, direction1)
        head2 = self.simulate_turn_head_only(self.allowed__body_pos, self.allowed__current_direction, direction2)

        distance1 = math.dist(head1, fruit.pos)
        distance2 = math.dist(head2, fruit.pos)

        if distance1 < distance2:
            return direction1
        
        return distance2

    def get_direction_to_a_specific_fruit(self, fruit, current_direction):

        if self.allowed__body_pos[0][0] > fruit.pos[0]:
            if (current_direction == Direction.RIGHT):
                return self.chose_a_good_direction_when_wants_the_opposite(Direction.UP, Direction.DOWN, fruit)
            else:
                return Direction.LEFT
        
        if self.allowed__body_pos[0][0] < fruit.pos[0]:
            if (current_direction == Direction.LEFT):
                return self.chose_a_good_direction_when_wants_the_opposite(Direction.UP, Direction.DOWN, fruit)
            else:
                return Direction.RIGHT
        
        if self.allowed__body_pos[0][0] == fruit.pos[0]:

            if self.allowed__body_pos[0][1] < fruit.pos[1]:
                if (current_direction == Direction.UP):
                    return self.chose_a_good_direction_when_wants_the_opposite(Direction.RIGHT, Direction.LEFT, fruit)
                else:
                    return Direction.DOWN

            if self.allowed__body_pos[0][1] > fruit.pos[1]:
                if (current_direction == Direction.DOWN):
                    return self.chose_a_good_direction_when_wants_the_opposite(Direction.RIGHT, Direction.LEFT, fruit)
                else:
                    return Direction.UP