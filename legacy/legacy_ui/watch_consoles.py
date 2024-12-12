import pandas as pd

# Dictionary to store the table data for HANWASH Overall Performance
watch_data = {
    'title': [
        'Adopt-A-Well',
        'HANWASH Performance Indicators',
        'SAEP Monthly Report',
        'Commune Action Plan',
    ],
    'shared_links': [
        'https://go.mwater.co/adopt_a_well',  # Placeholder for Investment status link
        'https://go.mwater.co/logframe_and_indicators',  # Placeholder for HANWASH Logframe link
        'https://go.mwater.co/saep_monthly_report',   # Placeholder for Lessons Learned link
        'https://go.mwater.co/commune_action_plan',  # Placeholder for Commune Action Plans link
    ],
    'authorization': ['HANWASH USER'] * 4  # All have the same authorization
}

# Create a pandas DataFrame
df = pd.DataFrame(watch_data)

# Combine title and link in a format that might be more useful in mWater
df['combined'] = df['title'] + ': ' + df['shared_links']

# Display the DataFrame
print(df)

# Export to Excel
excel_file = './ui/components/watch_sharedlinks.xlsx'
df.to_excel(excel_file, index=False)
print(f"\nData exported to {excel_file}")

# Display the combined column, which might be what you'd use in mWater
print("\nCombined data (title: link) for potential use in mWater:")
print(df['combined'].to_string(index=False))
