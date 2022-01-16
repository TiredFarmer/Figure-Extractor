from asyncio import streams
from PyPDF2 import PdfFileReader, PdfFileWriter
from image_extractor import get_pdf_images, opener

PATH = "split_pdf/"

def split_pdf_get_images(pdf_name: str, start: int, end: int) -> str:

    FINAL_NAME = pdf_name + "_extracted"

    pdf_in = PdfFileReader("raw_pdf/" + pdf_name + ".pdf")
    pdf_out = PdfFileWriter()

    if end == -1:
        end = pdf_in.getNumPages()

    if start - 1 < 0 or end > pdf_in.getNumPages():
        return

    for page in range(start - 1, end):
        pdf_out.addPage(pdf_in.getPage(page))

    new_name = PATH + pdf_name + "_split.pdf"

    print("OPENING NEW_NAME")
    with open(new_name, 'wb') as output_pdf:
        pdf_out.write(output_pdf)

    print("STARTING GET_PDF_IMAGES")
    get_pdf_images(opener(new_name), FINAL_NAME)

    return FINAL_NAME

if __name__ == "__main__":
    print(split_pdf_get_images("in", 1, -1))
