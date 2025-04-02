from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    rol = db.Column(db.String(50), nullable=False, default='usuario')

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


class Entidad(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    ambito = db.Column(db.String(100))
    contactos = db.relationship('ContactoEntidad', backref='entidad', lazy=True)
    solicitudes = db.relationship('SolicitudSubvencion', backref='entidad_relacionada', lazy=True)

class ContactoEntidad(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    entidad_id = db.Column(db.Integer, db.ForeignKey('entidad.id'), nullable=False)
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(120))
    cargo = db.Column(db.String(120))

class SolicitudSubvencion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    expediente_opensea = db.Column(db.String(120))
    expediente_subvencion = db.Column(db.String(120))
    entidad_id = db.Column(db.Integer, db.ForeignKey('entidad.id', name='fk_entidad_id'), nullable=True)
    concepto = db.Column(db.String(200))
    tipo_fondo = db.Column(db.String(100))
    fecha_presentacion_solicitud = db.Column(db.Date)
    estado = db.Column(db.String(50))
    importe_estimado = db.Column(db.Float)
    importe_subvencionado = db.Column(db.Float)
    fondos_propios = db.Column(db.Float)
    documentacion_inicio_expediente = db.Column(db.Boolean, default=False)
    documentacion_informe_tecnico = db.Column(db.Boolean, default=False)
    documentacion_propuesta_jgl = db.Column(db.Boolean, default=False)
    documentacion_ficha_captacion = db.Column(db.Boolean, default=False)
    observaciones = db.Column(db.Text)
    bloqueada = db.Column(db.Boolean, default=False)
    historial = db.relationship('HistorialSolicitud', backref='solicitud', lazy=True)

