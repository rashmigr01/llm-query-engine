import pandas as pd
import spacy

def preprocess_text(row):
    text_cols = ['product', 'category', 'sub_category', 'brand', 'type', 'description']
    numeric_cols = ['sale_price', 'market_price', 'rating']

    text = ' '.join(str(row[col]) for col in text_cols)
    doc_text = nlp(text)
    tokens_text = [token.text.lower() for token in doc_text if token.is_alpha]
    text_processed = ' '.join(tokens_text)

    numeric_info = ' '.join(str(row[col]) for col in numeric_cols)

    return f'{text_processed} {numeric_info}'

if __name__ == "__main__":

    csv_path = './BigBasketProducts.csv'
    df = pd.read_csv(csv_path)

    df = df.replace({pd.NA: ''})

    nlp = spacy.load('en_core_web_sm')
    
    preprocessed_data = df.apply(preprocess_text, axis=1)

    preprocessed_data.to_pickle('./preprocessed_data.pkl')
    preprocessed_data.to_csv('./preprocessed_data.csv', index=False)
