import models
from flask import Flask, g, jsonify
from flask_cors import CORS
from flask_login import LoginManager
from resources.plants import plants
from resources.users import users

DEBUG = True
PORT = 8000


login_manager = LoginManager()


# Initialize an instance of the Flask class.
# This starts the website!
app = Flask(__name__)

app.secret_key = "moomomoomomomomoom"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


@app.before_request  # decorator function, that runs before a function
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response  # returning the reponse back to the client, in our
    # case it will be some type of jsonfiy()


CORS(plants, origins=["http://localhost:3000"], supports_credentials=True)
CORS(users, origins=["http://localhost:3000"], supports_credentials=True)

app.register_blueprint(plants, url_prefix="/api/v1/plants")
app.register_blueprint(users, url_prefix="/api/v1/users")

# The default URL ends in / ("my-website.com/").
@app.route("/")
def index():
    return "hi"


# Run the app when the program starts!
if __name__ == "__main__":
    models.initialize()
    app.run(debug=DEBUG, port=PORT)
