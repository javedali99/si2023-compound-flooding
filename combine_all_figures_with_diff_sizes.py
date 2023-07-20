"""
Description: This Python script combines multiple images of different sizes into a single image using the Python Imaging Library (PIL).

Author: Javed Ali (javed.ali@ucf.edu)

Date: July 20, 2023

"""

# Import libraries
import matplotlib.pyplot as plt
from PIL import Image

# List of image paths
images = [
    "max_gauge_8461490_storm_surge_everythingin1.png",
    "max_gauge_8465705_storm_surge_everythingin1.png",
    "max_gauge_8467150_storm_surge_everythingin1.png",
    "max_gauge_8510560_storm_surge_everythingin1.png",
    "max_gauge_8516945_storm_surge_everythingin1.png",
    "max_gauge_8518750_storm_surge_everythingin1.png",
]

# # Open images and get their sizes
# imgs = [Image.open(i) for i in images]
# sizes = [img.size for img in imgs]

# # Get maximum width and height
# max_width = max([size[0] for size in sizes])
# max_height = max([size[1] for size in sizes])

# # Resize all images to the same size
# imgs = [img.resize((max_width, max_height)) for img in imgs]

# # Create an empty image with appropriate size to place the smaller images
# # The color of the new image is set to white
# final_img = Image.new("RGB", (3 * max_width, 2 * max_height), "white")

# # Iterate over the smaller images and paste them into the final image
# for i, img in enumerate(imgs):
#     final_img.paste(img, ((i % 3) * max_width, (i // 3) * max_height))


# # Save the final image with a high DPI for better quality
# final_img.save("all_stations_irene_geoclaw.png", dpi=(2000, 2000))

# Show the final image
# plt.imshow(final_img)
# plt.axis("off")  # to hide axis
# plt.show()

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
final_img = Image.new("RGB", (3 * max_width, 2 * max_height), "white")

# Iterate over the smaller images and paste them into the final image
for i, img in enumerate(imgs):
    final_img.paste(img, ((i % 3) * max_width, (i // 3) * max_height))

# Save the final image with a high DPI for better quality
# Use a figure with large size to accommodate the labels
fig = plt.figure(figsize=(20, 10))
ax = fig.add_subplot(111)
ax.imshow(final_img)
ax.axis("off")  # to hide axis

plt.tight_layout()  # adjust layout to prevent clipping of labels
plt.savefig("all_stations_irene_geoclaw.svg", dpi=2000, bbox_inches="tight")

# Show the final image
plt.show()
