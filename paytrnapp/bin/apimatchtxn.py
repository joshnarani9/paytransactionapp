"""
author@joshnarani
"""

import pandas as pd
import torch
from transformers import BertTokenizer, BertModel

transactions_df = pd.read_csv('transactions.csv').drop_duplicates()
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

# Preprocess transactions data
transaction_tokens = tokenizer(list(transactions_df['description']), add_special_tokens=True, return_tensors='pt',
                               padding=True, truncation=True)
with torch.no_grad():
    transaction_embeddings = model(**transaction_tokens)[0].mean(dim=1)  # Average pooling over tokens


def find_similar_transactions(input_string):
    input_tokens = tokenizer.encode(input_string, add_special_tokens=True, return_tensors='pt')
    with torch.no_grad():
        input_embedding = model(input_tokens)[0].mean(dim=1)
    similarities = torch.cosine_similarity(input_embedding, transaction_embeddings).tolist()
    similar_transactions = [{'id': row.id, 'similarity': similarity} for row, similarity in
                            zip(transactions_df.itertuples(), similarities)]

    return {'transactions': similar_transactions, 'total_number_of_tokens_used': len(input_tokens)}
