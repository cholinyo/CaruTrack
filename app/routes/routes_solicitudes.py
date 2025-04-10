from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from flask_login import login_required, current_user
from app.models.SolicitudSubvencion import Solicitud
from app.models.db import db
import csv
import io

solicitudes_bp = Blueprint('solicitudes_bp', __name__)

# Aquí van las rutas de solicitudes

# Listar solicitudes con filtros y exportación a Excel
@solicitudes_bp.route('/solicitudes', methods=['GET', 'POST'])
@login_required
def listar_solicitudes():
    # Filtros de búsqueda
    query = Solicitud.query
    expediente_opensea = request.args.get('expediente_opensea')
    tipo_fondo = request.args.get('tipo_fondo')

    if expediente_opensea:
        query = query.filter(Solicitud.expediente_opensea.ilike(f"%{expediente_opensea}%"))
    if tipo_fondo:
        query = query.filter(Solicitud.tipo_fondo == tipo_fondo)

    solicitudes = query.all()

    # Exportar a Excel
    if request.args.get('export') == 'excel':
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['ID', 'Expediente OpenSea', 'Tipo Fondo', 'Fecha Solicitud', 'Importe Total'])
        for solicitud in solicitudes:
            writer.writerow([solicitud.id, solicitud.expediente_opensea, solicitud.tipo_fondo, solicitud.fecha_solicitud, solicitud.importe_total_proyecto])
        output.seek(0)
        return send_file(io.BytesIO(output.getvalue().encode('utf-8')), mimetype='text/csv', as_attachment=True, download_name='solicitudes.csv')

    return render_template('solicitudes/listar.html', solicitudes=solicitudes)

# Visualizar una solicitud
@solicitudes_bp.route('/solicitudes/<int:id>')
@login_required
def ver_solicitud(id):
    solicitud = Solicitud.query.get_or_404(id)
    return render_template('solicitudes/ver.html', solicitud=solicitud)

# Editar una solicitud (solo gestor y administrador)
@solicitudes_bp.route('/solicitudes/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_solicitud(id):
    if current_user.rol not in ['gestor', 'administrador']:
        flash('No tienes permiso para editar esta solicitud.', 'danger')
        return redirect(url_for('solicitudes_bp.listar_solicitudes'))

    solicitud = Solicitud.query.get_or_404(id)
    if request.method == 'POST':
        solicitud.expediente_opensea = request.form['expediente_opensea']
        solicitud.tipo_fondo = request.form['tipo_fondo']
        solicitud.fecha_solicitud = request.form['fecha_solicitud']
        solicitud.importe_total_proyecto = request.form['importe_total_proyecto']
        db.session.commit()
        flash('Solicitud actualizada correctamente.', 'success')
        return redirect(url_for('solicitudes_bp.listar_solicitudes'))

    return render_template('solicitudes/editar.html', solicitud=solicitud)

# Eliminar una solicitud (solo administrador)
@solicitudes_bp.route('/solicitudes/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_solicitud(id):
    if current_user.rol != 'administrador':
        flash('No tienes permiso para eliminar esta solicitud.', 'danger')
        return redirect(url_for('solicitudes_bp.listar_solicitudes'))

    solicitud = Solicitud.query.get_or_404(id)
    db.session.delete(solicitud)
    db.session.commit()
    flash('Solicitud eliminada correctamente.', 'success')
    return redirect(url_for('solicitudes_bp.listar_solicitudes'))