# STEP 1
# import libraries
import fitz
import io
from PIL import Image

# TODO what if no images?
def get_pdf_images(doc):
    images = []
    rects = []

    for i in range(doc.pageCount):
        page = doc[i]
        page_rects = []
        # loop through images in a page
        for item in page.get_images(full = True):
            pix = fitz.Pixmap(doc, item[0])  # pixmap from the image xref
            pix0 = fitz.Pixmap(fitz.csRGB, pix)  # force into RGB
            data = pix0.tobytes()
            img = Image.open(io.BytesIO(data))
            images.append(img)

            rect = page.get_image_bbox(item)
            print(rect)
            page_rects.append(rect)
            page.draw_rect(rect, color=[1,1,0,0], overlay=True,width=3,fill_opacity=1)

        # loop through paragraphs in a page
        for block in page.getText("dict")["blocks"]:
            if block['type'] == 0: # block contains text
                page.draw_rect(block['bbox'], color = [1,0,0,0], overlay=True, width = 0.5, fill_opacity=1)
        
        # loop through drawings in a page
        for p in page.getDrawings():
            for item in p["items"]:
                print(item)
                if item[0] == "l":
                    page.draw_line(item[1], item[2], color = [0,1,0,0], overlay=True, width = 3)
                if item[0] == "c":
                    page.draw_bezier(item[1], item[2], item[3], item[4], color = [0,0,1,0], overlay=True, width = 3)
                


        rects.append(page_rects)
        # print(page_rects)
        pix = page.get_pixmap()
        page_image = Image.open(io.BytesIO(pix.tobytes()))
        page_image.show()
        if i >= 0:
            break

    print(len(images))
    print(len(rects))
    print(rects)    
    images[0].save("raw_pdfs\extracted.pdf", save_all = True, append_images = images[1:])
  
# file = "raw_pdfs\\bio_book.pdf"
file = "raw_pdfs\\tikz_demo.pdf"

pdf_file = fitz.open(file)

get_pdf_images(pdf_file)
