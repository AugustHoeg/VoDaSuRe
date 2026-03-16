from PIL import Image
import os

# Folder containing the JPG images
input_folder = "static/images/"

# Output file
output_file = "static/images/stitched.jpg"

# Get all jpg files and sort them
file_names = [
    "bamboo_v1.jpg",
    "cardboard_v1.jpg",
    "elm_v1.jpg",
    "larch_v1.jpg",
    "mdf_v1.jpg",
    "oak_v1.jpg",
    "cypress_v1.jpg",
    "ox-bone_1.jpg", 
    "vertebrae_v1.jpg",
    "femur_v1.jpg",
]

# Open images
images = [Image.open(os.path.join(input_folder, f)) for f in file_names]

# Calculate total width and max height
total_width = sum(img.width for img in images)
max_height = max(img.height for img in images)

# Create blank canvas
stitched_image = Image.new("RGB", (total_width, max_height))

# Paste images side-by-side
x_offset = 0
for img in images:
    stitched_image.paste(img, (x_offset, 0))
    x_offset += img.width

# Save result
stitched_image.save(output_file)

print(f"Saved stitched image as {output_file}")