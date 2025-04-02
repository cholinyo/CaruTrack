from datetime import datetime
from .. import db

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

class HistorialSolicitud(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    solicitud_id = db.Column(db.Integer, db.ForeignKey('solicitud_subvencion.id'), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    usuario = db.Column(db.String(80))
    descripcion = db.Column(db.Text)
