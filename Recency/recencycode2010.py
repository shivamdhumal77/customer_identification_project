import pandas as pd
import matplotlib.pyplot as plt

# Load data from the Excel file
df = pd.read_excel("C:\\Users\\dhuma\\Downloads\\Copy of customer_transactions_sample.xlsx")

# Convert 'InvoiceDate' to datetime format
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], format='%d-%m-%Y %H:%M')

# Calculate year for each invoice
df['Year'] = df['InvoiceDate'].dt.year

# Focus on data for year 2010
df_2010 = df[df['Year'] == 2010]

# Calculate Recency (days since last purchase in 2010) for each customer
recency_2010 = (df_2010.groupby('Customer ID')['InvoiceDate'].max().max() - df_2010.groupby('Customer ID')['InvoiceDate'].max()).dt.days

# Define customer types based on recency
def get_customer_type(recency):
    if recency <= 30:
        return 'Active (loyal) Customers'
    elif 30 < recency <= 90:
        return ' Less Active customers'
    elif 90 < recency <= 180:
        return 'Potential Churn Customers'
    elif 180 < recency <= 365:
        return 'Churn Risk Customers'
    else:
        return 'Inactive Customers'

# Apply function to calculate customer types
customer_types_2010 = recency_2010.apply(get_customer_type)

# Plot the bar graph to visualize recency distribution by customer types
plt.figure(figsize=(10, 6))

# Plot the bar graph using a single color
ax = customer_types_2010.value_counts().plot(kind='bar', color='skyblue', edgecolor='black')

# Add values above each bar
for i in ax.patches:
    plt.text(i.get_x() + i.get_width() / 2, i.get_height() + 5, str(int(i.get_height())), ha='center', va='bottom')

plt.xlabel('Customer Type')
plt.ylabel('Number of Customers')
plt.title('Recency Distribution by Customer Types (2010)')
plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for readability
plt.grid(axis='y', linestyle='--', alpha=0.7)  # Add grid lines on y-axis
plt.tight_layout()  # Adjust spacing for better readability
plt.show()
