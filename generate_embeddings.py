from tqdm import tqdm
from transformers import AutoTokenizer, AutoModel
import torch
import pandas as pd

def generate_embeddings(texts):
    tokens = tokenizer(texts, return_tensors='pt', padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**tokens)
    embeddings = outputs.last_hidden_state.mean(dim=1).squeeze()
    return embeddings

if __name__ == "__main__":
    preprocessed_data = pd.read_pickle('./preprocessed_data.pkl')

    model_name = 'bert-base-uncased'
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)

    batch_size = 8
    embeddings = []

    for i in tqdm(range(0, len(preprocessed_data), batch_size), desc="Generating Embeddings", unit="batch"):
        batch_texts = preprocessed_data[i:i + batch_size].tolist()
        batch_embeddings = generate_embeddings(batch_texts)
        embeddings.append(batch_embeddings)

    embeddings_tensor = torch.cat(embeddings)
    embeddings_df = pd.DataFrame(embeddings_tensor.numpy())
    embeddings_df.to_csv('./embeddings.csv', index=False)
