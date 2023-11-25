import pandas as pd
import json

def csv_to_json(csv_path, json_path):
    embeddings = pd.read_csv(csv_path)

    ids = embeddings['id'].tolist()

    vectors = embeddings.drop('id', axis=1).values.tolist()

    payload = {"vectors": vectors, "ids": ids}

    with open(json_path, 'w') as json_file:
        json.dump(payload, json_file, indent=4)  # Adds indentation for better readability

if __name__ == "__main__":
    csv_path = './modified_embeddings.csv'
    json_path = 'qdrant_payload.json'
    csv_to_json(csv_path, json_path)
