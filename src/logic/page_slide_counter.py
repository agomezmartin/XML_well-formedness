import os
from pptx import Presentation
from docx import Document
import PyPDF2
from .. import messages  # Import messages
from datetime import datetime
import math
from src.config import minutes_dict  # Config with default DTP page/slide times

# Global variables to store minutes per page for each file type
MINUTES_PER_PAGE_WORD = 5
MINUTES_PER_PAGE_PPT = 7
MINUTES_PER_PAGE_PDF = 15

def set_minutes_per_page(word_minutes, ppt_minutes, pdf_minutes):
    """
    Set custom minutes per page for each file type (Word, PowerPoint, PDF).

    Args:
        word_minutes (int): Minutes per Word page.
        ppt_minutes (int): Minutes per PowerPoint slide.
        pdf_minutes (int): Minutes per PDF page.
    """
    global MINUTES_PER_PAGE_WORD, MINUTES_PER_PAGE_PPT, MINUTES_PER_PAGE_PDF

    if word_minutes > 0:
        MINUTES_PER_PAGE_WORD = word_minutes
    if ppt_minutes > 0:
        MINUTES_PER_PAGE_PPT = ppt_minutes
    if pdf_minutes > 0:
        MINUTES_PER_PAGE_PDF = pdf_minutes


def count_pages_and_slides_in_directory(directory, log_file):
    """
    Count pages (for Word documents), slides (for PowerPoint presentations),
    and pages (for PDF files) in all supported files in a provided directory,
    and save results to a log.

    Args:
        directory (str): Path to the directory containing the files.
        log_file (str): Path to the log file.

    Returns:
        str: Log result containing the count of pages, slides, PDF pages, and DTP time.
    """
    if not os.path.isdir(directory):
        return messages.INVALID_DIRECTORY.format(directory)

    results, total_word_pages, total_ppt_slides, total_pdf_pages = [], 0, 0, 0

    try:
        with open(log_file, 'a') as log:
            write_log_header(log, directory)

            supported_extensions = ('.doc', '.docx', '.docm', '.ppt', '.pptx', '.pptm', '.pdf')

            for file_name in os.listdir(directory):
                file_path = os.path.join(directory, file_name)

                if file_name.lower().endswith(supported_extensions):
                    result, word_pages, ppt_slides, pdf_pages = count_pages_or_slides(file_path)
                    if result:
                        log.write(result + "\n")
                        results.append(result)
                        log.write(messages.LOG_FILE_SEPARATOR + "\n")
                        total_word_pages += word_pages
                        total_ppt_slides += ppt_slides
                        total_pdf_pages += pdf_pages

            # Calculate and log the total DTP time for each file type
            word_time, ppt_time, pdf_time = calculate_DTP_time(total_word_pages, total_ppt_slides, total_pdf_pages, minutes_dict)
            write_log_totals(log, total_word_pages, total_ppt_slides, total_pdf_pages, word_time, ppt_time, pdf_time)

        return messages.LOG_SAVED.format(log_file) if results else messages.NO_MS365_FILES_FOUND

    except Exception as e:
        return messages.LOG_FILE_ERROR.format(str(e))


def write_log_header(log, directory):
    """Write the header to the log file."""
    log.write(messages.LOG_SEPARATOR + "\n")
    log.write(f"{messages.LOG_HEADER} {directory}\n")
    log.write(messages.LOG_TIMESTAMP.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + "\n")
    log.write(messages.LOG_FILE_SEPARATOR + "\n")


def write_log_totals(log, total_word_pages, total_ppt_slides, total_pdf_pages, word_time, ppt_time, pdf_time):
    """Write the total counts and DTP time for each file type to the log file."""
    log.write(messages.TOTAL_WORD_PAGES.format(total_word_pages) + "\n")
    log.write(messages.TOTAL_PPT_SLIDES.format(total_ppt_slides) + "\n")
    log.write(messages.TOTAL_PDF_PAGES.format(total_pdf_pages) + "\n")
    log.write(messages.WORD_DTP_TIME.format(word_time) + "\n")  # Correctly formatted DTP time
    log.write(messages.PPT_DTP_TIME.format(ppt_time) + "\n")    # Correctly formatted DTP time
    log.write(messages.PDF_DTP_TIME.format(pdf_time) + "\n")    # Correctly formatted DTP time
    total_dtp_time = word_time + ppt_time + pdf_time
    log.write(messages.TOTAL_DTP_TIME.format(total_dtp_time) + "\n")  # Total DTP time in the log


