import uuid
import json
from backend.config import STARTING_BALANCE
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature


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
		self.serialize_public_key()

	def sign(self, data):
		"""
		Generate a signature based on the data using the local private key.
		"""
		return self.private_key.sign(
			# transform to json and then encode so that any kind
			# of dataa is accepted
			json.dumps(data).encode('utf-8'), 
			ec.ECDSA(hashes.SHA256())
		)

	def serialize_public_key(self):
		"""
		Reset the public key to its serialize version
		"""
		self.public_key = self.public_key.public_bytes(
			encoding = serialization.Encoding.PEM,
			format = serialization.PublicFormat.SubjectPublicKeyInfo
		).decode('utf-8')

	@staticmethod
	def verify(public_key, data, signature):
		"""
		Verify a signature based on the original public key and data.
		"""
		deserialized_public_key = serialization.load_pem_public_key(
			public_key.encode('utf-8'),
			default_backend()
		)
		try:
			deserialized_public_key.verify(
				signature,
				json.dumps(data).encode('utf-8'), 
				ec.ECDSA(hashes.SHA256())
			)
			return True
		except InvalidSignature:
			return False




def main():
	wallet = Wallet()
	print(f'wallet.__dict__: {wallet.__dict__}')

	data = {'foo': 'bar'}
	signature = wallet.sign(data)
	print(f'signature: {signature}')

	is_valid = Wallet.verify(wallet.public_key, data, signature)
	print(f'is_valid: {is_valid}')

	is_not_valid = Wallet.verify(Wallet().public_key, data, signature)
	print(f'is_not_valid: {is_not_valid}')

 
if __name__ == '__main__':
	main()









