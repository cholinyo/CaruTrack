from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from app.config import Config

# Inicializaciones globales
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

# Esta instancia de SQLAlchemy se usa en todos los modelos
from app.models.db import db

# Cargar modelo de usuario para Flask-Login
from app.models.usuario import Usuario

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

def create_app():
    # Crear la instancia principal de la app Flask
    app = Flask(__name__)

    # Cargar configuración desde el objeto Config (config.py)
    app.config.from_object(Config)

    # Inicializar extensiones con la app
    db.init_app(app)
    login_manager.init_app(app)
    Migrate(app, db)

    # Registrar blueprints (rutas divididas por funcionalidad)
    from app.routes.routes_main import main_bp
    from app.routes.routes_usuarios import usuarios_bp
    from app.routes.routes_entidades import entidades_bp
    from app.routes.routes_solicitudes import solicitudes_bp
    from app.routes.routes_subvenciones import subvenciones_bp
    from app.routes.routes_historial import historial_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(entidades_bp)
    app.register_blueprint(solicitudes_bp)
    app.register_blueprint(subvenciones_bp)
    app.register_blueprint(historial_bp)

    return app
