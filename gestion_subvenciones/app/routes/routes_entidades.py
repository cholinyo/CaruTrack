from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from ..models.entidad import Entidad
from ..models import db



entidades_bp = Blueprint('entidades_bp', __name__)

# --- Listado de entidades ---
@entidades_bp.route('/entidades')
@login_required
def listar_entidades():
    entidades = Entidad.query.order_by(Entidad.nombre).all()
    return render_template('entidades/listar.html', entidades=entidades)

# --- Crear nueva entidad ---
@entidades_bp.route('/entidades/nueva', methods=['GET', 'POST'])
@login_required
def crear_entidad():
    if current_user.rol != 'admin':
        abort(403)

    if request.method == 'POST':
        try:
            nombre = request.form.get('nombre', '')
            ambito = request.form.get('ambito', '')

            entidad = Entidad(
                nombre=nombre,
                ambito=ambito,
                contacto1_telefono=request.form.get('contacto1_telefono', ''),
                contacto1_email=request.form.get('contacto1_email', ''),
                contacto1_cargo=request.form.get('contacto1_cargo', ''),
                contacto2_telefono=request.form.get('contacto2_telefono', ''),
                contacto2_email=request.form.get('contacto2_email', ''),
                contacto2_cargo=request.form.get('contacto2_cargo', ''),
                contacto3_telefono=request.form.get('contacto3_telefono', ''),
                contacto3_email=request.form.get('contacto3_email', ''),
                contacto3_cargo=request.form.get('contacto3_cargo', '')
            )

            db.session.add(entidad)
            db.session.commit()
            flash("✅ Entidad creada correctamente", "success")
            return redirect(url_for('entidades_bp.listar_entidades'))

        except Exception as e:
            db.session.rollback()
            flash(f"❌ Error al crear la entidad: {str(e)}", "danger")

    return render_template('entidades/nueva.html')

# --- Editar entidad ---
@entidades_bp.route('/entidades/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_entidad(id):
    entidad = Entidad.query.get_or_404(id)

    if current_user.rol != 'admin':
        abort(403)

    if request.method == 'POST':
        try:
            entidad.nombre = request.form.get('nombre', entidad.nombre)
            entidad.ambito = request.form.get('ambito', entidad.ambito)
            entidad.contacto1_telefono = request.form.get('contacto1_telefono', '')
            entidad.contacto1_email = request.form.get('contacto1_email', '')
            entidad.contacto1_cargo = request.form.get('contacto1_cargo', '')
            entidad.contacto2_telefono = request.form.get('contacto2_telefono', '')
            entidad.contacto2_email = request.form.get('contacto2_email', '')
            entidad.contacto2_cargo = request.form.get('contacto2_cargo', '')
            entidad.contacto3_telefono = request.form.get('contacto3_telefono', '')
            entidad.contacto3_email = request.form.get('contacto3_email', '')
            entidad.contacto3_cargo = request.form.get('contacto3_cargo', '')

            db.session.commit()
            flash("✅ Entidad actualizada", "success")
            return redirect(url_for('entidades_bp.listar_entidades'))

        except Exception as e:
            db.session.rollback()
            flash(f"❌ Error al actualizar: {str(e)}", "danger")

    return render_template('entidades/editar.html', entidad=entidad)

# --- Eliminar entidad ---
@entidades_bp.route('/entidades/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_entidad(id):
    if current_user.rol != 'admin':
        abort(403)
    entidad = Entidad.query.get_or_404(id)
    try:
        db.session.delete(entidad)
        db.session.commit()
        flash("🗑️ Entidad eliminada", "info")
    except Exception as e:
        db.session.rollback()
        flash(f"❌ Error al eliminar entidad: {str(e)}", "danger")
    return redirect(url_for('entidades_bp.listar_entidades'))