"""

@kylel

"""

import json
import os
import pathlib

from papermage.magelib import Document
from papermage.recipes import CoreRecipe
from papermage.visualizers.visualizer import plot_entities_on_page

# load doc
recipe = CoreRecipe()
# pdfpath = pathlib.Path(__file__).parent.parent / "tests/fixtures/1903.10676.pdf"
# pdfpath = pathlib.Path(__file__).parent.parent / "tests/fixtures/2304.02623v1.pdf"
pdfpath = pathlib.Path(__file__).parent.parent / "tests/fixtures/2305.14772.pdf"
doc = recipe.from_pdf(pdf=pdfpath)

# visualize tokens
page_id = 0
plot_entities_on_page(page_image=doc.images[page_id], entities=doc.pages[page_id].tokens)

# visualize tables
page_id = 5
tables = doc.pages[page_id].intersect_by_box("tables")
plot_entities_on_page(page_image=doc.images[page_id], entities=tables)
for table in tables:
    print(table.text)

# visualize figures
figures = doc.pages[page_id].intersect_by_box("figures")
for figure in figures:
    print(figure.text)
plot_entities_on_page(page_image=doc.images[page_id], entities=figures)

# visualize blocks
blocks = doc.pages[page_id].intersect_by_box("blocks")
for block in blocks:
    print(block.text)
plot_entities_on_page(page_image=doc.images[page_id], entities=blocks)

# visualize sections
page_id = 4
sections = doc.pages[page_id].intersect_by_box("sections")
for section in sections:
    print(section.text)
plot_entities_on_page(page_image=doc.images[page_id], entities=sections)
