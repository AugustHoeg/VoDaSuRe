import fitz
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)  # go up one folder

input_folder = os.path.join(PROJECT_ROOT, "static", "pdfs")
output_file = os.path.join(PROJECT_ROOT, "static", "pdfs", "examples_stitched.pdf")

orientation = "vertical"

file_names = [
    "Examples_1.pdf",
    "Examples_2.pdf",
    "Examples_4.pdf",
    "Examples_3.pdf",
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