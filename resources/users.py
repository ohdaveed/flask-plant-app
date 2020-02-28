import models
from flask import Blueprint, jsonify, request
from flask_bcrypt import check_password_hash, generate_password_hash
from flask_login import current_user, login_user
from playhouse.shortcuts import model_to_dict

# make this a blueprint
users = Blueprint("users", "users")

# @users.route('/', methods=['GET'])
# def test_user_controller():
#   return "hi you have a user resource"


@users.route("/register", methods=["POST"])
def register():
    # this is like grabbing req.body in a var
    payload = request.get_json()

    payload["username"].lower()  # emails are case insensitive in the world

    try:
        # don't create the user if it already exists
        # this is analogous to User.find({username: req.body.username)
        models.User.get(models.User.username == payload["username"])

        # if we didn't just throw an error, the user must already exist
        return (
            jsonify(
                data={},
                status={
                    "code": 401,
                    "message": "A user with that email already exists",
                },
            ),
            401,
        )

    except models.DoesNotExist:
        # if the user wasn't there this "error" would happen, which means
        # we're safe to go ahead and register them

        # encrypt pw with bcrypt
        # note: we are replacing pw in the payload dict with the hashed pw
        payload["password"] = generate_password_hash(payload["password"])

        # register them in the db
        # note the ** is like the spread oper in JS (...)
        # shorthand for writing out all the properties like we did in dog create
        user = models.User.create(**payload)

        # this is where we
        # actually use flask-login
        # this "logs in" the user, and starts a session
        login_user(user)

        user_dict = model_to_dict(user)

        # check out the user we created
        print(user_dict)

        # we're gonna send this back to client, they don't need pw, so why risk it?
        del user_dict["password"]

        return (
            jsonify(
                data=user_dict,
                status={
                    "code": 201,
                    "message": "Successfully registered {}".format(user_dict["username"]),
                },
            ),
            201,
        )


@users.route("/", methods=["GET"])
def list_users():
    users = models.User.select()
    for u in users:
        print(u)

        # subscriptable baseically just means something can be made into a dict

        user_dicts = [model_to_dict(u) for u in users]

        # lets delete the passwords for fun well see how map() in python
        # define our callback

        def remove_password(u):
            u.pop("password")
            return u

        user_dicts_without_pw = list(map(remove_password, user_dicts))

        return jsonify(data=user_dicts_without_pw), 200


@users.route('/login', methods=['POST'])
def login():
    payload = request.get_json()

    try:
        # look up user by username
        user = models.User.get(models.User.username == payload['username'])

        # so we can acces the info in username

        user_dict = model_to_dict(user)

        # check user's password using bcrypt

        if(check_password_hash(user_dict['password'], payload['password'])):

            # user can move forward

            login_user(user)

            del user_dict['password']

            return jsonify(data=user_dict, status={'code': 200, 'message': "successfully logged in {}".format(user_dict['username'])}), 200
    else:
        print('password aint correct')
        return jsonify(data={}, status={'code': 401, 'message': "Email or password is incorrect"}), 401


@users.route("/logged_in", methods=["GET"])
def get_logged_in_user():

    if not current_user.is_authenticated:
        return jsonify(data={}, status={
            'code': 401,
            'message': "no user is currently logged in"
        }), 401
    else:
        print(current_user)  # inspect just prints current user's ID
        print(type(current_user))  # what is a werkzeug anyway?
        user_dict = model_to_dict(current_user)
        print(user_dict)
        user_dict.pop('password')
        return jsonify(data=user_dict, status={
            'code': 200,
            'message': "Current user is {}".format(user_dict['username'])
        }), 200
