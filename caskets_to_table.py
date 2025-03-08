import pandas as pd
import os

# Define the path to the text file
file_path = 'caskets_text/2022-Batesville-Wood-Caskets - Ponders Funeral Home, Georgia, small.txt'

# Read the file
with open(file_path, 'r') as file:
    lines = file.readlines()

# Filter out empty lines
lines = [line for line in lines if line.strip()]

# Initialize a list to store the casket data
casket_data = []

# Process the lines in blocks of 5
for i in range(0, len(lines), 5):
    # Check if there are enough lines remaining for a complete block
    if i + 4 < len(lines):
        # Extract each piece of information
        model = lines[i].strip()
        interior = lines[i+1].strip()
        wood = lines[i+2].strip()
        item_number = lines[i+3].strip()
        price = lines[i+4].strip()
        
        # Append the data as a dictionary
        casket_data.append({
            'Model': model,
            'Interior': interior,
            'Wood': wood,
            'Item Number': item_number,
            'Price': price
        })

# Create a DataFrame from the list of dictionaries
casket_df = pd.DataFrame(casket_data)

# Define the output CSV file path
output_csv_path = 'caskets_data.csv'

# If the file exists already, load its contents into a DataFrame and merge with the new data
if os.path.exists(output_csv_path):
    existing_df = pd.read_csv(output_csv_path)
    casket_df = pd.concat([existing_df, casket_df])
    casket_df = casket_df.drop_duplicates()

# Write the DataFrame to a CSV file
casket_df.to_csv(output_csv_path, index=False)

print(f"Data has been written to {output_csv_path}") 