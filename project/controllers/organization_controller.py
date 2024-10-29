from bson import ObjectId
from project.db import *
from project.controllers.user_controller import *
from project.models.organization_model import Organization

def create_org(org: Organization):
    organizations_collection.insert_one(org)

def update_org(organization_obj_id: str, organization_name: str, organization_description: str):
    organizations_collection.update_one({'_id': organization_obj_id}, {'$set': {'name': organization_name, 'description': organization_description}})

def delete_org(organization_obj_id: ObjectId):
    organizations_collection.delete_one({'_id': organization_obj_id})

def add_member_to_org(organization_obj_id: ObjectId, member_email: str):
    member = users_collection.find_one({'email': member_email})
    organization = organizations_collection.find_one({'_id': organization_obj_id})
    organization['organization_members'].append({
        'name': member['name'],
        'email': member['email'],
        'access_level': 'read-only',
    })
    organizations_collection.update_one({'_id': organization_obj_id}, {'$set': {'organization_members': organization['organization_members']}})