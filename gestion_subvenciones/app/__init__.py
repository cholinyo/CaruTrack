from flask import Flask
from .models import db
from .routes import main  # AsegÃºrate de que defines un blueprint 'main' en routes.py

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')  # AsegÃºrate de tener un archivo config.py con la clase Config
    db.init_app(app)
    app.register_blueprint(main)
    return app
