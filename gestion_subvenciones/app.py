from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gestion_subvenciones.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

@app.route('/')
def home():
    return "Bienvenido a la aplicación de gestión de subvenciones"

def create_app():
    from routes.grant_routes import grant_routes  # Importación local para evitar dependencia circular
    app.register_blueprint(grant_routes)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run()