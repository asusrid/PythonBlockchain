from flask import Flask
from backend.blockchain.blockchain import Blockchain

app = Flask(__name__)
blockchain = Blockchain()

for i in range(3):
	blockchain.add_block(i)

@app.route('/')
def route_default():
	return 'Welcome to the blockchain'

@app.route('/blockchain')
def route_blockchain():
	return blockchain.chain.__repr__()

# by default on port 5000
# app.run()
app.run(port=5001)