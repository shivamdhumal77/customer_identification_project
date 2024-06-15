import pandas as pd
import numpy as np

# Load sales data
sales_data = pd.read_excel("C:\\Users\\dhuma\\Downloads\\Copy of customer_transactions_sample.xlsx")

# Step 1: Calculate ABI index
def calculate_abi_index(sales_data):
    # Group sales data by InvoiceNo to get items bought together
    basket = sales_data.groupby('Invoice')['StockCode'].apply(list)
    
    # Initialize ABI index dictionary
    abi_index = {}
    
    # Iterate through each basket
    for items in basket:
        # Generate pairs of items bought together
        pairs = [(items[i], items[j]) for i in range(len(items)) for j in range(i+1, len(items))]
        
        # Update ABI index for each pair
        for pair in pairs:
            abi_index[pair] = abi_index.get(pair, 0) + 1
            
    # Calculate ABI index by dividing frequency of pairs by total transactions
    total_transactions = len(basket)
    for pair in abi_index:
        abi_index[pair] /= total_transactions
        
    return abi_index

# Step 2: Identify top 10 selling stock codes
def top_10_selling_stock_codes(sales_data):
    # Group sales data by StockCode and sum quantity sold
    stock_sales = sales_data.groupby('StockCode')['Quantity'].sum()
    
    # Sort stock codes by total quantity sold and get top 10
    top_10 = stock_sales.nlargest(10)
    
    return top_10.index

# Step 3: Find next best product for each top-selling product based on ABI index
def next_best_product(top_10, abi_index):
    # Initialize dictionary to store next best product for each top-selling product
    next_best = {}
    
    # Iterate through top 10 selling products
    for stock_code in top_10:
        # Filter ABI index dictionary to get pairs involving the current product
        pairs = {pair: abi_index[pair] for pair in abi_index if stock_code in pair}
        
        # Exclude pairs involving the current product itself
        pairs = {pair: pairs[pair] for pair in pairs if pair[0] != stock_code}
        
        # Find the product with the highest ABI index
        if pairs:
            next_best[stock_code] = max(pairs, key=pairs.get)[1]
        else:
            next_best[stock_code] = None
    
    return next_best

# Step 1: Calculate ABI index
abi_index = calculate_abi_index(sales_data)

# Step 2: Identify top 10 selling stock codes
top_10 = top_10_selling_stock_codes(sales_data)

# Step 3: Find next best product for each top-selling product
next_best = next_best_product(top_10, abi_index)

# Create table to display results
result_table = pd.DataFrame({'Top Selling Product': top_10,
                             'Next Best Product': [next_best[stock_code] for stock_code in top_10]})

print(result_table)
