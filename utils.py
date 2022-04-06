"""Util functions to calculate Double seeds"""
"""
	Everything on this script is based
	on Blaze formulas that can be found in
	this official code snippet of the company:
	https://codesandbox.io/s/lpjx3ko13z

	Official information can be found in
	https://blaze.com/pt/provably-fair/double
"""
from typing import AnyStr, ByteString, List

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

def get_previous_seeds(server_seed: AnyStr, amount: int) -> List[ByteString]:
	"""Get the seeds prior to `server_seed`"""
	if isinstance(server_seed, str):
		server_seed = server_seed.encode()

	chain = [server_seed]
	for _ in range(amount):
		_hash = hashlib.sha256()
		_hash.update(chain[-1])
		chain.append(_hash.hexdigest().encode())
	return chain

def calc_seed(seed: AnyStr):
	"""Calculate the hash of `seed` in order to parse the obtained hash,
		resulting in the stats (color, roll number and server_seed) of it"""
	if isinstance(seed, str):
		seed = seed.encode()

	n = int(float.fromhex(hmac.new(seed, salt, hashlib.sha256).hexdigest()) % 15)
	return { "color": tiles[n], "roll": n, "server_seed": seed.decode() }