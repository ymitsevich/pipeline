#!/usr/bin/env python3
"""
pandas Transforms: groupby, joins/merge, reshape
Learn by doing - run each section and observe the outputs
"""

import pandas as pd
import numpy as np

print("=" * 70)
print("PANDAS TRANSFORMS: GroupBy, Joins/Merge, Reshape")
print("=" * 70)

# =============================================================================
# 1. GROUPBY: Aggregating data by groups
# =============================================================================
print("\n" + "=" * 70)
print("1. GROUPBY OPERATIONS")
print("=" * 70)

# Sample sales data
sales_data = {
    'date': ['2025-01-01', '2025-01-01', '2025-01-02', '2025-01-02', '2025-01-03'],
    'region': ['North', 'South', 'North', 'South', 'North'],
    'product': ['Widget', 'Gadget', 'Widget', 'Widget', 'Gadget'],
    'sales': [100, 150, 200, 120, 180],
    'quantity': [10, 15, 20, 12, 18]
}
df_sales = pd.DataFrame(sales_data)
df_sales['date'] = pd.to_datetime(df_sales['date'])

print("\nOriginal sales data:")
print(df_sales)

# Basic groupby with single aggregation
print("\n--- Basic groupby: Total sales by region ---")
sales_by_region = df_sales.groupby('region')['sales'].sum()
print(sales_by_region)

# Multiple aggregations
print("\n--- Multiple aggregations: sum, mean, count ---")
region_stats = df_sales.groupby('region').agg({
    'sales': ['sum', 'mean', 'count'],
    'quantity': 'sum'
})
print(region_stats)

# Multiple group columns
print("\n--- Group by multiple columns: region + product ---")
region_product_sales = df_sales.groupby(['region', 'product'])['sales'].sum()
print(region_product_sales)

# Reset index to convert back to regular DataFrame
print("\n--- Reset index for easier use ---")
print(region_product_sales.reset_index())

# Custom aggregation functions
print("\n--- Custom aggregation: range (max - min) ---")
sales_range = df_sales.groupby('region')['sales'].agg(
    total='sum',
    average='mean',
    sales_range=lambda x: x.max() - x.min()
)
print(sales_range)

# Transform: apply function and return same-sized result
print("\n--- Transform: normalize sales within each region ---")
df_sales['sales_pct_of_region'] = df_sales.groupby('region')['sales'].transform(
    lambda x: x / x.sum() * 100
)
print(df_sales[['region', 'sales', 'sales_pct_of_region']])

# Filter groups
print("\n--- Filter: only regions with total sales > 250 ---")
high_sales_regions = df_sales.groupby('region').filter(lambda x: x['sales'].sum() > 250)
print(high_sales_regions)


# =============================================================================
# 2. JOINS/MERGE: Combining DataFrames
# =============================================================================
print("\n\n" + "=" * 70)
print("2. JOINS/MERGE OPERATIONS")
print("=" * 70)

# Sample data: customers and orders
customers = pd.DataFrame({
    'customer_id': [1, 2, 3, 4],
    'name': ['Alice', 'Bob', 'Charlie', 'Diana'],
    'city': ['NYC', 'LA', 'Chicago', 'Boston']
})

orders = pd.DataFrame({
    'order_id': [101, 102, 103, 104, 105],
    'customer_id': [1, 2, 1, 3, 5],  # Note: customer 5 doesn't exist in customers
    'amount': [250, 180, 320, 150, 400]
})

print("\nCustomers:")
print(customers)
print("\nOrders:")
print(orders)

# Inner join (default) - only matching records
print("\n--- Inner join: only customers with orders ---")
inner = pd.merge(customers, orders, on='customer_id', how='inner')
print(inner)

# Left join - all customers, even without orders
print("\n--- Left join: all customers, orders if available ---")
left = pd.merge(customers, orders, on='customer_id', how='left')
print(left)

# Right join - all orders, even if customer unknown
print("\n--- Right join: all orders, customer info if available ---")
right = pd.merge(customers, orders, on='customer_id', how='right')
print(right)

# Outer join - everything
print("\n--- Outer join: all customers and all orders ---")
outer = pd.merge(customers, orders, on='customer_id', how='outer')
print(outer)

# Merge on different column names
products = pd.DataFrame({
    'prod_id': ['W1', 'G1', 'W2'],
    'product_name': ['Widget A', 'Gadget B', 'Widget C']
})

inventory = pd.DataFrame({
    'product_code': ['W1', 'G1', 'D1'],
    'stock': [50, 30, 20]
})

print("\n--- Merge on different column names ---")
merged_products = pd.merge(
    products, 
    inventory, 
    left_on='prod_id', 
    right_on='product_code',
    how='left'
)
print(merged_products)

# Merge with suffixes for overlapping columns
df1 = pd.DataFrame({
    'id': [1, 2, 3],
    'value': [10, 20, 30]
})

df2 = pd.DataFrame({
    'id': [1, 2, 4],
    'value': [100, 200, 400]
})

print("\n--- Merge with suffixes for overlapping columns ---")
merged_suffix = pd.merge(df1, df2, on='id', how='outer', suffixes=('_left', '_right'))
print(merged_suffix)


# =============================================================================
# 3. RESHAPE: pivot, melt, stack/unstack
# =============================================================================
print("\n\n" + "=" * 70)
print("3. RESHAPE OPERATIONS")
print("=" * 70)

# Sample time-series data
time_data = pd.DataFrame({
    'date': ['2025-01-01', '2025-01-01', '2025-01-02', '2025-01-02'],
    'metric': ['revenue', 'cost', 'revenue', 'cost'],
    'value': [1000, 600, 1200, 650]
})
print("\nOriginal time-series data (long format):")
print(time_data)

