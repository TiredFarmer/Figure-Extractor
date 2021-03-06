import fitz
import io
from PIL import Image
from bounding_box import BoundingBox

def get_pdf_images(doc, final_name):
    images = []
    

    for i in range(doc.pageCount):
        page = doc[i]
        print("EXTRACTING PAGE", i)
        l = get_page_images(page, doc)
        if not l:
            continue
        for image in l:
            images.append(image)
    
    if len(images) <= 1:
        return

    images[0].save(f"pdf\{final_name}.pdf", save_all = True, append_images = images[1:])


def get_page_images(page, doc):
    """ return final cropped images within a page """
    final_boxes = []
    page_images = []
        
    pix = page.get_pixmap()
    page_image = Image.open(io.BytesIO(pix.tobytes()))
    initial_boxes = get_initial_boxes(page, doc, page_image.size)

    if not initial_boxes:
        return

    final_boxes.append(initial_boxes[0])

    initial_boxes.sort(key=lambda x : final_boxes[0].distance(x))

    for box_b in initial_boxes[1:]:
        for box_a in final_boxes:
            if box_a.is_valid(box_b):
                box_a.merge_boxes(box_b)
                break

        else:
            final_boxes.append(box_b)
    
    final_boxes = [b for b in final_boxes if b.area() >= 150]

    for box in final_boxes:
        text_boxes = get_text_boxes(page)
        box.CUTOFF = 40
        text_boxes = [b for b in text_boxes if box.is_valid(b)]

        for text_box in text_boxes:
            box.merge_boxes(text_box)
        
        img = page_image.crop((box.x0, box.y0, box.x1, box.y1))
        page_images.append(img)

    for box in final_boxes:
        page.draw_rect(fitz.Rect(box.x0, box.y0, box.x1, box.y1), color = [1,0,0,0], overlay=True, width = 1, fill_opacity=1)

    return page_images


def get_initial_boxes(page, doc, size):
    """ return all BoundaryBoxes of images, text, and drawings within a page """
    initial_boxes = []

    # loop through images in a page
    for item in page.get_images(full = True):
        rect = page.get_image_bbox(item)
        initial_boxes.append(BoundingBox(rect.x0, rect.y0, rect.x1, rect.y1, size))

    # loop through drawings in a page
    for p in page.get_drawings():
        for item in p["items"]:
            if item[0] == "l":
                x0 = min(item[1].x, item[2].x)
                y0 = min(item[1].y, item[2].y)
                x1 = max(item[1].x, item[2].x)
                y1 = max(item[1].y, item[2].y)

                initial_boxes.append(BoundingBox(x0, y0, x1, y1, size))

            if item[0] == "c":
                x0 = min(item[1].x, item[2].x, item[3].x, item[4].x)
                y0 = min(item[1].y, item[2].y, item[3].y, item[4].y)
                x1 = max(item[1].x, item[2].x, item[3].x, item[4].x)
                y1 = max(item[1].y, item[2].y, item[3].y, item[4].y)
            
                initial_boxes.append(BoundingBox(x0, y0, x1, y1, size))

    return initial_boxes

def get_text_boxes(page):
    bound_boxes = []
    # loop through paragraphs in a page
    for block in page.get_text("dict")["blocks"]:
        if block['type'] == 0: # block contains text
            rect = block['bbox']
            bound_boxes.append(BoundingBox(rect[0], rect[1], rect[2], rect[3], 0))
    
    return bound_boxes

def opener(file):
    return fitz.open(file)
