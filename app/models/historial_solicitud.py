# app/models/historial_solicitud.py

from datetime import datetime
from app.models.db import db
from flask import Blueprint, request, render_template
from flask_login import login_required
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, BooleanField, DateField
from wtforms.validators import DataRequired

solicitud_bp = Blueprint('solicitud_bp', __name__)

class HistorialSolicitud(db.Model):
    __tablename__ = 'historial_solicitud'

    id = db.Column(db.Integer, primary_key=True)
    solicitud_id = db.Column(db.Integer, db.ForeignKey('solicitud_subvencion.id'), nullable=False)
    usuario = db.Column(db.String(100), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    descripcion = db.Column(db.Text, nullable=False)

    # Relación inversa (acceso desde la solicitud)
    solicitud = db.relationship('SolicitudSubvencion', back_populates='historial')

    @staticmethod
    def crear_historial(solicitud_id, usuario, descripcion):
        return HistorialSolicitud(
            solicitud_id=solicitud_id,
            usuario=usuario,
            descripcion=descripcion
        )

historial = HistorialSolicitud.crear_historial(
    solicitud_id=solicitud.id,
    usuario=current_user.username,
    descripcion="Creación de solicitud"
)
db.session.add(historial)

class SolicitudForm(FlaskForm):
    expediente_opensea = StringField('Expediente OpenSea', validators=[DataRequired()])
    expediente_subvencion = StringField('Expediente Subvención')
    entidad_id = StringField('Entidad', validators=[DataRequired()])
    fecha_presentacion_solicitud = DateField('Fecha de Presentación', format='%Y-%m-%d')
    # Otros campos...

form = SolicitudForm()
if form.validate_on_submit():
    solicitud = SolicitudSubvencion(
        expediente_opensea=form.expediente_opensea.data,
        # Otros campos...
    )

@solicitud_bp.route('/solicitudes')
@login_required
def listar_solicitudes():
    page = request.args.get('page', 1, type=int)
    solicitudes = SolicitudSubvencion.query.order_by(
        SolicitudSubvencion.fecha_presentacion_solicitud.desc()
    ).paginate(page=page, per_page=10)
    return render_template('solicitudes/listar.html', solicitudes=solicitudes)