from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash

from app.models.usuario import Usuario
from app.extensions import db

usuarios_bp = Blueprint('usuarios_bp', __name__)

def rol_requerido(*roles):
    """Decorador para restringir acceso a usuarios con roles específicos."""
    def decorator(f):
        from functools import wraps
        @wraps(f)
        def wrapped(*args, **kwargs):
            if current_user.rol not in roles:
                abort(403)
            return f(*args, **kwargs)
        return wrapped
    return decorator

@usuarios_bp.route('/usuarios')
@login_required
@rol_requerido('admin', 'gestor', 'consulta')
def listar_usuarios():
    usuarios = Usuario.query.all()
    return render_template('usuarios/listar.html', usuarios=usuarios)

@usuarios_bp.route('/usuarios/nuevo', methods=['GET', 'POST'])
@login_required
@rol_requerido('admin', 'gestor')
def crear_usuario():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            rol = request.form['rol']
            email = request.form['email']

            nuevo_usuario = Usuario(
                username=username,
                password_hash=generate_password_hash(password),
                rol=rol,
                email=email
            )
            db.session.add(nuevo_usuario)
            db.session.commit()
            flash("✅ Usuario creado exitosamente", "success")
            return redirect(url_for('usuarios_bp.listar_usuarios'))
        except Exception as e:
            db.session.rollback()
            flash(f"❌ Error al crear usuario: {e}", "danger")

    return render_template('usuarios/nuevo.html')

@usuarios_bp.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@rol_requerido('admin', 'gestor')
def editar_usuario(id):
    usuario = Usuario.query.get_or_404(id)

    if request.method == 'POST':
        try:
            usuario.username = request.form['username']
            usuario.rol = request.form['rol']
            usuario.email = request.form['email']
            if request.form.get('password'):
                usuario.password_hash = generate_password_hash(request.form['password'])
            db.session.commit()
            flash("✅ Usuario actualizado", "success")
            return redirect(url_for('usuarios_bp.listar_usuarios'))
        except Exception as e:
            db.session.rollback()
            flash(f"❌ Error al actualizar usuario: {e}", "danger")

    return render_template('usuarios/editar.html', usuario=usuario)

@usuarios_bp.route('/usuarios/eliminar/<int:id>', methods=['POST'])
@login_required
@rol_requerido('admin')
def eliminar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    try:
        db.session.delete(usuario)
        db.session.commit()
        flash("🗑️ Usuario eliminado", "info")
    except Exception as e:
        db.session.rollback()
        flash(f"❌ Error al eliminar usuario: {e}", "danger")
    return redirect(url_for('usuarios_bp.listar_usuarios'))
