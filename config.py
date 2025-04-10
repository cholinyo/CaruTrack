import os

class Config:
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///Carutrack.db'  # Ruta a la base de datos SQLite
SQLALCHEMY_TRACK_MODIFICATIONS = False