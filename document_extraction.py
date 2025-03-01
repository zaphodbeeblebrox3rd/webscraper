import os
from google.cloud import storage, documentai_v1beta3 as documentai
import pandas as pd

# Initialize Google Cloud Storage client
storage_client = storage.Client()
bucket_name = 'funeral-gpl'
bucket = storage_client.get_bucket(bucket_name)

# Initialize Document AI client
documentai_client = documentai.DocumentUnderstandingServiceClient()
project_id = 'weighty-time-452302-e5'
location = 'us'
processor_id = 'a9c2b37de03944df'
name = f'projecta9c2b37de03944df/{project_id}/locations/{location}/processors/{processor_id}'

# Function to process a single PDF file
def process_pdf(file_name):
    blob = bucket.blob(file_name)
    pdf_content = blob.download_as_bytes()

    # Configure the request
    request = {
        "name": name,
        "raw_document": {
            "content": pdf_content,
            "mime_type": "application/pdf"
        }
    }

    # Process the document
    result = documentai_client.process_document(request=request)
    document = result.document

    # Extract required fields from the document
    # This part will depend on the structure of your document and how Document AI processes it
    # For demonstration, let's assume the fields are extracted as follows:
    provider = extract_field(document, 'provider')
    location = extract_field(document, 'location')
    website = extract_field(document, 'website')
    basicservicesfee = extract_field(document, 'basicservicesfee')
    embalming = extract_field(document, 'embalming')
    date = extract_field(document, 'date')

    return {
        'provider': provider,
        'location': location,
        'website': website,
        'basicservicesfee': basicservicesfee,
        'embalming': embalming,
        'date': date
    }

# Dummy function to extract fields - replace with actual logic
def extract_field(document, field_name):
    print(document)
    # Implement your logic to extract the field from the document
    return "extracted_value"

# List all PDF files in the bucket
#blobs = bucket.list_blobs()
#pdf_files = [blob.name for blob in blobs if blob.name.endswith('.pdf')]

# List the first 5 pdf files in the bucket
blobs = bucket.list_blobs()
pdf_files = [blob.name for blob in blobs if blob.name.endswith('.pdf')][:5]

# Process each PDF and collect results
results = []
for pdf_file in pdf_files:
    result = process_pdf(pdf_file)
    results.append(result)

# Create a DataFrame and save to a spreadsheet
df = pd.DataFrame(results, columns=['provider', 'location', 'website', 'basicservicesfee', 'embalming', 'date'])
df.to_excel('output.xlsx', index=False) 

# Save the output.xlsx file to disk
#df.to_excel('output.xlsx', index=False)


