
from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback

pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-9b74736c-b244-11ea-afa6-debb908608d9'
pnconfig.publish_key = 'pub-c-559c320d-2803-499d-90ae-0630c2040afb'

pubnub = PubNub(pnconfig)

TEST_CHANNEL = 'TEST_CHANNEL'

pubnub.subscribe().channels([TEST_CHANNEL]).execute()


class Listener(SubscribeCallback):
	def message(self, pubnub, message_object):
		print(f'\n-- Incoming message_object: {message_object}')


pubnub.add_listener(Listener())


def main():
	pubnub.publish().channel(TEST_CHANNEL).message({'foo':'bar'}).sync()

if __name__ == '__main__':
	main()