import pandas as pd

df=pd.read_csv("transactions.csv")
dfusers=pd.read_csv("users.csv")
# print(df.head())
# print(dfusers.head())
# print(df.describe())
# print(dfusers.isnull().sum())
vals=df[df["id"]=="mkcUo5Z7"]['description'].values[0]
parts=vals.split('for ')
print(parts[0].split('from ')[1].strip())

import torch
def calculate_similarity_batch(batch_transaction_embeddings):
    return torch.cosine_similarity(input_embedding, batch_transaction_embeddings).tolist()


# Parallelize similarity calculation using joblib
similarity_scores = Parallel(n_jobs=-1)(delayed(calculate_similarity_batch)(transaction_embeddings[i:i + 100])
                                        for i in range(0, len(transaction_embeddings), 100))
similarity_scores = [score for batch_scores in similarity_scores for score in batch_scores]
similar_transactions = [{'id': row.id, 'similarity': similarity} for row, similarity in
                        zip(transactions_df.itertuples(), similarity_scores)]

app = Flask(__name__)
executor = ThreadPoolExecutor()

@app.route('/api/match_users', methods=['POST'])
def match_users():
    transaction_id = request.args.get('transaction_id')
    future = executor.submit(find_matching_users, transaction_id)
    return jsonify(result=future.result())

import asyncio

app = Flask(__name__)

@app.route('/api/match_users', methods=['POST'])
async def match_users():
    transaction_id = request.args.get('transaction_id')
    result = await asyncio.to_thread(find_matching_users, transaction_id)
    return jsonify(result)