import pandas as pd
import spacy

def preprocess_text(text):
    doc = nlp(text)
    tokens = [token.text.lower() for token in doc if token.is_alpha]
    return ' '.join(tokens)

if __name__ == "__main__":
    csv_path = './BigBasketProducts.csv'
    df = pd.read_csv(csv_path)

    text_data = (df['product'] + ' ' + df['description']).astype(str)
    text_data = text_data.replace({pd.NA: ''})

    nlp = spacy.load('en_core_web_sm')
    preprocessed_data = text_data.apply(preprocess_text)

    preprocessed_data.to_csv('./preprocessed_data.csv', index=False)
