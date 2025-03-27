from flask import Flask
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from .models import db, Usuario  # db viene ya creado en models

bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'main.login'
migrate = Migrate()



def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # ✅ Primero se crea 'app', luego se inicializa cada extensión
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from .routes import main
    app.register_blueprint(main)

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    return app
