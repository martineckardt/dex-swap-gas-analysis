import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file into a DataFrame
file_path = 'dataset_inscription.csv'  # Replace with the actual path to your CSV file
df = pd.read_csv(file_path)

# Convert 'BlockTimestamp' to datetime with explicit format
df['BlockTimestamp'] = pd.to_datetime(df['BlockTimestamp'], format='%Y-%m-%d %H:%M:%S %z UTC')

# Filter rows based on MethodHash
method_hash_to_include = "0x64617461"
filtered_df = df[(df['MethodHash'] == method_hash_to_include) & (df['BlockTimestamp'] >= '2023-12-13')]

# Drop duplicates based on 'TxHash'
filtered_df = filtered_df.drop_duplicates(subset='TxHash')

# Group by date and calculate the mean, max, and min TxFee(NativeToken) for each day
result_df = filtered_df.groupby(filtered_df['BlockTimestamp'].dt.date).agg({
    'TxFee(NativeToken)': ['median', 'mean']
}).reset_index()

# Plotting
fig, ax = plt.subplots(figsize=(10, 6))

# Plot Mean TxFee
ax.plot(result_df['BlockTimestamp'], result_df['TxFee(NativeToken)', 'median'], label='Median TxFee')

# Plot Max TxFee
ax.plot(result_df['BlockTimestamp'], result_df['TxFee(NativeToken)', 'mean'], label='Mean TxFee')

ax.set_title('Inscription TxFee in AVAX')
ax.set_xlabel('Date')
ax.set_ylabel('TxFee (AVAX)')
ax.legend()
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()
