import pandas as pd
import os

# Load the Excel file
file_path = './mWater_usage/username_hanwash_mwater.xlsx'
data = pd.read_excel(file_path)

# Clean up the HTML escape characters (e.g., `-&gt;` becomes `->`)
data['Branch'] = data['Branch'].str.replace('&gt;', '>')

# Create a unique user_ID based on the Username column
data['user_ID'] = data['Username'].astype('category').cat.codes

# Split the branch information on '->' to extract different committees
data['Committees'] = data['Branch'].apply(lambda x: list(set([item.strip() for item in x.split('->')])))

# Get a list of all unique committees/subcommittees across the dataset
unique_committees = sorted(set([item for sublist in data['Committees'] for item in sublist]))

# Create a column for each unique committee
for committee in unique_committees:
    data[committee] = data['Committees'].apply(lambda x: 'Yes' if committee in x else 'No')

# Drop the temporary 'Committees' column for tidiness
data.drop(columns=['Committees'], inplace=True)

# Create a 'reports' directory if it doesn't exist
output_dir = './mWater_usage/reports'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Define the output file path
output_file = os.path.join(output_dir, 'user_mwater_data.xlsx')

# Export the final table to Excel
data.to_excel(output_file, index=False)

print(f"Final table exported to: {output_file}")
