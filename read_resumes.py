import os
from pathlib import Path
from resume_utils import extract_all_text_from_pdf

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
    # Scan all PDF files in the specified folder
    pdf_files = [file for file in os.listdir(folder_path) if file.endswith('.pdf')]

    if not pdf_files:
        print("No PDF files found in the specified folder.")
        return

    raw_data =[]

    # Loop through each PDF file and extract text
    for pdf_file in pdf_files:
        file_path = os.path.join(folder_path, pdf_file)
        print(f"Extracting text from {pdf_file}...")

        try:
            # extracted_text = extract_text_from_pdf_page(file_path, page_number=0)
            extracted_text = extract_all_text_from_pdf(file_path)
            
            #print(f"Text from {pdf_file}:\n{extracted_text}\n{'-'*40}\n{'-'*40}\n")
            raw_data.append(extracted_text)
            
        except Exception as e:
            print(f"Error reading {pdf_file}: {e}")
    
    return raw_data

# Specify the folder containing CV/PDF files
folder_path = "resume.ranker/CV" #Path("D:/523/Resume.classifier/resume.ranker/CV")  
extract_texts_from_pdfs_in_folder(folder_path)