import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Load the data
df = pd.read_csv('caskets_data.csv')

# Convert 'Date' to datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Clean the 'Price' column
df['Price'] = df['Price'].str.replace('[$,]', '', regex=True)
df['Price'] = pd.to_numeric(df['Price'])

# Filter the DataFrame for Batesville Casket Company
batesville_df = df[df['Manufacturer'] == 'Batesville']

# Scatter plot of Price vs Date for the Batesville Casket Company
plt.figure(figsize=(12, 12))
sns.scatterplot(data=batesville_df, x='Date', y='Price')
plt.title('Price Over Time for Batesville Casket Company')
plt.xticks()

# Set y-axis ticks in increments of $500
max_batesville_price = batesville_df['Price'].max()
plt.yticks(np.arange(0, max_batesville_price + 500, 500))

# Save the scatter plot to a file
plt.savefig('price_over_time_batesville.png')
plt.show()

# Box plot of Price by Manufacturer
plt.figure(figsize=(12, 12))
sns.boxplot(data=df, x='Manufacturer', y='Price')
plt.title('Price Distribution by Manufacturer')
plt.xticks(fontsize=10)

# Set y-axis ticks in increments of $500
max_price = df['Price'].max()
plt.yticks(np.arange(0, max_price + 500, 500))

# Save the box plot to a file
plt.savefig('price_distribution_by_manufacturer.png')
plt.show()

# Bar plot of average Price by Interior Fabric
plt.figure(figsize=(12, 12))
sns.barplot(data=df, x='Interior Fabric', y='Price', estimator=lambda x: sum(x) / len(x))
plt.title('Average Price by Interior Fabric')
plt.xticks(fontsize=10)

# Set y-axis ticks in increments of $500
plt.yticks(np.arange(0, max_price + 500, 500))

# Save the bar plot to a file
plt.savefig('average_price_by_interior_fabric.png')
plt.show()

# Calculate average price by materials and sort
materials_avg_price = df.groupby('Materials')['Price'].mean().sort_values()

# Bar plot of average Price by Materials
plt.figure(figsize=(20, 20))
sns.barplot(x=materials_avg_price.index, y=materials_avg_price.values)
plt.title('Average Price by Materials')
plt.xticks(rotation=90, fontsize=6)

# Set y-axis ticks in increments of $500
plt.yticks(np.arange(0, max_price + 500, 500))

# Save the bar plot to a file
plt.savefig('average_price_by_materials.png')
plt.show()




