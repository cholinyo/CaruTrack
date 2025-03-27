import os

class Config:
    # Configuración de la clave secreta
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    # Configuración de la base de datos
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///subvenciones.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False