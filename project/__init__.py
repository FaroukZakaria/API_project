import os
from redis import Redis
from flask_jwt_extended import JWTManager
from flask import Flask
from project.routes.user_routes import user_routes
from project.routes.organization_routes import organization_routes
from project.routes.token_routes import token_routes

app = Flask(__name__)
# configure the app
app.config['JWT_SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['JWT_REFRESH_SECRET_KEY'] = os.getenv('SECRET_KEY_REFRESH')
JWTManager(app)

# Configure Redis
app.config['redis_host'] = os.getenv("REDIS_HOST", "localhost")
app.config['redis_port'] = os.getenv("REDIS_PORT", 6379)
app.redis = Redis(host=app.config['redis_host'], port=app.config['redis_port'])

# define the routes
app.register_blueprint(user_routes)
app.register_blueprint(organization_routes)
app.register_blueprint(token_routes)