def calculate_DTP_time(total_word_pages, total_ppt_slides, total_pdf_pages, minutes_dict):
    """
    Calculate the DTP time for each file type, rounding up to the nearest 0.25 hours.

    Args:
        total_word_pages (int): Total number of pages in Word documents.
        total_ppt_slides (int): Total number of slides in PowerPoint presentations.
        total_pdf_pages (int): Total number of pages in PDF files.

    Returns:
        tuple: DTP time in hours for Word, PowerPoint, and PDF files rounded to the nearest 0.25.
    """

    # Access values from the minutes_dict for each file type
    word_minutes = minutes_dict.get('word', MINUTES_PER_PAGE_WORD) # Default to Word global constant if user figure not provided
    ppt_minutes = minutes_dict.get('ppt', MINUTES_PER_PAGE_PPT) # Default to PowerPoint global constant if user figure not provided
    pdf_minutes = minutes_dict.get('pdf', MINUTES_PER_PAGE_PDF) # Default to PDF global constant if user figure not provided


    #word_minutes = minutes_dict['word',MINUTES_PER_PAGE_WORD] # Default to Word global constant if user figure not provided
    #ppt_minutes = minutes_dict['ppt', MINUTES_PER_PAGE_PPT] # Default to PowerPoint global constant if user figure not provided
    #pdf_minutes = minutes_dict['pdf', MINUTES_PER_PAGE_PDF] # Default to PDF global constant if user figure not provided

    # Calculate time in hours for each file type based on the number of pages or slides
    word_time = (total_word_pages * word_minutes) / 60  # Word time in hours
    ppt_time = (total_ppt_slides * ppt_minutes) / 60  # PowerPoint time in hours
    pdf_time = (total_pdf_pages * pdf_minutes) / 60  # PDF time in hours

    # Round up to the nearest 0.25 hour
    word_time = math.ceil(word_time * 4) / 4
    ppt_time = math.ceil(ppt_time * 4) / 4
    pdf_time = math.ceil(pdf_time * 4) / 4

    return word_time, ppt_time, pdf_time


def count_pages_or_slides(file_path):
    """
    Count pages/slides in a given file (Word, PowerPoint, or PDF).

    Args:
        file_path (str): Path to the file.

    Returns:
        tuple: Result of the page/slide counting for the file, 
               and counts for Word pages, PowerPoint slides, and PDF pages.
    """
    file_name = os.path.basename(file_path)
    
    word_pages, ppt_slides, pdf_pages = 0, 0, 0

    if file_path.lower().endswith(('.doc', '.docx', '.docm')):
        return count_word_pages(file_path, file_name)

    elif file_path.lower().endswith(('.ppt', '.pptx', '.pptm')):
        return count_ppt_slides(file_path, file_name)

    elif file_path.lower().endswith('.pdf'):
        return count_pdf_pages(file_path, file_name)

    return None, word_pages, ppt_slides, pdf_pages  # No result for unsupported files


def count_word_pages(file_path, file_name):
    """Count the pages in a Word document."""
    try:
        doc = Document(file_path)
        word_pages = len(doc.paragraphs)  # Placeholder for actual page counting logic
        return messages.PAGE_COUNT_RESULT.format(file_name, word_pages), word_pages, 0, 0
    except Exception as e:
        return messages.FILE_PARSE_ERROR.format(file_name, str(e)), 0, 0, 0


def count_ppt_slides(file_path, file_name):
    """Count the slides in a PowerPoint presentation."""
    try:
        prs = Presentation(file_path)
        ppt_slides = len(prs.slides)
        return messages.SLIDE_COUNT_RESULT.format(file_name, ppt_slides), 0, ppt_slides, 0
    except Exception as e:
        return messages.FILE_PARSE_ERROR.format(file_name, str(e)), 0, 0, 0


def count_pdf_pages(file_path, file_name):
    """Count the pages in a PDF file."""
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            pdf_pages = len(reader.pages)
        return messages.PDF_PAGE_COUNT_RESULT.format(file_name, pdf_pages), 0, 0, pdf_pages
    except Exception as e:
        return messages.FILE_PARSE_ERROR.format(file_name, str(e)), 0, 0, 0
