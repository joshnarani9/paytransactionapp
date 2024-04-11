"""
author@joshnarani
"""

import os

import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

def get_model(model_name='paraphrase-distilroberta-base-v1', cache_folder='.cache/sentence_transformers'):
    model_path = os.path.join(cache_folder, model_name)
    if os.path.exists(model_path):
        model = SentenceTransformer(model_path)
    else:
        model = SentenceTransformer(model_name, cache_folder=cache_folder)
    return model

model = get_model()
transactions_df = pd.read_csv('transactions.csv')
users_df = pd.read_csv('users.csv')
user_names = users_df['name'].dropna().str.lower().values
user_embeddings = model.encode(user_names)

def find_matching_users(transaction_id):
    try:
        transaction_description = transactions_df.loc[transactions_df['id'] == transaction_id, 'description'].values[0]
        transaction_name = extract_name_from_description(transaction_description).lower()
        transaction_embedding = model.encode([transaction_name])[0]
        similarity_scores = cosine_similarity([transaction_embedding], user_embeddings)[0]
        matches_df = pd.DataFrame({
            'name': user_names,
            'match_metric': similarity_scores
        })
        matches_df.sort_values(by='match_metric', ascending=False, inplace=True)
        matched_users = matches_df.to_dict(orient='records')
        total_matches = len(matched_users)
        return {'users': matched_users, 'total_number_of_matches': total_matches}
    except FileNotFoundError:
        return {'error': 'File not found. Please check file paths.'}
    except (IndexError, KeyError, TypeError):
        return {'error': 'Invalid transaction ID or data format.'}
    except Exception as e:
        return {'error': str(e)}


def extract_name_from_description(description):
    description_lower = description.lower()
    parts = description_lower.split('for ')
    if len(parts) > 1:
        name_part = parts[0]
    else:
        name_part = description_lower
    if 'from ' in name_part:
        name = name_part.split('from ')[1].split(',')[0].strip()
    else:
        name = name_part.strip()
    return name
