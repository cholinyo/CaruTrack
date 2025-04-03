# filepath: app/models/solicitud.py
from app.models.db import db
from datetime import date
from sqlalchemy.dialects.mysql import DECIMAL

class Solicitud(db.Model):
    __tablename__ = 'solicitudes'

    id = db.Column(db.Integer, primary_key=True)
    expediente_opensea = db.Column(db.String(100), nullable=False, unique=True)
    expediente_subvencion = db.Column(db.String(100), nullable=False, unique=True)
    entidad_id = db.Column(db.Integer, db.ForeignKey('entidades.id'), nullable=False)
    concepto = db.Column(db.String(255), nullable=False)
    tipo_fondo = db.Column(db.Enum('Fondos Europeos', 'Fondos Nacionales', 'Fondos Autonómicos', 
                                   'Fondos Provinciales', 'Otros', name='tipo_fondo_enum'), nullable=False)
    fecha_solicitud = db.Column(db.Date, nullable=False, default=date.today)
    importe_total_proyecto = db.Column(DECIMAL(15, 2), nullable=False)
    importe_subvencionado = db.Column(DECIMAL(15, 2), nullable=False)
    aportacion_fondos_propios = db.Column(DECIMAL(15, 2), nullable=False)

    inicio_expediente = db.Column(db.Boolean, default=False)
    informe_tecnico = db.Column(db.Boolean, default=False)
    propuesta_jgl_decreto = db.Column(db.Boolean, default=False)
    ficha_departamento_captacion = db.Column(db.Boolean, default=False)

    gestor_responsable = db.Column(db.String(100), nullable=False)
    mail_gestor = db.Column(db.String(120), nullable=False)
    observaciones = db.Column(db.Text, nullable=True)

    entidad = db.relationship('Entidad', backref='solicitudes', lazy=True)

    def __repr__(self):
        return f'<Solicitud {self.expediente_opensea}>'