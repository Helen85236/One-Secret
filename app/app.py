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

	secret = request.json['secret']
	key = request.json['key']

	crypted_secret = crypt.encrypt(secret, key)
	crypted_secret['url'] = uuid.uuid4().hex

	try:
		database.insert_one(crypted_secret)
		return crypted_secret['url']
	except Exception as e:
		print(e)
		return 'Something went wrong with database', 500


@app.route('/secrets/<string:secret_url>')
def secrets(secret_url):
	"""
	Using 'key' in GET request to
	decrypt secret with AES 256 algorithm
	Then, delete secret from the database
	"""

	if s := database.find_one({"url": secret_url}):
		key = request.args.get('key')
		decrypted_s = crypt.decrypt(s, key)
		database.delete_one(s)

		return decrypted_s
	else:
		return 'Not Found', 404


if __name__ == '__main__':
	app.run()
