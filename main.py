import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from grid import Grid
from algorithms import SearchAlgorithms
import sys

def main():
    print("\n--- AI Pathfinder: Uninformed Search ---")

    try:
        rows = int(input("Rows (10-30, default 15): ") or 15)
        cols = int(input("Cols (10-30, default 15): ") or 15)
        density = float(input("Walls density (0-0.5, default 0.2): ") or 0.2)
        delay = float(input("Visualization delay (default 0.05): ") or 0.05)
    except:
        rows, cols, density, delay = 15, 15, 0.2, 0.05

    grid = Grid(rows, cols, density)
    search = SearchAlgorithms(grid, delay)

    while True:
        print("\nSelect Algorithm:")
        print("1. Breadth-First Search (BFS)")
        print("2. Depth-First Search (DFS)")
        print("3. Uniform-Cost Search (UCS)")
        print("4. Depth-Limited Search (DLS)")
        print("5. Iterative Deepening DFS (IDDFS)")
        print("6. Bidirectional Search")
        print("0. Exit")

        try:
            choice = int(input("\nChoice: "))
        except: continue

        if choice == 0: break

        if choice == 1: search.breadth_first_search()
        elif choice == 2: search.depth_first_search()
        elif choice == 3: search.uniform_cost_search()
        elif choice == 4:
            limit = int(input("Depth Limit: ") or 15)
            search.depth_limited_search(limit)
        elif choice == 5:
            max_d = int(input("Max Depth: ") or 25)
            search.iterative_deepening_dfs(max_d)
        elif choice == 6: search.bidirectional_search()

        input("\nPress Enter to return to menu...")

if __name__ == "__main__":
    main()