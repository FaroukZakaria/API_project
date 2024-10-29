import os
from flask_jwt_extended import JWTManager
from flask import Flask
from project.routes.user_routes import user_routes
from project.routes.organization_routes import organization_routes

app = Flask(__name__)
# configure the app
app.config['JWT_SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['JWT_REFRESH_SECRET_KEY'] = os.getenv('SECRET_KEY_REFRESH')
JWTManager(app)

# define the routes
app.register_blueprint(user_routes)
app.register_blueprint(organization_routes)