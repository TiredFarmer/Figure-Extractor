# STEP 1
# import libraries
import fitz
import io
from PIL import Image

def get_pdf_images(doc):
    images = []

    for i in range(doc.pageCount):
        for item in doc.getPageImageList(i):
            pix = fitz.Pixmap(doc, item[0])  # pixmap from the image xref
            pix0 = fitz.Pixmap(fitz.csRGB, pix)  # force into RGB
            data = pix0.getImageData()
            img = Image.open(io.BytesIO(data))
            images.append(img)
    
    images[0].save("raw_pdfs\extracted.pdf", save_all = True, append_images = images[1:])

  
file = "raw_pdfs\Scott Freeman Kim Quillin Lizabeth Allison Michael Black Greg Podgorski Emily Taylor Jeff Carmichael Michael Harrington Joan C. Sharp - Biological Science, Third Canadian Edition, 3rd edition-Pearson  (1).pdf"

pdf_file = fitz.open(file)

get_pdf_images(pdf_file)
  