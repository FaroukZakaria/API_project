import datetime, bcrypt
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required
from project.db import *
from flask import request, jsonify, Blueprint, current_app
from project.controllers.user_controller import *

user_routes = Blueprint('user_routes', __name__)


@user_routes.route('/signup', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if users_collection.find_one({'name': name}):
        return jsonify({'message': 'Username already exists'}), 400
    
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    
    create_user(User(
        name=name,
        email=email,
        password=hashed_password
        ))
    return jsonify({'message': 'User registered successfully'}), 201

@user_routes.route('/signin', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = get_user_by_email(email)
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        access_token = create_access_token(str(user['_id']), expires_delta=datetime.timedelta(minutes=15))
        refresh_token = create_refresh_token(str(user['_id']), expires_delta=datetime.timedelta(days=7))
        return jsonify({'access_token': access_token, 'refresh_token': refresh_token}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@user_routes.route('/refresh-token', methods=['POST'])
def refresh_token():
    token = request.get_json().get('refresh_token')
    if not token:
        return jsonify({'message': 'Refresh token required'}), 401

    decoded_token = verify_token(token)
    if decoded_token:
        if decoded_token['type'] != 'refresh':
            return jsonify({'message': 'Not a refresh token'}), 401
        new_access_token = create_access_token(decoded_token['sub'])
        return jsonify({'message': 'Token refreshed', 'access_token': new_access_token, 'refresh_token': token}), 200
    return jsonify({'message': 'Invalid or expired refresh token'}), 401