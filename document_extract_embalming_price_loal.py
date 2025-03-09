import os
import re
import PyPDF2

def extract_embalming_price(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()

            # Regular expression to find the embalming price
            match = re.search(r'embalming.*?\$?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)', text, re.IGNORECASE)
            if match:
                return match.group(1)
            else:
                return "Price not found"
    except Exception as e:
        print(f"Failed to extract price from {pdf_path}: {e}")
        return None

def main():
    # Directory where PDFs are stored
    pdf_directory = '.'

    # Iterate over all PDF files in the directory
    for filename in os.listdir(pdf_directory):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(pdf_directory, filename)
            price = extract_embalming_price(pdf_path)
            print(f"Embalming price in {filename}: {price}")

if __name__ == "__main__":
    main() 