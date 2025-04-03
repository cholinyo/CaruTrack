from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

# Inicializar extensiones
db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_class='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializar extensiones
    db.init_app(app)
    login_manager.init_app(app)
    Bootstrap(app)

    # Registrar blueprints
    from app.routes import register_blueprints
    register_blueprints(app)

    return app

def register_blueprints(app):
    from app.routes.routes_solicitudes import solicitudes_bp
    from app.routes.routes_auth import auth_bp
    from app.routes.routes_main import main_bp  # Importar el blueprint de la página principal

    app.register_blueprint(solicitudes_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)  # Registrar el blueprint