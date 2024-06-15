import pandas as pd
import matplotlib.pyplot as plt

# Load data from the Excel file (assuming the data is in the second sheet)
df = pd.read_excel("C:\\Users\\dhuma\\Downloads\\Copy of customer_transactions_sample.xlsx", sheet_name=1)

# Group by product description and sum the quantity sold
product_sales = df.groupby('Description')['Quantity'].sum()

# Find the top 10 selling products
top_10_products = product_sales.nlargest(10)

# Plot the top 10 selling products in a bar graph
plt.figure(figsize=(10, 6))
ax = top_10_products.plot(kind='bar', color='skyblue', edgecolor='black')
plt.xlabel('Product Description')
plt.ylabel('Total Quantity Sold')
plt.title('Top 10 Selling Products of the Year')
plt.xticks(rotation=45, ha='right')

# Add actual values on top of each bar
for i in ax.patches:
    plt.text(i.get_x() + i.get_width() / 2, i.get_height() + 5, str(int(i.get_height())), ha='center', va='bottom')

plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
