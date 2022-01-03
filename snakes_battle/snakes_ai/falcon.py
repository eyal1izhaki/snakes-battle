import random
from snakes_battle.snake import Snake, Direction
import sys


class unit:
    def __init__(self, string = " ", safe = True, fruit = False, snake = False, my_snake = False, bomb = False, head = False):
        if snake:
            if my_snake:
                string = "S"
            else: 
                string = 's'
        self.__str__ = string + " "
        self.safe = safe
        self.fruit = fruit 
        self.snake = snake
        self.my_snake = my_snake
        self.bomb = bomb
        self.head = head


class Falcon(Snake):
    def __init__(self, borders_cells, color, name) -> None:
        super().__init__(color, name)
        self.init(borders_cells)



    def init(self, borders_cells):
        # Your bot initializations will be here.
        self.allowed__version = 1.0
        # All the cells that are fill with borders. This variable will store a list of (x, y) pairs
        self.border_cells = borders_cells
        self.allowed__border_cells = borders_cells
        # print (self.allowed__border_cells[-1])
        self.max_height = self.allowed__border_cells[-1][1]
        self.max_width  = self.allowed__border_cells[-1][0]
        print (f"""
        max height:  {self.max_width}
        max width:   {self.max_height}
        
        """)
        # print (self.allowed__border_cells)
        self.count = 0 
    
    def make_decision(self, board_state):
        print ("new round \n\n\n")
        self.board_state = board_state
        self.count += 1



        



        # .... #
        # borad_state = {
        #   "snakes": [snake1, snake2, ...],            "snakes" contains a list of Snake objects.
        #   "fruits": [fruit1, fruit2, fruit3, ....]    "fruits" contains a list of Fruit objects.
        #

        
        # You need to make a decision based on the board state.
        self.fruits = board_state["fruits"]
        self.current_pos = super().allowed__body_position()

        # print ("making board")
        self.make_board(board_state)
        
        # marks all of the special fruits (if existing)
        self.mark_specials()
        
        
        # print ("added special stuff, runing through options")
        possible_moves = []
    
        # print ("running through possible directions")
        for d in self.possible_directions():
        #  [ Direction.RIGHT , Direction.UP, Direction.DOWN, Direction.LEFT]:
            
            print ("trying")
            print (d)
            # next_head = self.next_head_location(self.direction)
            if self.is_dangerous(self.next_head_location(d)):
                # print ("This is gonna be dangerous")
                pass
            else:
                
                # print ("we found a non-dangrous path, we will be going here")
                # print(self.next_head_location(self.direction))
                possible_moves.append(d)
        # print (possible_moves[0])
        # return possible_moves[0]

        return self.make_best_choice(possible_moves)

    def make_best_choice(self, possible_moves):
        print (f"These were the given safe moves {possible_moves}")
        t = self.target()
        print ("getting target ")
        try:
            x, y = t
            print("getting directions")
            recommended = self.moovit(y ,x)
            print (f"This is the target{t}")
            print (f"These were the given directions{recommended}")
            random.shuffle(recommended)
            random.shuffle(possible_moves)
            for i in recommended: 

                if i in possible_moves:
                    
                    return i
                else: 
                    pass 
            else: 
                pass
        except:
            print ("Couldn't unpack target")
            pass
        return possible_moves[0]


            
        pass

        # if pos[0][0] > fruits[0].pos[0]:
        #     if (self.direction == Direction.RIGHT):
        #         return Direction.UP
        #     else:
        #         return Direction.LEFT
        
        # if pos[0][0] < fruits[0].pos[0]:
        #     if (self.direction == Direction.LEFT):
        #         return Direction.UP
        #     else:
        #         return Direction.RIGHT
        
        # if pos[0][0] == fruits[0].pos[0]:

        #     if pos[0][1] < fruits[0].pos[1]:
        #         if (self.direction == Direction.UP):
        #             return Direction.RIGHT
        #         else:
        #             return Direction.DOWN

        #     if pos[0][1] > fruits[0].pos[1]:
        #         if (self.direction == Direction.DOWN):
        #             return Direction.RIGHT
        #         else:
        #             return Direction.UP


    

        super.allowed__change_direction(Direction.RIGHT)

        super.allowed__change_direction(Direction.UP)

        super.allowed__change_direction(Direction.DOWN)
    def best_and_closest(self):
        pass

    def moovit_eta(self, y, x):
        
        head = self.current_pos[0]
        # I dont' know 
        head = [head[1], head[0]]
        return abs(abs(y) - abs(head[0])) + abs(abs(x) - abs(head[1])    )
        

    def possible_directions(self):
        moves = [ Direction.RIGHT , Direction.UP, Direction.DOWN, Direction.LEFT]
        

        if self.direction == Direction.RIGHT:
            
            moves.remove(Direction.LEFT)
            return moves 

        elif self.direction == Direction.LEFT:
            moves.remove(Direction.RIGHT)
            return moves 

        if self.direction == Direction.UP:
            moves.remove(Direction.DOWN )
            return moves 

        elif self.direction == Direction.DOWN:
            moves.remove(Direction.UP)
            return moves 

        
    


    def make_board(self, board_state):
        self.board = create_board(self.max_height+1, self.max_width+1)
        for x,y in self.border_cells:
            # print (f"These are the border cells, x: {x} y:{y}")
            # print (f"x: {x} y:{y} max{self.max_width}{self.max_height}")
            self.board[y][x] = unit(string="+", safe=False)
        


    def mark_specials(self):

        for snake in self.board_state['snakes']:
            # print ("this is a snake")
            # snake.body_pos
            #add the snake head to the board
            # print (f"snake body position : {p[0]} {p[1]}")
            # self.board[p[0]][p[1]]  = unit(string='s', safe=False, snake = True, head = True)
            
            head = snake.body_pos[0]
            #I don't know 
            my_snake = False
            if head == self.current_pos[0]:
                my_snake = True

            head = [head[1], head[0]]
            has_knife = self.allowed__is_knife() or self.allowed__is_king()
            print (f"is knife: {self.allowed__is_knife()} is king: {self.allowed__is_king()}")
            

            for p in snake.body_pos:
                try: self.board[p[1]][p[0]]  = unit(safe=has_knife and not my_snake, snake = True, my_snake=my_snake)
                except: (f"snake body position : {p[1]} {p[0]}")

            # mark the area around the head
            for y in [head[0]-1, head[0] + 1]:
                for x in [head[1]-1, head[1] + 1]:
                    try: self.board[p[0]][p[1]]  = unit( safe=False, snake = True, my_snake=my_snake)
                    except: pass
            
            # if it's an enemy snake mark his neck
            if not my_snake:
                self.enemy_weak_spot = snake.body_pos[2]


        self.mark_self()


            # print ("added the snakes")
        # print ("finished running through the snakes")
        # print ("we created the snakes")
        
        for fruit in self.board_state['fruits']:
            # I don't know 
            pos = fruit.pos
            pos = [pos[1], pos[0]]
            
            try:

                if fruit.kind['name'] in ['KING','DRAGON_FRUIT', 'STRAWBERRY', 'SHIELD', 'KNIFE'] :
                    
                    self.board[pos[0]][pos[1]] = unit(string = "F", fruit = fruit.kind['name'], safe=True) 
                elif fruit.kind['name'] in ['BOMB', 'SKULL']:
                    
                    self.board[pos[0]][pos[1]] = unit(string = "X", fruit = fruit.kind['name'], safe=False) 
                # print ("added fruits to list")
            except:
                print ("crashed while adding fruits to list")

            # print ("we have entered the fruit position")
            # print (f"length of the board{len(self.board)}   With of the board {len(self.board[0])}  fruit position W: {pos[0]} H:{pos[1]}   Height: {self.max_height}  Width: {self.max_width}")
            
            
        
        print_matrix(self.board, self.count)
        # self.king   = False 
        # self.knife  = False 
        # self.shield = False 
        # self.fruit  = False 
        # self.dfruit = False

        # if self.direction == Direction.RIGHT:
        #     for fruit in self.fruits:
        pass 

    


    def next_head_location(self, direction):
        # print ("this is the upcoming position")
        # print (f"This is the direction {direction} ")
        # print ("this is where i am ")
        head = self.current_pos[0]
        # I dont' know 
        head = [head[1], head[0]]
        print (head)
        if direction == Direction.UP:
            return head[0]-1, head[1]  
        elif direction == Direction.DOWN:
            return head[0] + 1, head[1]  
        elif direction == Direction.RIGHT:
            return head[0], head[1] + 1  
        elif direction == Direction.LEFT:
            return head[0], head[1] - 1   


    def is_dangerous(self, loc):
        y,x = loc
        if not self.safe_test_scenario(y,x):
            return False
        else: pass
        # for snake in self.board['snakes']:
        # print(f"y: {y}  x: {x}")
        # if y >= self.max_height-1 or y <= 0+1 or x >= self.max_width-1 or x <= 0+1:
        #     print ("don't go there's a border")
        #     return True

        if self.board[y][x].safe:
            print ("safe")
            return False 
        else: 
            return True 
            
    def safe_test_scenario(self, y, x):
        return True
        matrix = []
        for row_n in range(len(self.board)):
            matrix.append([])
            for unit in self.board[row_n]:
                matrix[row_n].append(unit.safe)
        
    

    def next_move(self):
            
        pass 

    def space_is_opened(self):
        pass 
    
    def suicide_protocol(self):
        pass
    def mark_self(self):
        x , y = self.current_pos[0]
        self.board[y][x] = unit(string="O")
    
    def close_enemy_location(self):
        head_y,head_x = self.current_pos[0][1], self.current_pos[0][0]
        for y in [head_y+1, head_y-1]:
            for x in [head_x+1, head_x-1]:
                if self.board[y][x].snake and not self.board[y][x].my_snake:
                    return [x,y]
        return False

    def target(self):
        try:
                
            if self.allowed__is_king() or self.allowed__is_knife():
                print ("I'm going for a snake")
                close_snake = self.close_enemy_location()
                if close_snake:
                    print (f"Attacking {close_snake}!!!")
                    return close_snake
                return self.enemy_weak_spot()
            
        except:
            pass
        # print ("we are going to look for fruit")
        goods = []
        for fruit in self.board_state['fruits']:
            if fruit.kind['name'] in ['KING','DRAGON_FRUIT', 'STRAWBERRY', 'SHIELD', 'KNIFE'] :
                goods.append(fruit)
        fruits = []
        print ("This is the target")
        for i in goods:
            for food in ['KING', 'KNIFE', 'SHIELD', 'DRAGON_FRUIT', 'STRAWBERRY']:
                if i.kind['name'] == food:
                    if self.worth_it(i):
                        fruits.append({
                            'pos': i.pos,
                            'name': food,
                            'eta': self.moovit_eta(i.pos[1], i.pos[0])
                        })
                        
        current_goal = fruits[0]
        for i in fruits:
            if i['eta'] < current_goal['eta']:
                current_goal = i
        print(f"The target is: {current_goal}")
        return current_goal['pos']
            # if i.kind['name'] == 'KING':
            #     if self.worth_it(i):
            #         print ("KING")
            # elif i.kind['name'] == 'KNIFE':
            #     if self.worth_it(i):
            #         print ("KNIFE")
            #         return i.pos
            # elif i.kind['name'] == 'SHIELD':
            #     if self.worth_it(i):
            #         print ("SHIELD")
            #         return i.pos
            # elif i.kind['name'] == 'DRAGON_FRUIT':
            #     if self.worth_it(i):
            #         print ("DRAGON_FRUIT")
            #         return i.pos
            # elif i.kind['name'] == 'STRAWBERRY':
            #     if self.worth_it(i):
            #         print ("STRAWBERRY")
            #         return i.pos
        return 0,0
        # return 
    def worth_it(self, i):
        # calculates whether it's worth going for a fruit 
        
        if i.kind['lifespan'] < 0:
            return True
        if i.kind['lifespan'] > self.moovit_eta(i.pos[1], i.pos[0]) :
            return True
        else:
            
            return False

    def moovit(self, y ,x):
        head = self.current_pos[0]
        # I dont' know 
        head = [head[1], head[0]]
        ds = []
        if y < head[0]:
            print ("I need to go up")
            ds.append(Direction.UP)
        elif y > head[0]:
            ds.append(Direction.DOWN)
        else: pass

        if x < head[1]:
            ds.append(Direction.LEFT)
        elif x > head[1]:
            ds.append(Direction.RIGHT)
        else: pass
        return ds

            

def create_board(height, width):
    matrix = []
    for row in range(height):
        matrix.append([])
        for column in range(width):
            
            matrix[row].append( unit())
        
    return matrix


def get_char(val):
    return val.__str__
    


def print_matrix(matrix, c):
    return
    text = ""
    # text += str(len(matrix[0])) + '|'
    # text += str(len(matrix[1]))
    for i in range(10):
        text += str(i) + " "
    for i in range(10,len(matrix[0])):
        text += str(i) + ""
    for n, row in enumerate(matrix):
        text += "\n"
        for unit in row:
            
            text += get_char(unit)
        text += str(n)
        
    text += str(c)
    print (text)


# def recursion_check_safe(matrix, n, y ,x):
#     if n > 20:
#         return True
#     else:
#         temp = [x[:]for x in matrix]
#         temp[y][x] = False
#         for 
