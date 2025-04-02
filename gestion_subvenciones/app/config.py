import os

class Config:
    SECRET_KEY = "tu_clave_secreta"
    SQLALCHEMY_DATABASE_URI = "sqlite:///../instance/subvenciones.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

