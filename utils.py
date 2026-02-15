from typing import Tuple, List, Optional, Dict
import heapq

class Node:

    def __init__(self, position: Tuple[int, int], parent: Optional['Node'] = None, cost: float = 0):
        self.position = position
        self.parent = parent
        self.cost = cost
        self.depth = 0 if parent is None else parent.depth + 1

    def __lt__(self, other):
        return self.cost < other.cost

class PriorityQueue:

    def __init__(self):
        self.elements = []
        self.count = 0
    def empty(self) -> bool: return len(self.elements) == 0
    def put(self, item: Node, priority: float):
        heapq.heappush(self.elements, (priority, self.count, item))
        self.count += 1
    def get(self) -> Node: return heapq.heappop(self.elements)[2]

def get_neighbors(pos: Tuple[int, int], rows: int, cols: int) -> List[Tuple[int, int]]:

    r, c = pos

    dirs = [(-1, 0), (0, 1), (1, 0), (1, 1), (0, -1), (-1, -1)]
    neighbors = []
    for dr, dc in dirs:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            neighbors.append((nr, nc))
    return neighbors

def calculate_movement_cost(p1: Tuple[int, int], p2: Tuple[int, int]) -> float:

    return 1.414 if abs(p1[0] - p2[0]) == 1 and abs(p1[1] - p2[1]) == 1 else 1.0

def reconstruct_path(came_from: Dict, curr: Tuple[int, int], start: Tuple[int, int]) -> List[Tuple[int, int]]:

    path = [curr]
    while curr != start:
        curr = came_from[curr]
        path.append(curr)
    return path[::-1]