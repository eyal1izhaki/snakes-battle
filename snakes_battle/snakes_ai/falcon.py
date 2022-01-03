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
            
            if self.is_dangerous(self.next_head_location(d)):
                # print (f"{d} will not be added because our system detects that it's dangerous")
                pass
            else:
                print ("appearrantly it's safe")
                
                possible_moves.append(d)
        if not len(possible_moves) == 0:
            print (f"these are the moves {possible_moves}")

            return self.make_best_choice(possible_moves)
        else: 
            print ("we are in trouble")
            for d in self.possible_directions():
        
                
                print ("trying")
                print (d)
                
                if self.is_dangerous(self.next_head_location(d), trouble=True):
                    #danger
                    pass
                else:
                    print ("appearrantly it's somewhat safe")
                    possible_moves.append(d)
        if not len(possible_moves) == 0:
            print (f"these are the moves {possible_moves}")

            return self.make_best_choice(possible_moves)
        else: 
            print ("we are in trouble")
            for d in self.possible_directions():
        
                
                print ("trying")
                print (d)
                
                if self.is_dangerous(self.next_head_location(d), trouble=2):
                    #danger
                    pass
                else:
                    print ("appearrantly it's somewhat safe")
                    possible_moves.append(d)
            
            return self.make_best_choice(possible_moves)
    
    


    def make_best_choice(self, possible_moves):
        print (f"These were the given safe moves {possible_moves}")
        try: t = self.target()
        except:
            t = 10, 10
        # print ("getting target ")
        try:
            x, y = t
            # print("getting directions")
            recommended = self.moovit(y ,x)
            print (f"This is the target{t}")
            print (f"These were the given directions{recommended}")
            random.shuffle(recommended)
            random.shuffle(possible_moves)
            for i in recommended: 

                if i in possible_moves:
                    print (f"final move: {i}")
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
        has_knife = self.allowed__is_knife() or self.allowed__is_king()
        print (f"is knife: {self.allowed__is_knife()} is king: {self.allowed__is_king()}")
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
            
            
            
            for p in snake.body_pos:
                try: self.board[p[1]][p[0]]  = unit(safe=(has_knife and not my_snake), snake = True, my_snake=my_snake)
                except: print (f"snake body position : {p[1]} {p[0]}")

            # mark the area around the head
            for y in [head[0]-1, head[0] + 1]:
                for x in [head[1]-1, head[1] + 1]:
                    try: self.board[p[0]][p[1]]  = unit( safe=False, snake = False, my_snake=my_snake)
                    except: print ("coudln't mark head as dangerous")
            
            # if it's an enemy snake mark his neck
            if not my_snake:
                try: self.enemy_weak_spot = snake.body_pos[2]
                except: 
                    try: self.enemy_weak_spot = snake.body_pos[1]
                    except: 
                        try: self.enemy_weak_spot = snake.body_pos[0]
                        except: self.enemy_weak_spot = [random.randint(1,30), random.randint(1,30)]
            

        self.mark_self()


            # print ("added the snakes")
        # print ("finished running through the snakes")
        # print ("we created the snakes")
            
            
        
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


    def is_dangerous(self, loc, trouble = True):
        y,x = loc
        print (f"this is the head we are checking y{y} x{x}")
        if not self.board[y][x].safe:
            print ("this space isn't safe")
            if (not trouble) or self.board[y][x].snake:
                return True
            else: pass
        else: pass 
        if trouble == 2:
            return False

        print ("this space itself isn't dangerous, we're going to check whether the envionment itself is contained using safe_test_scenario")
        if not self.safe_test_scenario(y,x, trouble = trouble): #if this is not a safe scenario return True since it is dangerous

            print ("tested safe scenario and detected that this doesn't lead to a safe environment")
            return True
        else:
            print ("tested safe scenario") 
            pass
        # for snake in self.board['snakes']:
        # print(f"y: {y}  x: {x}")
        # if y >= self.max_height-1 or y <= 0+1 or x >= self.max_width-1 or x <= 0+1:
        #     print ("don't go there's a border")
        #     return True

        # if self.board[y][x].safe:
        #     print ("safe")
        #     print (self.board[y][x].safe)
        #     return False 
        # else: 
        #     print ("This space isn't safe")
        #     return True 
            
    def safe_test_scenario(self, y, x, trouble = False):
        # return True
        
        matrix = []
        for row_n in range(len(self.board)):
            matrix.append([])
            for unit in self.board[row_n]:
                if unit.safe and (not unit.snake):
                    matrix[row_n].append(True)
                else: matrix[row_n].append(False)
        # matrix[y][x] = False
        print (f"checking path from y{y} x{x}")
        try: return  check_safe_path_recursive(matrix, 0, y ,x)
        except:
            print ("couldn't check path")
            return True
        
    

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
        print ("i'm going to get my snakes location")
        head_x, head_y = self.current_pos[0]
        print (f"head closest to me, i am y{y} x{x}")
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
    # print (text)


def check_safe_path_recursive(matrix, path_length, y ,x): #if we have where to go from here (this place is already blocked)
    # if we got to a depth of 20
    # print ("recursion")
    # print (path_length)
    # print (f"checking path safety with original y {y} x {x}")
    if path_length > 20:
        # print ("path length is over 20")
        return True  
    else:
        if matrix[y][x]:
            matrix[y][x] = False
            for ny, nx in [
                [y-1, x], 
                [y+1, x], 
                [y, x-1],
                [y, x+1]
                        ]:
                
                
                
                if check_safe_path_recursive(matrix, path_length + 1 , ny, nx ):
                    # print (ny, nx)
                    return True 
                # If we decide not to go through this path, mark it as safe 
            
            matrix[y][x] = True 
            
        # print ("hazard ahead!")
        return False 

                
                
