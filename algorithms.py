from collections import deque
from typing import Tuple, List, Set, Optional, Dict
from utils import Node, PriorityQueue, get_neighbors, calculate_movement_cost, reconstruct_path
from grid import Grid
import time

class SearchAlgorithms:

    def __init__(self, grid: Grid, step_delay: float = 0.05):
        self.grid = grid
        self.step_delay = step_delay
        self.algorithm_name = ""

    def _update_viz(self, title_suffix=""):

        if self.step_delay > 0:
            self.grid.visualize(
                title=f"{self.algorithm_name}{title_suffix}",
                step_delay=self.step_delay
            )

    def breadth_first_search(self) -> Optional[List[Tuple[int, int]]]:

        self.algorithm_name = "Breadth-First Search (BFS)"
        self.grid.reset_visualization()

        start, target = self.grid.start, self.grid.target
        queue = deque([Node(start)])
        visited = {start}
        came_from = {start: None}
        self.grid.frontier_nodes.add(start)

        while queue:
            current_node = queue.popleft()
            current_pos = current_node.position

            self.grid.current_node = current_pos
            self.grid.explored_nodes.add(current_pos)
            if current_pos in self.grid.frontier_nodes:
                self.grid.frontier_nodes.remove(current_pos)

            self._update_viz()

            if current_pos == target:
                path = reconstruct_path(came_from, target, start)
                self.grid.final_path = path
                self.grid.current_node = None
                self._update_viz(" - Path Found!")
                return path

            for neighbor_pos in get_neighbors(current_pos, self.grid.rows, self.grid.cols):
                if neighbor_pos not in visited and self.grid.is_valid(neighbor_pos):
                    visited.add(neighbor_pos)
                    came_from[neighbor_pos] = current_pos
                    queue.append(Node(neighbor_pos, current_node))
                    self.grid.frontier_nodes.add(neighbor_pos)
        return None

    def depth_first_search(self) -> Optional[List[Tuple[int, int]]]:

        self.algorithm_name = "Depth-First Search (DFS)"
        self.grid.reset_visualization()

        start, target = self.grid.start, self.grid.target
        stack = [Node(start)]
        visited = set()
        came_from = {start: None}
        self.grid.frontier_nodes.add(start)

        while stack:
            current_node = stack.pop()
            current_pos = current_node.position

            if current_pos in visited:
                continue
            visited.add(current_pos)

            self.grid.current_node = current_pos
            self.grid.explored_nodes.add(current_pos)
            if current_pos in self.grid.frontier_nodes:
                self.grid.frontier_nodes.remove(current_pos)

            self._update_viz()

            if current_pos == target:
                path = reconstruct_path(came_from, target, start)
                self.grid.final_path = path
                self.grid.current_node = None
                self._update_viz(" - Path Found!")
                return path

            neighbors = get_neighbors(current_pos, self.grid.rows, self.grid.cols)
            for neighbor_pos in reversed(neighbors):
                if neighbor_pos not in visited and self.grid.is_valid(neighbor_pos):
                    came_from[neighbor_pos] = current_pos
                    stack.append(Node(neighbor_pos, current_node))
                    self.grid.frontier_nodes.add(neighbor_pos)
        return None

    def uniform_cost_search(self) -> Optional[List[Tuple[int, int]]]:

        self.algorithm_name = "Uniform-Cost Search (UCS)"
        self.grid.reset_visualization()

        start, target = self.grid.start, self.grid.target
        pq = PriorityQueue()
        pq.put(Node(start, cost=0), 0)

        visited = set()
        came_from = {start: None}
        cost_so_far = {start: 0}
        self.grid.frontier_nodes.add(start)

        while not pq.empty():
            current_node = pq.get()
            current_pos = current_node.position

            if current_pos in visited:
                continue
            visited.add(current_pos)

            self.grid.current_node = current_pos
            self.grid.explored_nodes.add(current_pos)
            if current_pos in self.grid.frontier_nodes:
                self.grid.frontier_nodes.remove(current_pos)

            self._update_viz()

            if current_pos == target:
                path = reconstruct_path(came_from, target, start)
                self.grid.final_path = path
                self.grid.current_node = None
                self._update_viz(f" - Path Found! Cost: {cost_so_far[target]:.2f}")
                return path

            for n_pos in get_neighbors(current_pos, self.grid.rows, self.grid.cols):
                if self.grid.is_valid(n_pos):
                    new_cost = cost_so_far[current_pos] + calculate_movement_cost(current_pos, n_pos)
                    if n_pos not in cost_so_far or new_cost < cost_so_far[n_pos]:
                        cost_so_far[n_pos] = new_cost
                        came_from[n_pos] = current_pos
                        pq.put(Node(n_pos, current_node, new_cost), new_cost)
                        self.grid.frontier_nodes.add(n_pos)
        return None

    def depth_limited_search(self, limit: int = 15) -> Optional[List[Tuple[int, int]]]:

        self.algorithm_name = f"Depth-Limited Search (limit={limit})"
        self.grid.reset_visualization()
        return self._dls_helper(self.grid.start, limit, {self.grid.start: None}, set())

    def _dls_helper(self, curr, limit, came_from, visited) -> Optional[List[Tuple[int, int]]]:
        self.grid.current_node = curr
        self.grid.explored_nodes.add(curr)
        if curr in self.grid.frontier_nodes:
            self.grid.frontier_nodes.remove(curr)
        self._update_viz()

        if curr == self.grid.target:
            path = reconstruct_path(came_from, self.grid.target, self.grid.start)
            self.grid.final_path = path
            self.grid.current_node = None
            self._update_viz(" - Path Found!")
            return path

        if limit <= 0:
            return None

        visited.add(curr)
        neighbors = get_neighbors(curr, self.grid.rows, self.grid.cols)
        for n in neighbors:
            if n not in visited and self.grid.is_valid(n):
                self.grid.frontier_nodes.add(n)

        for n in neighbors:
            if n not in visited and self.grid.is_valid(n):
                came_from[n] = curr
                result = self._dls_helper(n, limit - 1, came_from, visited)
                if result:
                    return result
        visited.remove(curr)
        return None

    def iterative_deepening_dfs(self, max_depth: int = 25) -> Optional[List[Tuple[int, int]]]:

        self.algorithm_name = "Iterative Deepening DFS (IDDFS)"
        for depth in range(max_depth + 1):
            self.grid.reset_visualization()
            result = self._dls_helper(self.grid.start, depth, {self.grid.start: None}, set())
            if result:
                return result
        return None

    def bidirectional_search(self) -> Optional[List[Tuple[int, int]]]:

        self.algorithm_name = "Bidirectional Search"
        self.grid.reset_visualization()

        start, target = self.grid.start, self.grid.target
        f_queue, b_queue = deque([start]), deque([target])
        f_visited, b_visited = {start: None}, {target: None}
        self.grid.frontier_nodes.add(start)
        self.grid.frontier_nodes.add(target)

        while f_queue and b_queue:

            curr_f = f_queue.popleft()
            self.grid.current_node = curr_f
            self.grid.explored_nodes.add(curr_f)
            self._update_viz(" (Forward Step)")
            if curr_f in b_visited:
                return self._join_bi_path(f_visited, b_visited, curr_f)
            for n in get_neighbors(curr_f, self.grid.rows, self.grid.cols):
                if n not in f_visited and self.grid.is_valid(n):
                    f_visited[n] = curr_f
                    f_queue.append(n)
                    self.grid.frontier_nodes.add(n)

            curr_b = b_queue.popleft()
            self.grid.current_node = curr_b
            self.grid.explored_nodes.add(curr_b)
            self._update_viz(" (Backward Step)")
            if curr_b in f_visited:
                return self._join_bi_path(f_visited, b_visited, curr_b)
            for n in get_neighbors(curr_b, self.grid.rows, self.grid.cols):
                if n not in b_visited and self.grid.is_valid(n):
                    b_visited[n] = curr_b
                    b_queue.append(n)
                    self.grid.frontier_nodes.add(n)
        return None

    def _join_bi_path(self, f_map, b_map, join_node):
        path_f = []
        curr = join_node
        while curr is not None:
            path_f.append(curr)
            curr = f_map[curr]
        path_f.reverse()

        path_b = []
        curr = b_map[join_node]
        while curr is not None:
            path_b.append(curr)
            curr = b_map[curr]

        full = path_f + path_b
        self.grid.final_path = full
        self.grid.current_node = None
        self._update_viz(" - Path Found!")
        return full