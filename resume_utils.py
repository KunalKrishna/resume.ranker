from PyPDF2 import PdfReader

def extract_text_from_pdf_page(file_path, page_number=0):
    """
    Extracts text from a specific page of a PDF.

    Parameters:
        file_path (str): The path to the PDF file.
        page_number (int): The page number to extract text from (0-based index).

    Returns:
        str: The extracted text from the specified page.
    """
    reader = PdfReader(file_path)
    if page_number < len(reader.pages):
        page = reader.pages[page_number]
        text = page.extract_text()
        return text
    else:
        raise ValueError(f"Page number {page_number} exceeds number of pages in PDF.")


def extract_all_text_from_pdf(file_path):
    """
    Extracts text from a specific PDF.

    Parameters:
        file_path (str): The path to the PDF file.

    Returns:
        str: The extracted text from ALL the pages.
    """
    full_text  = ""

    reader = PdfReader(file_path)
    print(f"{file_path} has pages : " , len(reader.pages))

    for page_number, page in enumerate(reader.pages):
        try:
            page_text = page.extract_text()
            if page_text:  # Ensure text was successfully extracted
                #print(f"Text from page {page_number + 1}:\n{page_text}\n")  # Print text from each page
                full_text += page_text + "\n"  # Add newline between pages for readability
        except Exception as e:
            print(f"Error reading {file_path}: {e}")

    return full_text  # Return concatenated text of all page

