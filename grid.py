import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import random
from typing import Tuple, List, Set, Optional

class Grid:

    EMPTY = 0
    WALL = 1
    START = 2
    TARGET = 3

    def __init__(self, rows: int, cols: int, obstacle_density: float = 0.2):
        self.rows = rows
        self.cols = cols
        self.grid = np.zeros((rows, cols), dtype=int)
        self.start, self.target = None, None

        self.frontier_nodes = set()
        self.explored_nodes = set()
        self.current_node = None
        self.final_path = []
        self.fig, self.ax = None, None

        self._setup_grid(obstacle_density)

    def _setup_grid(self, density: float):

        for i in range(self.rows):
            for j in range(self.cols):
                if random.random() < density:
                    self.grid[i][j] = self.WALL

        empty = [(i, j) for i in range(self.rows) for j in range(self.cols) if self.grid[i][j] == self.EMPTY]
        if len(empty) < 2:
            self.grid.fill(self.EMPTY)
            empty = [(i, j) for i in range(self.rows) for j in range(self.cols)]

        self.start = random.choice(empty)
        empty.remove(self.start)
        self.target = random.choice(empty)

        self.grid[self.start], self.grid[self.target] = self.START, self.TARGET

    def is_valid(self, pos: Tuple[int, int]) -> bool:
        r, c = pos
        return 0 <= r < self.rows and 0 <= c < self.cols and self.grid[r][c] != self.WALL

    def reset_visualization(self):
        self.frontier_nodes.clear()
        self.explored_nodes.clear()
        self.current_node = None
        self.final_path = []

    def visualize(self, title: str = "AI Search", step_delay: float = 0.05):
        if self.fig is None or not plt.fignum_exists(self.fig.number):
            self.fig, self.ax = plt.subplots(figsize=(10, 8))
            plt.subplots_adjust(right=0.8)
        else:
            self.ax.clear()

        color_map = np.ones((self.rows, self.cols, 3)) 

        for r in range(self.rows):
            for c in range(self.cols):
                pos = (r, c)
                if self.grid[r][c] == self.WALL:
                    color_map[r, c] = [0, 0, 0] 
                elif pos == self.start:
                    color_map[r, c] = [0, 1, 0] 
                elif pos == self.target:
                    color_map[r, c] = [1, 0, 0] 
                elif pos in self.final_path:
                    color_map[r, c] = [1, 1, 0] 
                elif pos == self.current_node:
                    color_map[r, c] = [1, 0.65, 0] 
                elif pos in self.frontier_nodes:
                    color_map[r, c] = [0.68, 0.85, 0.9] 
                elif pos in self.explored_nodes:
                    color_map[r, c] = [0.83, 0.83, 0.83] 

        self.ax.imshow(color_map, interpolation='nearest')
        self.ax.set_title(title, fontsize=14, fontweight='bold')
        self.ax.set_xticks(np.arange(-0.5, self.cols, 1), minor=True)
        self.ax.set_yticks(np.arange(-0.5, self.rows, 1), minor=True)
        self.ax.grid(which='minor', color='gray', linestyle='-', linewidth=0.5)
        self.ax.tick_params(which='both', size=0, labelsize=0)

        if self.start: self.ax.text(self.start[1], self.start[0], 'S', ha='center', va='center', color='white', fontweight='bold')
        if self.target: self.ax.text(self.target[1], self.target[0], 'T', ha='center', va='center', color='white', fontweight='bold')

        if self.final_path:
            pts = np.array(self.final_path)
            self.ax.plot(pts[:, 1], pts[:, 0], color='yellow', linewidth=3)

        legend = [
            mpatches.Patch(color='green', label='Start (S)'),
            mpatches.Patch(color='red', label='Target (T)'),
            mpatches.Patch(color='black', label='Wall'),
            mpatches.Patch(color='lightblue', label='Frontier'),
            mpatches.Patch(color='lightgray', label='Explored'),
            mpatches.Patch(color='orange', label='Current'),
            mpatches.Patch(color='yellow', label='Final Path')
        ]
        self.ax.legend(handles=legend, loc='center left', bbox_to_anchor=(1, 0.5))

        plt.draw()
        if step_delay > 0:
            plt.pause(step_delay)