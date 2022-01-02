from snakes_battle.snake import Snake, Direction
import sys


class unit:
    def __init__(self, string = " ", safe = True, fruit = False, snake = False, my_snake = False, bomb = False, head = False):
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
            
            print ("tyring")
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
            # print (f"x: {x} y:{y} max{self.max_width}{self.max_height}")
            self.board[y][x] = unit(string="+", safe=False)
        


    def mark_specials(self):

        for snake in self.board_state['snakes']:
            # print ("this is a snake")
            # snake.body_pos
            #add the snake head to the board
            # print (f"snake body position : {p[0]} {p[1]}")
            # self.board[p[0]][p[1]]  = unit(string='s', safe=False, snake = True, head = True)
            

            for p in snake.body_pos:
                try: self.board[p[1]][p[0]]  = unit(string='s', safe=False, snake = True)
                except: (f"snake body position : {p[1]} {p[0]}")

            # mark the area around the head
            #I don't know 
            head = snake.body_pos[0]
            head = [head[1], head[0]]
            for y in [head[0]-1, head[0] + 1]:
                for x in [head[1]-1, head[1] + 1]:
                    try: self.board[p[0]][p[1]]  = unit(string='s', safe=False, snake = True)
                    except: pass

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
        # for snake in self.board['snakes']:
        print(f"y: {y}  x: {x}")
        # if y >= self.max_height-1 or y <= 0+1 or x >= self.max_width-1 or x <= 0+1:
        #     print ("don't go there's a border")
        #     return True

        if self.board[y][x].safe:
            print ("safe")
            return False 
        else: 
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

    def target(self):
        try:
                
            if self.allowed__is_king:
                return self.board_state['snakes'][0].body_pos[3]
            elif self.allowed__is_knife:
                return self.board_state['snakes'][0].body_pos[3]
        except:
            pass
        goods = []
        for fruit in self.board_state['fruits']:
            if fruit.kind['name'] in ['KING','DRAGON_FRUIT', 'STRAWBERRY', 'SHIELD', 'KNIFE'] :
                goods.append(fruit)
        for i in goods:
            if i.kind['name'] == 'KING':
                if self.worth_it(i):
                    return i.pos
            elif i.kind['name'] == 'KNIFE':
                if self.worth_it(i):
                    return i.pos
            elif i.kind['name'] == 'SHIELD':
                if self.worth_it(i):
                    return i.pos
            elif i.kind['name'] == 'DRAGON_FRUIT':
                if self.worth_it(i):
                    return i.pos
            elif i.kind['name'] == 'STRAWBERRY':
                if self.worth_it(i):
                    return i.pos
        return 0,0
        # return 
    def worth_it(self, i):
        # calculates whether it's worth going for a fruit 
        if (i.kind['lifespan']) > self.moovit_eta(i.pos[1], i.pos[0]):
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
    text = ""
    for row in matrix:
        text += "\n"
        for unit in row:
            
            text += get_char(unit)
    text += str(c)
    print (text)


