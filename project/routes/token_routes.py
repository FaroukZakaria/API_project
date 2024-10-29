from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token
from project.controllers.token_controller import *

token_routes = Blueprint('token_routes', __name__)

@token_routes.route('/refresh-token', methods=['POST'])
def refresh_token():
    token = request.get_json().get('refresh_token')
    if not token:
        return jsonify({'message': 'Refresh token required'}), 401

    decoded_token = verify_token(token)
    if decoded_token:
        if decoded_token['type'] != 'refresh':
            return jsonify({'message': 'Not a refresh token'}), 401
        # Check if the refresh token is revoked
        if is_refresh_token_revoked(token):
            return jsonify({"message": "Refresh token has been revoked"}), 401
        new_access_token = create_access_token(decoded_token['sub'])
        return jsonify({'message': 'Token refreshed', 'access_token': new_access_token, 'refresh_token': token}), 200
    return jsonify({'message': 'Invalid or expired refresh token'}), 401

@token_routes.route('/revoke-refresh-token', methods=['POST'])
def revoke_refresh_token():
    try:
        token = request.headers.get('Authorization').split()[1]
    except AttributeError:
        return jsonify({'message': 'Client token required'}), 401
    except IndexError:
        token = request.headers.get('Authorization')
    if not verify_token(token):
        # placeholder for token refresh
        return jsonify({'message': 'Client token is invalid or expired'}), 401
    
    data = request.get_json()
    refresh_token = data.get('refresh_token')
    if not refresh_token:
        return jsonify({'message': 'Refresh token required'}), 401
    decoded_token = verify_token(refresh_token)
    if is_refresh_token_revoked(refresh_token):
        return jsonify({'message': 'Refresh token has already been revoked'}), 401
    if decoded_token:
        if decoded_token['type'] != 'refresh':
            return jsonify({'message': 'Not a refresh token'}), 401
        
        current_app.redis.set(refresh_token, 'revoked', ex=3600)
        return jsonify({'message': 'Token revoked'}), 200
    
    return jsonify({'message': 'Invalid or expired refresh token'}), 401