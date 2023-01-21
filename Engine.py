import matplotlib.pyplot as plt
from Grid import Grid
from math import ceil, sqrt

class Engine():
    def __init__(self, init_grid: Grid, generations : int):
        self.history = [init_grid]
        self.generations = generations
        self.curr_gen = 0

    def run(self):
        for i in range(self.generations):
            self.history.append(self.history[-1].next_gen())

            self.curr_gen += 1
        
    def visualize(self):
        dim = ceil(sqrt(self.generations))
        ROWS, COLS =(dim, dim)
        fig, ax = plt.subplots(nrows=ROWS, ncols=COLS, figsize=(30,30))
    
        # Display the initial state in the first subplot
        for y in range(COLS):
            for x in range(ROWS):
                if (x+y*COLS > self.generations):
                    plt.show()         
                    return None

                ax[y][x].imshow(self.history[x+y*COLS].to_matrix(), cmap='tab10')
                ax[y][x].axis('off')
                ax[y][x].set_title(f'generation {x+y*COLS}')    
        
        plt.show()         
 
    def visualize_potential(self):
        dim = ceil(sqrt(self.generations))
        ROWS, COLS =(dim, dim)
        fig, ax = plt.subplots(nrows=ROWS, ncols=COLS, figsize=(30,30))
    
        # Display the initial state in the first subplot
        for y in range(COLS):
            for x in range(ROWS):
                if (x+y*COLS > self.generations):
                    plt.show()         
                    return None

                ax[y][x].imshow(self.history[x+y*COLS].get_potential_matrix(), cmap='viridis')
                ax[y][x].axis('off')
                ax[y][x].set_title(f'generation {x+y*COLS}')    
        
        plt.show() 