"""Fetch the last games of Double (blaze.com) by calculating their seeds"""


from utils import get_hashes, get_previous_seeds


import aiohttp
import asyncio
import websockets
import ujson


client_session = None


blaze_ws_url = "wss://api-v2.blaze.com/replication/?EIO=3&transport=websocket"
blaze_api_games_url = "https://blaze.com/api/roulette_games/{}"


seeds_amount = 1000 # Amount of seeds to calculate


async def parse_payload(payload):
	data = None

	_id = payload["id"]

	async with client_session.get(blaze_api_games_url.format(_id)) as response:
		if response.status == 200:
			data = await response.json()

	if data:
		seed = data.get("server_seed")
		if seed:
			chain = get_previous_seeds(seed, seeds_amount)
			with open("./last_games.json", "w+") as f:
				ujson.dump(list(map(get_hashes, chain)), f)
		else:
			print(f"Seed of roll with id `{_id}` was not found.")


async def receive_message(ws):
	while True:
		message = await ws.recv()
		if isinstance(message, str):
			if "roulette.update" in message:
				payload = ujson.loads(message[2:])[1]["payload"]
				if payload["status"] == "complete":
					await parse_payload(payload)

			await ws.send("2")


async def main():
	global client_session
	client_session = aiohttp.ClientSession()

	print("Running websockets...")

	async for ws in websockets.connect(blaze_ws_url):
		try:
			await ws.send('420["cmd",{"id":"subscribe","payload":{"room":"chat_room_2"}}]')
			await ws.send('421["cmd",{"id":"subscribe","payload":{"room":"roulette"}}]')

			print("Connection established.")

			await receive_message(ws)
		except websockets.ConnectionClosed:
			continue


if __name__ == "__main__":
	asyncio.run(main())
