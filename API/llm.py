from transformers import AutoTokenizer, AutoModel, T5Tokenizer, T5ForConditionalGeneration
from qdrant_client import QdrantClient
import torch
import json
import os
from dotenv import load_dotenv

class LanguageModel:
    def __init__(self, index_name="product_embeddings"):
        load_dotenv()

        qdrant_url = os.getenv("QDRANT_URL")
        qdrant_api_key = os.getenv("QDRANT_API_KEY")

        self.client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
        self.index_name = index_name

    def text_to_vector(self, text):
        model_name = 'bert-base-uncased'
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModel.from_pretrained(model_name)
        
        tokens = tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=512)
        with torch.no_grad():
            outputs = model(**tokens)
        embeddings = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
        return embeddings
    
    def generate_answer(self, question, payload):

        tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-small", legacy=False)
        model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-small")

        input_text = f"Answer the Question: {question}\nConsidering the information: {json.dumps(payload)}"

        input_ids = tokenizer(input_text, return_tensors="pt").input_ids

        outputs = model.generate(input_ids, max_length=200)
        answer = tokenizer.decode(outputs[0], skip_special_tokens=True)

        return answer


    def generate_contextual_answer(self, text):
        query_vector = self.text_to_vector(text)

        search_result = self.client.search(
            collection_name=self.index_name,
            query_vector=query_vector,
            limit=5,
            with_payload=True
        )

        # for i in range(5):
        #     print(search_result[i].payload['product'])
        #     print(search_result[i].score)

        if search_result and search_result[0]:
            relevant_payload = search_result[0].payload

            answer = self.generate_answer(text, relevant_payload)
        else:
            answer = "This question is outside the bounds of the information available! Try something else!"

        return answer
