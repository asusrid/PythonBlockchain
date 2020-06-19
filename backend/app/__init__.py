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

	return jsonify(blockchain.chain[-1].to_json())







# by default on port 5000
# app.run()
app.run(port=5001)