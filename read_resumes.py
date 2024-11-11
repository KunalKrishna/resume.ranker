import os, asyncio
import warnings
from pathlib import Path
from resume_utils import *
from demo_pdf_reader import parsePDF
from config import PINECONESettings

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
    warnings.warn(
        "deprecated_function() is deprecated and will be removed in a future version. Use new_function() instead.",
        DeprecationWarning,
        stacklevel=2
    )
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

async def extract_texts_from_pdfs_in_folder_v2(folder_path):
    """
    Extracts and prints text from all PDF files in the specified folder.

    Parameters:
        folder_path (str): Path to the folder containing PDF files.
    
    Returns:
        list of str: A list where each element is the extracted text from a PDF file.
                     If no PDFs are found or an error occurs, the list may be empty.
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
            extracted_text = await parsePDF(file_path)
            print(extracted_text,end="\n************\n")
            
            #print(f"Text from {pdf_file}:\n{extracted_text}\n{'-'*40}\n{'-'*40}\n")
            raw_data.append({pdf_file: extracted_text}) # [{'PID','text'},{'PID','text'},{'PID','text'}]#TODO replace filname with PID
            
        except Exception as e:
            print(f"Error reading {pdf_file}: {e}")
    
    return raw_data

if __name__ == "__main__":
    folder_path = os.path.join(os.path.dirname(__file__), PINECONESettings.cv_repo_name) 
        #folder_path = "D:/523/Resume.classifier/resume.ranker/CV/" 
    #extract_texts_from_pdfs_in_folder(folder_path)
    asyncio.run(extract_texts_from_pdfs_in_folder_v2(folder_path))