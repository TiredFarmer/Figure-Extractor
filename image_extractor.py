# STEP 1
# import libraries
import fitz
import io
from PIL import Image

def get_pdf_images(doc, final_name):
    images = []

    for i in range(doc.pageCount):
        for item in doc.getPageImageList(i):
            pix = fitz.Pixmap(doc, item[0])  # pixmap from the image xref
            pix0 = fitz.Pixmap(fitz.csRGB, pix)  # force into RGB
            data = pix0.getImageData()
            img = Image.open(io.BytesIO(data))
            images.append(img)
    
    images[0].save(f"pdf\{final_name}.pdf", save_all = True, append_images = images[1:])

def opener(file):
    return fitz.open(file)

# if __name__ == "__main__":
  
#     file = "raw_pdfs/bio_book.pdf"
#     pdf_file = fitz.open(file)
#     get_pdf_images(pdf_file)