#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 11:04:08 2024

@author: mazilui and ChatGPT
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import label

# Monte Carlo Simulation Function
def monte_carlo_simulation(grid_size, alpha, beta, gamma, steps):
    # Initialize the grid (0 = empty, 1 = occupied)
    grid = np.zeros((grid_size, grid_size), dtype=int)
    
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
                    if np.random.random() < attach_prob:
                        grid[i, j] = 1  # Attach particle

                elif grid[i, j] == 1:  # If site is occupied
                    # Compute detachment probability
                    if np.random.random() < gamma:
                        grid[i, j] = 0  # Detach particle
        
    return grid

# Function to label clusters using connected component labeling
def label_clusters(grid):
    labeled_grid, num_clusters = label(grid)
    
    # Manual computation of cluster sizes
    unique_labels, counts = np.unique(labeled_grid, return_counts=True)
    print("Unique labels and counts:", list(zip(unique_labels, counts)))  # Debugging cluster counts

    cluster_sizes = counts[1:]  # Exclude background (label 0)
    print("Cluster sizes after excluding background:", cluster_sizes)  # Debugging
    
    return labeled_grid, cluster_sizes

# Function to visualize the grid
def visualize_grid(grid):
    plt.figure(figsize=(6, 6))
    plt.imshow(grid, cmap='gray', interpolation='nearest')
    plt.colorbar(label='Occupation (0 = empty, 1 = occupied)')
    plt.title("Final Occupation Grid")
    plt.show()

# Function to visualize labeled clusters
def visualize_labeled_clusters(labeled_grid):
    plt.figure(figsize=(6, 6))
    plt.imshow(labeled_grid, cmap='nipy_spectral', interpolation='nearest')
    plt.colorbar(label='Cluster Labels')
    plt.title("Labeled Clusters in the Grid")
    plt.show()

# Function to plot the histogram of clusters
def plot_cluster_histogram(cluster_sizes):
    # Check if there are any valid clusters to plot
    if len(cluster_sizes) == 0:
        print("No clusters found.")
        return

    # Plot histogram of cluster sizes with appropriate binning
    plt.figure(figsize=(8, 6))
    plt.hist(cluster_sizes, bins=range(1, max(cluster_sizes)+2), edgecolor='black', align='left')
    plt.xlabel("Cluster Size")
    plt.ylabel("Frequency")
    plt.title("Histogram of Cluster Sizes")
    plt.grid(True)
    plt.show()

# Parameters
grid_size = 10  # Define the size of the grid (10x10 grid in this case)
alpha = 0.1    # Attachment probability constant
beta = 0.8      # Exponential attachment constant
gamma = 0.1     # Detachment probability
steps = 100     # Number of Monte Carlo steps

# Run the simulation
final_grid = monte_carlo_simulation(grid_size, alpha, beta, gamma, steps)

# Visualize the final grid
visualize_grid(final_grid)

# Label clusters in the final grid
labeled_grid, cluster_sizes = label_clusters(final_grid)

# Visualize labeled clusters
visualize_labeled_clusters(labeled_grid)

# Plot histogram of cluster sizes
plot_cluster_histogram(cluster_sizes)

# Output the final grid, labeled clusters, and cluster sizes
print("Final grid after Monte Carlo simulation:")
print(final_grid)
print("Labeled grid of clusters:")
print(labeled_grid)
print("Cluster sizes:", cluster_sizes)