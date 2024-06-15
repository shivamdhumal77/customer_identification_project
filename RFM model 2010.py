import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import seaborn as sns

# Load data from the Excel file
df = pd.read_excel("C:\\Users\\dhuma\\Downloads\\Copy of customer_transactions_sample.xlsx")

# Convert 'InvoiceDate' to datetime format
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], format='%d-%m-%Y %H:%M')

# Calculate year for each invoice
df['Year'] = df['InvoiceDate'].dt.year

# Focus on data for year 2010
df_2010 = df[df['Year'] == 2010]

# Calculate Recency (days since last purchase in 2010) for each customer
last_purchase = df_2010.groupby('Customer ID')['InvoiceDate'].max()
recency_2010 = (last_purchase.max() - last_purchase).dt.days.reset_index()
recency_2010.columns = ['Customer ID', 'Recency']

# Calculate Frequency (number of transactions in 2010) for each customer
frequency_2010 = df_2010.groupby('Customer ID').size().reset_index(name='Frequency')

# Calculate Monetary (total spending in 2010) for each customer
df_2010['TotalPrice'] = df_2010['Quantity'] * df_2010['Price']
monetary_2010 = df_2010.groupby('Customer ID')['TotalPrice'].sum().reset_index()
monetary_2010.columns = ['Customer ID', 'Monetary']

# Merge Recency, Frequency, and Monetary into a single DataFrame
rfm_2010 = recency_2010.merge(frequency_2010, on='Customer ID').merge(monetary_2010, on='Customer ID')

# Perform K-Means clustering on the RFM data
kmeans = KMeans(n_clusters=4, random_state=42)
rfm_2010['Cluster'] = kmeans.fit_predict(rfm_2010[['Recency', 'Frequency', 'Monetary']])

# Define customer types based on clusters
def get_customer_type(cluster):
    if cluster == 0:
        return 'High Value Customers'
    elif cluster == 1:
        return 'Low Value Customers'
    elif cluster == 2:
        return 'Medium Value Customers'
    else:
        return 'New Customers'

rfm_2010['Customer Type'] = rfm_2010['Cluster'].apply(get_customer_type)

# Plot the bar graph to visualize recency distribution by customer types
plt.figure(figsize=(10, 6))

# Define colors for each customer type
colors = {'High Value Customers': 'blue', 
          'Low Value Customers': 'red', 
          'Medium Value Customers': 'orange', 
          'New Customers': 'green'}

# Plot the bar graph using a single color for each type
ax = rfm_2010['Customer Type'].value_counts().plot(kind='bar', color=[colors[x] for x in rfm_2010['Customer Type']], edgecolor='black')

# Add values above each bar
for p in ax.patches:
    ax.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))

plt.xlabel('Customer Type')
plt.ylabel('Number of Customers')
plt.title('Recency Distribution by Customer Types (2010)')
plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for readability
plt.grid(axis='y', linestyle='--', alpha=0.7)  # Add grid lines on y-axis
plt.tight_layout()  # Adjust spacing for better readability
plt.show()

# Scatter Plot of RFM Clusters
plt.figure(figsize=(10, 6))
sns.scatterplot(data=rfm_2010, x='Recency', y='Monetary', hue='Customer Type', palette=colors)
plt.title('RFM Segmentation (2010)')
plt.xlabel('Recency')
plt.ylabel('Monetary')
plt.grid(True)
plt.tight_layout()
plt.show()

# Display the first few rows of the RFM table
print(rfm_2010.head())