# PIVOT: long to wide format
print("\n--- Pivot: convert long to wide format ---")
wide = time_data.pivot(index='date', columns='metric', values='value')
print(wide)

# MELT: wide to long format
print("\n--- Melt: convert wide back to long format ---")
long = wide.reset_index().melt(id_vars='date', var_name='metric', value_name='value')
print(long)

# Pivot table with aggregation
sales_pivot_data = pd.DataFrame({
    'date': ['2025-01-01', '2025-01-01', '2025-01-01', '2025-01-02', '2025-01-02'],
    'region': ['North', 'North', 'South', 'North', 'South'],
    'product': ['Widget', 'Gadget', 'Widget', 'Widget', 'Widget'],
    'sales': [100, 150, 200, 120, 180]
})

print("\n\nSales data for pivot table:")
print(sales_pivot_data)

print("\n--- Pivot table: region vs product with sales sum ---")
pivot_table = pd.pivot_table(
    sales_pivot_data,
    values='sales',
    index='region',
    columns='product',
    aggfunc='sum',
    fill_value=0
)
print(pivot_table)

# Add totals to pivot table
print("\n--- Pivot table with margins (totals) ---")
pivot_with_totals = pd.pivot_table(
    sales_pivot_data,
    values='sales',
    index='region',
    columns='product',
    aggfunc='sum',
    fill_value=0,
    margins=True,
    margins_name='Total'
)
print(pivot_with_totals)

# Stack/Unstack
print("\n--- Stack: columns to rows ---")
stacked = pivot_table.stack()
print(stacked)

print("\n--- Unstack: rows to columns ---")
unstacked = stacked.unstack()
print(unstacked)


# =============================================================================
# 4. EXERCISES
# =============================================================================
print("\n\n" + "=" * 70)
print("4. PRACTICE EXERCISES")
print("=" * 70)

# Create sample e-commerce dataset
np.random.seed(42)
exercise_data = pd.DataFrame({
    'order_id': range(1, 21),
    'customer_id': np.random.choice([101, 102, 103, 104], 20),
    'category': np.random.choice(['Electronics', 'Clothing', 'Books'], 20),
    'amount': np.random.randint(50, 500, 20),
    'date': pd.date_range('2025-01-01', periods=20, freq='D')
})

customer_info = pd.DataFrame({
    'customer_id': [101, 102, 103, 104],
    'name': ['Alice', 'Bob', 'Charlie', 'Diana'],
    'tier': ['Gold', 'Silver', 'Gold', 'Bronze']
})

print("\nExercise data - Orders:")
print(exercise_data.head(10))
print("\nCustomer info:")
print(customer_info)

print("\n" + "-" * 70)
print("EXERCISE 1: Find total amount spent by each customer")
print("-" * 70)
# YOUR CODE HERE:
ex1_solution = exercise_data.groupby('customer_id')['amount'].sum()
print(ex1_solution)

print("\n" + "-" * 70)
print("EXERCISE 2: Find average order amount by category")
print("-" * 70)
# YOUR CODE HERE:
ex2_solution = exercise_data.groupby('category')['amount'].mean()
print(ex2_solution)

print("\n" + "-" * 70)
print("EXERCISE 3: Merge orders with customer info (include customer name and tier)")
print("-" * 70)
# YOUR CODE HERE:
ex3_solution = pd.merge(exercise_data, customer_info, on='customer_id', how='left')
print(ex3_solution[['order_id', 'name', 'tier', 'category', 'amount']].head(10))

print("\n" + "-" * 70)
print("EXERCISE 4: Create pivot table - customer vs category, showing total amount")
print("-" * 70)
# YOUR CODE HERE:
ex4_solution = pd.pivot_table(
    ex3_solution,
    values='amount',
    index='name',
    columns='category',
    aggfunc='sum',
    fill_value=0
)
print(ex4_solution)

print("\n" + "-" * 70)
print("EXERCISE 5: Find customers who spent more than $1000 total")
print("-" * 70)
# YOUR CODE HERE:
ex5_solution = exercise_data.groupby('customer_id').filter(lambda x: x['amount'].sum() > 1000)
ex5_customers = ex5_solution['customer_id'].unique()
print(f"Customer IDs with total spending > $1000: {ex5_customers}")

print("\n" + "-" * 70)
print("EXERCISE 6: Add column showing each order as % of customer's total spending")
print("-" * 70)
# YOUR CODE HERE:
exercise_data['pct_of_customer_total'] = exercise_data.groupby('customer_id')['amount'].transform(
    lambda x: (exercise_data.loc[x.index, 'amount'] / x.sum() * 100)
)
print(exercise_data[['order_id', 'customer_id', 'amount', 'pct_of_customer_total']].head(10))


# =============================================================================
# BONUS: Combining multiple operations
# =============================================================================
print("\n\n" + "=" * 70)
print("BONUS: COMPLEX TRANSFORMATION PIPELINE")
print("=" * 70)

print("\nTask: Find top-spending customer in each tier")
print("Steps: merge → groupby → sort → select top")

# Solution
result = (
    ex3_solution
    .groupby(['tier', 'name'])['amount']
    .sum()
    .reset_index()
    .sort_values('amount', ascending=False)
    .groupby('tier')
    .head(1)
    .sort_values('amount', ascending=False)
)

print("\nTop spender by tier:")
print(result)

print("\n" + "=" * 70)
print("COMPLETED! Review the outputs above.")
print("=" * 70)
print("\nKey takeaways:")
print("  • groupby: aggregate, transform, filter")
print("  • merge: inner/left/right/outer joins")
print("  • pivot: long ↔ wide format conversions")
print("  • Combine operations for complex analysis")

