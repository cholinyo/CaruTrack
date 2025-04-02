from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from .config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    # Importar y registrar blueprints
    from .routes.routes_entidades import entidades_bp
    from .routes.routes_solicitudes import solicitudes_bp
    from .routes.routes_usuarios import usuarios_bp
    app.register_blueprint(entidades_bp)
    app.register_blueprint(solicitudes_bp)
    app.register_blueprint(usuarios_bp)

    return app
