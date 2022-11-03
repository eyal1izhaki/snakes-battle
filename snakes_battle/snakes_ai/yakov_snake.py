from multiprocessing import current_process
from xml.dom.xmlbuilder import Options
from snakes_battle.snake import Snake, Direction
from snakes_battle.fruit import FruitKind


class Yakov(Snake):
    def __init__(self, borders_cells, color, name) -> None:
        super().__init__(color, name)

        self.version = 1.0
        self.border_cells = borders_cells
        self.MAX_DISTANCE = 100000

    def find_not_die(self,head, fruits,his_snake):
        my_snake = self.body_position
        snakes = his_snake+ my_snake
        if (head[0]+1,head[1]) not in self.border_cells:
            if [head[0]+1,head[1]] not in snakes:
                for fruit in fruits:
                    if fruit.pos == [head[0]+1,head[1]]:
                        if fruit.kind not in FruitKind.harmful_fruits:
                            return [head[0]+1,head[1]]
                        elif fruit.kind['name']!='SKULL':
                            return [head[0]+1,head[1]]
                    else:
                        return [head[0]+1,head[1]]

        if (head[0]-1,head[1]) not in self.border_cells:
            if [head[0]-1,head[1]] not in snakes:
                for fruit in fruits:
                    if fruit.pos == [head[0]-1,head[1]]:
                        if fruit.kind not in FruitKind.harmful_fruits:
                            return [head[0]-1,head[1]]
                        elif fruit.kind['name']!='SKULL':
                            return [head[0]-1,head[1]]
                    else:
                        return [head[0]-1,head[1]]

        if (head[0],head[1]-1) not in self.border_cells:
            if [head[0],head[1]-1] not in snakes:
                for fruit in fruits:
                    if fruit.pos == [head[0],head[1]-1]:
                        if fruit.kind not in FruitKind.harmful_fruits:
                            return [head[0],head[1]-1]
                        elif fruit.kind['name']!='SKULL':
                            return [head[0],head[1]-1]
                    else:
                        return [head[0],head[1]-1]

        if (head[0],head[1]+1) not in self.border_cells:
            if [head[0],head[1]+1] not in snakes:
                for fruit in fruits:
                    if fruit.pos == [head[0],head[1]+1]:
                        if fruit.kind not in FruitKind.harmful_fruits:
                            return [head[0],head[1]+1]
                        elif fruit.kind['name']!='SKULL':
                            return [head[0],head[1]+1]
                    else:
                        return [head[0],head[1]-1]

        return [head[0],head[1]+1]
                    
    def get_direction(self, close):
        head = self.body_position[0]
        direction = 1
        if head[0] > close[0]:
            direction = Direction.LEFT

        if head[0] < close[0]:
            direction = Direction.RIGHT

        if head[0] == close[0]:

            if head[1] < close[1]:
                direction = Direction.DOWN

            if head[1] > close[1]:
                direction = Direction.UP

        return direction

    def bad_next(self, his_snake, fruits, direction):
        my_snake = self.body_position
        head = my_snake[0]

        next = [0, 0]
        if direction == Direction.RIGHT:
            next = [head[0]+1, head[1]]
        elif direction == Direction.LEFT:
            next = [head[0]-1, head[1]]
        elif direction == Direction.UP:
            next = [head[0], head[1]-1]
        elif direction == Direction.DOWN:
            next = [head[0]-1, head[1]+1]

        for fruit in fruits:
            if fruit.kind in FruitKind.harmful_fruits and next == fruit.pos:
                return True

        for place in his_snake[1:]:
            if next == place:
                return True
        if his_snake !=[]:
            if [next[0]+1, next[1]] == his_snake[0] or [next[0]-1, next[1]] == his_snake[0] or [next[0], next[1]-1] == his_snake[0] or [next[0], next[1]+1] == his_snake[0]:
                return True

        if next in my_snake:
            return True

        if next in self.border_cells:
            return True

        return False
    def get_general(self,fruits, his_snake):
        head = self.body_position[0]
        for fruit in fruits:
            if fruit.kind in FruitKind.beneficial_fruits or fruit.kind in FruitKind.special_fruits:
                current_best = fruit.pos
                if self.bad_next(his_snake, fruits, self.get_direction(current_best)):
                    fruits1 = [frui for frui in fruits if frui.pos !=fruit.pos ]
                    if len(fruits1)==0:
                        return self.find_not_die(head,fruits,his_snake)
                    else:
                        for fruit in fruits1:
                            if fruit.kind in FruitKind.beneficial_fruits or fruit.kind in FruitKind.special_fruits:
                                current_best = fruit.pos
                                if self.bad_next(his_snake, fruits, self.get_direction(current_best)):
                                    fruits2 = [frui for frui in fruits if frui.pos !=fruit.pos ]
                                    if len(fruits2)==0:
                                        return self.find_not_die(head,fruits,his_snake)
                                    else:
                                        for fruit in fruits2:
                                            if fruit.kind in FruitKind.beneficial_fruits or fruit.kind in FruitKind.special_fruits:
                                                current_best = fruit.pos
                                                if self.bad_next(his_snake, fruits, self.get_direction(current_best)):
                                                    return self.find_not_die(head,fruits,his_snake)
                                                else:
                                                    return current_best  
                                else:
                                    return current_best    
                else:
                    return current_best
        
        return self.find_not_die(head,fruits,his_snake)
        
    def get_best_plain(self, the_min,my_options, fruits, his_snake):
        head = self.body_position[0]
        for option in my_options:
            if option["value"] == the_min:
                current_best = option['place'][0]
                if self.bad_next(his_snake, fruits, self.get_direction(current_best)):
                    my_options1 = [optio for optio in my_options if optio["value"] !=option["value"] ]
                    if len(my_options1)==0:
                        return self.find_not_die(head,fruits,his_snake)
                    else:
                        the_min = min(option["value"] for option in my_options1)
                        for option in my_options1:
                            if option["value"] == the_min:
                                current_best = option['place'][0]
                                if self.bad_next(his_snake, fruits, self.get_direction(current_best)):
                                    my_options1 = [optio for optio in my_options if optio["value"] !=option["value"] ]
                                    if len(my_options1)==0:
                                        return self.find_not_die(head,fruits,his_snake)
                                    else:
                                        the_min = min(option["value"] for option in my_options1)
                                        for option in my_options1:
                                            if option["value"] == the_min:
                                                current_best = option['place'][0]
                                                if self.bad_next(his_snake, fruits, self.get_direction(current_best)):
                                                    my_options1 = [optio for optio in my_options if optio["value"] !=option["value"] ]
                                                    if len(my_options1)==0:
                                                        return self.find_not_die(head,fruits,his_snake)
                                                    else:
                                                        the_min = min(option["value"] for option in my_options1)
                                                        for option in my_options1:
                                                            if option["value"] == the_min:
                                                                current_best = option['place'][0]
                                                                if self.bad_next(his_snake, fruits, self.get_direction(current_best)):
                                                                    return self.find_not_die(head,fruits,his_snake)
                                                                else:
                                                                    return current_best
                                                else:
                                                    return current_best
                                else:
                                    return current_best
                else:
                    return current_best
        
        return self.get_general(head,fruits,his_snake)

    def get_best_knife(self,fruits, his_snake,my_options):
        head = self.body_position[0]
        if len(his_snake)>6:
            for i in his_snake[4:int(len(his_snake)*0.80)]:
                current_best = i
                if not self.bad_next([], fruits, self.get_direction(current_best)):
                    return current_best        
        else:
            the_min = min(option["value"] for option in my_options)
            return self.get_best_plain(the_min, my_options,fruits,his_snake)
        the_min = min(option["value"] for option in my_options)
        return self.get_best_plain(the_min,head,fruits,his_snake)
    
    def get_best_king(self,fruits, his_snake,my_options):
        head = self.body_position[0]
        if len(his_snake)>6:
            for i in his_snake[4:int(len(his_snake)*0.80)]:
                current_best = i
                dir = self.get_direction(current_best)
                next = []
                if dir == Direction.LEFT:
                    next = [current_best[0]+1,current_best[1]]
                elif dir == Direction.RIGHT:
                    next = [current_best[0]-1,current_best[1]]
                elif dir == Direction.UP:
                    next = [current_best[0],current_best[1]-1]
                elif dir == Direction.DOWN:
                    next = [current_best[0],current_best[1]+1]

                if (next[0],next[1]) not in self.border_cells:
                    return current_best        
        else:
            return self.get_best_knife(fruits,his_snake,my_options)
        
        return self.get_best_knife(fruits,his_snake,my_options)

    def closest(self, kind, fruits):
        my_snake = self.body_position
        head = my_snake[0]
        best = [-1, -1]
        distance = self.MAX_DISTANCE
        f = 0

        for fruit in fruits:
            dis = abs(head[0]-fruit.pos[0]) + abs(head[1]-fruit.pos[1])
            if fruit.kind['name'] == kind and (dis < distance):
                distance = dis
                best = fruit.pos
                f = fruit

        return best, distance, f

    def get_best(self, fruits, snakes):
        head = self.body_position[0]
        shield = self.shield
        knife = self.knife
        king = self.king

        his_snake = []
        snakes = snakes

        for snake in snakes:
            if snake != self:
                for cell in snake.body_position:
                    his_snake.append(cell)

        my_options = []
        if not king:
            close_king = {"place": self.closest(
                'KING', fruits), "name": 'KING'}
            close_king["value"] = close_king["place"][1]
            if close_king["place"][1] != self.MAX_DISTANCE :
                if ((abs(head[0]-close_king["place"][0][0]) + abs(head[1]-close_king["place"][0][0]))<=close_king["place"][2].kind["lifespan"]):
                    my_options.append(close_king)
        if not shield:
            close_shield = {"place": self.closest(
                'SHIELD', fruits), "name": 'SHIELD'}
            close_shield["value"] = close_shield["place"][1]*2
            if close_shield["place"][1] != self.MAX_DISTANCE:
                if ((abs(head[0]-close_shield["place"][0][0]) + abs(head[1]-close_shield["place"][0][0]))<=close_shield["place"][2].kind["lifespan"]):
                    my_options.append(close_shield)
        if not knife:
            close_knife = {"place": self.closest(
                'KNIFE', fruits), "name": 'KNIFE'}
            if len(his_snake)>10:
                close_knife["value"] = close_knife["place"][1]*2.5
            else:
                close_knife["value"] = close_knife["place"][1]*2.3
            if close_knife["place"][1] != self.MAX_DISTANCE:
                if (abs(head[0]-close_knife["place"][0][0]) + abs(head[1]-close_knife["place"][0][0])) <= close_knife["place"][2].kind["lifespan"]:
                    my_options.append(close_knife)

        close_strawberry = {"place": self.closest(
            'STRAWBERRY', fruits), "name": 'STRAWBERRY'}
        close_dragon_fruit = {"place": self.closest(
            'DRAGON_FRUIT', fruits), "name": 'DRAGON_FRUIT'}

        close_strawberry["value"] = close_strawberry["place"][1]*4
        close_dragon_fruit["value"] = close_dragon_fruit["place"][1]*3

        if close_strawberry["place"][1] != self.MAX_DISTANCE:
            my_options.append(close_strawberry)
        if close_dragon_fruit["place"][1] != self.MAX_DISTANCE:
            my_options.append(close_dragon_fruit)

        the_min = min(option["value"] for option in my_options)
        if his_snake == []:
            return self.get_general(fruits,his_snake)
        elif not king and not knife and not shield:
            return self.get_best_plain(the_min,my_options,fruits,his_snake)
        elif king:
            return self.get_best_king(fruits,his_snake, my_options)
        elif knife:
            return self.get_best_knife(fruits,his_snake, my_options)
        else:
            return self.get_general(fruits,his_snake)


    def make_decision(self, board_state):

        try:
            fruits = board_state["fruits"]
            snakes = board_state["snakes"]

            best = self.get_best(fruits, snakes)
            direction = self.get_direction(best)
        except:
            pass
        

        return direction
