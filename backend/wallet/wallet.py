import uuid
import json
from backend.config import STARTING_BALANCE
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes


class Wallet:
	"""
	An individiual wallet for a miner.
	Keep track of the miner's balance.
	Allows the miner to auth tx.
	"""
	def __init__(self):
		self.address = str(uuid.uuid4())[0:8]
		self.balance = STARTING_BALANCE
		self.private_key = ec.generate_private_key(
			ec.SECP256K1(),
			default_backend()
		)
		self.public_key = self.private_key.public_key()

	def sign(self, data):
		"""
		Generate a signature based on the data using the local private key.
		"""
		return self.private_key.sign(
			json.dumps(data).encode('utf-8'), 
			ec.ECDSA(hashes.SHA256())
		)


def main():
	wallet = Wallet()
	print(f'wallet.__dict__: {wallet.__dict__}')

	data = {'foo': 'bar'}
	signature = wallet.sign(data)
	print(f'signature: {signature}')
 
if __name__ == '__main__':
	main()