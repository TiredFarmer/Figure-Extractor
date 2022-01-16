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
            page_rects.append(rect)
            page.draw_rect(rect, color=[0,1,1,0], overlay=True,width=0.5,fill_opacity=1)

        # loop through paragraphs in a page
        for block in page.getText("dict")["blocks"]:
            if block['type'] == 0: # block contains text
                page.draw_rect(block['bbox'], color = [1,0,0,0], overlay=True, width = 0.5, fill_opacity=1)
        
        rects.append(page_rects)
        print(page_rects)
        pix = page.getPixmap()
        page_image = Image.open(io.BytesIO(pix.tobytes()))
        page_image.show()
        if i >= 4:
            break

    print(len(images))
    print(len(rects))
    print(rects)    
    images[0].save("raw_pdfs\extracted.pdf", save_all = True, append_images = images[1:])

  
file = "raw_pdfs\\tikz_demo.pdf"

pdf_file = fitz.open(file)

get_pdf_images(pdf_file)
