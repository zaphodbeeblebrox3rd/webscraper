# Web Scraper Project

This project contains various scripts for web scraping and document processing for research on funeral services.  It can also be as a model for scraping and parsing PDFs on the web for other fields of research.

## Overview

In order to work with this data, there are several steps involved. Firstly, the PDF files need to be gathered.  This would need to be done by collecting them manually and scanning them, or by scraping the websites of funeral homes.  These approaches could be combined if desired.

Once the PDF files are gathered, they need to be processed to extract the text and structured data.  This is done using Google Cloud's Document AI.  The output of this is a spreadsheet with the text and structured data.  This is a slow, sequential process with a large number of files, but I felt that parallelizing the process would incur risks of incurring expenses too quickly to adjust my approach if needed.

The data needs to be cleaned.  This means removing the brackets, newlines, and other characters that don't belong in the Excel file.  Also, dates and pricesneed to be formatted uniformly. This is done using the `clean_data.py` script.

Once the data is cleaned, it can be used for analysis.  Some examples of analysis are provided.  One way I wanted to look at the idea was to see trends over time and show a scatter plot of median basic service prices, median embalming prices year by year.  Another scatter plot I wanted to show was basic service prices and embalming prices by state.  I was also interested to see if there was an inverse relationship between basic service prices and embalming prices, which would suggest that the funeral homes tend to place a larger consideration on the total price rather than their cost for the individual items.  This is done using the `data_analysis` scripts

This project includes the following scripts:

1. `funeral_scraper.py`: Scrapes the pdf data from the websites
2. `document_extraction.py`: Extracts text and structured data from PDF documents using Google Cloud's Document AI.
3. `extract_text_from_pdfs.py`: Extracts text from PDF documents using less sophisticated methods.
4. `clean_data.py`: Cleans the data from the PDF documents and saves it to an Excel file.
5. `data_analysis_basic_to_cpi.py`: Analyzes the relationship between basic service prices and the consumer price index (CPI).
6. `data_analysis_embalming_to_cpi.py`: Analyzes the relationship between embalming prices and the consumer price index (CPI).
7. `data_analysis_basic_to_embalming.py`: Analyzes the relationship between basic service prices and embalming prices.



## Setting Up the Environment

This project uses Conda for managing dependencies. Conda is an open-source package management system and environment management system that runs on Windows, macOS, and Linux. It allows you to create isolated environments with specific versions of Python and other packages.

### Importing the Conda Environment

To set up the environment for this project, you need to import the environment from the `environment.yml` file. Follow these steps:

1. **Install Conda**: If you haven't already, download and install Conda from [Anaconda's website](https://www.anaconda.com/products/distribution) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html).

2. **Create the Environment**: Open a terminal or command prompt and navigate to the project directory. Run the following command to create the environment:

   ```bash
   conda env create -f environment.yml
   ```

3. **Activate the Environment**: Once the environment is created, activate it using:

   ```bash
   conda activate your_environment_name
   ```

   Replace `your_environment_name` with the name specified in the `environment.yml` file.

## Setting Up Google Cloud

### Creating a free Google Cloud account and setting up billing
Setting up a new Google Gloud account comes with $300 in free credits.  This is more than enough to run the scripts in this project.  You can sign up for a free account at [Google Cloud](https://cloud.google.com/).

### Enabling the Document AI API
1. Go to the [Google Cloud Console](https://console.cloud.google.com/) and create a new project.
2. Enable the Document AI API.
3. Create a service account and download the credentials file.
4. Set up billing for the project.

### Setting Up the Google Cloud SDK
Go to the [Google Cloud SDK](https://cloud.google.com/sdk/docs) for instructions on installing the SDK on your system.

### Setting Up the Google Cloud Storage Bucket
Go to the [Google Cloud Storage](https://cloud.google.com/storage) for instructions on setting up a storage bucket.

### Training the Document AI Model
Go to the [Document AI](https://cloud.google.com/document-ai) for instructions on training a custom model.


## Setting up OCR

### Setting up Tesseract

Tesseract is a powerful OCR tool that can be used to extract text from images.  It is a part of the Google Cloud OCR API, but I burned up my free credits before got to this point.  So, I'm using it locally.

1. Download the Tesseract executable from [here](https://github.com/UB-Mannheim/tesseract/wiki).
2. Extract the files to a directory.
3. Add the directory to your system's PATH.

### Setting up poppler

Poppler is a PDF library that can be used to extract text from PDF documents.  It is a part of the Google Cloud OCR API, but I burned up my free credits before got to this point.  So, I'm using it locally.

1. Download the Poppler executable from [here](https://github.com/oschwartz10612/poppler-windows/releases).
2. Extract the files to a directory.
3. Add the directory to your system's PATH.

## Purpose and Use of Scripts

### funeral_scraper.py

The `funeral_scraper.py` script is designed to scrape data from funeral service websites. It automates the process of collecting information such as service fees, provider details, and contact information. This script is useful for aggregating data from multiple sources into a structured format for analysis or reporting.

**Usage**:
- Ensure that the necessary dependencies are installed and the environment is activated.
> This means you need to 'conda activate your_environment_name' before you try to run any of the scripts!
< .is-info >

- Run the script using Python:

  ```bash
  python funeral_scraper.py
  ```

- The script will output the collected data into a specified format, such as a CSV or JSON file.

### extract_text_from_pdfs.py

The `extract_text_from_pdfs.py` script processes PDF documents to extract text and relevant information. It utilizes Google Cloud's Document AI to analyze and extract structured data from PDFs, which is particularly useful for processing funeral service documents.

**Usage**:
- Ensure that your Google Cloud SDK is set up and authenticated.
- Run the script using Python:

  ```bash
  python extract_text_from_pdfs.py
  ```

- The script will process the PDFs in the specified Google Cloud Storage bucket and output the extracted data into a structured format, such as an Excel file.

## Additional Information

- Ensure that you have the necessary permissions and API access for Google Cloud services.
- Modify the scripts as needed to fit your specific use case and document structure.

# Author

This project is developed by Eric Hoy, a systems engineer and cloud developerwith a passion for supporting social sciences research. https://github.com/zaphodbeeblebrox3rd

# License

This project is licensed under the MIT License. See the LICENSE file for details.
