import pandas as pd

# Load the dataset
df = pd.read_excel("C:\\Users\\dhuma\\Downloads\\Copy of customer_transactions_sample.xlsx")

# Convert 'InvoiceDate' to datetime format
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], format='%d-%m-%Y %H:%M')

# Calculate Recency (days since last purchase) for each customer
recency = df.groupby('Customer ID')['InvoiceDate'].max()
recent_cutoff = recency.max() - pd.Timedelta(days=180)  # Last 6 months of data
recency = (recency.max() - recency).dt.days.reset_index()
recency.columns = ['Customer ID', 'Recency']

# Calculate Monetary (total spending) for each customer
df['Monetary'] = df['Quantity'] * df['Price']  # Calculate Monetary
monetary = df.groupby('Customer ID')['Monetary'].sum().reset_index()

# Merge Recency and Monetary into a single DataFrame
rm_merged = recency.merge(monetary, on='Customer ID')

# Set thresholds for Recency and Monetary
recency_threshold = 90  # Number of days without purchase
monetary_threshold = 1000  # Total spending threshold

# Filter customers based on Recency and Monetary thresholds
churn_candidates = rm_merged[(rm_merged['Recency'] > recency_threshold) & (rm_merged['Monetary'] < monetary_threshold)]

# Add customer names and country
customer_info = df[['Customer ID', 'Country']].drop_duplicates()

# Merge customer names and country with churn candidates
churn_candidates_info = churn_candidates.merge(customer_info, on='Customer ID')

# Display churn candidate information
print(churn_candidates_info[['Customer ID', 'Country']])

# Export churn candidate information to a new Excel file
churn_candidates_info.to_excel("churn_candidates_info.xlsx", index=False)
