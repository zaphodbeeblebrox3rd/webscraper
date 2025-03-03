import pandas as pd

# Load the Excel file
file_path = 'output.xlsx'
df = pd.read_excel(file_path)

# Check if 'Country' and 'State' columns exist, if not, create them
if 'Country' not in df.columns:
    df['Country'] = None

if 'State' not in df.columns:
    df['State'] = None

# Function to extract country and state from location
def extract_country_state(location):
    # Example logic to extract country and state
    # This should be replaced with actual logic based on your data
    if ',' in location:
        parts = location.split(',')
        state = parts[-2].strip() if len(parts) > 1 else None
        country = parts[-1].strip() if len(parts) > 0 else None
    else:
        state = None
        country = location.strip()
    return country, state

# Populate 'Country' and 'State' columns
for index, row in df.iterrows():
    location = row.get('Location', '')
    country, state = extract_country_state(location)
    df.at[index, 'Country'] = country
    df.at[index, 'State'] = state

# Save the updated DataFrame back to Excel
df.to_excel('output_cleaned.xlsx', index=False)
