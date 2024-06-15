import pandas as pd

# Load the dataset from the second sheet (assuming it's named "2011_data")
df_2011 = pd.read_excel("C:\\Users\\dhuma\\Downloads\\Copy of customer_transactions_sample.xlsx", sheet_name="Year 2010-2011")

# Convert 'InvoiceDate' to datetime format
df_2011['InvoiceDate'] = pd.to_datetime(df_2011['InvoiceDate'], format='%d-%m-%Y %H:%M')

# Calculate Recency (days since last purchase) for each customer
recency_2011 = df_2011.groupby('Customer ID')['InvoiceDate'].max()
recent_cutoff_2011 = recency_2011.max() - pd.Timedelta(days=180)  # Last 6 months of data
recency_2011 = (recency_2011.max() - recency_2011).dt.days.reset_index()
recency_2011.columns = ['Customer ID', 'Recency']

# Calculate Monetary (total spending) for each customer
df_2011['Monetary'] = df_2011['Quantity'] * df_2011['Price']  # Calculate Monetary
monetary_2011 = df_2011.groupby('Customer ID')['Monetary'].sum().reset_index()

# Merge Recency and Monetary into a single DataFrame
rm_merged_2011 = recency_2011.merge(monetary_2011, on='Customer ID')

# Set thresholds for Recency and Monetary
recency_threshold = 90  # Number of days without purchase
monetary_threshold = 1000  # Total spending threshold

# Filter customers based on Recency and Monetary thresholds
churn_candidates_2011 = rm_merged_2011[(rm_merged_2011['Recency'] > recency_threshold) & (rm_merged_2011['Monetary'] < monetary_threshold)]

# Add customer names and country
customer_info_2011 = df_2011[['Customer ID', 'Country']].drop_duplicates()

# Merge customer names and country with churn candidates
churn_candidates_info_2011 = churn_candidates_2011.merge(customer_info_2011, on='Customer ID')

# Display churn candidate information for 2011
print(churn_candidates_info_2011[['Customer ID', 'Country']])

# Export churn candidate information for 2011 to a new Excel file
churn_candidates_info_2011.to_excel("churn_candidates_info_2011.xlsx", index=False)
