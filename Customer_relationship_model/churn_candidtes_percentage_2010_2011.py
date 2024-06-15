import pandas as pd
import matplotlib.pyplot as plt

df_2011 = pd.read_excel("C:\\Users\\dhuma\\Downloads\\Copy of customer_transactions_sample.xlsx", sheet_name= 'Year 2010-2011')

# Convert 'InvoiceDate' to datetime format
df_2011['InvoiceDate'] = pd.to_datetime(df_2011['InvoiceDate'], format='%d-%m-%Y %H:%M')

# Extract year and month from 'InvoiceDate'
df_2011['YearMonth'] = df_2011['InvoiceDate'].dt.to_period('M')

# Calculate churn rate for each month in 2011
churn_rate_2011 = df_2011.groupby('YearMonth').size() / len(df_2011) * 100

# Plot the churn rate percentages over time for 2011
plt.figure(figsize=(10, 6))
plt.plot(churn_rate_2011.index.astype(str), churn_rate_2011.values, label='Churn Rate 2011', color='orange')
plt.xlabel('Year-Month')
plt.ylabel('Churn Rate (%)')
plt.title('Monthly Churn Rate (2011)')
plt.legend()
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

# Cut the above values before using it 
# Load the dataset for 2011
df_2011 = pd.read_excel("C:\\Users\\dhuma\\Downloads\\Copy of customer_transactions_sample.xlsx", sheet_name="2011_data")

# Convert 'InvoiceDate' to datetime format
df_2011['InvoiceDate'] = pd.to_datetime(df_2011['InvoiceDate'], format='%d-%m-%Y %H:%M')

# Extract year and month from 'InvoiceDate'
df_2011['YearMonth'] = df_2011['InvoiceDate'].dt.to_period('M')

# Calculate churn rate for each month in 2011
churn_rate_2011 = df_2011.groupby('YearMonth').size() / len(df_2011) * 100

# Plot the churn rate percentages over time for 2011
plt.figure(figsize=(10, 6))
plt.plot(churn_rate_2011.index.astype(str), churn_rate_2011.values, label='Churn Rate 2011', color='orange')
plt.xlabel('Year-Month')
plt.ylabel('Churn Rate (%)')
plt.title('Monthly Churn Rate (2011)')
plt.legend()
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()
