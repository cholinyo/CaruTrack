# Ruta: app/routes/routes_solicitud_subvencion.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from datetime import datetime
from ..models import db
from ..models.solicitud_subvencion import SolicitudSubvencion
from ..models.historial_solicitud import HistorialSolicitud
from ..models.entidad import Entidad

solicitud_bp = Blueprint('solicitud_bp', __name__)

# Decorador para roles

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

# Listado de solicitudes con colapso para historial
@solicitud_bp.route('/solicitudes')
@login_required
def listar_solicitudes():
    solicitudes = SolicitudSubvencion.query.order_by(SolicitudSubvencion.fecha_presentacion_solicitud.desc()).all()
    return render_template('solicitudes/listar.html', solicitudes=solicitudes)

# Crear nueva solicitud
@solicitud_bp.route('/solicitudes/nueva', methods=['GET', 'POST'])
@login_required
@rol_requerido('admin', 'gestor')
def nueva_solicitud():
    entidades = Entidad.query.order_by(Entidad.nombre).all()
    if request.method == 'POST':
        try:
            solicitud = SolicitudSubvencion(
                expediente_opensea=request.form.get('expediente_opensea', ''),
                expediente_subvencion=request.form.get('expediente_subvencion', ''),
                entidad_id=request.form.get('entidad_id'),
                concepto=request.form.get('concepto', ''),
                tipo_fondo=request.form.get('tipo_fondo', ''),
                fecha_presentacion_solicitud=datetime.strptime(request.form.get('fecha_presentacion_solicitud', ''), "%Y-%m-%d") if request.form.get('fecha_presentacion_solicitud') else None,
                importe_total=request.form.get('importe_total', 0),
                importe_subvencionado=request.form.get('importe_subvencionado', 0),
                fondos_propios=request.form.get('fondos_propios', 0),
                doc_inicio_expediente='doc_inicio_expediente' in request.form,
                doc_informe_tecnico='doc_informe_tecnico' in request.form,
                doc_propuesta_jgl='doc_propuesta_jgl' in request.form,
                doc_ficha_captacion='doc_ficha_captacion' in request.form,
                observaciones=request.form.get('observaciones', ''),
                gestor_responsable=request.form.get('gestor_responsable', ''),
                email_gestor=request.form.get('email_gestor', ''),
                url_referencia=request.form.get('url_referencia', ''),
                estado=request.form.get('estado', 'Solicitada'),
                motivo_no_solicitada=request.form.get('motivo_no_solicitada', '')
            )

            # Validación documentos si estado == Solicitada
            if solicitud.estado == 'Solicitada':
                if not (solicitud.doc_inicio_expediente and solicitud.doc_informe_tecnico and solicitud.doc_propuesta_jgl and solicitud.doc_ficha_captacion):
                    flash("❌ No puedes marcar como 'Solicitada' sin tener toda la documentación", 'danger')
                    return render_template('solicitudes/nueva.html', entidades=entidades)

            db.session.add(solicitud)
            db.session.flush()  # Para obtener el ID

            # Historial de creación
            historial = HistorialSolicitud(
                solicitud_id=solicitud.id,
                usuario=current_user.username,
                descripcion="Creación de solicitud"
            )
            db.session.add(historial)
            db.session.commit()
            flash("✅ Solicitud creada con éxito", "success")
            return redirect(url_for('solicitud_bp.listar_solicitudes'))

        except Exception as e:
            db.session.rollback()
            flash(f"❌ Error: {e}", "danger")

    return render_template('solicitudes/nueva.html', entidades=entidades)

