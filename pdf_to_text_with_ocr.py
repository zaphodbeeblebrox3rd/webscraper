import os
from pdf2image import convert_from_path
import pytesseract
from PIL import Image

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update this path

# Define the directory containing the PDF files
pdf_directory = 'caskets'

# Define the output directory for the text files
output_directory = 'caskets_text'

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Loop through each file in the PDF directory
for filename in os.listdir(pdf_directory):
    if filename.endswith('.pdf'):
        pdf_path = os.path.join(pdf_directory, filename)
        
        # Convert PDF to images
        images = convert_from_path(pdf_path, poppler_path=r'C:\Program Files\poppler-24.08.0\Library\bin')
        
        # Initialize a string to hold the text
        text_content = ''
        
        # Extract text from each image
        for image in images:
            text_content += pytesseract.image_to_string(image)
        
        # Define the output text file path
        text_filename = os.path.splitext(filename)[0] + '.txt'
        text_path = os.path.join(output_directory, text_filename)
        
        # Write the text to a file
        with open(text_path, 'w', encoding='utf-8') as text_file:
            text_file.write(text_content)

print("PDF to text conversion with OCR completed.") 