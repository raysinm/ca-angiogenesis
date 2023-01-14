from collections import namedtuple
from copy import deepcopy
import matplotlib.pyplot as plt
from enum import Enum
import numpy as np
Point = namedtuple('Point', 'x y')
class ActionType(Enum):
    KILL = 1
    DIVIDE = 2

ABSENT = -1
DEAD = 0
ALIVE = 1

class Cell:
    # def __init__(self, x: int, y: int, max_cycle: int):     #This is INIT 
    def __init__(self):     #This is INIT 
        self.status = ALIVE
        # self.p_propagate = 0.5
        # self.p_die = 0.5
        # self.cycle = 1
        # # self.x, self.y = (x,y)
        # self.max_cycle = max_cycle
    
    def next(self):
        if self.status != ALIVE: return (self.x, self.y)
        self.update_probs()
        if self.should_die():
            return self.die()

        self.cycle += 1
        self.update_p()

        if self.should_propagate():
            return self.propagate()
        else:
            return (self.x, self.y) #Not right
            
    def update_probs(self):
        '''Update probabilities of this cell to divide or to die'''
        if self.status == ALIVE:
            if self.cycle >= self.max_cycle:
                self.p_die = 1.0
            
    # def should_die(self):
    #         return False
    #     return True
    
    # def die(self):
    #     self.status = DEAD
    #     self.cycle = 0

    # def update_p(self):

    def is_alive(self):
        return self.status == ALIVE


        from collections import namedtuple
from copy import deepcopy
import matplotlib.pyplot as plt
from enum import Enum
Point = namedtuple('Point', 'x y')
class ActionType(Enum):
    KILL = 1
    DIVIDE = 2
    
#* Grid gives cell context, cell returns to grid the actions it wants to make
class GridContext():
    def __init__(self, alive_neighbors: int, dead_neighbors: int):
        self.alive_neighbors = alive_neighbors
        self.dead_neighbors = dead_neighbors
class CellContext():
    def __init__(self, radius_alive_neighbors: int, radius_dead_neighbors: int):
        self.radius_alive_neighbors = radius_alive_neighbors
        self.radius_dead_neighbors = radius_dead_neighbors
class Action():
    def __init__(self):
        self.src = self
        self.dst = self
        self.type = ActionType.KILL #for example   


class Grid: 
    def __init__(self, width: int, height: int, init_config):   #init_config: : Dict(str, List(Point) --type hinting
        self.height = height
        self.width = width
        # t = [ [0]*3 for i in range(3)]
        self.grid = [[None]*width for i in range(height)]
        self.init_grid_objects(init_config)
        self.src_grid = deepcopy(self.grid)
        print(self.grid)


    def init_grid_objects(self, init_config):
        for c in init_config['alive_cells']:
            self.grid[c.x][c.y] = Cell() 
        
        # .. More classes of cells supported T.B.D

    def next_gen(self):
        for x in range(self.height):
            for y in range(self.width):
                cell = self.grid[x][y]
                cell_context= cell.get_context()
                actions = cell.get_actions(self.generate_context(cell_context=cell_context, point=(x,y)))
                exec_cell_actions(actions=actions, point=(x,y))
        self.src_grid = deepcopy(self.grid)
        
    def generate_context(self, cell_context : CellContext, point: Point):
        pass

    def exec_cell_actions(self, actions : List(Action), point: Point):
        # TODO: 1. Implement and test get_context get_actions and generate_context and exec_actions functions. 2. Implement cell die()
        #TODO: add enum for ALIVE, DEAD
        for action in actions:
            if action.type == ActionType.KILL:
                self.grid[action.dst].die()     #* For example, TBD

    def to_matrix(self):
        output = np.zeros(shape=(self.height,self.width), dtype=int)
        for x in range(self.height):
            for y in range(self.width):
                gridcell = self.grid[x][y]
                if gridcell != None:
                    output[x][y] = int(gridcell.is_alive())
        return output
    

class Engine():
    def __init__(self, init_grid: Grid, generations : int):
        self.history = [init_grid]
        self.generations = generations
        self.curr_gen = 0

    def run(self):
        for i in range(self.generations):
            self.history.append(deepcopy(self.history[-1]))
            self.history[-1].next_gen()
            self.curr_gen += 1
        
    def visualize(self):
        ROWS, COLS =(6,6)
        fig, ax = plt.subplots(nrows=ROWS, ncols=COLS, figsize=(30,30))
    
        # Display the initial state in the first subplot
        for x in range(ROWS):
            for y in range(COLS):
                # print(self.history[x+y*COLS].to_matrix())
                ax[x][y].imshow(self.history[x+y*COLS].to_matrix(), cmap='gray')
                ax[x][y].axis('off')
                ax[x][y].set_title(f'generation {x+y*COLS}')
        
        plt.show()         
        return None


    