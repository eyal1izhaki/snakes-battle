from snakes_battle.fruit import FruitKind
from snakes_battle.snake import Snake, Direction

class DavidalkKing(Snake):
    def __init__(self, borders_cells, color, name) -> None:
        super().__init__(color, name)
        self.init(borders_cells)

    def init(self, borders_cells):
        self.allowed__version = 1.0
        self.allowed__border_cells = borders_cells
    
    def allowed_get_all_direction_points(self, position):
        node_position_up = (position[0], position[1] - 1)
        node_position_down = (position[0], position[1] + 1)
        node_position_left = (position[0] - 1, position[1])
        node_position_right = (position[0] + 1, position[1])
        return node_position_up, node_position_down, node_position_left, node_position_right
    
    def allowed_is_position_valid(self, board_state, position):
        border_x, border_y = self.allowed__border_cells[-1][0], self.allowed__border_cells[-1][1]

        # Checking if the point is out of bounds
        if (position in self.allowed__border_cells):
            return False
        if (position[0] <= 0 or position[1] <= 0 or position[0] > border_x or position[1] > border_y):
            return False

        # Checking if the point is harmful
        fruits = board_state["fruits"]
        for fruit in fruits:
            if (fruit.kind in FruitKind.harmful_fruits and fruit.pos == position):
                return False
        
        # Checking if the point collides with another snake
        snakes = board_state["snakes"]
        for snake in snakes:
            # Skipping me if I have shield or crown
            # if ((self.allowed__is_shield() or self.allowed__is_king()) and snake.__class__ == DavidalkKing):
            #     continue
            
            for node_position in snake.allowed__body_position():
                if (node_position == position):
                    return False
        
        # If everything is fine - return True
        return True

    def allowed_create_graph_from_board(self, board_state):
        graph = {}
        border_x, border_y = self.allowed__border_cells[-1][0], self.allowed__border_cells[-1][1]
        for x_run in range(1, border_x + 1):
            for y_run in range(1, border_y + 1):
                allowed_moves = []
                node_position = (x_run, y_run)

                # All possible nodes that will be connected
                node_position_up, node_position_down, node_position_left, node_position_right = self.allowed_get_all_direction_points(node_position)

                # Checking if we want these nodes and if we do - add them to the array
                if (self.allowed_is_position_valid(board_state, node_position_up)):
                    allowed_moves.append(str(node_position_up))
                if (self.allowed_is_position_valid(board_state, node_position_down)):
                    allowed_moves.append(str(node_position_down))
                if (self.allowed_is_position_valid(board_state, node_position_left)):
                    allowed_moves.append(str(node_position_left))
                if (self.allowed_is_position_valid(board_state, node_position_right)):
                    allowed_moves.append(str(node_position_right))
                
                # Put the array in the graph
                graph[str(node_position)] = allowed_moves
        return graph

    def allowed_get_distance(self, position1, position2):
        return abs(position1[0] - position2[0]) + abs(position1[1] - position2[1])
    
    def allowed_get_good_fruits(self, fruits):
        good_fruits = [x for x in fruits if x.kind not in FruitKind.harmful_fruits]
        return good_fruits
    
    def allowed_get_target_fruit(self, board_state):
        body = self.allowed__body_position()
        head = body[0]
        good_fruits = self.allowed_get_good_fruits(board_state["fruits"])
        closest_fruit = good_fruits[0]
        for fruit in good_fruits[1:]:
            if (self.allowed_get_distance(fruit.pos, head) < self.allowed_get_distance(closest_fruit.pos, head)):
                closest_fruit = fruit
        return closest_fruit
    
    def allowed_choose_path(self, target_position, board_state):
        body = self.allowed__body_position()
        head = body[0]
        graph = self.allowed_create_graph_from_board(board_state)
        path = self.allowed_BFS_SP(graph, str(tuple(head)), str(tuple(target_position)))
        splitted_next_node = path[1][1:-1].strip().split(",")
        splitted_next_node = [int(x) for x in splitted_next_node]
        return tuple(splitted_next_node)
    
    def make_decision(self, board_state):
        # Choosing a target fruit
        target_fruit = self.allowed_get_target_fruit(board_state)

        # Choose next node to move to
        next_node = self.allowed_choose_path(target_fruit.pos, board_state)
        
        # Converting it to direction
        body = self.allowed__body_position()
        head = body[0]
        node_position_up, node_position_down, node_position_left, node_position_right = self.allowed_get_all_direction_points(head)
        target_direction = None
        if (next_node == node_position_up):
            # Making sure there is no backtracking
            if (self.allowed__get_direction() != Direction.DOWN):
                target_direction = Direction.UP
            else:
                if (self.allowed_is_position_valid(node_position_left)):
                    target_direction = Direction.LEFT
                elif (self.allowed_is_position_valid(node_position_right)):
                    target_direction = Direction.RIGHT
                else:
                    target_direction = Direction.DOWN # Might die here if all access points are blocked
        elif (next_node == node_position_down):
            if (self.allowed__get_direction() != Direction.UP):
                target_direction = Direction.DOWN
            else:
                # Checking which direction will not kill me
                if (self.allowed_is_position_valid(node_position_left)):
                    target_direction = Direction.LEFT
                elif (self.allowed_is_position_valid(node_position_right)):
                    target_direction = Direction.RIGHT
                else:
                    target_direction = Direction.UP # Might die here if all access points are blocked
        elif (next_node == node_position_left):
            if (self.allowed__get_direction() != Direction.RIGHT):
                target_direction = Direction.LEFT
            else:
                # Checking which direction will not kill me
                if (self.allowed_is_position_valid(node_position_up)):
                    target_direction = Direction.UP
                elif (self.allowed_is_position_valid(node_position_down)):
                    target_direction = Direction.DOWN
                else:
                    target_direction = Direction.RIGHT # Might die here if all access points are blocked
        elif (next_node == node_position_right):
            if (self.allowed__get_direction() != Direction.LEFT):
                target_direction = Direction.RIGHT
            else:
                # Checking which direction will not kill me
                if (self.allowed_is_position_valid(node_position_up)):
                    target_direction = Direction.UP
                elif (self.allowed_is_position_valid(node_position_down)):
                    target_direction = Direction.DOWN
                else:
                    target_direction = Direction.LEFT # Might die here if all access points are blocked
        
        # If not backtracing - return the target dir
        return target_direction

    def allowed_BFS_SP(self, graph, start, goal):
        explored = []
        
        # Queue for traversing the
        # graph in the BFS
        queue = [[start]]
        
        # If the desired node is
        # reached
        if start == goal:
            # print("Same Node")
            return
        
        # Loop to traverse the graph
        # with the help of the queue
        while queue:
            path = queue.pop(0)
            node = path[-1]
            
            # Condition to check if the
            # current node is not visited
            if node not in explored:
                neighbours = graph[node]
                
                # Loop to iterate over the
                # neighbours of the node
                for neighbour in neighbours:
                    new_path = list(path)
                    new_path.append(neighbour)
                    queue.append(new_path)
                    
                    # Condition to check if the
                    # neighbour node is the goal
                    if neighbour == goal:
                        # print("Shortest path = ", *new_path)
                        return new_path
                explored.append(node)
    
        # Condition when the nodes
        # are not connected
        # print("So sorry, but a connecting"\
                    # "path doesn't exist :(")
        return
