# Description: Combine all storm event figures into one figure
# Author: Javed Ali (javed.ali@ucf.edu)
# Date: July 19, 2023

# Import libraries
import matplotlib.pyplot as plt
from PIL import Image

# List of image paths
images = [
    "figures/CFE results/Hurricane Arthur_discharge.png",
    "figures/CFE results/Hurricane Dorian_discharge.png",
    "figures/CFE results/Hurricane Hanna_discharge.png",
    "figures/CFE results/Hurricane Irene_discharge.png",
    "figures/CFE results/Hurricane Sandy_discharge.png",
    "figures/CFE results/Tropical Storm Barry_discharge.png",
    "figures/CFE results/Tropical Storm Jose_discharge.png",
    "figures/CFE results/Tropical Storm Ogla_discharge.png",
    "figures/CFE results/Tropical Storm Philippe_discharge.png",
]

# Open images and resize if needed
imgs = [Image.open(i) for i in images]

# Assume all images have the same size as the first one
width, height = imgs[0].size

# Create an empty image with appropriate size to place the smaller images
final_img = Image.new("RGB", (3 * width, 3 * height))

# Iterate over the smaller images and paste them into the final image
for i, img in enumerate(imgs):
    final_img.paste(img, ((i % 3) * width, (i // 3) * height))

# Save the final image
final_img.save("all_storm_events_discharge_final.png", dpi=(400, 400))

# Show the final image
plt.imshow(final_img)
