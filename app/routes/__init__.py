from flask import Flask
from flask_login import LoginManager
from app.config import Config
from app.models.db import db
from app.routes import main_bp
from app.routes.routes_entidades import entidades_bp
from app.routes.routes_usuarios import usuarios_bp
from app.routes.routes_solicitud_subvencion import solicitud_subvencion_bp

# ...otros blueprints

login_manager = LoginManager()
login_manager.login_view = 'usuarios_bp.login'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    from app.models.usuario import Usuario
    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    app.register_blueprint(main_bp)
    app.register_blueprint(entidades_bp)
    app.register_blueprint(usuarios_bp)
    # ...otros blueprints

    return app

