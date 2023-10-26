import os
from flask import Flask
from dotenv import load_dotenv
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

api = Api()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    load_dotenv()

    current_directory = os.path.dirname(__file__)

    database_directory = ''

    database_path = os.path.join(current_directory, '..', database_directory, os.getenv('DATABASE_NAME'))

    if not os.path.exists(os.path.dirname(database_path)):
        os.makedirs(os.path.dirname(database_path))

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + database_path
    db.init_app(app)

    import main.resources as resources

    api.add_resource(resources.ProductosResources, "/productos")
    api.add_resource(resources.ProductoResource, "/producto/<id>")
    api.add_resource(resources.RatingsResources, "/ratings")
    api.add_resource(resources.RatingResource, "/rating/<id>")

    api.init_app(app)

    return app