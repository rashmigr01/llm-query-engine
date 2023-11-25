from qdrant_client import QdrantClient
from qdrant_client.http import models
import pandas as pd
import json

def delete_index(client, index_name):
    client.delete_collection(collection_name=index_name)
    print(f"Index '{index_name}' deleted successfully.")

def create_index(client, index_name, dimension):
    client.create_collection(
        collection_name=index_name,
        vectors_config=models.VectorParams(size=dimension, distance=models.Distance.COSINE)
    )
    print(f"Index '{index_name}' created successfully.")

def upsert_vectors(client, index_name, json_path, meta_path):
    with open(json_path, 'r') as json_file:
        payload = json.load(json_file)

    vectors = payload["vectors"]
    ids = payload["ids"]

    with open(meta_path, 'r') as meta_file:
        meta = json.load(meta_file)
    
    total_vectors = len(ids)
    print(f"Total vectors to upsert: {total_vectors}")

    for i, (vector, id, meta_info) in enumerate(zip(vectors, ids, meta)):

        point = models.PointStruct(
            id=id,
            payload=meta_info,
            vector=vector
        )

        client.upsert(collection_name=index_name, points=[point])

        print(f"Vector {i+1}/{total_vectors} upserted successfully.")

if __name__ == "__main__":

    index_name = 'product_embeddings'
    dimension = 768
    json_path = './qdrant_payload.json'
    meta_path = './metadata.json'

    client = QdrantClient(
                            url="https://e274dc64-5827-4dd7-b39c-df002a2b34d2.us-east4-0.gcp.cloud.qdrant.io:6333", 
                            api_key="uA29yEhCIXweeTV6ZDuCRSEms2hjICwfi6HLEBfwduJJH2ye4pjeYQ",
                        )

    create_index(client, index_name, dimension)
    upsert_vectors(client, index_name, json_path, meta_path)
