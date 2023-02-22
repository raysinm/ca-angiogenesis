import matplotlib.pyplot as plt
from Grid import Grid
from math import ceil, sqrt

class Engine():
    def __init__(self, init_grid: Grid, generations : int):
        self.history = [init_grid]
        self.generations = generations
        self.curr_gen = 0
        init_grid.visualize_potential_matrix()


    def run(self):
        for i in range(self.generations):
            self.history.append(self.history[-1].next_gen())
            self.history[-1].visualize_potential_matrix()

            self.curr_gen += 1
        
    def visualize(self):
        dim = ceil(sqrt(self.generations))
        ROWS, COLS =(dim, dim)
        fig, ax = plt.subplots(nrows=ROWS, ncols=COLS, figsize=(30,30))
        # ax.set_facecolor('white')
        # Display the initial state in the first subplot
        import matplotlib.colors as mcolors
        colors = [(0,0,0), (1,0,0), (1,1,0), (0,0,1)]
        cmap = mcolors.ListedColormap(colors)

        # Use the colormap with imshow()
        for y in range(COLS):
            for x in range(ROWS):
                # print(self.history[x+y*COLS].to_matrix())
                if (x+y*COLS > self.generations):       #TODO: FIX This 
                    plt.show()         
                    return None
                # ax[x][y].imshow(self.history[x+y*COLS].to_matrix(), cmap='gray')
                # ax[x][y].axis('off')
                # ax[x][y].set_title(f'generation {x+y*COLS}')  
                mat = self.history[x+y*COLS].to_matrix()
                # print(mat)  
                # ax[y][x].imshow(mat, cmap='tab10')
                im = ax[y][x].imshow(mat, cmap=cmap, vmin=0, vmax=3)
                fig.set_facecolor('white')
                ax[y][x].axis('off')
                ax[y][x].set_title(f'generation {x+y*COLS}')    
        
        plt.show()         
        return None