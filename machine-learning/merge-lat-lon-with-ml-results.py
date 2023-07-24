"""
Comparing ML Results

Author: Javed Ali (javed.ali@ucf.edu)
Date: July 23, 2023

Description: This script loads the combined results of three ML algorithms (MLP, RF, SVM) and 
a file with gauge location data, merges them based on the gauge column.

"""

# Import necessary libraries
import os

import pandas as pd

# Define the directory where the CSV files are located
results_dir = "results"
location_dir = "data"


# Load the combined results
df_combined = pd.read_csv(os.path.join(results_dir, "Combined_FeatureImportance_BestResult.csv"))
# Remove trailing white spaces from column names
df_combined.columns = df_combined.columns.str.strip()

# Print column names of df_combined
print("Columns in df_combined: ", df_combined.columns)

# Load the gauge location data
df_location = pd.read_csv(os.path.join(location_dir, "Manhattan_points.csv"))
# Remove trailing white spaces from column names
df_location.columns = df_location.columns.str.strip()

# Print column names of df_location
print("Columns in df_location: ", df_location.columns)

# Merge the dataframes on the 'Gauge' column, retaining all rows from df_combined
df_combined = pd.merge(df_combined, df_location, on="Gauge", how="left")


# Save the merged dataframe to a new CSV file in the same directory
df_combined.to_csv(os.path.join(results_dir, "combined_ml_result_with_location.csv"), index=False)
