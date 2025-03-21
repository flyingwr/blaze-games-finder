"""Util functions to calculate Double seeds"""
"""
	Everything on this script is based
	on Blaze formulas that can be found in
	these official code snippets of the company:
	https://codesandbox.io/s/o5orm2mmrq
	https://codesandbox.io/p/sandbox/kymc9p

	Official information can be found in:
	https://blaze.com/pt/provably-fair/crash
	https://blaze.com/pt/provably-fair/double
"""
from math import floor
from typing import AnyStr, Dict, List, Literal, Union

import hashlib
import hmac

type RollColor = Literal["black", "red", "white"]

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

"""the hash of bitcoin block 570128 (https://medium.com/@blazedev/blaze-com-crash-seeding-event-v2-d774d7aeeaad)"""
crash_salt = b"0000000000000000000415ebb64b0d51ccee0bb55826e43846e5bea777d91966"

"""hash of bitcoin block 823307 (https://bitcointalk.org/index.php?topic=5479580.msg63404290#msg63404290)"""
double_salt = b"0000000000000000000292453e3be843129d4a0fb13f6249935524225b545c7b"

def get_previous_seeds(server_seed: AnyStr, amount: int) -> List[bytes]:
	"""Get the seeds prior to `server_seed`"""
	if isinstance(server_seed, str):
		server_seed = server_seed.encode()

	chain = [server_seed]
	for _ in range(amount):
		_hash = hashlib.sha256(chain[-1]).hexdigest().encode()
		chain.append(_hash)
	return chain

def divisible(_hash: bytes, mod: int) -> bool:
	"""Check if a crash hash is divisible by `mod`"""
	hash_len = len(_hash)

	result = 0

	o = hash_len % 4
	i = o - 4 if o > 0 else 0
	while i < hash_len:
		result <<= 16
		result += int(_hash[i:i + 4], 16)
		result %= mod

		i += 4

	return result == 0

def get_point(_hash: bytes) -> float:
	"""Calculate a crash point with its hash"""
	if divisible(_hash, 15):
		return 0

	h = int(_hash[0:int(52 / 4)], 16)
	e = 2 ** 52

	return float(f"{(floor((100 * e - h) / (e - h)) / 100):.02f}")

def calc_crash_seed(seed: AnyStr) -> Dict[str, Union[float, str]]:
	"""Calculate the hash of `seed` in order to parse the obtained hash,
		resulting in the stats (crash_point and server_seed) of it"""
	if isinstance(seed, str):
		seed = seed.encode()

	_hash = hmac.new(seed, crash_salt, hashlib.sha256).hexdigest().encode()
	return { "crash_point": get_point(_hash), "server_seed": seed.decode() }

def calc_double_seed(seed: AnyStr) -> Dict[str, Union[int, str]]:
	"""Calculate the hash of `seed` in order to parse the obtained hash,
		resulting in the stats (color, roll number and server_seed) of it"""
	if isinstance(seed, str):
		seed = seed.encode()

	integ = int(hmac.new(seed, double_salt, hashlib.sha256).hexdigest(), 16)
	randval = integ / 2 ** 256
	n = int(randval * 15)
	return { "color": tiles[n], "roll": n, "server_seed": seed.decode() }

def count_roll_occurrences(
	seed: str,
	rounds: int,
	color: RollColor | None = None,
	roll: int | None = None,
	sequence: int | None = None,
	pattern: list[RollColor] | list[int] | None = None
) -> int:
	"""Counts occurrences of a specific roll or color in past Double rounds,
	optionally checking for consecutive occurrences or a specific color pattern."""

	if pattern is not None:
		key = "color" if all(isinstance(item, str) for item in pattern) else "roll"
		rolls = [
			roll[key]
			for roll in map(calc_double_seed, get_previous_seeds(seed, rounds))
		]
		plen = len(pattern)
		return sum(rolls[i : i + plen] == pattern for i in range(len(rolls) - plen + 1))

	if color is None and roll is None:
		raise ValueError("Please specify either 'color' or 'roll' parameter")

	key = "color" if color is not None else "roll"
	target = color if color is not None else roll

	rolls = [
		roll[key]
		for roll in map(calc_double_seed, get_previous_seeds(seed, rounds))
	]

	if sequence is None:
		return rolls.count(target)

	return sum(
		rolls[i : i + sequence] == [target] * sequence
		for i in range(len(rolls) - sequence + 1)
	)