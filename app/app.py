from flask import Flask, jsonify, json, request
from db import database
import crypt
import uuid


app = Flask(__name__)


@app.route('/generate', methods=['POST'])
def generate():
	"""
	Using JSON keys 'secret' and 'key' in POST request to
	encrypt client secret with AES 256 algorithm
	return random url using uuid library
	"""

	secret: str = ''
	key: str = ''

	if 'secret' in request.json:
		secret = request.json['secret']
	else:
		return 'secret is missing', 422

	if len(secret) < 1:
		return 'secret length < 1', 422

	if 'key' in request.json:
		key = request.json['key']
	else:
		return 'key is missing', 422

	if len(key) < 1:
		return 'key length < 1', 422

	crypted_secret: dict[str, str] = crypt.encrypt(secret, key)
	crypted_secret['url'] = uuid.uuid4().hex

	try:
		database.insert_one(crypted_secret)
		return crypted_secret['url']
	except Exception as e:
		print(e)
		return 'Something went wrong with the database', 500


@app.route('/secrets/<string:secret_url>')
def secrets(secret_url):
	"""
	Using JSON key 'key' in POST request to
	decrypt secret with AES 256 algorithm
	Then, delete secret from the database
	"""

	s: any = database.find_one({"url": secret_url})
	if s:
		key: str = ''

		if 'key' in request.json:
			key = request.json['key']
		else:
			return 'key is missing', 422

		if len(key) < 1:
			return 'key length < 1', 422

		try:
			decrypted_s: str = crypt.decrypt(s, key)
		except ValueError:
			return 'Wrong password!'

		database.delete_one(s)

		return decrypted_s
	else:
		return 'Not Found', 404


if __name__ == '__main__':
	app.run()
