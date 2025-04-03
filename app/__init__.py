from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate

# Inicializar extensiones
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # Redirigir a esta vista si no está autenticado
login_manager.login_message = "Por favor, inicia sesión para acceder a esta página."
migrate = Migrate()

def create_app(config_class='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializar extensiones
    db.init_app(app)
    login_manager.init_app(app)
    Bootstrap(app)
    migrate.init_app(app, db)

    # Registrar blueprints
    from app.routes import register_blueprints
    register_blueprints(app)

    return app