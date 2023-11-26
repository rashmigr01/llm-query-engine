import pandas as pd

def modify_csv(input_csv, output_csv):

    df = pd.read_csv(input_csv)

    df.insert(0, 'id', range(1, len(df) + 1))

    df.to_csv(output_csv, index=False)

if __name__ == "__main__":
    input_csv_path = 'embeddings.csv'
    output_csv_path = 'modified_embeddings.csv'

    modify_csv(input_csv_path, output_csv_path)
