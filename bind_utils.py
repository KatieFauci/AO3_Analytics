import PyPDF2
import csv
import os
import io
from datetime import datetime
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader
from env import *

def get_pdf_page_size(reader, page_num):
    try:
        packet = io.BytesIO()
        can = canvas.Canvas(packet)
        media_box = reader.pages[page_num].mediabox
        can.setPageSize((media_box.width, media_box.height))
        width, height = can._pagesize
        can.save()
        packet.seek(0)
        return width, height
    except Exception as e:
        print(f"Error detecting page size: {e}")
        return None, None

def determine_page_format(width, height):
    formats = {
        'Letter Folio': (5.5 * 72, 8.5 * 72),
        'Letter Quarto': (4.25 * 72, 5.5 * 72),
        'Legal Quarto': (4.25 * 72, 7 * 72)
    }
    for name, (w, h) in formats.items():
        if abs(width - w) < 5 and abs(height - h) < 5:
            return name
    return "Other"

def ask_for_page_format():
    formats = {
        '1': ('Letter Folio', 5.5, 8.5),
        '2': ('Letter Quarto', 4.25, 5.5),
        '3': ('Legal Quarto', 4.25, 7),
        '4': 'Other'
    }
    print("Please select the page format or enter custom dimensions:")
    for key, value in formats.items():
        if isinstance(value, tuple):
            name, _, _ = value
            print(f"{key}. {name}")
        else:
            print(f"{key}. {value}")
    
    while True:
        choice = input("Enter your choice or dimensions (e.g., 8.5x11 for custom): ")
        if choice in formats:
            if choice == '4':
                custom = input("Enter custom dimensions (width x height in inches): ").split('x')
                return f"Custom {custom[0]}x{custom[1]}", float(custom[0]), float(custom[1])
            else:
                name, width, height = formats[choice]
                return name, width, height
        elif 'x' in choice:
            try:
                width, height = map(float, choice.split('x'))
                return f"Custom {width}x{height}", width, height
            except ValueError:
                print("Invalid format. Use widthxheight in inches.")
        else:
            print("Invalid choice. Please try again.")

def pdf_metrics(file_path, skip_pages=0):
    """
    Analyze a PDF file for basic metrics and optionally store results in a CSV.

    :param file_path: Path to the PDF file.
    :param skip_pages: Number of pages to skip from the beginning for word counting.
    :return: Dictionary containing metrics.
    """
    try:
        with open(file_path, 'rb') as file:
            reader = PdfReader(file)
            width, height = get_pdf_page_size(reader, 0)
            if width is None or height is None:
                page_format, width, height = ask_for_page_format()
                width, height = width * 72, height * 72  # Convert back to points for consistency in CSV
            else:
                page_format = determine_page_format(width, height)
            
            total_pages = len(reader.pages)
            if skip_pages >= total_pages:
                raise ValueError("The number of pages to skip cannot be greater than or equal to the total number of pages.")

            total_words = sum(len(page.extract_text().split()) for page in reader.pages[skip_pages:])

        avg_words_per_page = total_words / (total_pages - skip_pages) if total_pages > skip_pages else 0

        metrics = {
            'file_name': os.path.basename(file_path),
            'total_pages': total_pages,
            'total_words': total_words,
            'avg_words_per_page': avg_words_per_page,
            'pages_skipped': skip_pages,
            'analysis_date': datetime.now().isoformat(),
            'page_width': width / 72,  # Convert points to inches for user readability
            'page_height': height / 72,
            'page_format': page_format
        }

        while True:
            record = input("Do you want to record these metrics? (yes/no): ").lower()
            if record in ['yes', 'no']:
                if record == 'yes':
                    if record_to_csv(metrics):
                        print("Metrics recorded successfully.")
                    else:
                        print("This entry already exists in the CSV file, not saved to avoid duplication.")
                break
            else:
                print("Please enter 'yes' or 'no'.")
        
        return metrics

    except PyPDF2.errors.PdfReadError:
        print(f"Error: '{file_path}' is not a valid PDF or could not be read.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def record_to_csv(metrics):
    file_exists = os.path.isfile(BIND_DATA_FILE_NAME)
    fieldnames = ['file_name', 'total_pages', 'total_words', 'avg_words_per_page', 'pages_skipped', 
                  'page_width', 'page_height', 'page_format', 'analysis_date']

    with open(BIND_DATA_FILE_NAME, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()

        if not _is_duplicate(BIND_DATA_FILE_NAME, metrics):
            writer.writerow(metrics)
            return True
        return False

def _is_duplicate(BIND_DATA_FILE_NAME, metrics):
    if not os.path.exists(BIND_DATA_FILE_NAME):
        return False

    with open(BIND_DATA_FILE_NAME, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if (row['file_name'] == metrics['file_name'] and 
                row['pages_skipped'] == str(metrics['pages_skipped']) and
                row['analysis_date'].startswith(metrics['analysis_date'][:10])):
                return True
    return False