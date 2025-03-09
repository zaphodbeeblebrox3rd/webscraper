import os
from google.cloud import storage, documentai_v1 as documentai
import pandas as pd
import json
from google.protobuf import json_format
from google.cloud.documentai_v1 import types as documentai_types
import re

# Initialize Google Cloud Storage client
storage_client = storage.Client()
bucket_name = 'funeral-gpl'
bucket = storage_client.get_bucket(bucket_name)

# Initialize Document AI client
documentai_client = documentai.DocumentProcessorServiceClient()
project_number = '397128907620'  # This is actually the Project Number, not the Project ID
location = 'us'
processor_id = 'a9c2b37de03944df'
name = f'projects/{project_number}/locations/{location}/processors/{processor_id}'

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

    # Attempt to convert the document to a dictionary
    try:
        document_dict = json_format.MessageToDict(document)
        with open(file_name + '.json', 'w', encoding='utf-8') as f:
            json.dump(document_dict, f, indent=4)
    except Exception as e:
        print(f"Error converting document to dict: {e}")
        # Debug: Print the type and content of the document
        print(f"Document type: {type(document)}")
        # print(document)

    # Extract fields from the document
    provider = extract_field(document, 'Provider')
    location = extract_field(document, 'Location')
    website = extract_field(document, 'Website')
    basicservicesfee = extract_field(document, 'BasicServicesFee')
    embalming = extract_field(document, 'Embalming')
    date = extract_field(document, 'Date')

    # Print extracted fields
    print(f"Provider: {provider}")
    print(f"Location: {location}")
    print(f"Website: {website}")
    print(f"Basic Services Fee: {basicservicesfee}")
    print(f"Embalming: {embalming}")
    print(f"Date: {date}")

    return {
        'provider': provider,
        'location': location,
        'website': website,
        'basicservicesfee': basicservicesfee,
        'embalming': embalming,
        'date': date
    }

# Function to extract fields from the document
def extract_field(document, field_name):
    # Create a list to store all mentions of the field
    field_values = []
    
    # Iterate over the entities in the document
    for entity in document.entities:
        # Check if the entity type matches the field name
        if entity.type_ == field_name:
            # Append the mention text of the entity to the list
            field_values.append(entity.mention_text)
    
    # Return the list of field values, or None if no values were found
    return field_values if field_values else None

# List all PDF files in the bucket
blobs = bucket.list_blobs()
pdf_files = [blob.name for blob in blobs if blob.name.endswith('.pdf')]

# Process each PDF and collect results
for pdf_file in pdf_files:
    results = []
    try:
        result = process_pdf(pdf_file)
        results.append(result)

        # Check if the Excel file exists
        if os.path.exists('output.xlsx'):
            # Read the existing data
            existing_df = pd.read_excel('output.xlsx')
            # Append the new data
            df = pd.DataFrame(results, columns=['provider', 'location', 'website', 'basicservicesfee', 'embalming', 'date'])
            combined_df = pd.concat([existing_df, df], ignore_index=True)
        else:
            # If the file doesn't exist, create a new DataFrame
            combined_df = pd.DataFrame(results, columns=['provider', 'location', 'website', 'basicservicesfee', 'embalming', 'date'])

        # Write the combined data back to the Excel file
        combined_df.to_excel('output.xlsx', index=False)

    except Exception as e:
        print(f"Error processing {pdf_file}: {e}")




