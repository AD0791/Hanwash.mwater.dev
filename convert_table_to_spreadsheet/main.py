import pandas as pd
from bs4 import BeautifulSoup
import os

def convert_html_table_to_excel(html_path, excel_path):
    """
    Parses an HTML file to find the first table, extracts its data,
    and saves it to an Excel (.xlsx) file.

    Args:
        html_path (str): The file path for the input HTML file.
        excel_path (str): The file path for the output Excel file.
    """
    # Check if the HTML file exists
    if not os.path.exists(html_path):
        print(f"Error: The file '{html_path}' was not found.")
        return

    try:
        # Read the HTML file with UTF-8 encoding
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, 'lxml')

        # Find the first table in the HTML.
        # You can make this more specific if you have multiple tables,
        # e.g., by finding a table with a specific ID or class:
        # table = soup.find('table', {'id': 'my-table-id'})
        table = soup.find('table')

        if not table:
            print("Error: No table found in the HTML file.")
            return

        # --- Extract Table Headers ---
        # Find all header cells (th) in the table's header section (thead)
        headers = []
        for th in table.find('thead').find_all('th'):
            # Extract text and strip any leading/trailing whitespace
            headers.append(th.get_text(strip=True))

        # --- Extract Table Rows ---
        # Find all rows (tr) in the table's body section (tbody)
        rows = []
        for tr in table.find('tbody').find_all('tr'):
            # For each row, find all data cells (td) and extract their text
            cells = [td.get_text(strip=True) for td in tr.find_all('td')]
            rows.append(cells)

        # Create a pandas DataFrame from the headers and rows
        df = pd.DataFrame(rows, columns=headers)

        # --- Save DataFrame to Excel ---
        # Use the to_excel method to save the data.
        # index=False prevents pandas from writing row indices to the file.
        df.to_excel(excel_path, index=False, engine='openpyxl')

        print(f"Successfully converted the table from '{html_path}' to '{excel_path}'")

    except Exception as e:
        print(f"An error occurred: {e}")

# --- Main execution block ---
if __name__ == "__main__":
    # Define the input and output file names.
    # The script will look for this HTML file in the same directory.
    input_html_file = 'customer_pignon_saep.html'
    
    # This will be the name of the generated Excel file.
    output_excel_file = 'customer_pignon_saep_data.xlsx'

    # Call the conversion function
    convert_html_table_to_excel(input_html_file, output_excel_file)
