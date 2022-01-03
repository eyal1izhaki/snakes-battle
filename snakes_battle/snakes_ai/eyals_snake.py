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
        
    def get_sorted_children(self, harmful_fruits, all_snakes, my_snake, border_cells):
        
        self.number_of_potential_dangerous = self.calculate_potential_dangerous(harmful_fruits, all_snakes, my_snake, border_cells)
        children = self.get_children()
        sorted_children = sorted(children, key=lambda child: child.number_of_potential_dangerous)
        return sorted_children

    def calculate_potential_dangerous(self, harmful_fruits, all_snakes, my_snake, border_cells):

        if self.is_leaf():
            if not self.is_it_a_safe_step(harmful_fruits, all_snakes, my_snake, border_cells):
                self.number_of_potential_dangerous += 1

            return self.number_of_potential_dangerous
            
        for child in self.get_children():
            self.number_of_potential_dangerous += child.calculate_potential_dangerous(harmful_fruits, all_snakes, my_snake, border_cells)
        
        return self.number_of_potential_dangerous

    def is_it_a_safe_step(self, harmful_fruits, all_snakes, my_snake, border_cells):

        for fruit in harmful_fruits:
            if self.body_pos[0][0] == fruit.pos[0] and self.body_pos[0][1] == fruit.pos[1]:
                if not my_snake.allowed__is_shield():
                    return False
        
        for snake in all_snakes:

            if snake.name == my_snake.name: # my snake
                for index, cell in enumerate(snake.body_pos):
                    if index != 0 and self.body_pos[0][0] == cell[0] and self.body_pos[0][1] == cell[1]:
                        if not self.depending_on_a_shield and not my_snake.allowed__is_shield() and not my_snake.allowed__is_king_for_next_3_steps():
                            return False
                        else:
                            self.depending_on_a_shield = True
            
            else: # other snakes
                for cell in snake.body_pos:
                    if self.body_pos[0][0] == cell[0] and self.body_pos[0][1] == cell[1]:
                        if not self.depending_on_a_knife and not my_snake.allowed__is_knife() and not self.depending_on_a_shield and not my_snake.allowed__is_shield() and not my_snake.allowed__is_king_for_next_3_steps():
                            return False
                        else:
                            self.depending_on_a_shield = True
                            self.depending_on_a_knife = True
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
        self.allowed__version = "4.0"
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

        wanted_direction = self.get_direction_to_a_specific_fruit(best_fruit.pos, self.allowed__current_direction)

        best_direction = self.get_best_direction(wanted_direction)

        new_head_pos = self.simulate_turn_head_only(self.allowed__body_pos, self.allowed__current_direction, best_direction)

        if new_head_pos in self.allowed__border_cells:
            return wanted_direction

        return best_direction

    
    def get_best_direction(self, wanted_direction):

        root = self.create_tree()

        sorted_children = root.get_sorted_children(self.allowed__harmful_fruits, self.allowed_all_snakes, self, self.allowed__border_cells)

        returned_direction = sorted_children[0].direction

        for child in sorted_children:

            if child.direction == wanted_direction:
                avg_of_safe_and_worst = (sorted_children[0].number_of_potential_dangerous + sorted_children[-1].number_of_potential_dangerous)/2
                if child.number_of_potential_dangerous <= avg_of_safe_and_worst * 0.9:
                    returned_direction = wanted_direction

        # print(f"wanted: {wanted_direction}      current: {self.allowed__current_direction}")
        return returned_direction

    def create_tree(self):

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

        return root
            
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

        return closest_fruit

    def choose_a_good_direction_when_wants_the_opposite(self, direction1, direction2, location):
        head1 = self.simulate_turn_head_only(self.allowed__body_pos, self.allowed__current_direction, direction1)
        head2 = self.simulate_turn_head_only(self.allowed__body_pos, self.allowed__current_direction, direction2)

        distance1 = math.dist(head1, location)
        distance2 = math.dist(head2, location)

        if distance1 < distance2:
            return direction1
        
        return direction2

    def get_direction_to_a_specific_fruit(self, location, current_direction):

        if self.allowed__body_pos[0][0] > location[0]:
            if (current_direction == Direction.RIGHT):
                return self.choose_a_good_direction_when_wants_the_opposite(Direction.UP, Direction.DOWN, location)
            else:
                return Direction.LEFT
        
        if self.allowed__body_pos[0][0] < location[0]:
            if (current_direction == Direction.LEFT):
                return self.choose_a_good_direction_when_wants_the_opposite(Direction.UP, Direction.DOWN, location)
            else:
                return Direction.RIGHT
        
        if self.allowed__body_pos[0][0] == location[0]:

            if self.allowed__body_pos[0][1] < location[1]:
                if (current_direction == Direction.UP):
                    return self.choose_a_good_direction_when_wants_the_opposite(Direction.RIGHT, Direction.LEFT, location)
                else:
                    return Direction.DOWN

            if self.allowed__body_pos[0][1] > location[1]:
                if (current_direction == Direction.DOWN):
                    return self.choose_a_good_direction_when_wants_the_opposite(Direction.RIGHT, Direction.LEFT, location)
                else:
                    return Direction.UP
    
    def allowed__is_king_for_next_3_steps(self):
        if self.allowed__is_king() == False:
            return False

        remain = self.allowed__get_king_remaining_effection()

        if remain > 3:
            return True