import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file into a DataFrame
file_path = 'dataset_dex.csv'  # Replace with the actual path to your CSV file
df = pd.read_csv(file_path)

# Convert 'BlockTimestamp' to datetime with explicit format
df['BlockTimestamp'] = pd.to_datetime(df['BlockTimestamp'], format='%Y-%m-%d %H:%M:%S %z UTC')

# Filter rows based on MethodName
methods_to_include = ["swapExactTokensForTokens", "swapNATIVEForExactTokens", "swapExactTokensForTokens", "swapExactTokensForNATIVESupportingFeeOnTransferTokens", "swapTokensForExactNATIVE", "swapNATIVEForExactTokens", "swapTokensForExactTokens", "swapExactNATIVEForTokensSupportingFeeOnTransferTokens", "swapExactTokensForTokensSupportingFeeOnTransferTokens"]
filtered_df = df[df['MethodName'].isin(methods_to_include)]

# Calculate the average TxFee and number of transactions per day
result_df = filtered_df.groupby(filtered_df['BlockTimestamp'].dt.date).agg({
    'TxFee(NativeToken)': ['median', 'mean'],
}).reset_index()

# Plotting
fig, ax = plt.subplots(figsize=(10, 6))

# Plot Median
ax.plot(result_df['BlockTimestamp'], result_df.xs(('TxFee(NativeToken)', 'median'), axis=1), label='Median TxFee in Native Token')

# Plot Mean
ax.plot(result_df['BlockTimestamp'], result_df.xs(('TxFee(NativeToken)', 'mean'), axis=1), label='Mean TxFee in Native Token')

ax.set_title('Dex Swap TxFee in AVAX - Median, Mean')
ax.set_xlabel('Date')
ax.set_ylabel('TxFee (AVAX)')
ax.legend()
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()
