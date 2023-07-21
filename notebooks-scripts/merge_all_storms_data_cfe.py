"""
Title: Merge River Discharge Data of Different Storm Events
Author: Javed Ali
Date: July 20, 2023

Description:
This script combines data from multiple CSV files corresponding to different storm events. 
Each file contains data related to a particular storm, with the storm's name embedded in the 
file name. The script extracts the storm name from each file name and adds it as a new column 
in the corresponding data table. All tables are then concatenated into a single dataframe, 
which is saved to a new CSV file, `merged_storm_data.csv`. This facilitates subsequent analysis 
by providing all data in a single, standardized format, with a clear indication of the storm 
associated with each data point.
"""

# Import necessary libraries
import os

import pandas as pd


# Function to extract storm name from filename
def extract_storm_name(filename):
    # Split the filename at the underscore, take the first part (the storm name),
    # then remove the file extension
    return os.path.splitext(filename)[0].split("_")[0]


# Directory where all CSV files are stored
directory = "data/CFE outputs/"

# Get a list of all CSV files in the directory that start with "Hurricane" or "Tropical"
csv_files = [
    os.path.join(directory, file)
    for file in os.listdir(directory)
    if file.endswith(".csv") and (file.startswith("Hurricane") or file.startswith("Tropical"))
]


# Empty list to store dataframes
dfs = []

# For each CSV file
for file in csv_files:
    # Read the file into a dataframe
    df = pd.read_csv(file)

    # Extract the storm name from the file name
    # os.path.basename(file) gets the filename without the directory
    storm_name = extract_storm_name(os.path.basename(file))

    # Add a new column to the dataframe with the storm name
    df["storm_name"] = storm_name

    # Add the dataframe to the list of dataframes
    dfs.append(df)

# Concatenate all dataframes in the list into one dataframe
# ignore_index=True reassigns row indices in the combined dataframe
final_df = pd.concat(dfs, ignore_index=True)

# Save the final dataframe to a new CSV file
# index=False prevents pandas from writing row indices
final_df.to_csv("data/cfe_merged_storm_data.csv", index=False)
