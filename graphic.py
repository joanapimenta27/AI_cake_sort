import os
import pandas as pd
import matplotlib.pyplot as plt

# Define a mapping from algorithm name to CSV file path.
algorithm_files = {
    "A*": "results/a_star_metrics.csv",
    "BFS": "results/bfs_metrics.csv",
    "DFS": "results/dfs_metrics.csv",
    "Greedy": "results/greedy_metrics.csv",
    "MC": "results/mc_metrics.csv"
}

# Container to hold DataFrames.
dfs = []

# Read each CSV file into a DataFrame and add an "Algorithm" column.
for algo, filepath in algorithm_files.items():
    if not os.path.exists(filepath):
        print(f"CSV file '{filepath}' not found. Skipping {algo}.")
        continue
    df = pd.read_csv(filepath)
    df["Algorithm"] = algo  # tag each row with the algorithm name
    dfs.append(df)

# If no files were loaded, exit.
if not dfs:
    print("No CSV files loaded. Please check your file paths.")
    exit(1)

# Combine all DataFrames into one.
all_data = pd.concat(dfs, ignore_index=True)
print("Combined Data Preview:")
print(all_data.head())

# Create an output directory for plots if it doesn't exist.
os.makedirs("results", exist_ok=True)

# --- Graph 1: Score vs Algorithm Depth (if 'Score' exists) ---
if "Score" in all_data.columns:
    plt.figure(figsize=(10, 6))
    for algo, group in all_data.groupby("Algorithm"):
        plt.scatter(group["Algorithm Depth"], group["Score"], label=algo)
    plt.title("Score vs Algorithm Depth")
    plt.xlabel("Algorithm Depth")
    plt.ylabel("Score Obtained")
    plt.legend()
    plt.grid(True)
    plt.savefig("results/score_vs_depth.png")
    plt.show()
else:
    print("Column 'Score' not found in data. Skipping Score vs Depth plot.")

# --- Graph 2: Time Taken vs Algorithm Depth ---
if "Time Taken" in all_data.columns:
    plt.figure(figsize=(10, 6))
    for algo, group in all_data.groupby("Algorithm"):
        plt.scatter(group["Algorithm Depth"], group["Time Taken"], label=algo)
    plt.title("Time Taken vs Algorithm Depth")
    plt.xlabel("Algorithm Depth")
    plt.ylabel("Time Taken (seconds)")
    plt.legend()
    plt.grid(True)
    plt.savefig("results/time_vs_depth.png")
    plt.show()
else:
    print("Column 'Time Taken' not found. Skipping Time Taken plot.")

# --- Graph 3: Nodes Visited vs Algorithm Depth ---
if "Nodes Visited" in all_data.columns:
    plt.figure(figsize=(10, 6))
    for algo, group in all_data.groupby("Algorithm"):
        group["Algorithm Depth"] = pd.to_numeric(group["Algorithm Depth"], errors="coerce")
        group["Nodes Visited"] = pd.to_numeric(group["Nodes Visited"], errors="coerce")
        group = group.dropna(subset=["Algorithm Depth", "Nodes Visited"])
    
        plt.scatter(group["Algorithm Depth"], group["Nodes Visited"], label=algo)
    
    plt.title("Nodes Visited vs Algorithm Depth")
    plt.xlabel("Algorithm Depth")
    plt.ylabel("Nodes Visited")
    plt.legend()
    plt.grid(True)
    plt.savefig("results/nodes_vs_depth.png")
    plt.show()
else:
    print("Column 'Nodes Visited' not found. Skipping Nodes Visited plot.")

# --- Graph 4: Best Moves Count vs Algorithm Depth ---
if "Best Moves Count" in all_data.columns:
    plt.figure(figsize=(10, 6))
    for algo, group in all_data.groupby("Algorithm"):
        plt.scatter(group["Algorithm Depth"], group["Best Moves Count"], label=algo)
    plt.title("Best Moves Count vs Algorithm Depth")
    plt.xlabel("Algorithm Depth")
    plt.ylabel("Best Moves Count")
    plt.legend()
    plt.grid(True)
    plt.savefig("results/moves_vs_depth.png")
    plt.show()
else:
    print("Column 'Best Moves Count' not found. Skipping Best Moves Count plot.")

# --- Graph 5: Cakes Count vs Algorithm Depth (if useful) ---
if "Cakes Count" in all_data.columns:
    plt.figure(figsize=(10, 6))
    for algo, group in all_data.groupby("Algorithm"):
        plt.scatter(group["Algorithm Depth"], group["Cakes Count"], label=algo)
    plt.title("Cakes Count vs Algorithm Depth")
    plt.xlabel("Algorithm Depth")
    plt.ylabel("Cakes Count")
    plt.legend()
    plt.grid(True)
    plt.savefig("results/cakes_vs_depth.png")
    plt.show()
else:
    print("Column 'Cakes Count' not found. Skipping Cakes Count plot.")
