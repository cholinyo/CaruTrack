from . import db
from datetime import date

class Subvencion(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Identificadores
    expediente_opensea = db.Column(db.String(50))
    expediente_subvencion = db.Column(db.String(50))

    # Información básica
    entidad = db.Column(db.String(150))
    concepto = db.Column(db.String(250))
    tipo_fondo = db.Column(db.String(100))

    # Fechas y estado
    fecha_solicitud = db.Column(db.Date)
    estado = db.Column(db.String(100))

    # Información económica
    fondos_propios = db.Column(db.String(10))
    importe_solicitado = db.Column(db.Float)
    importe_concedido = db.Column(db.Float)
    importe_pagado = db.Column(db.Float)

    # Trazabilidad
    observaciones = db.Column(db.Text)

    def __repr__(self):
        return f"<Subvencion {self.expediente_subvencion} - {self.entidad}>"

