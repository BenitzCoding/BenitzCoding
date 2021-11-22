import os
import beni
import requests
from beni import generation

TOKEN = os.getenv()
beni = generation(version=2.3, debug=True)

@beni.listen('started')
async def start():
	print("BenitzCoding activated")

@beni.listen('command', prefix="b!")
async def command_listener(command, *, args):
	payload = {
		"token": os.getenv("API_TOKEN"),
		"command": command,
		"args": args
	}
	response = requests.post(os.getenv("API") + "/command-handle").json()
	await beni.respond_with(content=response["action"])
	log_payload = {
		"request_payload": payload,
		"response_payload": response,
		"timestamp": beni.now()
	}
	await beni.log(log_payload)

@beni.listen('message')
async def listener(message):
	payload = {
		"token": os.getenv("API_TOKEN"),
		"message": message
	}
	response = requests.post(os.getenv("API") + "/process-message").json()
	await beni.respond_with(content=response["action"])
	log_payload = {
		"request_payload": payload,
		"response_payload": response,
		"timestamp": beni.now()
	}
	await beni.log(log_payload)

@beni.listen('interaction')
async def interact(action, expectation):
	output = beni.process_interaction(action)
	if output != expectation:
		log_payload = {
			"action": action,
			"expectation": expectation,
			"timestamp": beni.now()
		}
		await beni.log(log_payload)

	else:
		await beni.respond_with(action=action)

beni.run(generated_beni=beni, token=TOKEN)
