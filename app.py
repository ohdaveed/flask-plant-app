from flask import Flask, jsonify, g
from flask_cors import CORS

from resources.plants import plant

import models

DEBUG = True
PORT = 8000

# Initialize an instance of the Flask class.
# This starts the website!
app = Flask(__name__)

@app.before_request # decorator function, that runs before a function
def before_request():
	"""Connect to the database before each request."""
	g.db = models.DATABASE
	g.db.connect()

@app.after_request
def after_request(response):
	"""Close the database connection after each request."""
	g.db.close()
	return response # returning the reponse back to the client, in our
	# case it will be some type of jsonfiy()

CORS(plant, origins=['http://localhost:3000'],supports_credentials=True)

app.register_blueprint(plant, url_prefix='/api/v1/plants')

# The default URL ends in / ("my-website.com/").
@app.route('/')
def index():
	return 'hi'

# Run the app when the program starts!
if __name__ == '__main__':
	models.initialize()
	app.run(debug=DEBUG, port=PORT)