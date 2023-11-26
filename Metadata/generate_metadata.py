import pandas as pd
import json

csv_path = './BigBasketProducts.csv'
original_data = pd.read_csv(csv_path)

metadata_columns = ['product', 'category', 'sub_category', 'brand', 'type', 'description', 'sale_price', 'market_price', 'rating']

metadata = []
for _, row in original_data.iterrows():
    metadata_dict = {col: row[col] if not pd.isna(row[col]) else "missing" for col in metadata_columns}
    metadata.append(metadata_dict)

metadata_json_path = '../Qdrant/metadata.json'
with open(metadata_json_path, 'w') as json_file:
    json.dump(metadata, json_file)

print("Metadata created successfully.")
