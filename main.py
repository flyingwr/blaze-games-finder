"""Fetch the last games of Double (blaze.com) by calculating their seeds"""
from utils import calc_double_seed, get_previous_seeds

import aiohttp
import asyncio

try:
	import ujson as json
except ImportError:
	import json

blaze_api_games_url = "https://blaze.com/api/roulette_games/recent"

seeds_amount = 1000 # Amount of seeds to calculate

async def main():
	async with aiohttp.ClientSession() as session:
		async with session.get(blaze_api_games_url) as response:
			if response.ok:
				data = await response.json() # Supposed to be a list
				if len(data) > 0:
					seed = data[0].get("server_seed") # Last game of Double is first in list
					if seed:
						with open("./last_games.json", "w+") as f:
							result = list(map(calc_double_seed, get_previous_seeds(seed, seeds_amount)))
							json.dump(result, f)

						print(f"Successfully calculated a total of {len(result)} seeds")
					else:
						print("Invalid data: `server_seed` parameter not found")
				else:
					print("Failed to parse data because it's empty")
			else:
				print("Blaze API sent an error response")

if __name__ == "__main__":
	asyncio.run(main())