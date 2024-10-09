import pandas as pd

# Dictionary to store the table data for Pignon
pignon_data = {
    'title': [
        'Commune Action Plan',
        'Project performance',
        'Service providers performance',
        'Investment status',
        'Lessons Learned',
        #'Global Grants',
        #'Adopt A Well',
        #'CPEs',
        #'Professional Operators'
    ],
    'shared_links': [
        'https://go.mwater.co/pignon_cap',  # Placeholder for Commune Action Plan link
        '---',  # Placeholder for Project performance link
        '---',  # Placeholder for Service providers' performance link
        '---',  # Placeholder for Investment status link
        '---',  # Placeholder for Lessons Learned link
        #'',  # Placeholder for Global Grants link
        #'',  # Placeholder for Adopt A Well link
        #'',  # Placeholder for CPEs link
        #''   # Placeholder for Professional Operators link
    ],
    #'authorization': ['HANWASH USER'] * 9  # All have the same authorization
    'authorization': ['HANWASH USER'] * 5  # All have the same authorization
}

# Create a pandas DataFrame
df = pd.DataFrame(pignon_data)

# Combine title and link in a format that might be more useful in mWater
df['combined'] = df['title'] + ': ' + df['shared_links']

# Display the DataFrame
print(df)

# Export to Excel
excel_file = './ui/components/pignon_sharedlinks.xlsx'
df.to_excel(excel_file, index=False)
print(f"\nData exported to {excel_file}")

# Display the combined column, which might be what you'd use in mWater
print("\nCombined data (title: link) for potential use in mWater:")
print(df['combined'].to_string(index=False))
