#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 10:12:22 2024

@author: mazilui+ChatGPT
"""

import numpy as np
import random
import matplotlib.pyplot as plt

def monte_carlo_simulation(grid_size, alpha, beta, gamma, steps):
    # Initialize the grid (0 = empty, 1 = occupied)
    grid = np.zeros((grid_size, grid_size), dtype=int)
    
    # List to store the overall occupation of the grid at each step
    occupation_history = []

    # Function to get the sum of neighbors
    def sum_of_neighbors(i, j):
        neighbors = [
            grid[i-1, j] if i > 0 else 0,  # up
            grid[i+1, j] if i < grid_size-1 else 0,  # down
            grid[i, j-1] if j > 0 else 0,  # left
            grid[i, j+1] if j < grid_size-1 else 0   # right
        ]
        return sum(neighbors)

    # Perform the Monte Carlo steps
    for step in range(steps):
        # Loop through each site in the grid
        for i in range(grid_size):
            for j in range(grid_size):
                occupied_neighbors = sum_of_neighbors(i, j)
                
                if grid[i, j] == 0:  # If site is empty
                    # Compute attachment probability
                    attach_prob = alpha * (beta ** occupied_neighbors)
                    if random.random() < attach_prob:
                        grid[i, j] = 1  # Attach particle

                elif grid[i, j] == 1:  # If site is occupied
                    # Compute detachment probability
                    if random.random() < gamma:
                        grid[i, j] = 0  # Detach particle
        
        # Calculate the overall occupation of the grid at this step
        occupied_sites = np.sum(grid)
        total_sites = grid_size * grid_size
        occupation_fraction = occupied_sites / total_sites
        occupation_history.append(occupation_fraction)

    return grid, occupation_history

# Parameters
grid_size = 10  # Define the size of the grid (10x10 grid in this case)
alpha = 0.5     # Attachment probability constant
beta = 0.9      # Exponential attachment constant
gamma = 0.1     # Detachment probability
steps = 100     # Number of Monte Carlo steps

# Run the simulation
final_grid, occupation_history = monte_carlo_simulation(grid_size, alpha, beta, gamma, steps)

# Plot the overall occupation as a function of steps
plt.figure(figsize=(8, 6))
plt.plot(range(steps), occupation_history, label="Occupation Fraction")
plt.xlabel("Monte Carlo Steps")
plt.ylabel("Occupation Fraction")
plt.title("Occupation of the Grid Over Time")
plt.legend()
plt.grid(True)
plt.show()

# Output the final grid
print("Final grid after Monte Carlo simulation:")
print(final_grid)