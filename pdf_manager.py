from PyPDF2 import PdfFileReader, PdfFileWriter
from image_extractor import get_pdf_images, opener

PATH = "pdf/"

def split_pdf_get_images(pdf_name: str, start: int, end: int) -> None:

    pdf_in = PdfFileReader(PATH + pdf_name + ".pdf")
    pdf_out = PdfFileWriter()

    if end == -1:
        end = pdf_in.getNumPages()


    for page in range(start - 1, end):
        pdf_out.addPage(pdf_in.getPage(page))

    new_name = PATH + pdf_name + "_split.pdf"

    with open(new_name, 'wb') as output_pdf:
        pdf_out.write(output_pdf)

    get_pdf_images(opener(new_name))

if __name__ == "__main__":
    split_pdf_get_images("in", 1, -1)
