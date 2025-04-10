from datetime import datetime
from app.models.db import db

class SolicitudSubvencion(db.Model):
    __tablename__ = "solicitud_subvencion"

    id = db.Column(db.Integer, primary_key=True)
    expediente_opensea = db.Column(db.String(120))
    expediente_subvencion = db.Column(db.String(120))
    entidad_id = db.Column(db.Integer, db.ForeignKey('entidad.id'))
    concepto = db.Column(db.String(200))
    tipo_fondo = db.Column(db.String(100))
    fecha_presentacion_solicitud = db.Column(db.Date)
    importe_total = db.Column(db.Float)
    importe_subvencionado = db.Column(db.Float)
    fondos_propios = db.Column(db.Float)

    # Estado de la solicitud
    estado = db.Column(db.String(50), nullable=False, default='No solicitada')
    motivo_no_solicitada = db.Column(db.String(255))

    # Documentación requerida
    doc_inicio_expediente = db.Column(db.Boolean, default=False)
    doc_informe_tecnico = db.Column(db.Boolean, default=False)
    doc_propuesta_jgl = db.Column(db.Boolean, default=False)
    doc_ficha_captacion = db.Column(db.Boolean, default=False)

    # Observaciones y responsables
    observaciones = db.Column(db.Text)
    gestor_responsable = db.Column(db.String(100))
    email_gestor = db.Column(db.String(120))

    # Relación con historial
    historial = db.relationship("HistorialSolicitud", backref="solicitud", lazy=True, cascade="all, delete-orphan")

    def documentos_completos(self):
        return all([
            self.doc_inicio_expediente,
            self.doc_informe_tecnico,
            self.doc_propuesta_jgl,
            self.doc_ficha_captacion
        ])

    def esta_bloqueada(self):
        return self.estado in ["No solicitada", "Concedida", "Denegada"]