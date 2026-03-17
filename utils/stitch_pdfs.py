import fitz
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)  # go up one folder

out_filename = "model_comparison_v1_vodasure_only"
input_folder = os.path.join(PROJECT_ROOT, "static", "pdfs")
output_file = os.path.join(PROJECT_ROOT, "static", "pdfs", out_filename + ".pdf")

orientation = "vertical"
save_as_image = True
image_format = "png" # or "jpg"

#file_names = [
#    "Ablation_input_ablation_input_27_256_website.pdf",
#    "Ablation_input_ablation_input_18_256_website.pdf",
#]

file_names = [
    #"CTSpine1K_img_idx_[72]_128.pdf",
    #"LIDC-IDRI_img_idx_[72]_128.pdf",
    "VoDaSuRe_DOWN_img_idx_[45]_128.pdf",
    "VoDaSuRe_img_idx_[45]_128.pdf",
    "VoDaSuRe_DOWN_img_idx_[63]_128.pdf",
    "VoDaSuRe_img_idx_[63]_128.pdf",
]

files = [os.path.join(input_folder, f) for f in file_names]

docs = []
sizes = []

# Load first page of each pdf
for f in files:
    doc = fitz.open(f)
    page = doc.load_page(0)
    rect = page.rect
    docs.append((doc, page))
    sizes.append((rect.width, rect.height))


# Compute final canvas size
if orientation == "horizontal":
    total_width = sum(w for w, h in sizes)
    total_height = max(h for w, h in sizes)
else:
    total_width = max(w for w, h in sizes)
    total_height = sum(h for w, h in sizes)


# Create output PDF
out = fitz.open()
new_page = out.new_page(width=total_width, height=total_height)


# Place pages
offset_x = 0
offset_y = 0

for (doc, page), (w, h) in zip(docs, sizes):

    if orientation == "horizontal":
        rect = fitz.Rect(offset_x, 0, offset_x + w, h)
        offset_x += w
    else:
        rect = fitz.Rect(0, offset_y, w, offset_y + h)
        offset_y += h

    new_page.show_pdf_page(rect, doc, 0)


# Save result
out.save(output_file)
print(f"Saved stitched PDF as {output_file}")

# Option to save as image
if save_as_image:
    image_output_file = os.path.join(PROJECT_ROOT, "static", "images", f"{out_filename}.{image_format}")
    # Render the page to an image
    pix = new_page.get_pixmap(dpi=300) 
    pix.save(image_output_file)
    print(f"Saved stitched image as {image_output_file}")