# Editar solicitud
@solicitud_bp.route('/solicitudes/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@rol_requerido('admin', 'gestor')
def editar_solicitud(id):
    solicitud = SolicitudSubvencion.query.get_or_404(id)
    entidades = Entidad.query.order_by(Entidad.nombre).all()

    if solicitud.estado in ['Concedida', 'Denegada', 'No solicitada']:
        flash("❌ Esta solicitud está bloqueada y no puede modificarse", "warning")
        return redirect(url_for('solicitud_bp.listar_solicitudes'))

    if request.method == 'POST':
        try:
            campos_cambiados = []
            for campo in ['expediente_opensea', 'expediente_subvencion', 'entidad_id', 'concepto', 'tipo_fondo', 'fecha_presentacion_solicitud', 'importe_total', 'importe_subvencionado', 'fondos_propios', 'gestor_responsable', 'email_gestor', 'url_referencia', 'observaciones']:
                valor_nuevo = request.form.get(campo)
                if campo == 'fecha_presentacion_solicitud' and valor_nuevo:
                    valor_nuevo = datetime.strptime(valor_nuevo, "%Y-%m-%d")
                if str(getattr(solicitud, campo)) != str(valor_nuevo):
                    campos_cambiados.append(f"{campo}: {getattr(solicitud, campo)} -> {valor_nuevo}")
                    setattr(solicitud, campo, valor_nuevo)

            for doc in ['doc_inicio_expediente', 'doc_informe_tecnico', 'doc_propuesta_jgl', 'doc_ficha_captacion']:
                nuevo = doc in request.form
                if getattr(solicitud, doc) != nuevo:
                    campos_cambiados.append(f"{doc}: {getattr(solicitud, doc)} -> {nuevo}")
                    setattr(solicitud, doc, nuevo)

            nuevo_estado = request.form.get('estado')

            # Validación de documentos si cambia a 'Solicitada'
            if nuevo_estado == 'Solicitada':
                if not (solicitud.doc_inicio_expediente and solicitud.doc_informe_tecnico and solicitud.doc_propuesta_jgl and solicitud.doc_ficha_captacion):
                    flash("❌ No se puede cambiar a 'Solicitada' sin toda la documentación", 'danger')
                    return render_template('solicitudes/editar.html', solicitud=solicitud, entidades=entidades)

            if solicitud.estado != nuevo_estado:
                campos_cambiados.append(f"estado: {solicitud.estado} -> {nuevo_estado}")
                solicitud.estado = nuevo_estado

                # Crear subvención si es concedida
                if nuevo_estado == 'Concedida':
                    from ..models.subvencion import Subvencion
                    subvencion = Subvencion(
                        expediente_opensea=solicitud.expediente_opensea,
                        expediente_subvencion=solicitud.expediente_subvencion,
                        entidad=solicitud.entidad.nombre if solicitud.entidad else '',
                        concepto=solicitud.concepto,
                        tipo_fondo=solicitud.tipo_fondo,
                        fecha_solicitud=solicitud.fecha_presentacion_solicitud,
                        estado='Concedida',
                        fondos_propios=solicitud.fondos_propios,
                        importe_solicitado=solicitud.importe_total,
                        importe_concedido=solicitud.importe_subvencionado,
                        observaciones=solicitud.observaciones
                    )
                    db.session.add(subvencion)

            elif nuevo_estado == 'Denegada':
                from ..models.subvencion_denegada import SubvencionDenegada
                db.session.add(SubvencionDenegada(
                    expediente=solicitud.expediente_opensea,
                    concepto=solicitud.concepto,
                    resolucion="Pendiente",  # Esto se puede mejorar luego
                    motivo=solicitud.observaciones
                ))

            elif nuevo_estado == 'No solicitada':
                if not solicitud.motivo_no_solicitada:
                    flash("❌ Debes indicar un motivo para marcar como 'No solicitada'", 'danger')
                    return render_template('solicitudes/editar.html', solicitud=solicitud, entidades=entidades)

            if campos_cambiados:
                descripcion = " | ".join(campos_cambiados)
                historial = HistorialSolicitud(
                    solicitud_id=solicitud.id,
                    usuario=current_user.username,
                    descripcion=descripcion
                )
                db.session.add(historial)

            db.session.commit()
            flash("✅ Solicitud actualizada con éxito", "success")
            return redirect(url_for('solicitud_bp.listar_solicitudes'))

        except Exception as e:
            db.session.rollback()
            flash(f"❌ Error: {e}", 'danger')

    return render_template('solicitudes/editar.html', solicitud=solicitud, entidades=entidades)

# Eliminar solicitud (opcional, solo si lo deseas realmente)
@solicitud_bp.route('/solicitudes/eliminar/<int:id>', methods=['POST'])
@login_required
@rol_requerido('admin')
def eliminar_solicitud(id):
    solicitud = SolicitudSubvencion.query.get_or_404(id)
    try:
        db.session.delete(solicitud)
        db.session.commit()
        flash("🗑️ Solicitud eliminada", "info")
    except Exception as e:
        db.session.rollback()
        flash(f"❌ Error al eliminar: {e}", "danger")
    return redirect(url_for('solicitud_bp.listar_solicitudes'))