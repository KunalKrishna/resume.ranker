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
    print(text)
    # if full_text:
    #     return text
    # pages_text = await getPageWiseText(text)
    # return pages_text

# def read_pdftotext(pdf_binary, full_text=True):
#     pdfToTextCommand = ['pdftotext', '-layout', '-', '-']
#     process = subprocess.Popen(
#         pdfToTextCommand, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
#     )
#     stout, _ = process.communicate(input=pdf_binary)
#     text = stout.decode('utf-8').strip()

#     print(text)
#     return text

# def foo(folder_path):
#     pdf_files = [file for file in os.listdir(folder_path) if file.endswith('.pdf')]

#     if not pdf_files:
#         print("No PDF files found in the specified folder.")
#         return

#     raw_data =[]
#     for pdf_file in pdf_files:
#         file_path = os.path.join(folder_path, pdf_file)
#         with open(file_path,"rb") as pdf_binary : 
#             pdf_text = read_pdftotext(pdf_binary, True)
#             raw_data.append(pdf_text)
#         # with open(filename, "rb") as f:
#         # pdf = pdftotext.PDF(f) 
#     print(raw_data)
#     return raw_data

async def main():
    pdf_path = 'D:/523/Resume.classifier/resume.ranker/CV/Yashas_Majmudar_Resume.pdf'
    
    # Read the PDF as binary data
    with open(pdf_path, 'rb') as pdf_file:
        pdf_binary = pdf_file.read()

    await parsePDFUsingPDFToText(pdf_binary)

asyncio.run(main())

# if __name__ == "__main__":
#     folder_path = "D:/523/Resume.classifier/resume.ranker/CV" #Path("D:/523/Resume.classifier/resume.ranker/CV")  

    

'''
successFUL

import ocrmypdf

if __name__ == '__main__': # To ensure correct behavior on Windows and macOS
    ocrmypdf.ocr('D:/523/Resume.classifier/resume.ranker/CV/Binder1.pdf', 'D:/523/Resume.classifier/resume.ranker/CV/code.pdf', deskew=False)
'''