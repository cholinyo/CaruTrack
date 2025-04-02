from .. import db

class Subvencion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    expediente_opensea = db.Column(db.String(120))
    expediente_subvencion = db.Column(db.String(120))
    entidad = db.Column(db.String(120))
    concepto = db.Column(db.String(200))
    tipo_fondo = db.Column(db.String(100))
    fecha_solicitud = db.Column(db.Date)
    estado = db.Column(db.String(50))
    fondos_propios = db.Column(db.String(50))
    importe_solicitado = db.Column(db.Float)
    importe_concedido = db.Column(db.Float)
    importe_pagado = db.Column(db.Float)
    observaciones = db.Column(db.Text)

class SubvencionDenegada(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    entidad = db.Column(db.String(120))
    concepto = db.Column(db.String(200))
    tipo_fondo = db.Column(db.String(100))
    fecha_solicitud = db.Column(db.Date)
    estado = db.Column(db.String(50))
    observaciones = db.Column(db.Text)
    importe_estimado = db.Column(db.Float)
    documentacion_adjunta = db.Column(db.Boolean)
    motivo_denegacion = db.Column(db.Text)
    resolucion = db.Column(db.Text)
