from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Subvencion(db.Model):
    __tablename__ = 'subvenciones'

    id = db.Column(db.Integer, primary_key=True)
    expediente_opensea = db.Column(db.String(120), unique=True, nullable=False)
    expediente_subvencion = db.Column(db.String(120), unique=True, nullable=False)
    entidad = db.Column(db.String(120), nullable=False)
    concepto = db.Column(db.String(200), nullable=False)
    tipo_fondo = db.Column(db.String(100), nullable=False)
    fecha_solicitud = db.Column(db.Date, nullable=False)
    estado = db.Column(db.String(50), nullable=False)
    fondos_propios = db.Column(db.String(50), nullable=False)
    importe_solicitado = db.Column(db.Float, nullable=False)
    importe_concedido = db.Column(db.Float)
    importe_pagado = db.Column(db.Float)
    observaciones = db.Column(db.Text)

    def __repr__(self):
        return f'<Subvencion {self.expediente_opensea} - {self.entidad}>'
