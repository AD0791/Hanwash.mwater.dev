import pandas as pd

# Dictionary to store the table data for HANWASH Overall Performance
hanwash_overall_data = {
    'title': [
        'HANWASH Logframe & indicators progression',
        'Commune Action Plans',
        #'Progress towards the indicators',
        'Investment status',
        'Lessons Learned'
    ],
    'shared_links': [
        'https://go.mwater.co/logframe_and_indicators',  # Placeholder for HANWASH Logframe link
        'https://go.mwater.co/commune_action_plan',  # Placeholder for Commune Action Plans link
        #'',  # Placeholder for Progress towards the indicators link
        '---',  # Placeholder for Investment status link
        '---'   # Placeholder for Lessons Learned link
    ],
    'authorization': ['HANWASH USER'] * 4  # All have the same authorization
}

# Create a pandas DataFrame
df = pd.DataFrame(hanwash_overall_data)

# Combine title and link in a format that might be more useful in mWater
df['combined'] = df['title'] + ': ' + df['shared_links']

# Display the DataFrame
print(df)

# Export to Excel
excel_file = './ui/components/hanwash_overall_sharedlinks.xlsx'
df.to_excel(excel_file, index=False)
print(f"\nData exported to {excel_file}")

# Display the combined column, which might be what you'd use in mWater
print("\nCombined data (title: link) for potential use in mWater:")
print(df['combined'].to_string(index=False))
