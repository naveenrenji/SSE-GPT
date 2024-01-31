# auth.py
from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_pymongo import PyMongo
from flask_jwt_extended import create_access_token
import datetime

auth = Blueprint('auth', __name__)
bcrypt = Bcrypt()
mongo = PyMongo()

@auth.route('/register', methods=['POST'])
def register():
    print("reached")
    # Get data from request
    email = request.json.get('email')
    password = request.json.get('password')

    # Check if user already exists
    if mongo.db.users.find_one({'email': email}):
        return jsonify({"error": "Email already in use"}), 400

    # Hash password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Create new user
    mongo.db.users.insert_one({'email': email, 'password': hashed_password})

    return jsonify({"message": "User registered successfully"}), 201

@auth.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    user = mongo.db.users.find_one({'email': email})

    if user and bcrypt.check_password_hash(user['password'], password):
        # Create JWT token
        expires = datetime.timedelta(days=1)
        access_token = create_access_token(identity=email, expires_delta=expires)
        return jsonify({"token": access_token}), 200

    return jsonify({"error": "Invalid credentials"}), 401
