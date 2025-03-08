import os
import PyPDF2
import pytesseract

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
        
        # Open the PDF file
        with open(pdf_path, 'rb') as pdf_file:
            # Create a PDF reader object
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            # Initialize a string to hold the text
            text_content = ''
            
            # Extract text from each page
            for page in pdf_reader.pages:
                text_content += page.extract_text()
            
            # Define the output text file path
            text_filename = os.path.splitext(filename)[0] + '.txt'
            text_path = os.path.join(output_directory, text_filename)
            
            # Write the text to a file
            with open(text_path, 'w', encoding='utf-8') as text_file:
                text_file.write(text_content)

print("PDF to text conversion completed.") 