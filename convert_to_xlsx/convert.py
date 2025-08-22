
import pandas as pd

csv_file_path = '/home/alexandrod/Desktop/Hanwash.mwater.dev/hanwash_cavaillon_check.csv'
xlsx_file_path = '/home/alexandrod/Desktop/Hanwash.mwater.dev/convert_to_xlsx/hanwash_cavaillon_check.xlsx'

df = pd.read_csv(csv_file_path)
df.to_excel(xlsx_file_path, index=False)

print(f'Successfully converted {csv_file_path} to {xlsx_file_path}')
