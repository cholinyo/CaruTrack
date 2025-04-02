# gestion_subvenciones/app/models/entidad.py

from flask_sqlalchemy import SQLAlchemy

from .db import db  # Asegúrate de que db esté definido en models/__init__.py

class Entidad(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    ambito = db.Column(db.String(100), nullable=True)

    contacto1_telefono = db.Column(db.String(20))
    contacto1_email = db.Column(db.String(100))
    contacto1_cargo = db.Column(db.String(100))

    contacto2_telefono = db.Column(db.String(20))
    contacto2_email = db.Column(db.String(100))
    contacto2_cargo = db.Column(db.String(100))

    contacto3_telefono = db.Column(db.String(20))
    contacto3_email = db.Column(db.String(100))
    contacto3_cargo = db.Column(db.String(100))
