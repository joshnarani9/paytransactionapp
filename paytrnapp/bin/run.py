"""
author@joshnarani
"""

from flask import Flask, jsonify, request

from apimatchtxn import find_similar_transactions
from apimatchusers import find_matching_users

app = Flask(__name__)


@app.route('/api/match_users', methods=['GET'])
def match_users():
    transaction_id = request.args.get('transaction_id')
    result = find_matching_users(transaction_id)
    response=jsonify(result)
    response.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
    return response


@app.route('/api/match_txns', methods=['GET'])
def find_similar_transactions_handler():
    input_string = request.args.get('description')
    result = find_similar_transactions(input_string)
    response=jsonify(result)
    return response


if __name__ == '__main__':
    app.run(debug=True)

# http://127.0.0.1:5000/api/match_users?transaction_id=mkcUo5Z7
# inputstring ref ToCu6iXjX7jMACC//307338080372//CNTR From Hannah Wood for Deel,
# 127.0.0.1 - - [08/Mar/2024 00:41:17] "GET /api/find_similar_transactions?description=ref%20ToCu6iXjX7jMACC//307338080372//CNTR%20From%20Hannah%20Wood%20for%20Deel, HTTP/1.1" 200 -
