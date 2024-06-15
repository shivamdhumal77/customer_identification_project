import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset (replace 'customer_data.xlsx' with the path to your dataset)
df = pd.read_excel("C:\\Users\\dhuma\\Downloads\\Copy of customer_transactions_sample.xlsx")

# Function to assign customer types based on RFM scores
def assign_customer_type(row):
    if row['Recency'] < 30:
        return 'Active'
    elif 30 <= row['Recency'] <= 90:
        return 'At Risk'
    elif 90 < row['Recency'] <= 180:
        return 'Potential Churn'
    elif 180 < row['Recency'] <= 365:
        return 'Churn Risk'
    else:
        return 'Inactive'

# Apply the function to create a new column 'Customer_Type'
df['Customer_Type'] = df.apply(assign_customer_type, axis=1)

# Identify customers likely to churn based on customer types
churn_candidates = df[df['Customer_Type'].isin(['Potential Churn', 'Churn Risk'])]

# Display the churn candidates' IDs in a table using Matplotlib
plt.figure(figsize=(10, 6))
plt.table(cellText=churn_candidates[['Customer_ID']].values,
          colLabels=['Customer ID'],
          cellLoc='center',
          loc='center',
          colWidths=[0.1] * len(churn_candidates.columns))
plt.title('Customers Likely to Churn')
plt.axis('off')
plt.show()
