"""
Author: Javed Ali
Email: javed.ali@ucf.edu
Date: June 12, 2023
Description: This script merges output CSV files from different catchments in a watershed into a single DataFrame and 
creates a plot of the river discharge data over time. If there are 10 or more catchments, the plot shows 
the average, minimum, and maximum discharges across all catchments, as well as the discharges from the 
top 10 catchments with the highest and lowest maximum discharges. If there are fewer than 10 catchments, 
the discharges from all catchments are plotted.
"""

# Importing required libraries
import pandas as pd
import matplotlib.pyplot as plt
import os
import re
from tqdm.notebook import tqdm

def get_catchment_id(filename):
    """
    Extracts catchment ID from the given filename.

    Args:
    filename : str : Name of the file.

    Returns:
    str : Catchment ID prefixed by 'catch-', suffixed by '-discharge', or None if no match.
    """
    match = re.search(r'nex-(\d+)_output.csv', filename)
    return 'catch-' + match.group(1) + '-discharge' if match else None

def combine_csvs(csv_files):
    """
    Combine all the CSV files into a single dataframe.

    Args:
    csv_files : list : List of CSV file names to be combined.

    Returns:
    DataFrame : Combined DataFrame of all CSV files.
    """
    all_data = pd.DataFrame()
    for file in tqdm(csv_files):
        df = pd.read_csv(file, header=None, names=['index', 'time', 'river_discharge'])
        df = df.drop(columns=['index'])
        catchment_id = get_catchment_id(file)
        df = df.rename(columns={'river_discharge': catchment_id})
        if all_data.empty:
            all_data = df
        else:
            all_data = pd.merge(all_data, df, on='time', how='outer')
    
    return all_data

def plot_data(df, wb_id, storm_name):
    """
    Plot the merged data from all CSV files.

    Args:
    df : DataFrame : Merged DataFrame of all CSV files.
    wb_id : str : ID of the watershed.
    storm_name : str : Name of the storm.
    """
    df['time'] = pd.to_datetime(df['time'])
    discharge_cols = [col for col in df.columns if 'discharge' in col.lower()]
    df['average'] = df[discharge_cols].mean(axis=1)
    df['minimum'] = df[discharge_cols].min(axis=1)
    df['maximum'] = df[discharge_cols].max(axis=1)

    max_values = df[discharge_cols].max()
    if len(discharge_cols) >= 10:
        top_max = max_values.nlargest(10).index.tolist()
        top_min = max_values.nsmallest(10).index.tolist()
    else:
        top_max = max_values.nlargest(len(discharge_cols)).index.tolist()
        top_min = max_values.nsmallest(len(discharge_cols)).index.tolist()
    
    subset_cols = top_max + top_min

    fig, ax = plt.subplots(figsize=(15, 7))
    special_lines = {'average': 'black', 'minimum': 'blue', 'maximum': 'red'}
    for line, color in special_lines.items():
        ax.plot(df['time'], df[line], label=line, linewidth=2, linestyle='--', color=color)

    for col in subset_cols:
        ax.plot(df['time'], df[col], label=col.replace('-discharge', ''), color='lightgray')

    ax.set_title(f'Discharge in Watershed {wb_id} in NYC (Tropical Storm {storm_name})', fontsize=18, y=1.03)
    ax.set_xlabel('Time', fontsize=12)
    ax.set_ylabel('Discharge', fontsize=12)

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    handles, labels = ax.get_legend_handles_labels()
    h_special = [handles.pop(labels.index(l)) for l in special_lines]
    l_special = [labels.pop(labels.index(l)) for l in special_lines]
    h_discharge = handles
    l_discharge = labels

    legend_discharge = ax.legend(h_discharge, l_discharge, loc='upper left', bbox_to_anchor=(0.10, 0.8), title='Catchments', ncol=2)
    ax.add_artist(legend_discharge)

    for line, color in special_lines.items():
        value = df[line].iat[-1]
        pos = df['time'].iat[-1]
        ax.annotate(f'{line.capitalize()}: {value:.2f}', xy=(pos, value), xycoords='data', color=color, xytext=(-15, 10), 
                    textcoords='offset points', arrowprops=dict(arrowstyle="->", color=color))

    fig.savefig(f"../{wb_id}_discharge_{storm_name}.png", dpi=400, bbox_inches='tight')
    plt.show()

# Directory of CSV files
dir_path = "Tropical Storm Barry/wb-694856/outputs"
os.chdir(dir_path)

# List of CSV files
csv_files = [f for f in os.listdir() if f.endswith('.csv') and f.startswith('nex')]

# Combine all CSV files into one DataFrame
merged_data = combine_csvs(csv_files)
merged_data.to_csv(f'../wb-694856_merged_output.csv', index=False)

# Plot the combined data
plot_data(merged_data, wb_id="wb-694856", storm_name="Barry")
