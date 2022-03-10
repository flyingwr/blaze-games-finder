"""Util functions to calculate Double seeds"""
"""
	Everything on this script is based
	on Blaze formulas that can be found in
	this official code snippet of the company:
	https://codesandbox.io/s/lpjx3ko13z

	Official information can be found in
	https://blaze.com/pt/provably-fair/double
"""


import hashlib
import hmac


tiles = {
	0: "white",
	11: "black",
	5: "red",
	10: "black",
	6: "red",
	9: "black",
	7: "red",
	8: "black",
	1: "red",
	14: "black",
	2: "red",
	13: "black",
	3: "red",
	12: "black",
	4: "red"
}


"""hash of bitcoin block 570120 (https://medium.com/@blazedev/blaze-com-double-seeding-event-d3290ef13454)"""
salt = b"0000000000000000002aeb06364afc13b3c4d52767e8c91db8cdb39d8f71e8dd"


def get_previous_seeds(server_seed, amount):
	chain = [server_seed.encode()]
	for _ in range(amount):
		_hash = hashlib.sha256()
		_hash.update(chain[-1])
		chain.append(_hash.hexdigest().encode())
	return chain


def get_hashes(seed):
	_hash = hmac.new(seed, salt, hashlib.sha256).hexdigest()
	n = int(float.fromhex(_hash) % 15)
	return { "color": tiles[n], "roll": n, "server_seed": seed.decode(), "hash": _hash}
