
from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback

from backend.blockchain.block import Block

pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-9b74736c-b244-11ea-afa6-debb908608d9'
pnconfig.publish_key = 'pub-c-559c320d-2803-499d-90ae-0630c2040afb'



CHANNELS = {
	'TEST': 'TEST',
	'BLOCK': 'BLOCK'
}


class Listener(SubscribeCallback):

	def __init__(self, blockchain):
		self.blockchain = blockchain

	def message(self, pubnub, message_object):
		print(f'\n-- Channel: {message_object.channel} | Message: {message_object.message}')

		if message_object.channel == CHANNELS['BLOCK']:
			block = Block.from_json(message_object.message)
			potential_chain = self.blockchain.chain[:]
			potential_chain.append(block)

			try:
				self.blockchain.replace_chain(potential_chain)
			except Exception as e:
				print(f'\n Did not replace chain: {e}')

class PubSub():
	"""
	Handles the pub/sub layer of the app
	Provides communication between the nodes of the blockain net
	"""
	def __init__(self, blockchain):
		self.pubnub = PubNub(pnconfig)
		self.pubnub.subscribe().channels(CHANNELS.values()).execute()
		self.pubnub.add_listener(Listener(blockchain))

	def publish(self, channel, message):
		"""
		Publish the message object to the channel
		"""
		self.pubnub.publish().channel(channel).message(message).sync()

	def broadcast_block(self, block):
		"""
		Broadcast a block instance to all net
		"""
		self.publish(CHANNELS['BLOCK'], block.to_json())


def main():
	pubsub = PubSub()
	pubsub.publish(CHANNELS['TEST'], {'foo':'bar'})
	

if __name__ == '__main__':
	main()