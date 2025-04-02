from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# from app.models.db import db
from app.routes import main_bp
from app.routes.routes_entidades import entidades_bp
from app.routes.routes_solicitudes import solicitudes_bp
from app.routes.routes_subvenciones import subvenciones_bp
from app.routes.routes_usuarios import usuarios_bp
# Si tienes más, los añades aquí

login_manager = LoginManager()
login_manager.login_view = 'login'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    # Registrar Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(entidades_bp)
    app.register_blueprint(solicitudes_bp)
    app.register_blueprint(subvenciones_bp)
    app.register_blueprint(usuarios_bp)

    return app
