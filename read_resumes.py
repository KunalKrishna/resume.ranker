import os
from pathlib import Path
from resume_utils import *
# import pypdfium2 as pdfium
# import PyMuPDF as pymu

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

def extract_texts_from_pdfs_in_folder(folder_path):
    """
    Extracts and prints text from all PDF files in the specified folder.

    Parameters:
        folder_path (str): Path to the folder containing PDF files.
    
    Returns:
        list of str: A list where each element is the extracted text from a PDF file.
                     If no PDFs are found or an error occurs, the list may be empty.
    
    Example:
        raw_data = extract_texts_from_pdfs_in_folder("path/to/folder")
        for text in raw_data:
            print(text)
    """
    print(f"Scanning resumes/PDF files in directory: {folder_path}.")
    pdf_files = [file for file in os.listdir(folder_path) if file.endswith('.pdf')]

    if not pdf_files:
        print("No PDF files found in the specified folder.")
        return

    raw_data =[]

    for pdf_file in pdf_files:
        file_path = os.path.join(folder_path, pdf_file)
        print(f"Extracting text from {pdf_file}...")

        try:
            # extracted_text = extract_text_from_pdf_page(file_path, page_number=0)
            extracted_text = extract_all_text_from_pdf(file_path)
            print(extracted_text,end="\n************\n")
            
            #print(f"Text from {pdf_file}:\n{extracted_text}\n{'-'*40}\n{'-'*40}\n")
            raw_data.append({pdf_file: extracted_text}) # [{'PID','text'},{'PID','text'},{'PID','text'}]#TODO replace filname with PID
            
        except Exception as e:
            print(f"Error reading {pdf_file}: {e}")
    
    return raw_data

if __name__ == "__main__":
    folder_path = "resume.ranker/CV" #Path("D:/523/Resume.classifier/resume.ranker/CV")  
    #extract_texts_from_pdfs_in_folder(folder_path)
    
    #read_pdfium()
    #pdf_text = read_pdf("D:/523/Resume.classifier/resume.ranker/CV/Grace_Hopper.pdf")
    #print(pdf_text)

    pdf_file = "D:/523/Resume.classifier/resume.ranker/CV/Grace_Hopper.pdf"
    
    read_pdftotext(pdf_file.file.read(), True)
    
    #read_ocrmypdf(folder_path)