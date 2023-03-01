import matplotlib.pyplot as plt
from Grid import Grid
from math import ceil, sqrt
from utils import EngineStatistics
class Engine():
    def __init__(self, init_grid: Grid, generations : int):
        self.history = [init_grid]
        self.generations = generations
        self.curr_gen = 0
        self.stats = EngineStatistics(num_generations=generations, area=init_grid.get_area())
        #init_grid.visualize_potential_matrix()


    def run(self):
        for i in range(self.generations):
            self.history.append(self.history[-1].next_gen())
            #self.history[-1].visualize_potential_matrix()
            self.stats.update(gen=i, stats=self.history[-1].get_stats()) 
            self.curr_gen += 1
        self.stats.update_clustering_coef(coef=self.history[-1].calc_clustering_coef())
    
    def get_stats(self) -> EngineStatistics :
        return self.stats


    def visualize(self):
        dim = ceil(sqrt(self.generations))
        if dim == 0:
            return None
        ROWS, COLS =(dim, dim)
        fig, ax = plt.subplots(nrows=ROWS, ncols=COLS, figsize=(30,30))
        # ax.set_facecolor('white')
        # Display the initial state in the first subplot
        import matplotlib.colors as mcolors
        colors = [(0,0,0), (1,0,0), (1,1,0), (0,0,1)]
        labels = ['Empty', 'Stalk', 'Tip', 'Attractor']

        cmap = mcolors.ListedColormap(colors)
        if dim == 1:
            mat = self.history[-1].to_matrix()
            im = ax.imshow(mat, cmap=cmap, vmin=0, vmax=3)
            fig.set_facecolor('white')
            ax.axis('off')
            ax.set_title(f'Generation {self.generations - 1}')
        else:
            for y in range(COLS):
                for x in range(ROWS):
                    # print(self.history[x+y*COLS].to_matrix())
                    if (x+y*COLS > self.generations):       #TODO: FIX This 
                        plt.show()         
                        return None
                
                    mat = self.history[x+y*COLS].to_matrix()
                    im = ax[y][x].imshow(mat, cmap=cmap, vmin=0, vmax=3)
                    fig.set_facecolor('white')
                    ax[y][x].axis('off')
                    ax[y][x].set_title(f'Generation {x+y*COLS}')    
        
        # import matplotlib.patches as mpatches
        # legend_patches = [mpatches.Patch(color=color, label=label) for color, label in zip(colors, labels)]
        # fig.legend(handles=legend_patches, loc='upper left', bbox_to_anchor=(0, 1))
        
        plt.show()        
        return None
    
    def visualize_few(self):
        dim = ceil(sqrt(self.generations))
        if dim == 0:
            return None
        gens = range(0,101,20)
        ROWS, COLS =(1, len(gens))
        fig, ax = plt.subplots(nrows=1, ncols=COLS, figsize=(30,30))
        # ax.set_facecolor('white')
        # Display the initial state in the first subplot
        import matplotlib.colors as mcolors
        colors = [(0,0,0), (1,0,0), (1,1,0), (0,0,1)]
        labels = ['Empty', 'Stalk', 'Tip', 'Attractor']

        cmap = mcolors.ListedColormap(colors)
        if dim == 1:
            mat = self.history[-1].to_matrix()
            im = ax.imshow(mat, cmap=cmap, vmin=0, vmax=3)
            fig.set_facecolor('white')
            ax.axis('off')
            ax.set_title(f'Generation {self.generations - 1}')
        else:
            for y,gen in enumerate(gens):
                mat = self.history[gen].to_matrix()
                im = ax[y].imshow(mat, cmap=cmap, vmin=0, vmax=3)
                fig.set_facecolor('white')
                ax[y].axis('off')
                ax[y].set_title(f'Generation {gen}',fontsize='xx-large')    
             
        
        # import matplotlib.patches as mpatches
        # legend_patches = [mpatches.Patch(color=color, label=label) for color, label in zip(colors, labels)]
        # fig.legend(handles=legend_patches, loc='upper left', bbox_to_anchor=(0, 1))
        
        plt.show()        
        return None
    
    def save_results(self):
         ## SAVING IMAGES:
        import matplotlib.colors as mcolors
        colors = [(0,0,0), (1,0,0), (1,1,0), (0,0,1)]
        cmap = mcolors.ListedColormap(colors)
        # image resolution
        dpi=96

        # For each year:
        for gen in range(self.generations):
        
            # Turn interactive plotting off
            plt.ioff()

            # initialize a figure
            fig = plt.figure(figsize=(680/dpi, 680/dpi), dpi=dpi)
            
            subsetData = self.history[gen].to_matrix()
            # plt.figimage(subsetData, cmap=cmap, vmin=0, vmax=3, resize=True)
            plt.imshow(subsetData, cmap=cmap, vmin=0, vmax=3, extent=(0, 10, 0, 10))
            fig.set_facecolor('white')
            plt.axis('off')   # Replace fig.axis('off') with plt.axis('off')
            fig.tight_layout(pad=3)
            fig.suptitle(f'Generation {gen}', fontsize='x-large')      
                    
            # Save it & close the figure
            if gen<10:
                filename=f'./images/sim{0}/Iteration0{gen}.png'
            else:
                filename=f'./images/sim{0}/Iteration{gen}.png'
            plt.savefig(fname=filename, dpi=96)
            plt.gca()
            plt.close(fig)

        return None