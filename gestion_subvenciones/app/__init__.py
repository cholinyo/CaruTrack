from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Inicialización de extensiones para la base de datos y migraciones
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    # Crear instancia de la aplicación Flask
    app = Flask(__name__)

    # Configuración de la base de datos SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///subvenciones.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Clave secreta para sesiones (se recomienda usar una más segura en producción)
    app.secret_key = 'dev'

    # Inicializar las extensiones con la aplicación
    db.init_app(app)
    migrate.init_app(app, db)

    # Importar y registrar el blueprint principal con las rutas de la app
    from .routes import main
    app.register_blueprint(main)

    # Devolver la aplicación configurada
    return app
