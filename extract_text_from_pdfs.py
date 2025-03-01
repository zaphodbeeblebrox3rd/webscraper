import os
import PyPDF2

def extract_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text
    except Exception as e:
        print(f"Failed to extract text from {pdf_path}: {e}")
        return ""

def main():
    download_dir = 'downloads'
    all_texts = []

    for root, dirs, files in os.walk(download_dir):
        for file in files:
            if file.endswith('.pdf'):
                pdf_path = os.path.join(root, file)
                print(f"Extracting text from {pdf_path}")
                text = extract_text_from_pdf(pdf_path)
                all_texts.append(text)

    # Here you can analyze the extracted texts
    # For example, count occurrences of certain words or phrases
    # Or look for pricing patterns

if __name__ == "__main__":
    main() 