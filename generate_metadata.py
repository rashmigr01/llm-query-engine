import pandas as pd
import json

csv_path = './BigBasketProducts.csv'
original_data = pd.read_csv(csv_path)

metadata_columns = ['category', 'brand']

metadata = []
for _, row in original_data.iterrows():
    metadata_dict = {col: row[col] if not pd.isna(row[col]) else "NaN" for col in metadata_columns}
    metadata.append(metadata_dict)

metadata_json_path = 'metadata.json'
with open(metadata_json_path, 'w') as json_file:
    json.dump(metadata, json_file)

print("Metadata created successfully.")
