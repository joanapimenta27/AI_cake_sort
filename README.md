# AI Cake Sort Game

Cake Sort is a puzzle game developed in Python using Pygame. The game challenges you to sort cake slices by moving plates from a table onto a board. The project also showcases several search algorithms (DFS, BFS, Monte Carlo, Greedy, A*) used for AI decision-making.

## Features

- **Game Modes:**  
  - **Human Mode:** Manually select and place plates.  
  - **AI Mode:** Choose between different search algorithms to let the AI play the game.
- **Settings:**  
  - **Changeble Game Settings:** In the settings you can change all kinds of aspects of the game (board size, number of slices, algorithms used to calculate hints given, number of plates in table and even number of total cakes the game will have).  
- **Search Algorithms:**  
  - **Uninformed Search:** DFS and BFS  
  - **Informed Search:** Greedy and A*  
  - **Metaheuristic:** Monte Carlo Tree Search  
- **Dynamic Rendering:**  
  Custom renderers for the board, table, plates, and cake slices, with visual hints and overlays.
- **Performance Metrics:**  
  Logs metrics (e.g., time taken, nodes visited) to CSV files for further analysis.
- **Results Plotting:**  
  Use the provided plotting script (with pandas and matplotlib) to generate graphs from the logged metrics.

## Prerequisites

- **Python:** Version 3.10 or higher (tested with Python 3.10.12)  
- **Pygame:** Version 2.6.1 or compatible  
- **Pandas and Matplotlib:** For running the results plotting script

## Instructions
After opening the project in the respective directory just run:

``` python3 main.py``` 

and the game will open the initial menu.
