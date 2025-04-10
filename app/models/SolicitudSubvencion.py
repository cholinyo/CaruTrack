from datetime import datetime
from app.models.db import db

class SolicitudSubvencion(db.Model):
    __tablename__ = 'solicitudes_subvencion'

    id = db.Column(db.Integer, primary_key=True)

    expediente_opensea = db.Column(db.String(100))
    expediente_subvencion = db.Column(db.String(100))

    entidad_id = db.Column(db.Integer, db.ForeignKey('entidades.id'))
    entidad = db.relationship('Entidad', backref=db.backref('solicitudes', lazy=True))

    concepto = db.Column(db.String(255))
    tipo_fondo = db.Column(db.String(100))
    fecha_presentacion_solicitud = db.Column(db.Date)

    importe_total = db.Column(db.Float)
    importe_subvencionado = db.Column(db.Float)
    fondos_propios = db.Column(db.Float)

    # Documentos requeridos
    doc_inicio_expediente = db.Column(db.Boolean, default=False)
    doc_informe_tecnico = db.Column(db.Boolean, default=False)
    doc_propuesta_jgl = db.Column(db.Boolean, default=False)
    doc_ficha_captacion = db.Column(db.Boolean, default=False)

    observaciones = db.Column(db.Text)

    gestor_responsable = db.Column(db.String(100))
    email_gestor = db.Column(db.String(100))
    url_referencia = db.Column(db.String(255))

    # Estados posibles
    estado = db.Column(db.String(50), nullable=False, default='No solicitada')
    motivo_no_solicitada = db.Column(db.Text)

    # Timestamps
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relación con historial
    historial = db.relationship('HistorialSolicitud', backref='solicitud', lazy=True, cascade='all, delete-orphan')
