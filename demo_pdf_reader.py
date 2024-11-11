import subprocess
import os
import pdftotext
import ocrmypdf
import tempfile, io, asyncio

async def ocrPDF(daf_binary, force_ocr=False):
    ocr_output_data = daf_binary
    with tempfile.NamedTemporaryFile(suffix='.pdf') as pdf_output:
        ocrmypdf.ocr(
            io.BytesI0(daf_binary), pdf_output.name, language='eng', skip_text=True, 
            output_type='pdf', optimize=3, progress_bar=False, quiet=True, force_ocr=force_ocr
        )

    with open(pdf_output.name, 'rb') as ocr_output:
        ocr_output_data = ocr_output. read()
    return ocr_output_data

async def parsePDFUsingPDFToText(pdf_binary, full_text=True):
    pdfToTextCommand = ['pdftotext', '-layout', '-', '-']
    process = subprocess. Popen(
        pdfToTextCommand, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
    stdout, _ = process.communicate(input=pdf_binary)
    text = stdout.decode('utf-8').strip()
    return(text)

async def parsePDF(pdf_path):
    with open(pdf_path, 'rb') as pdf_file:
        pdf_binary = pdf_file.read()

    text = await parsePDFUsingPDFToText(pdf_binary)
    return text


if __name__ == "__main__":
    pdf_path = 'D:/523/Resume.classifier/resume.ranker/CV/Yashas_Majmudar_Resume.pdf'
    print (asyncio.run(parsePDF(pdf_path)))

'''
import pypdfium2 as pdfium
import PyMuPDF as pymu

def read_ocrmypdf(folder_path):
    pdf_files = [file for file in os.listdir(folder_path) if file.endswith('.pdf')]

    if not pdf_files:
        print("No PDF files found in the specified folder.")
        return

    for pdf_file in pdf_files:
        file_path = os.path.join(folder_path, pdf_file)
        print(f"Extracting text from {pdf_file}...")

        try:
            # extracted_text = extract_text_from_pdf_page(file_path, page_number=0)
            extracted_text = extract_all_text_from_pdf(file_path)
            print(extracted_text,end="\n************\n")
            
            #print(f"Text from {pdf_file}:\n{extracted_text}\n{'-'*40}\n{'-'*40}\n")
            
        except Exception as e:
            print(f"Error reading {pdf_file}: {e}")

def read_pdfium() :
    pdf = pdfium.PdfDocument("D:/523/Resume.classifier/resume.ranker/CV/Grace_Hopper.pdf") #./path/to/document.pdf 
    version = pdf.get_version()  # get the PDF standard version
    n_pages = len(pdf)  # get the number of pages in the document
    page = pdf[0]  # load a page
    textpage = page.get_textpage()
    print(textpage)

def read_pdfium2(pdf_path):
    with pdfium.PdfDocument(pdf_path) as pdf:
        text = ""
        for page in pdf:
            textpage = page.get_textpage()
            text += textpage.get
            textpage.close()
    return text
'''

'''
successFUL

import ocrmypdf

if __name__ == '__main__': # To ensure correct behavior on Windows and macOS
    ocrmypdf.ocr('D:/523/Resume.classifier/resume.ranker/CV/Binder1.pdf', 'D:/523/Resume.classifier/resume.ranker/CV/code.pdf', deskew=False)
'''