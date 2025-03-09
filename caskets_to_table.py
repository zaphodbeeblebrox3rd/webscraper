import pandas as pd
import os

# Define the path to the directory containing the text files
directory_path = 'caskets_text'

# Initialize a list to store the casket data
casket_data = []

# Read a block of lines up until an empty line is encountered   
def read_block(lines):
    block = []
    for line in lines:
        if line.strip():
            block.append(line.strip())
        else:
            break
    return block

# Process each file in the directory
for file_name in os.listdir(directory_path):
    if file_name.endswith('.txt'):
        file_path = os.path.join(directory_path, file_name)
        # Read the file
        with open(file_path, 'r') as file:
            lines = file.readlines()

            # Process each block of lines
            while lines:
                block = read_block(lines)
                if not block:
                    break

                # Create a dictionary for the block
                block_dict = {str(i+1): block[i] if i < len(block) else 'n/a' for i in range(6)}
                casket_data.append(block_dict)

                # Remove the processed block from lines
                lines = lines[len(block)+1:]  # +1 to skip the empty line

# Create a DataFrame from the list of dictionaries
casket_df = pd.DataFrame(casket_data)

# Define the output CSV file path
output_csv_path = 'caskets_data.csv'

# If the file exists already, load its contents into a DataFrame and merge with the new data
if os.path.exists(output_csv_path):
    existing_df = pd.read_csv(output_csv_path)
    casket_df = pd.concat([existing_df, casket_df])
    casket_df = casket_df.drop_duplicates()

# Write the CSV file
casket_df.to_csv(output_csv_path, index=False)
print(f"Data has been written to {output_csv_path}") 