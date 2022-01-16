# STEP 1
# import libraries
from re import I
import fitz
import io
from PIL import Image
from BoundingBox import BoundingBox

def get_pdf_images(doc):
    images = []

    for i in range(doc.pageCount):
        page = doc[i]
        get_page_images(page, doc)
        if i >= 2:
            break



    # images[0].save("raw_pdfs\extracted.pdf", save_all = True, append_images = images[1:])


def get_page_images(page, doc):
    """ return final cropped images within a page """
    final_boxes = []
    initial_boxes = get_initial_boxes(page, doc)

    if not initial_boxes:
        return

    final_boxes.append(initial_boxes[0])

    initial_boxes.sort(key=lambda x : final_boxes[0].distance(x))

    for box_b in initial_boxes[1:]:
        print("EXECUTING LOOP")
        for box_a in final_boxes:
            if box_a.is_valid(box_b):
                box_a.merge_boxes(box_b)
                print("MERGED")
                break

        else:
            print("BOX ADDED TO FINAL_BOXES")
            final_boxes.append(box_b)

    
    print("FINAL BOXES:++++")

    final_boxes = [b for b in final_boxes if b.area() >= 150]
    for box in final_boxes:
        page.draw_rect(fitz.Rect(box.x0, box.y0, box.x1, box.y1), color = [1,0,0,0], overlay=True, width = 5, fill_opacity=1)
        print(box)
        print(box.area())
    
    pix = page.get_pixmap()
    page_image = Image.open(io.BytesIO(pix.tobytes()))
    page_image.show()

    # TODO loop through boxes, compare, merge/add to final

def get_initial_boxes(page, doc):
    """ return all BoundaryBoxes of images, text, and drawings within a page """
    initial_boxes = []

        # loop through images in a page
    for item in page.get_images(full = True):
        rect = page.get_image_bbox(item)
        initial_boxes.append(BoundingBox(rect.x0, rect.y0, rect.x1, rect.y1))

        # page.draw_rect(rect, color=[1,1,0,0], overlay=True,width=3,fill_opacity=1)
    
    # loop through drawings in a page
    for p in page.get_drawings():
        for item in p["items"]:
            if item[0] == "l":
                x0 = min(item[1].x, item[2].x)
                y0 = min(item[1].y, item[2].y)
                x1 = max(item[1].x, item[2].x)
                y1 = max(item[1].y, item[2].y)

                initial_boxes.append(BoundingBox(x0, y0, x1, y1))

                # page.draw_line(item[1], item[2], color = [0,1,0,0], overlay=True, width = 3)

            if item[0] == "c":
                x0 = min(item[1].x, item[2].x, item[3].x, item[4].x)
                y0 = min(item[1].y, item[2].y, item[3].y, item[4].y)
                x1 = max(item[1].x, item[2].x, item[3].x, item[4].x)
                y1 = max(item[1].y, item[2].y, item[3].y, item[4].y)
            
                initial_boxes.append(BoundingBox(x0, y0, x1, y1))

                # page.draw_bezier(item[1], item[2], item[3], item[4], color = [0,0,1,0], overlay=True, width = 3)

    for box in initial_boxes:
        print(box)
    return initial_boxes
  
file = "raw_pdfs\\bio_book.pdf"

# file = "raw_pdfs\\tikz_demo.pdf"

pdf_file = fitz.open(file)

get_pdf_images(pdf_file)
