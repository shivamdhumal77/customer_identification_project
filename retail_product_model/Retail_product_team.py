import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load data from the Excel file
df = pd.read_excel("C:\\Users\\dhuma\\Downloads\\Copy of customer_transactions_sample.xlsx")

# Convert 'InvoiceDate' to datetime format
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], format='%d-%m-%Y %H:%M')

# Calculate year for each invoice
df['Year'] = df['InvoiceDate'].dt.year

# Focus on data for the year 2010
df_2010 = df[df['Year'] == 2010]

# Calculate ABI index for each product pair
def calculate_abi_index(df):
    # Get list of unique stock codes
    stock_codes = df['StockCode'].unique()
    
    # Initialize ABI DataFrame
    abi_df = pd.DataFrame(index=stock_codes, columns=stock_codes, dtype=float)
    abi_df = abi_df.fillna(0)  # Fill NaN values with 0
    
    # Loop through unique stock codes and calculate ABI index
    for stock_code_a in stock_codes:
        for stock_code_b in stock_codes:
            if stock_code_a != stock_code_b:
                # Calculate co-occurrence
                co_occurrence = df[(df['StockCode'] == stock_code_a) & (df['Customer ID'].isin(df[df['StockCode'] == stock_code_b]['Customer ID']))]
                abi_index = len(co_occurrence) / len(df[df['StockCode'] == stock_code_a])
                abi_df.at[stock_code_a, stock_code_b] = abi_index
    
    return abi_df

# Calculate ABI index for 2010
abi_index_2010 = calculate_abi_index(df_2010)

# Plot ABI index heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(abi_index_2010, cmap='viridis', annot=True, fmt=".2f")
plt.title('Average Basket Item (ABI) Index by Product (2010)')
plt.xlabel('Product Stock Code')
plt.ylabel('Product Stock Code')
plt.xticks(rotation=45)
plt.yticks(rotation=0)
plt.tight_layout()
plt.show()
