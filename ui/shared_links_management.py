import pandas as pd

# Dictionary to store the table data
mwater_data = {
    'title': [
        'mWater M&E System',
        'Cavaillon Dashboard',
        'Leogane Dashboard',
        'Terre-Neuve Dashboard',
        'Ferrier Dashboard',
        'Pignon Dashboard',
        'HANWASH Overall Performance Dashboard'
    ],
    'shared_links': [
        'https://share.mwater.co/v3/console_link/145f59f97cd64e5e86fab7ecf98530ad?share=4ed30ce04ed7410e8a987ac55e480697',
        '',  # Placeholder for Cavaillon Dashboard link
        '',  # Placeholder for Leogane Dashboard link
        '',  # Placeholder for Terre-Neuve Dashboard link
        '',  # Placeholder for Ferrier Dashboard link
        '',  # Placeholder for Pignon Dashboard link
        ''   # Placeholder for HANWASH Overall Performance Dashboard link
    ],
    'authorization': [
        'M&E Team',
        'HANWASH USER',
        'HANWASH USER',
        'HANWASH USER',
        'HANWASH USER',
        'HANWASH USER',
        'HANWASH USER'
    ]
}

# Create a pandas DataFrame
df = pd.DataFrame(mwater_data)

# Combine title and link in a format that might be more useful in mWater
df['combined'] = df['title'] + ': ' + df['shared_links']

# Display the DataFrame
print(df)

# Export to Excel
excel_file = './ui/components/mwater_sharedlinks.xlsx'
df.to_excel(excel_file, index=False)
print(f"\nData exported to {excel_file}")

# Display the combined column, which might be what you'd use in mWater
print("\nCombined data (title: link) for potential use in mWater:")
print(df['combined'].to_string(index=False))