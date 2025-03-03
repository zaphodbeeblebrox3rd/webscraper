import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

# Collect all basic service prices and all embalming prices from output.xlsx
data = pd.read_excel('output.xlsx')

# Create a DataFrame
df = pd.DataFrame(data)

# Convert date to datetime in yyyy format
df['year'] = pd.to_datetime(df['date']).dt.year

# Exclude records before 2014
df = df[df['year'] >= 2014]

# Drop rows with missing values in 'basicservicesfee' and 'embalming' columns
df = df.dropna(subset=['basicservicesfee', 'embalming'])

# Convert columns to numeric
df['basicservicesfee'] = pd.to_numeric(df['basicservicesfee'], errors='coerce')
df['embalming'] = pd.to_numeric(df['embalming'], errors='coerce')

# Scatter plot will look like a downward sloping line if there is an inverse relationship
plt.scatter(df['basicservicesfee'], df['embalming'])
plt.title('Scatter plot of basic service prices vs embalming prices')
plt.xlabel('basic service prices')
plt.ylabel('embalming prices')
plt.show()

# Calculate correlation
correlation, _ = pearsonr(df['basicservicesfee'], df['embalming'])
print(f'Correlation coefficient: {correlation}')

# Interpretation
if correlation < 0:
    print("There is an inverse relationship between the prices of basic service fees and embalming prices.")
else:
    print("There is no inverse relationship between the prices of Service A and Service B.")

# Statistical significance
# Calculate the p-value for the correlation
p_value = pearsonr(df['basicservicesfee'], df['embalming'])[1]
print(f'p-value: {p_value}')

# Interpretation
if p_value < 0.05:
    print("The correlation is statistically significant at the 0.05 level.")
else:
    print("The correlation is not statistically significant at the 0.05 level.")

# Calculate the mean of the basic service fees and embalming prices
mean_basicservicesfee = df['basicservicesfee'].mean()
mean_embalming = df['embalming'].mean()

print(f'Mean of basic service fees: {mean_basicservicesfee}')
print(f'Mean of embalming prices: {mean_embalming}')
