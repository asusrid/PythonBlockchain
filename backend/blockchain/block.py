
import time
from backend.util.crypto_hash import crypto_hash
from backend.util.hex_to_binary import hex_to_binary
from backend.config import MINE_RATE

GENESIS_DATA = {
	'timestamp': 1, 
	'last_hash': 'genesis_last_hash',
	'hash': 'genesis_hash',
	'data': [],
	'difficulty': 3,
	'nonce': 'genesis_nonce'
}


class Block:

	"""
	Block: unit of storage
	Store tx in a blockchain that supports a cryptocurrency.
	"""
	def __init__(self, timestamp, last_hash, hash, data, difficulty, nonce):
		self.timestamp = timestamp
		self.last_hash = last_hash
		self.hash = hash
		self.data = data
		self.difficulty = difficulty
		self.nonce = nonce

	def __repr__(self):
		return (
			'Block('
			f'Timestamp: {self.timestamp}, '
			f'Last_hash: {self.last_hash}, '
			f'Hash: {self.hash}, '
			f'Data: {self.data}, '
			f'Difficulty: {self.difficulty}, '
			f'Nonce: {self.nonce})'
		)

	@staticmethod
	def mine_block(last_block, data):
		"""
		Mine a block on the given last_block and data, until a block
		hash is found to have the same leading 0s than the proof of work 
		difficulty
		"""
		timestamp = time.time_ns()
		last_hash = last_block.hash
		difficulty = Block.adjust_difficulty(last_block, timestamp)
		nonce = 0
		hash = crypto_hash(timestamp, last_hash, data, difficulty, nonce)

		while hex_to_binary(hash)[0:difficulty] != '0'* difficulty:
			nonce += 1
			timestamp = time.time_ns()
			difficulty = Block.adjust_difficulty(last_block, timestamp)
			hash = crypto_hash(timestamp, last_hash, data, difficulty, nonce)

		return Block(timestamp, last_hash, hash, data, difficulty, nonce)

	@staticmethod
	def genesis():
		"""
		Generate the genesis block
		"""
		# return Block(
		# 	GENESIS_DATA['timestamp'],
		# 	GENESIS_DATA['last_hash'],
		# 	GENESIS_DATA['hash'],
		# 	GENESIS_DATA['data']
		# )
		return Block(**GENESIS_DATA)

	@staticmethod
	def adjust_difficulty(last_block, new_timestamp):
		"""
		Compute the adjusted difficulty according to the MINE_RATE
		Increase difficulty if blocks were mined too quickly
		Decrease difficulty if blocks were mined too slowly
		"""
		if (new_timestamp - last_block.timestamp) < MINE_RATE:
			return last_block.difficulty + 1

		if (last_block.difficulty - 1) > 0:
			return last_block.difficulty - 1

		return 1


def main():
	genesis_block = Block.genesis()
	block = Block.mine_block(genesis_block, 'foo')
	print(block)

if __name__ == '__main__':
	main()






