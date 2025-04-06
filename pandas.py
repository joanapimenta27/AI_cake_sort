import os
import pandas as pd
import matplotlib.pyplot as plt

# Ensure the "results" directory exists and the CSV file is there.
csv_file_path = "results/bfs_metrics.csv"
if not os.path.exists(csv_file_path):
    print(f"CSV file '{csv_file_path}' not found. Please ensure the file exists.")
    exit(1)

# Read the CSV file into a pandas DataFrame.
df = pd.read_csv(csv_file_path)

# Print a preview of the data.
print("Data preview:")
print(df.head())

# Graph 1: Time Taken vs Algorithm Depth
plt.figure(figsize=(10, 6))
plt.scatter(df["Algorithm Depth"], df["Time Taken"], color="blue")
plt.title("Time Taken vs Algorithm Depth")
plt.xlabel("Algorithm Depth")
plt.ylabel("Time Taken (seconds)")
plt.grid(True)
plt.savefig("results/time_vs_depth.png")
plt.show()

# Graph 2: Nodes Visited vs Algorithm Depth
plt.figure(figsize=(10, 6))
plt.scatter(df["Algorithm Depth"], df["Nodes Visited"], color="green")
plt.title("Nodes Visited vs Algorithm Depth")
plt.xlabel("Algorithm Depth")
plt.ylabel("Nodes Visited")
plt.grid(True)
plt.savefig("results/nodes_vs_depth.png")
plt.show()

# Graph 3: Best Moves Count vs Algorithm Depth
plt.figure(figsize=(10, 6))
plt.scatter(df["Algorithm Depth"], df["Best Moves Count"], color="red")
plt.title("Best Moves Count vs Algorithm Depth")
plt.xlabel("Algorithm Depth")
plt.ylabel("Best Moves Count")
plt.grid(True)
plt.savefig("results/moves_vs_depth.png")
plt.show()

# Optional Graph 4: Plot all three metrics on one graph for comparison
plt.figure(figsize=(10, 6))
plt.plot(df["Algorithm Depth"], df["Time Taken"], label="Time Taken", marker="o")
plt.plot(df["Algorithm Depth"], df["Nodes Visited"], label="Nodes Visited", marker="x")
plt.plot(df["Algorithm Depth"], df["Best Moves Count"], label="Best Moves Count", marker="s")
plt.title("Metrics vs Algorithm Depth")
plt.xlabel("Algorithm Depth")
plt.ylabel("Metric Value")
plt.legend()
plt.grid(True)
plt.savefig("results/all_metrics_vs_depth.png")
plt.show()
