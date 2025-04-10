# Ruta: app/models/historial_solicitud.py

from datetime import datetime
from app.models.db import db

class HistorialSolicitud(db.Model):
    __tablename__ = 'historial_solicitud'

    id = db.Column(db.Integer, primary_key=True)
    solicitud_id = db.Column(db.Integer, db.ForeignKey('solicitud_subvencion.id'), nullable=False)
    usuario = db.Column(db.String(100), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    descripcion = db.Column(db.Text, nullable=False)

    solicitud = db.relationship('SolicitudSubvencion', back_populates='historial')

