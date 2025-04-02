# routes/usuarios.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from ..models.usuario import Usuario
from ..models import db

# Definir el Blueprint para usuarios
usuarios_bp = Blueprint('usuarios_bp', __name__)

# --- Listado de usuarios ---
@usuarios_bp.route('/usuarios')
@login_required
def listar_usuarios():
    usuarios = Usuario.query.order_by(Usuario.nombre).all()
    return render_template('usuarios/listar.html', usuarios=usuarios)

# --- Crear nuevo usuario ---
@usuarios_bp.route('/usuarios/nuevo', methods=['GET', 'POST'])
@login_required
def crear_usuario():
    if current_user.rol != 'admin':
        abort(403)

    if request.method == 'POST':
        try:
            nombre = request.form.get('nombre', '')
            email = request.form.get('email', '')
            rol = request.form.get('rol', '')

            usuario = Usuario(
                nombre=nombre,
                email=email,
                rol=rol
            )

            db.session.add(usuario)
            db.session.commit()
            flash("✅ Usuario creado correctamente", "success")
            return redirect(url_for('usuarios_bp.listar_usuarios'))

        except Exception as e:
            db.session.rollback()
            flash(f"❌ Error al crear el usuario: {str(e)}", "danger")

    return render_template('usuarios/nuevo.html')

# --- Editar usuario ---
@usuarios_bp.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_usuario(id):
    usuario = Usuario.query.get_or_404(id)

    if current_user.rol != 'admin':
        abort(403)

    if request.method == 'POST':
        try:
            usuario.nombre = request.form.get('nombre', usuario.nombre)
            usuario.email = request.form.get('email', usuario.email)
            usuario.rol = request.form.get('rol', usuario.rol)

            db.session.commit()
            flash("✅ Usuario actualizado", "success")
            return redirect(url_for('usuarios_bp.listar_usuarios'))

        except Exception as e:
            db.session.rollback()
            flash(f"❌ Error al actualizar: {str(e)}", "danger")

    return render_template('usuarios/editar.html', usuario=usuario)

# --- Eliminar usuario ---
@usuarios_bp.route('/usuarios/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_usuario(id):
    if current_user.rol != 'admin':
        abort(403)
    usuario = Usuario.query.get_or_404(id)
    try:
        db.session.delete(usuario)
        db.session.commit()
        flash("🗑️ Usuario eliminado", "info")
    except Exception as e:
        db.session.rollback()
        flash(f"❌ Error al eliminar usuario: {str(e)}", "danger")
    return redirect(url_for('usuarios_bp.listar_usuarios'))
