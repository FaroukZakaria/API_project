from project.db import *
from flask import request, jsonify, Blueprint
from project.controllers.user_controller import *
from project.controllers.organization_controller import *
from project.models.organization_model import Organization
from flask_jwt_extended import decode_token

organization_routes = Blueprint('organization_routes', __name__, url_prefix='/organization')

@organization_routes.route('/', methods=['GET'])
def get_organizations():
    try:
        token = request.headers.get('Authorization').split()[1]
    except AttributeError:
        return jsonify({'message': 'Token required'}), 401
    except IndexError:
        token = request.headers.get('Authorization')
    if not verify_token(token):
        # placeholder for token refresh
        return jsonify({'message': 'Invalid or expired token'}), 401
    organizations = organizations_collection.find()
    org_list = []
    for organization in organizations:
        organization['_id'] = str(organization['_id'])
        org_list.append(organization)
    return jsonify(org_list), 200

@organization_routes.route('/', methods=['POST'])
def create_organization():
    try:
        token = request.headers.get('Authorization').split()[1]
    except AttributeError:
        return jsonify({'message': 'Token required'}), 401
    except IndexError:
        token = request.headers.get('Authorization')
    if not verify_token(token):
        # placeholder for token refresh
        return jsonify({'message': 'Invalid or expired token'}), 401
    current_user = users_collection.find_one({'_id': ObjectId(decode_token(token)['sub'])})
    data = request.get_json()
    organization_name = data.get('name')
    organization_description = data.get('description')
    if not organization_name:
        return jsonify({'message': 'Organization name required'}), 400
    if not organization_description:
        return jsonify({'message': 'Organization description required'}), 400
    
    organization = Organization(
        name=organization_name,
        description=organization_description,
        organization_members=[{
            'name': current_user['name'],
            'email': current_user['email'],
            'access_level': 'admin',
        }])
    if organizations_collection.find_one({'name': organization.name}):
        return jsonify({'message': 'Organization already exists'}), 400
    
    create_org(organization.dict())
    id = str(organizations_collection.find_one(organization.dict())['_id'])
    return jsonify({'organization_id': id}), 201

@organization_routes.route('/<string:organization_id>', methods=['GET'])
def get_organization(organization_id):
    organization_obj_id = ObjectId(organization_id)
    try:
        token = request.headers.get('Authorization').split()[1]
    except AttributeError:
        return jsonify({'message': 'Token required'}), 401
    except IndexError:
        token = request.headers.get('Authorization')
    if not verify_token(token):
        # placeholder for token refresh
        return jsonify({'message': 'Invalid or expired token'}), 401
    
    organization = organizations_collection.find_one({'_id': organization_obj_id})
    if not organization:
        return jsonify({'message': 'Organization not found'}), 404
    return jsonify({
        'organization_id': organization_id,
        'name': organization['name'],
        'description': organization['description'],
        "organization_members": organization['organization_members']
        }), 200

@organization_routes.route('/<string:organization_id>', methods=['PUT'])
def update_organization(organization_id):
    organization_obj_id = ObjectId(organization_id)
    try:
        token = request.headers.get('Authorization').split()[1]
    except AttributeError:
        return jsonify({'message': 'Token required'}), 401
    except IndexError:
        token = request.headers.get('Authorization')
    if not verify_token(token):
        # placeholder for token refresh
        return jsonify({'message': 'Invalid or expired token'}), 401
    
    organization = organizations_collection.find_one({'_id': organization_obj_id})
    if not organization:
        return jsonify({'message': 'Organization not found'}), 404
    
    current_user = users_collection.find_one({'_id': ObjectId(decode_token(token)['sub'])})
    if (
        current_user['email'] not in [member['email'] for member in organization['organization_members']] or
        any(member['email'] == current_user['email'] and member['access_level'] != 'admin' for member in organization['organization_members'])
        ):
        return jsonify({'message': "You're not authorized to change this organization"}), 401
    
    data = request.get_json()
    organization_name = data.get('name')
    organization_description = data.get('description')
    if not organization_name:
        organization_name = organization['name']
    if organizations_collection.find_one({'name': organization_name}):
        return jsonify({'message': 'Organization name already exists'}), 400
    if not organization_description:
        organization_description = organization['description']

    update_org(organization_obj_id, organization_name, organization_description)
    return jsonify({
        'organization_id': organization_id,
        'name': organization_name,
        'description': organization_description,
        }), 200

@organization_routes.route('/<string:organization_id>', methods=['DELETE'])
def delete_organization(organization_id):
    organization_obj_id = ObjectId(organization_id)
    try:
        token = request.headers.get('Authorization').split()[1]
    except AttributeError:
        return jsonify({'message': 'Token required'}), 401
    except IndexError:
        token = request.headers.get('Authorization')
    if not verify_token(token):
        # placeholder for token refresh
        return jsonify({'message': 'Invalid or expired token'}), 401
    
    organization = organizations_collection.find_one({'_id': organization_obj_id})
    if not organization:
        return jsonify({'message': 'Organization not found'}), 404
    
    current_user = users_collection.find_one({'_id': ObjectId(decode_token(token)['sub'])})
    if (
        current_user['email'] not in [member['email'] for member in organization['organization_members']] or
        any(member['email'] == current_user['email'] and member['access_level'] != 'admin' for member in organization['organization_members'])
        ):
        return jsonify({'message': "You're not authorized to delete this organization"}), 401
    
    delete_org(organization_obj_id)
    return jsonify({'message': 'Organization deleted'}), 200

@organization_routes.route('/<string:organization_id>/invite', methods=['POST'])
def add_member(organization_id):
    organization_obj_id = ObjectId(organization_id)
    try:
        token = request.headers.get('Authorization').split()[1]
    except AttributeError:
        return jsonify({'message': 'Token required'}), 401
    except IndexError:
        token = request.headers.get('Authorization')
    if not verify_token(token):
        # placeholder for token refresh
        return jsonify({'message': 'Invalid or expired token'}), 401
    
    organization = organizations_collection.find_one({'_id': organization_obj_id})
    if not organization:
        return jsonify({'message': 'Organization not found'}), 404
    
    current_user = users_collection.find_one({'_id': ObjectId(decode_token(token)['sub'])})
    if (
        current_user['email'] not in [member['email'] for member in organization['organization_members']] or
        any(member['email'] == current_user['email'] and member['access_level'] != 'admin' for member in organization['organization_members'])
        ):
        return jsonify({'message': "You're not authorized to add members to this organization"}), 401
    
    data = request.get_json()
    member_email = data.get('email')
    member = users_collection.find_one({'email': member_email})
    if not member:
        return jsonify({'message': 'Member not found'}), 404
    if member_email in [member['email'] for member in organization['organization_members']]:
        return jsonify({'message': 'Member already in organization'}), 400
    add_member_to_org(organization_obj_id, member_email)
    return jsonify({'message': 'Member added successfully'}), 201