import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

# This script is used to plot the funeral embalming fee and the consumer price index (CPI) over time   
# It is used to see whether they are in line or if the funeral embalming fee outpaces inflation

# Pull in the data from output.xlsx
data = pd.read_excel('output.xlsx')

# Create a DataFrame
df = pd.DataFrame(data)

# Convert date to datetime in yyyy format
df['year'] = pd.to_datetime(df['date']).dt.year

# Exclude records before 2014
df = df[df['year'] >= 2014]

# CPI data for each year from the Federal Reserve Bank
cpi_data = {
    2014: 236.7,
    2015: 237,
    2016: 240,
    2017: 245.1,
    2018: 251.1,
    2019: 255.7,
    2020: 258.8,
    2021: 271,
    2022: 292.7,
    2023: 304.7,
    2024: 314.4,
    2025: 325.2
}

# Insert a new column for the CPI based on the year
df['CPI'] = df['year'].map(cpi_data)

# Drop rows with missing values in the 'embalming' column
df = df.dropna(subset=['embalming'])

# Convert columns to numeric
df['embalming'] = pd.to_numeric(df['embalming'], errors='coerce')
df['CPI'] = pd.to_numeric(df['CPI'], errors='coerce')

# Plotting
plt.figure(figsize=(12, 12))

# Line plot for Funeral Embalming Fee and CPI X 10
plt.scatter(df['year'], df['embalming'], label='Funeral Embalming Fee', color='blue')
plt.plot(df['year'], df['CPI'] * 10, label='CPI X 10', color='red')

# Adding titles and labels
plt.title('Funeral Embalming Fee and Consumer Price Index Over Time')
plt.xlabel('Year')
plt.ylabel('Value')
plt.legend()

# Show the plot
plt.show()

# Correlation between funeral embalming fee and CPI
correlation = df['embalming'].corr(df['CPI'])
print(f'Correlation between funeral embalming fee and CPI: {correlation}')

# Statistical test to see if the correlation is significant
p_value = pearsonr(df['embalming'], df['CPI'])

# Print the results
print(f'P-value: {p_value}')

# Interpretation
if p_value < 0.05:
    print("The correlation is statistically significant at the 0.05 level.")
else:
    print("The correlation is not statistically significant at the 0.05 level.")


