import os

class Config:
    # Clave secreta para formularios y sesiones
    SECRET_KEY = os.environ.get('SECRET_KEY', 'clave-secreta-por-defecto')

    # URI de conexión a la base de datos (por defecto SQLite)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///subvenciones.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
