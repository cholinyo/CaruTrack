from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from datetime import datetime
import pandas as pd
import os
from .models import db, Subvencion, Usuario, SolicitudSubvencion, SubvencionDenegada, HistorialSolicitud, Entidad

main = Blueprint('main', __name__)
bcrypt = Bcrypt()

def rol_requerido(*roles):
    def decorator(func):
        from functools import wraps
        @wraps(func)
        def wrapper(*args, **kwargs):
            if current_user.rol not in roles:
                abort(403)
            return func(*args, **kwargs)
        return wrapper
    return decorator

@main.route('/')
@login_required
def index():
    return redirect(url_for('main.listar_solicitudes'))

@main.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        usuario = Usuario.query.filter_by(username=request.form['username']).first()
        if usuario and bcrypt.check_password_hash(usuario.password_hash, request.form['password']):
            login_user(usuario)
            return redirect(url_for('main.index'))
        error = "Usuario o contraseña incorrectos"
    return render_template('login.html', error=error)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main.route('/solicitudes')
@login_required
def listar_solicitudes():
    solicitudes = SolicitudSubvencion.query.order_by(SolicitudSubvencion.fecha_presentacion_solicitud.desc()).all()
    return render_template('solicitudes.html', solicitudes=solicitudes)

@main.route('/solicitudes/nueva', methods=['GET', 'POST'])
@login_required
def nueva_solicitud():
    entidades = Entidad.query.order_by(Entidad.nombre).all()

    if request.method == 'POST':
        try:
            solicitud = SolicitudSubvencion(
                expediente_opensea=request.form.get('expediente_opensea', ''),
                expediente_subvencion=request.form.get('expediente_subvencion', ''),
                entidad_id=int(request.form.get('entidad_id')) if request.form.get('entidad_id') else None,
                concepto=request.form.get('concepto', ''),
                tipo_fondo=request.form.get('tipo_fondo', ''),
                fecha_presentacion_solicitud=datetime.strptime(
                    request.form.get('fecha_presentacion_solicitud', ''), "%Y-%m-%d")
                    if request.form.get('fecha_presentacion_solicitud') else None,
                importe_total=float(request.form.get('importe_total') or 0),
                importe_subvencionado=float(request.form.get('importe_subvencionado') or 0),
                fondos_propios=float(request.form.get('fondos_propios') or 0),
                doc_inicio_expediente='doc_inicio_expediente' in request.form,
                doc_informe_tecnico='doc_informe_tecnico' in request.form,
                doc_propuesta_jgl='doc_propuesta_jgl' in request.form,
                doc_ficha_captacion='doc_ficha_captacion' in request.form,
                observaciones=request.form.get('observaciones', '')
            )
            db.session.add(solicitud)
            db.session.flush()

            historial = HistorialSolicitud(
                solicitud_id=solicitud.id,
                usuario=current_user.username,
                descripcion="Solicitud creada"
            )
            db.session.add(historial)

            db.session.commit()
            flash("Solicitud creada con éxito ✅")
            return redirect(url_for('main.listar_solicitudes'))
        except Exception as e:
            db.session.rollback()
            flash(f"❌ Error al guardar la solicitud: {str(e)}")

    return render_template('nueva_solicitud.html', entidades=entidades)

@main.route('/solicitudes/editar/<int:id>', methods=['GET'])
@login_required
@rol_requerido('gestor')
def editar_solicitud(id):
    solicitud = SolicitudSubvencion.query.get_or_404(id)
    entidades = Entidad.query.order_by(Entidad.nombre).all()
    return render_template('editar_solicitud.html', solicitud=solicitud, entidades=entidades)

@main.route('/solicitudes/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_solicitud(id):
    solicitud = SolicitudSubvencion.query.get_or_404(id)
    try:
        db.session.delete(solicitud)
        db.session.commit()
        flash("Solicitud eliminada correctamente")
    except Exception as e:
        db.session.rollback()
        flash(f"Error al eliminar solicitud: {str(e)}")
    return redirect(url_for('main.listar_solicitudes'))

@main.route('/solicitudes/historial/<int:solicitud_id>')
@login_required
def ver_historial_solicitud(solicitud_id):
    historial = HistorialSolicitud.query.filter_by(solicitud_id=solicitud_id).order_by(HistorialSolicitud.fecha.desc()).all()
    return render_template('historial_solicitud.html', historial=historial)

@main.route('/solicitudes/denegadas')
@login_required
def listar_solicitudes_denegadas():
    denegadas = SolicitudSubvencion.query.filter_by(estado='Denegada').order_by(SolicitudSubvencion.fecha_presentacion_solicitud.desc()).all()
    return render_template('solicitudes_denegadas.html', solicitudes=denegadas)

@main.route('/solicitudes/exportar')
@login_required
def exportar_solicitudes_excel():
    solicitudes = SolicitudSubvencion.query.order_by(SolicitudSubvencion.fecha_presentacion_solicitud.desc()).all()
    datos = [
        {
            'Entidad': s.entidad.nombre if s.entidad else '',
            'Concepto': s.concepto,
            'Tipo Fondo': s.tipo_fondo,
            'Fecha Presentación': s.fecha_presentacion_solicitud,
            'Estado': s.estado,
            'Importe Total': s.importe_total,
            'Importe Subvencionado': s.importe_subvencionado,
            'Fondos Propios': s.fondos_propios
        } for s in solicitudes
    ]

    df = pd.DataFrame(datos)
    ruta_excel = os.path.join("app", "static", "export_solicitudes.xlsx")
    df.to_excel(ruta_excel, index=False)

    return redirect(url_for('static', filename='export_solicitudes.xlsx'))