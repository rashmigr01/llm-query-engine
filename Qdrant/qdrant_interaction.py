from qdrant_client import QdrantClient
from qdrant_client.http import models
import json
import os
from dotenv import load_dotenv

def delete_index(client, index_name):
    client.delete_collection(collection_name=index_name)
    print(f"Index '{index_name}' deleted successfully.")

def create_index(client, index_name, dimension):
    client.create_collection(
        collection_name=index_name,
        vectors_config=models.VectorParams(size=dimension, distance=models.Distance.COSINE)
    )
    print(f"Index '{index_name}' created successfully.")

def upsert_vectors(client, index_name, json_path, meta_path, batch_size=100):
    with open(json_path, 'r') as json_file:
        payload = json.load(json_file)

    vectors = payload["vectors"]
    ids = payload["ids"]

    with open(meta_path, 'r') as meta_file:
        meta = json.load(meta_file)
    
    total_vectors = len(ids)
    print(f"Total vectors to upsert: {total_vectors}")

    for i in range(0, total_vectors, batch_size):
        batch_vectors = vectors[i:i+batch_size]
        batch_ids = ids[i:i+batch_size]
        batch_meta = meta[i:i+batch_size]

        batch_points = [
            models.PointStruct(id=id, payload=meta_info, vector=vector)
            for vector, id, meta_info in zip(batch_vectors, batch_ids, batch_meta)
        ]

        client.upsert(collection_name=index_name, points=batch_points)

        print(f"Vectors {i+1}-{min(i+batch_size, total_vectors)} upserted successfully.")

if __name__ == "__main__":
    index_name = 'product_embeddings'
    dimension = 768
    json_path = './qdrant_payload.json'
    meta_path = './metadata.json'

    load_dotenv()

    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")

    client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key, timeout=100)

    #delete_index(client, index_name)
    create_index(client, index_name, dimension)
    upsert_vectors(client, index_name, json_path, meta_path, batch_size=100)
