from config import Config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.debug = True

    return app


app = create_app()
db = SQLAlchemy(app)
migrate = Migrate(app, db)


from app import api, models
db.create_all()