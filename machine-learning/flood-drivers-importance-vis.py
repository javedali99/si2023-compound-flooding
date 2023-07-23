"""
Flood Drivers Feature Importance Visualization

Author: Javed Ali (javed.ali@ucf.edu)
Date: July 23, 2023

Description: This script loads a dataset containing the relative importance of three flood drivers (Precipitation, Surge, and Discharge) at different gauge points. It then generates a pie chart for each gauge showing the relative importance of each flood driver. The pie charts are colored as follows: blue for Precipitation, red for Surge, and green for Discharge. By comparing the pie charts, one can understand how the importance of different flood drivers varies across different areas.

"""

# Required Libraries
import matplotlib.pyplot as plt
import pandas as pd

# Load the dataset
df = pd.read_csv("results/Combined_FeatureImportance_BestResult.csv")

# Create a figure with multiple subplots
# The layout is determined by the number of unique gauges
# The figure length has been adjusted to be shorter
# fig, axs = plt.subplots(nrows=(len(df) // 3) + 1, ncols=3, figsize=(20, len(df) // 3 * 5))
fig, axs = plt.subplots(nrows=7, ncols=3, figsize=(20, 35))  # Adjust the figure layout

# Flatten the axes array to easily iterate over it
axs = axs.flatten()

# Define lighter colors for the pie charts
# Light Blue for Precipitation, Light Red for Surge, and Light Green for Discharge
colors = ["#add8e6", "#ff7f7f", "#90ee90"]

# Create a pie chart for each unique gauge
for i, gauge in enumerate(df["Gauge "].unique()):
    # Subset the data for the current gauge
    df_gauge = df[df["Gauge "] == gauge]

    # Create a pie chart on the current subplot
    # autopct='%1.1f%%' is used to display the percentage on the pie chart
    axs[i].pie(
        df_gauge[["Precipitation_importance", "Surge_importance", "Discharge_importance"]].values[0],
        labels=["Precipitation", "Surge", "Discharge"],
        autopct="%1.1f%%",
        colors=colors,
        textprops={"fontsize": 14},  # increase the text size
    )

    # Set the title of the current subplot to the gauge number
    axs[i].set_title(f"Gauge {gauge}", fontweight="bold", fontsize=14)

# Remove extra subplots if the number of unique gauges is not a multiple of 3
for j in range(i + 1, len(axs)):
    fig.delaxes(axs[j])

# Adjust the layout to prevent overlapping
plt.tight_layout()

# Save the figure with high resolution
plt.savefig("figures/flood_drivers_pie_charts.png", dpi=300)

# Display the plot
plt.show()
