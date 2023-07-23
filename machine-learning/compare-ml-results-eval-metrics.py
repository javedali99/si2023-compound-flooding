"""
Comparing ML Results

Author: Javed Ali (javed.ali@ucf.edu)
Date: July 23, 2023

Description: This script loads the combined results of three ML algorithms (MLP, RF, SVM) and 
creates boxplots to compare the R-squared, RMSE, and KGE metrics. The plots are combined 
into a single figure and saved as a high-resolution PNG file.
"""

# Import necessary libraries
import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Define the directory where the CSV files are located
results_dir = "results"

# Define the directory where the figures will be saved
figures_dir = "figures"

# Load the combined results
df_combined = pd.read_csv(os.path.join(results_dir, "Combined_FeatureImportance_BestResult.csv"))


# Define a function to create a subplot for a given metric
def plot_metric(ax, metric, subplot_title):
    sns.boxplot(x="Algorithm", y=metric, data=df_combined, ax=ax)
    ax.set_title(subplot_title, fontweight="bold")
    ax.set_ylabel(metric, fontsize=14)
    ax.set_xlabel("")  # remove x-label for individual subplot
    ax.tick_params(axis="both", labelsize=14)  # increase tick label fontsize


# Create a figure with three subplots in a row
fig, ax = plt.subplots(1, 3, figsize=(18, 6))

# Create the subplots with subplot titles
plot_metric(ax[0], "R-squared", "(a) Coefficient of Determination (R-squared)")
plot_metric(ax[1], "RMSE", "(b) Root Mean Square Error (RMSE)")
plot_metric(ax[2], "KGE", "(c) Kling-Gupta Efficiency (KGE)")


# Adjust the layout and save the figure as a high-resolution PNG file
fig.tight_layout()
plt.savefig(os.path.join(figures_dir, "boxplot_comparison.png"), dpi=300)
plt.show()
