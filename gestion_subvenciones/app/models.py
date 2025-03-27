from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Subvencion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    expediente_opensea = db.Column(db.String(50))
    expediente_subvencion = db.Column(db.String(50))
    entidad = db.Column(db.String(150))
    concepto = db.Column(db.String(250))
    tipo_fondo = db.Column(db.String(100))
    fecha_solicitud = db.Column(db.Date)
    estado = db.Column(db.String(100))
    fondos_propios = db.Column(db.String(10))
    importe_solicitado = db.Column(db.Float)
    importe_concedido = db.Column(db.Float)
    importe_pagado = db.Column(db.Float)
    observaciones = db.Column(db.Text)

    def __repr__(self):
        return f"<Subvencion {self.expediente_subvencion} - {self.entidad}>"

class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f"<Usuario {self.username}>"
