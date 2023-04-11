import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.animation import FuncAnimation

from math import ceil, sqrt

from Grid import Grid
from utils import EngineStatistics, vis_stats_cells, vis_stats_density

# Colormap for visualization
colors = [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 0, 1)]
cmap = mcolors.ListedColormap(colors)


class Engine():
    """Class to execute the simulation (singleton)
       Starting from an initial state, the class will run the simulation generation after generation and save the entire history of board state.
    """

    def __init__(self, init_grid: Grid, generations: int):
        """Class constructor

        Args:
            init_grid (Grid): The initial state of the simulation (2d tile array)
            generations (int): number of generations to run in the simulation.
        """
        self.history = [init_grid]
        self.generations = generations
        self.curr_gen = 0
        self.stats = EngineStatistics(
            num_generations=generations, area=init_grid.get_area())
        # init_grid.visualize_potential_matrix()

    def run(self):
        """Run the simulation, main entry function.
        """
        for i in range(self.generations):
            # Append the next generation to the result history array
            self.history.append(self.history[-1].next_gen())

            self.stats.update(gen=i, stats=self.history[-1].get_stats())
            self.curr_gen += 1

        self.stats.update_clustering_coef(
            coef=self.history[-1].calc_clustering_coef())

    def get_stats(self) -> EngineStatistics:
        return self.stats

    def visualize_potential(self, gen: int = 0):
        self.history[gen].visualize_potential_matrix()

    def visualize(self):
        """ Build a plot showing all of the generations in the simulation."""
        dim = ceil(sqrt(self.generations))
        if dim == 0:  # verify input
            return None
        ROWS, COLS = (dim, dim)
        fig, ax = plt.subplots(nrows=ROWS, ncols=COLS, figsize=(30, 30))

        # Display the initial state in the first subplot
        colors = [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 0, 1)]
        cmap = mcolors.ListedColormap(colors)

        x = 0
        y = 0

        # Using a manual for loop here to make sure we only iterate up to last generation.
        # generations <(ceil(sqrt(generations)))^2 => generations <= plt size
        for g in range(self.generations):
            mat = self.history[x+y*COLS].to_matrix()
            im = ax[y][x].imshow(mat, cmap=cmap, vmin=0, vmax=3)
            fig.set_facecolor('white')
            ax[y][x].axis('off')
            ax[y][x].set_title(f'Generation {x+y*COLS}')

            x += 1
            if x == COLS:
                x = 0
                y += 1

        plt.show()

    def generate_animation_in_html(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        # assuming your list of matrices is called 'matrix_list'
        # images = [ for grid in self.history]

        def update(frame):
            mat = self.history[frame].to_matrix()
            img = ax.imshow(mat, cmap=cmap, vmin=0, vmax=3)
            # images[frame].set_data(mat)
            ax.set_title(f"Generation {frame}")
            return img,

        ani = FuncAnimation(fig, update, frames=self.generations, interval=1, blit=True)
        ani.save("../data/test4.mp4", writer='ffmpeg', fps=27)
        
        return ani.to_jshtml()


    def visualize_final_result(self):
        plt.imshow(self.history[-1].to_matrix(), cmap=cmap, vmin=0, vmax=3)

    def save_results(self):
        # SAVING IMAGES:
        colors = [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 0, 1)]
        cmap = mcolors.ListedColormap(colors)
        # image resolution
        dpi = 96

        # For each year:
        for gen in range(self.generations):

            # Turn interactive plotting off
            plt.ioff()

            # initialize a figure
            fig = plt.figure(figsize=(680/dpi, 680/dpi), dpi=dpi)

            subsetData = self.history[gen].to_matrix()
            # plt.figimage(subsetData, cmap=cmap, vmin=0, vmax=3, resize=True)
            plt.imshow(subsetData, cmap=cmap, vmin=0,
                       vmax=3, extent=(0, 10, 0, 10))
            fig.set_facecolor('white')
            plt.axis('off')   # Replace fig.axis('off') with plt.axis('off')
            fig.tight_layout(pad=3)
            fig.suptitle(f'Generation {gen}', fontsize='x-large')

            # Save it & close the figure
            if gen < 10:
                filename = f'./images/sim{0}/Iteration0{gen}.png'
            else:
                filename = f'./images/sim{0}/Iteration{gen}.png'
            plt.savefig(fname=filename, dpi=96)
            plt.gca()
            plt.close(fig)

        return None

    def visualize_statistics(self):
        stats = self.stats
        vis_stats_cells(stats=stats)
        vis_stats_density(stats=stats, grid_area=stats.area)
        print(f"Clustering Coefficient: {round(stats.clustering_coef, 3)}")
