# AI Pathfinder - Uninformed Search Visualization

A visualization tool for six fundamental uninformed search algorithms in a static grid environment.

## Features

- **6 Search Algorithms**: BFS, DFS, UCS, DLS, IDDFS, and Bidirectional Search
- **Real-time Visualization**: Watch algorithms explore the grid step-by-step
- **Static Environment**: Grid with fixed walls navigation
- **Interactive GUI**: Built with Matplotlib for clear visualization
- **Visual Feedback**: Distinguish between frontier nodes, explored nodes, and the final path.

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Dependencies

Install required packages:

```bash
pip install matplotlib numpy
```

## Usage

Run the main application:

```bash
python main.py
```

### GUI Controls

The application will present a menu to select:
1. Search algorithm (BFS, DFS, UCS, DLS, IDDFS, Bidirectional)
2. Grid size (Rows/Cols)
3. Obstacle density
4. Visualization delay (animation speed)

### Grid Legend

- **Green (S)**: Start point
- **Red (T)**: Target point
- **Black**: Static walls
- **Light Blue**: Frontier nodes (in queue/stack)
- **Light Gray**: Explored nodes
- **Yellow**: Final path
- **Orange**: Current node being expanded

## Algorithm Details

### 1. Breadth-First Search (BFS)
- Explores level by level
- Guarantees shortest path in unweighted grids
- Uses queue (FIFO)

### 2. Depth-First Search (DFS)
- Explores as deep as possible before backtracking
- Uses stack (LIFO)
- Does not guarantee shortest path

### 3. Uniform-Cost Search (UCS)
- Explores nodes in order of path cost
- Uses priority queue
- Guarantees optimal path based on movement costs (Diagonals cost more)

### 4. Depth-Limited Search (DLS)
- DFS with a specified depth limit
- Prevents infinite loops

### 5. Iterative Deepening DFS (IDDFS)
- Combines benefits of BFS and DFS
- Gradually increases depth limit
- Memory efficient with completeness guarantee

### 6. Bidirectional Search
- Searches from both start and goal simultaneously
- Significantly reduces search space by meeting in the middle

## Movement Rules

When expanding nodes, the algorithm follows a specific **Clockwise order** including only the **Main Diagonal**:
1. Up
2. Right
3. Bottom
4. Bottom-Right (Diagonal)
5. Left
6. Top-Left (Diagonal)

*Note: Top-Right and Bottom-Left diagonals are not checked, following the strict 6-direction movement requirement.*

## Project Structure

```
.
├── main.py                 # Main application entry point
├── algorithms.py           # Search algorithm implementations
├── grid.py                # Grid environment and visualization
├── utils.py               # Helper functions and data structures
├── README.md              # Project documentation
└── requirements.txt       # Python dependencies
```

## Author

Created by Ajmal Razaq (23F-0524) and Rania Shoaib (23F-0650)