import os
import random

from flask import Flask, jsonify
from backend.blockchain.blockchain import Blockchain
from backend.pubsub import PubSub



app = Flask(__name__)
blockchain = Blockchain()
pubsub = PubSub()



@app.route('/')
def route_default():
	return 'Welcome to the blockchain'

@app.route('/blockchain')
def route_blockchain():
	return jsonify(blockchain.to_json())

@app.route('/blockchain/mine')
def route_blockchain_mine():
	tx_data = 'tx_data'
	blockchain.add_block(tx_data)

	block = blockchain.chain[-1]
	pubsub.broadcast_block(block)

	return jsonify(block.to_json())


PORT = 5000

if os.environ.get('PEER') == 'True':
	PORT = random.randint(5001, 6000)

# by default on port 5000
# app.run()
app.run(port=PORT)