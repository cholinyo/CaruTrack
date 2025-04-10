from datetime import datetime
from app.models.db import db

class HistorialSolicitud(db.Model):
    __tablename__ = 'historial_solicitud'

    id = db.Column(db.Integer, primary_key=True)
    
    solicitud_id = db.Column(db.Integer, db.ForeignKey('solicitudes_subvencion.id'), nullable=False)
    solicitud = db.relationship("SolicitudSubvencion", back_populates="historial")

    usuario = db.Column(db.String(100), nullable=False)  # Nombre o username del usuario que realiza el cambio
    fecha_cambio = db.Column(db.DateTime, default=datetime.utcnow)
    
    descripcion = db.Column(db.Text, nullable=False)  # Qué se ha hecho: "Estado cambiado de X a Y", etc.

    def __repr__(self):
        return f'<HistorialSolicitud {self.id} - Solicitud {self.solicitud_id}>'
