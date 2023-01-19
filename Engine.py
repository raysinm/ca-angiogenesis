import matplotlib.pyplot as plt
from Grid import Grid


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