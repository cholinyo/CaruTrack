from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    rol = db.Column(db.String(50), nullable=False, server_default='gestor')


    def __repr__(self):
        return f"<Usuario {self.username}>"

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

class SolicitudSubvencion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    entidad = db.Column(db.String(150), nullable=False)
    concepto = db.Column(db.String(250), nullable=False)
    tipo_fondo = db.Column(db.String(100))
    fecha_solicitud = db.Column(db.Date)
    estado = db.Column(db.String(50), nullable=False, default='No solicitada')
    observaciones = db.Column(db.Text)
    importe_estimado = db.Column(db.Float)
    documentacion_adjunta = db.Column(db.Boolean, default=False)
    bloqueada = db.Column(db.Boolean, default=False)  # Nueva lógica de bloqueo

    def __repr__(self):
        return f"<Solicitud {self.entidad} - {self.estado}>"

class SubvencionDenegada(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    entidad = db.Column(db.String(150), nullable=False)
    concepto = db.Column(db.String(250), nullable=False)
    tipo_fondo = db.Column(db.String(100))
    fecha_solicitud = db.Column(db.Date)
    estado = db.Column(db.String(50))
    observaciones = db.Column(db.Text)
    importe_estimado = db.Column(db.Float)
    documentacion_adjunta = db.Column(db.Boolean, default=False)
    motivo_denegacion = db.Column(db.Text)
    resolucion = db.Column(db.Text)

    def __repr__(self):
        return f"<Denegada {self.entidad} - {self.estado}>"

class HistorialSolicitud(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    solicitud_id = db.Column(db.Integer, db.ForeignKey('solicitud_subvencion.id'), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    usuario = db.Column(db.String(100))
    descripcion = db.Column(db.Text)

    solicitud = db.relationship('SolicitudSubvencion', backref=db.backref('historial', lazy='dynamic'))
