from backend.util.hex_to_binary import hex_to_binary

def test_hext_to_binary():
	number = 123
	hex_number = hex(number)[2:]
	my_bin_num = hex_to_binary(hex_number)

	assert int(my_bin_num, 2) == number