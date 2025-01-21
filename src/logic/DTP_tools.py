import math
from docx import Document
from pptx import Presentation
import fitz  # PyMuPDF for PDFs
import win32com.client  # Required for handling .doc files on Windows

def count_pages_docx(file_path):
    # Check if it's a .doc file
    if file_path.lower().endswith('.doc'):
        return count_pages_doc(file_path)
    elif file_path.lower().endswith('.docx') or file_path.lower().endswith('.docm'):
        return count_pages_docx_with_docx(file_path)
    else:
        raise ValueError(self.tr(f"Unsupported file type: {file_path}"))

def count_pages_doc(file_path):
    """Count pages in .doc file using pywin32."""
    # Initialize COM object for Word
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False  # Word is not shown during the process

    # Open the document
    doc = word.Documents.Open(file_path)

    # Get the number of pages
    page_count = doc.ComputeStatistics(2)  # 2 corresponds to wdStatisticPages

    # Close the document and quit Word
    doc.Close(False)
    word.Quit()

    return page_count

def count_pages_docx_with_docx(file_path):
    """Count pages in .docx or .docm file."""
    doc = Document(file_path)
    return len(doc.paragraphs)


def count_slides_pptx(file_path):
    ppt = Presentation(file_path)
    return len(ppt.slides)

def count_pages_pdf(file_path):
    pdf = fitz.open(file_path)
    page_count = pdf.page_count
    pdf.close()
    return page_count

def is_editable_pdf(file_path):
    # Placeholder logic for editable PDF detection
    return True

def calculate_dtp_time(file_type, count, time_per_unit):
    """Calculate the DTP time for different file types and round up to the nearest quarter hour."""
    try:
        time_per_unit = float(time_per_unit)  # Ensure the input is numeric
    except ValueError:
        raise ValueError(self.tr("Time per unit must be a number."))

    # Calculate time in hours
    if file_type == 'word':
        time = (count * time_per_unit) / 60
    elif file_type == 'ppt':
        time = (count * time_per_unit) / 60
    elif file_type == 'pdf':
        time = (count * time_per_unit) / 60
    else:
        raise ValueError(self.tr(f"Unknown file type: {file_type}"))

    # Round up time to the nearest quarter hour (0.25 hours)
    rounded_time = math.ceil(time * 4) / 4

    return rounded_time
