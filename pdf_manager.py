from PyPDF2 import PdfFileReader, PdfFileWriter

# to be changed later
PATH = ""

def split_pdf_get_images(pdf_name: str, start: int, end: int) -> None:
    pdf_in = PdfFileReader(PATH + pdf_name)
    pdf_out = PdfFileWriter()

    for page in range(start, end + 1):
        pdf_out.addPage(pdf_in.getPage(page))


    with open("out.pdf", 'wb') as output_pdf:
        pdf_out.write(output_pdf)

if __name__ == "__main__":
    split_pdf_get_images("in.pdf", 1, 900)
