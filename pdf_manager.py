from PyPDF2 import PdfFileReader, PdfFileWriter
# from image_extractor import get_pdf_images

# to be changed later
PATH = ""

def split_pdf_get_images(pdf_name: str, start: int, end: int) -> None:
    pdf_in = PdfFileReader(PATH + pdf_name + ".pdf")
    pdf_out = PdfFileWriter()

    for page in range(start, end + 1):
        pdf_out.addPage(pdf_in.getPage(page))

    with open(pdf_name + "_split.pdf", 'wb') as output_pdf:
        pdf_out.write(output_pdf)

    #get_pdf_images()

if __name__ == "__main__":
    split_pdf_get_images("in_split", 1, 750)
