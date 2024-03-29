
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

	def __eq__(self, other):
		return self.__dict__ == other.__dict__


	def to_json(self):
		"""
		Serialize the block into a dict of its attributes
		"""
		return self.__dict__

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
	def from_json(block_json):
		"""
		Deserialize a block's json representation back into block instance.
		"""
		return Block(**block_json)

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

	@staticmethod
	def is_valid_block(last_block, block):
		"""
		Validate a block following these rules:
		1. The block must have the correct reference to the last_hash
		2. The block must meet the PoW
		3. The difficulty must only be increased by 1
		4. The block hash must be a combination of the block fields
		"""
		if block.last_hash != last_block.hash:
			raise Exception("The reference to the last_hash is incorrect!")
		
		if hex_to_binary(block.hash)[0:block.difficulty] != '0'*block.difficulty:
			raise Exception("The PoW is not met!")
		
		if abs(last_block.difficulty - block.difficulty) > 1:
			raise Exception("The difficulty must only be increased by 1!")
		
		regenerated_hash = crypto_hash(
			block.timestamp,
			block.last_hash,
			block.data,
			block.difficulty,
			block.nonce
		)

		if block.hash != regenerated_hash:
			raise Exception("The block hash is not created based on the block fields!")



def main():
	genesis_block = Block.genesis()
	bad_block = Block.mine_block(genesis_block, 'foo')
	bad_block.data = 'evil_data'

	try:
		Block.is_valid_block(genesis_block, bad_block)
	except Exception as e:
		print(f'is_valid_block: {e}')

if __name__ == '__main__':
	main()






