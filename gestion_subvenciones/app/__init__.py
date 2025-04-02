# Este archivo hace que el directorio `app` sea un paquete Python.

from flask import Flask
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'usuarios_bp.login'
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Registrar Blueprints
    from .routes.routes_solicitudes import solicitudes_bp
    from .routes.routes_entidades import entidades_bp
    from .routes.routes_usuarios import usuarios_bp

    app.register_blueprint(solicitudes_bp, url_prefix='/solicitudes')
    app.register_blueprint(entidades_bp, url_prefix='/entidades')
    app.register_blueprint(usuarios_bp, url_prefix='/usuarios')

    @login_manager.user_loader
    def load_user(user_id):
        from .models.usuario import Usuario
        return Usuario.query.get(int(user_id))

    return app
