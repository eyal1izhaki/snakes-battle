from snakes_battle.snake import Snake, Direction
from snakes_battle.fruit import FruitKind
harmful_fruits = FruitKind.harmful_fruits
class ElitzSnake(Snake):
    def __init__(self, borders_cells, color, name) -> None:
        super().__init__(color, name)

        self.version = 1.0
        self.border_cells = borders_cells

    
    def make_decision(self, board_state):
        distance = 100000
        fruits = board_state["fruits"]
        pos = self.body_position
        # for item in fruits:
        #     if item.kind in FruitKind.harmful_fruits:
        #         distance.append(pow(2, 31)-1)
        #     else:
        #         distance.append([abs(item.pos[0] - pos[0][0]) + abs(item.pos[1] - pos[0][1]), fruits.indexOf(item)])


        for item in fruits:
            dic = abs(item.pos[0] - pos[0][0]) + abs(item.pos[1] - pos[0][1])
            # if dic < distance 
            # to_get = distance.append(abs(item.pos[0] - pos[0][0]) + abs(item.pos[1] - pos[0][1]))
            # if item.kind  not in FruitKind.harmful_fruits and item.kind in FruitKind.special_fruits and to_get < item.lifespan:
            #     continue
            if item.kind  in FruitKind.harmful_fruits:
                continue
            # elif item.kind in FruitKind.special_fruits and :
            #     pass
            else:
                the_fruit = item
                break
        # print(fruits[0].kind['name'])
        # print(the_fruit.pos , the_fruit.kind['name'])
        if pos[0][0] > the_fruit.pos[0]:
            if self._direction == Direction.RIGHT:
                return Direction.UP
            else:
                return Direction.LEFT
        
        if pos[0][0] < the_fruit.pos[0]:
            if self._direction == Direction.LEFT:
                return Direction.UP
            else:
                return Direction.RIGHT
        
        if pos[0][0] == the_fruit.pos[0]:

            if pos[0][1] < the_fruit.pos[1]:
                if self._direction == Direction.UP:
                    return Direction.RIGHT
                else:
                    return Direction.DOWN

            if pos[0][1] > the_fruit.pos[1]:
                if self._direction == Direction.DOWN:
                    return Direction.RIGHT
                else:
                    return Direction.UP
    
        return Direction.CONTINUE