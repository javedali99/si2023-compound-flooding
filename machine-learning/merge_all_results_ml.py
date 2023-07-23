"""
Merging ML Results CSV Files

Author: Javed Ali (javed.ali@ucf.edu)
Date: July 23, 2023

Description: This script merges the results of three ML algorithms (MLP, RF, SVM) into a single 
CSV file. The resulting file includes a new column specifying the algorithm used.
"""

# Import necessary libraries
import os

import pandas as pd


# Define a function to load a CSV file and add a new column for the ML algorithm
def load_data(file_name, ml_algo):
    # Load the CSV file
    df = pd.read_csv(file_name)
    # Add a new column for the ML algorithm
    df["Algorithm"] = ml_algo
    return df


# Define the directory where the CSV files are located
results_dir = "results"

# Load the CSV files
df_mlp = load_data(os.path.join(results_dir, "FeatureImportance_MLP_BestResult.csv"), "MLP")
df_rf = load_data(os.path.join(results_dir, "FeatureImportance_RF_BestResult.csv"), "RF")
df_svm = load_data(os.path.join(results_dir, "FeatureImportance_SVM_BestResult.csv"), "SVM")

# Concatenate the dataframes
df_combined = pd.concat([df_mlp, df_rf, df_svm], ignore_index=True)

# Save the combined dataframe to a new CSV file in the same directory
df_combined.to_csv(os.path.join(results_dir, "Combined_FeatureImportance_BestResult.csv"), index=False)
