from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import DevConfig

# The SQLAlchemy object is defined globally
db = SQLAlchemy()


def create_app(config_class=DevConfig):
    """
    Creates an application instance to run
    :return: A Flask object
    """
    app = Flask(__name__)

    # Configure the Flask app wth the configuration settings from a class in config.py
    app.config.from_object(config_class)

    # Initialise the database so that the app can use it
    db.init_app(app)

    # Create tables in the database (the tables are defined in models.py)
    from app.models import Teacher, Student, Course, Grade
    with app.app_context():
        db.create_all()

    # Register Blueprints
    from app.main.routes import bp_main
    app.register_blueprint(bp_main)

    return app
