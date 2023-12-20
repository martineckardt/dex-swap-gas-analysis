import pandas as pd

# Load the CSV file into a DataFrame
file_path = 'dataset_dex.csv'  # Replace with the actual path to your CSV file
df = pd.read_csv(file_path)

# Convert 'BlockTimestamp' to datetime with explicit format
df['BlockTimestamp'] = pd.to_datetime(df['BlockTimestamp'], format='%Y-%m-%d %H:%M:%S %z UTC')

# Filter rows based on MethodName
methods_to_include = ["swapExactTokensForTokens", "swapNATIVEForExactTokens", "swapExactTokensForTokens", "swapExactTokensForNATIVESupportingFeeOnTransferTokens", "swapTokensForExactNATIVE", "swapNATIVEForExactTokens", "swapTokensForExactTokens", "swapExactNATIVEForTokensSupportingFeeOnTransferTokens", "swapExactTokensForTokensSupportingFeeOnTransferTokens"]
filtered_df = df[df['MethodName'].isin(methods_to_include)]

# Group by date and calculate the average TxFee and number of transactions for each method individually
result_df = filtered_df.groupby([filtered_df['BlockTimestamp'].dt.date, 'MethodName']).agg({
    'TxFee(NativeToken)': 'mean',
    'TxFee(USD)': 'mean',
    'TxHash': 'count'  # Counting the number of transactions
}).rename(columns={'TxHash': 'Number_of_Transactions'}).reset_index()

# Calculate totals for all filtered transactions per day
total_per_day_df = filtered_df.groupby(filtered_df['BlockTimestamp'].dt.date).agg({
    'TxFee(NativeToken)': 'sum',
    'TxFee(USD)': 'sum',
    'TxHash': 'count'  # Counting the number of transactions
}).rename(columns={'TxHash': 'Total_Number_of_Transactions'}).reset_index()

# Display the results
print("Average TxFee and Number of Transactions per day for each method individually:")
print(result_df)

print("\nTotal TxFee and Number of Transactions per day:")
print(total_per_day_df)
