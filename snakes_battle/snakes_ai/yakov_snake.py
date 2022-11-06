from fileinput import close
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

    def closest(self, kind, fruits):
        my_snake = self.body_position
        head = my_snake[0]
        best = [-1, -1]
        distance = self.MAX_DISTANCE
        the_fruit = 0

        for fruit in fruits:
            dis = abs(head[0]-fruit.pos[0]) + abs(head[1]-fruit.pos[1])
            if fruit.kind['name'] == kind and (dis < distance):
                distance = dis
                best = fruit.pos
                the_fruit = fruit

        return best, distance, the_fruit

    def find_not_die(self,head, fruits,his_snake):
        my_snake = self.body_position
        snakes = his_snake + my_snake
        bad_fruit_places = []
        for fruit in fruits:
            if fruit in FruitKind.harmful_fruits:
                bad_fruit_places.append(fruit.pos)

        if (head[0]+1,head[1]) not in self.border_cells:
            if [head[0]+1,head[1]] not in snakes:
                if [head[0]+1,head[1]] not in bad_fruit_places:
                    return [head[0]+1,head[1]]
                else:
                    for fruit in fruits:
                        if fruit.pos == [head[0]+1,head[1]] and fruit.kind['name']!='SKULL':
                            return [head[0]+1,head[1]]
     
        if (head[0]-1,head[1]) not in self.border_cells:
            if [head[0]-1,head[1]] not in snakes:
                if [head[0]-1,head[1]] not in bad_fruit_places:
                    return [head[0]-1,head[1]]
                else:
                    for fruit in fruits:
                        if fruit.pos == [head[0]-1,head[1]] and fruit.kind['name']!='SKULL':
                            return [head[0]-1,head[1]]

        if (head[0],head[1]-1) not in self.border_cells:
            if [head[0],head[1]-1] not in snakes:
                if [head[0],head[1]-1] not in bad_fruit_places:
                    return [head[0],head[1]-1]
                else:
                    for fruit in fruits:
                        if fruit.pos == [head[0],head[1]-1] and fruit.kind['name']!='SKULL':
                            return [head[0],head[1]-1]
        
        if (head[0],head[1]+1) not in self.border_cells:
            if [head[0],head[1]+1] not in snakes:
                if [head[0],head[1]+1] not in bad_fruit_places:
                    return [head[0],head[1]+1]
                else:
                    for fruit in fruits:
                        if fruit.pos == [head[0],head[1]+1] and fruit.kind['name']!='SKULL':
                            return [head[0],head[1]+1]

        if [head[0],head[1]+1] in his_snake[1:] or [head[0],head[1]+1] in my_snake[1:]:
            return [head[0],head[1]+1]
        elif [head[0],head[1]-1] in his_snake[1:] or [head[0],head[1]-1] in my_snake[1:]:
            return [head[0],head[1]-1]
        elif [head[0]-1,head[1]] in his_snake[1:] or [head[0]-1,head[1]] in my_snake[1:]:
            return [head[0]-1,head[1]]
        elif [head[0]+1,head[1]] in his_snake[1:] or [head[0]+1,head[1]] in my_snake[1:]:
            return [head[0]+1,head[1]]

        if len(my_snake)>len(his_snake) and his_snake!=[]:
            # move right
            if head[0]+1==his_snake[0][0] and head[1]==his_snake[0][1]+1:
                return [head[0]+1,head[1]]
            elif head[0]+1==his_snake[0][0] and head[1]==his_snake[0][1]-1:
                return [head[0]+1,head[1]]
            elif head[0]+1==his_snake[0][0]-1 and head[1]==his_snake[0][1]:
                return [head[0]+1,head[1]]

            # move down
            elif head[0]==his_snake[0][0] and head[1]+1==his_snake[0][1]-1:
                return [head[0],head[1]+1]
            elif head[0]==his_snake[0][0]+1 and head[1]+1==his_snake[0][1]:
                return [head[0],head[1]+1]
            elif head[0]==his_snake[0][0]-1 and head[1]+1==his_snake[0][1]:
                return [head[0],head[1]+1]

            # move left
            elif head[0]-1==his_snake[0][0] and head[1]==his_snake[0][1]-1:
                return [head[0]-1,head[1]]
            elif head[0]-1==his_snake[0][0] and head[1]==his_snake[0][1]+1:
                return [head[0]-1,head[1]]
            elif head[0]-1==his_snake[0][0]+1 and head[1]==his_snake[0][1]:
                return [head[0]-1,head[1]]

            # move up
            elif head[0]==his_snake[0][0]-1 and head[1]-1==his_snake[0][1]:
                return [head[0],head[1]-1]
            elif head[0]==his_snake[0][0]+1 and head[1]-1==his_snake[0][1]:
                return [head[0],head[1]-1]
            elif head[0]==his_snake[0][0] and head[1]-1==his_snake[0][1]+1:
                return [head[0],head[1]-1]
    

        return [head[0],head[1]+1]
                    
    def get_direction(self, close):
        head = self.body_position[0]

        if head[1] < close[1]:
            return Direction.DOWN

        elif head[1] > close[1]:
            return  Direction.UP

        else:
            if head[0] > close[0]:
                return Direction.LEFT

            elif head[0] < close[0]:
                return  Direction.RIGHT
 
        return 1

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
            next = [head[0], head[1]+1]

        for fruit in fruits:
            if fruit.kind in FruitKind.harmful_fruits:
                if next == fruit.pos:
                    return True

        for place in his_snake:
            if next == place:
                return True

        if his_snake !=[]:
            if [next[0]+1, next[1]] == his_snake[0] or [next[0]-1, next[1]] == his_snake[0] or [next[0], next[1]-1] == his_snake[0] or [next[0], next[1]+1] == his_snake[0]:
                return True

        if next in my_snake:
            return True

        if next[0]==0 or next[1]==0 or next[0]==40 or next[1]==40:
            return True

        if (next[0],next[1]) in self.border_cells:
            return True

        return False
        
    def get_for_single(self,fruits,his_snake):
        head = self.body_position[0]
        my_options = []

        best_strawberry = self.closest('STRAWBERRY', fruits)
        best_king = self.closest('KING', fruits)
        best_dragon_fruit  = self.closest('DRAGON_FRUIT', fruits)
        best_shield = self.closest('SHIELD', fruits)

        my_options.append(best_strawberry)
        my_options.append(best_king)
        my_options.append(best_dragon_fruit)
        if not self.shield:
            my_options.append(best_shield)

        best = [-1,-1]
        dis = self.MAX_DISTANCE
        for option in my_options:
            best = best
            if option[1]<dis:
                dis = option[1]
                best = option[0]

        if my_options==[] or self.bad_next(his_snake, fruits, self.get_direction(best)):
            return self.find_not_die(head,fruits,his_snake)

        return best
        
        
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
                        return self.get_for_single(fruits,his_snake)
                else:
                    return current_best
        return self.get_for_single(fruits,his_snake)

    def get_best_knife(self,fruits, his_snake,my_options):
        if len(his_snake)>10:
            for i in his_snake[4:int(len(his_snake)*0.80)]:
                current_best = i
                if not self.bad_next([his_snake[0]], fruits, self.get_direction(current_best)):
                    return current_best 
                elif i == int(len(his_snake)*0.80):
                    the_min = min(option["value"] for option in my_options)
                    return self.get_best_plain(the_min, my_options,fruits,his_snake)
        else:
            the_min = min(option["value"] for option in my_options)
            return self.get_best_plain(the_min, my_options,fruits,his_snake)

        the_min = min(option["value"] for option in my_options)
        return self.get_best_plain(the_min, my_options,fruits,his_snake)
    
    def get_best_king(self,fruits, his_snake,my_options):
        # when king sometimes goes out
        if len(his_snake)>6:
            for i in his_snake[4:int(len(his_snake)*0.80)]:
                current_best = i
                dir = self.get_direction(current_best)
                next = []
                if dir == Direction.LEFT:
                    next = [current_best[0]-1,current_best[1]]
                elif dir == Direction.RIGHT:
                    next = [current_best[0]+1,current_best[1]]
                elif dir == Direction.UP:
                    next = [current_best[0],current_best[1]-1]
                elif dir == Direction.DOWN:
                    next = [current_best[0],current_best[1]+1]

                if next != his_snake[0]:
                    if (next[0],next[1]) not in self.border_cells:
                        return current_best  
                    elif i == int(len(his_snake)*0.80):
                        return self.get_best_knife(fruits,[his_snake[0]],my_options)
                    elif self.bad_next([his_snake[0]], fruits, self.get_direction(current_best)):
                        if dir == Direction.LEFT:
                            return [current_best[0],current_best[1]+1]
                        elif dir == Direction.RIGHT:
                            next = [current_best[0],current_best[1]-1]
                        elif dir == Direction.UP:
                            next = [current_best[0]+1,current_best[1]]
                        elif dir == Direction.DOWN:
                            next = [current_best[0]-1,current_best[1]]
                else:
                    if dir == Direction.LEFT:
                            return [current_best[0],current_best[1]+1]
                    elif dir == Direction.RIGHT:
                        next = [current_best[0],current_best[1]-1]
                    elif dir == Direction.UP:
                        next = [current_best[0]+1,current_best[1]]
                    elif dir == Direction.DOWN:
                        next = [current_best[0]-1,current_best[1]]

                    if (next[0],next[1]) not in self.border_cells:
                        return current_best  
                    elif i == int(len(his_snake)*0.80):
                        return self.get_best_knife(fruits,[his_snake[0]],my_options)
        else:
            the_min = min(option["value"] for option in my_options)
            return self.get_best_plain(the_min, my_options,fruits,his_snake)  
        
        return self.get_best_knife(fruits,[his_snake[0]],my_options)

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
            close_king = {"place": self.closest('KING', fruits), "name": 'KING'}
            close_king["value"] = close_king["place"][1]
            if close_king["place"][1] != self.MAX_DISTANCE :
                if (abs(head[0]-close_king["place"][0][0]) + abs(head[1]-close_king["place"][0][1]))<=close_king["place"][2].lifespan:
                    my_options.append(close_king)
        if not shield:
            close_shield = {"place": self.closest('SHIELD', fruits), "name": 'SHIELD'}
            close_shield["value"] = close_shield["place"][1]*2
            if close_shield["place"][1] != self.MAX_DISTANCE:
                if (abs(head[0]-close_shield["place"][0][0]) + abs(head[1]-close_shield["place"][0][1]))<=close_shield["place"][2].lifespan:
                    my_options.append(close_shield)
        if not knife:
            close_knife = {"place": self.closest(
                'KNIFE', fruits), "name": 'KNIFE'}
            if len(his_snake)>10:
                close_knife["value"] = close_knife["place"][1]*2.6
            else:
                close_knife["value"] = close_knife["place"][1]*3.6
            if close_knife["place"][1] != self.MAX_DISTANCE:
                if (abs(head[0]-close_knife["place"][0][0]) + abs(head[1]-close_knife["place"][0][1])) <= close_knife["place"][2].lifespan:
                    my_options.append(close_knife)

        close_strawberry = {"place": self.closest('STRAWBERRY', fruits), "name": 'STRAWBERRY'}
        close_dragon_fruit = {"place": self.closest('DRAGON_FRUIT', fruits), "name": 'DRAGON_FRUIT'}

        close_strawberry["value"] = close_strawberry["place"][1]*3.2
        close_dragon_fruit["value"] = close_dragon_fruit["place"][1]*2.9


        if close_strawberry["place"][1] != self.MAX_DISTANCE:
            my_options.append(close_strawberry)
        if close_dragon_fruit["place"][1] != self.MAX_DISTANCE:
            my_options.append(close_dragon_fruit)

        the_min = min(option["value"] for option in my_options)
        if his_snake == []:
            return self.get_for_single(fruits,[])
        elif not king and not knife and not shield:
            return self.get_best_plain(the_min,my_options,fruits,his_snake)
        elif king:
            return self.get_best_king(fruits,his_snake, my_options)
        elif knife:
            return self.get_best_knife(fruits,his_snake, my_options)
        else:
            return self.get_best_plain(the_min,my_options,fruits,his_snake)


    def make_decision(self, board_state):
        direction = self.direction

        fruits = board_state["fruits"]
        snakes = board_state["snakes"]
        best = self.get_best(fruits, snakes)
        direction = self.get_direction(best)
        

        return direction
