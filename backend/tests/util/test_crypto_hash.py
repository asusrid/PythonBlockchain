from backend.util.crypto_hash import crypto_hash

def test_crypto_hash():
	assert crypto_hash(1, "one", [1]) == crypto_hash("one", [1], 1)
	assert crypto_hash('foo') == 'b2213295d564916f89a6a42455567c87c3f480fcd7a1c15e220f17d7169a790b'


