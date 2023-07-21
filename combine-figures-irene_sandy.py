"""
Description: This Python script combines multiple images of different sizes into a single image using the Python Imaging Library (PIL).

Author: Javed Ali (javed.ali@ucf.edu)

Date: July 20, 2023

"""

# Import libraries
import os

import matplotlib.pyplot as plt
from PIL import Image

# List of storm names
storm_names = ["Hurricane Irene", "Hurricane Sandy"]

# Directory that includes storm folders
base_directory = "figures/GeoClaw results/"

# Station Names and IDs
station_names = ["The Battery", "Kings Point", "Montauk", "Bridgeport", "New Haven", "New London"]
station_ids = ["8518750", "8516945", "8510560", "8467150", "8465705", "8461490"]

# Create a dictionary that maps station IDs to station names
station_dict = dict(zip(station_ids, station_names))

# Iterate over each storm
for storm_name in storm_names:
    # Directory for current storm
    directory = os.path.join(base_directory, storm_name, "Max gauge")

    # Get a list of all PNG files in the storm's directory
    images = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith(".png")]

    # Create a list of titles for the images
    titles = [
        (chr(97 + i), station_dict[file.split("_")[2]])
        for i, file in enumerate([f for f in os.listdir(directory) if f.endswith(".png")])
    ]

    # Open images and get their sizes
    imgs = [Image.open(i) for i in images]
    sizes = [img.size for img in imgs]

    # Get maximum width and height
    max_width = max([size[0] for size in sizes])
    max_height = max([size[1] for size in sizes])

    # Resize all images to the same size
    imgs = [img.resize((max_width, max_height)) for img in imgs]

    # Create an empty image with appropriate size to place the smaller images
    # The color of the new image is set to white
    final_img = Image.new(
        "RGB", (3 * max_width, 2 * max_height + 50), "white"
    )  # add 50 pixels to the height for the space between rows

    # Iterate over the smaller images and paste them into the final image
    for i, img in enumerate(imgs):
        final_img.paste(
            img, ((i % 3) * max_width, (i // 3) * max_height + (50 if i >= 3 else 0))
        )  # shift the images in the second row down by 50 pixels

    # Create a figure with large size to accommodate the labels
    fig = plt.figure(figsize=(20, 12))  # increase the height to make room for the titles
    ax = fig.add_subplot(111)

    # Display the final image
    ax.imshow(final_img)
    ax.axis("off")  # to hide axis

    # Add titles to the images
    for i, (letter, title) in enumerate(titles):
        # Position the title above the corresponding image
        x = (i % 3) * 0.33 + 0.17
        y = 1 - (i // 3) * 0.52  # adjust the y values to place the titles in the space between rows
        ax.text(
            x, y, f"({letter}) {title}", transform=ax.transAxes, ha="center", va="bottom", weight="bold", fontsize=16
        )  # make the title bold

    plt.tight_layout()  # adjust layout to prevent clipping of labels

    # Save the figure in the base directory with the storm name in the filename
    plt.savefig(
        os.path.join(base_directory, f"{storm_name.replace(' ', '_')}_combined_biased.png"),
        dpi=400,
        bbox_inches="tight",
    )

    # Show the final image
    plt.show()
