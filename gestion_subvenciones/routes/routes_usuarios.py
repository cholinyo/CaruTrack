from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from .models import Usuario, db

usuarios_bp = Blueprint('usuarios_bp', __name__)
bcrypt = Bcrypt()

@usuarios_bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        usuario = Usuario.query.filter_by(username=request.form['username']).first()
        if usuario and bcrypt.check_password_hash(usuario.password_hash, request.form['password']):
            login_user(usuario)
            return redirect(url_for('solicitudes_bp.listar_solicitudes'))
        error = "Usuario o contraseña incorrectos"
    return render_template('usuarios/login.html', error=error)

@usuarios_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('usuarios_bp.login'))

@usuarios_bp.route('/usuarios')
@login_required
def listar_usuarios():
    if current_user.rol != 'admin':
        abort(403)
    usuarios = Usuario.query.all()
    return render_template('usuarios/listar.html', usuarios=usuarios)

@usuarios_bp.route('/usuarios/nuevo', methods=['GET', 'POST'])
@login_required
def crear_usuario():
    if current_user.rol != 'admin':
        abort(403)

    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            rol = request.form['rol']

            if Usuario.query.filter_by(username=username).first():
                flash("❌ El nombre de usuario ya existe", "danger")
                return redirect(url_for('usuarios_bp.crear_usuario'))

            password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
            nuevo_usuario = Usuario(username=username, password_hash=password_hash, rol=rol)
            db.session.add(nuevo_usuario)
            db.session.commit()
            flash("✅ Usuario creado correctamente", "success")
            return redirect(url_for('usuarios_bp.listar_usuarios'))

        except Exception as e:
            db.session.rollback()
            flash(f"❌ Error al crear el usuario: {str(e)}", "danger")

    return render_template('usuarios/nuevo.html')

@usuarios_bp.route('/usuarios/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_usuario(id):
    if current_user.rol != 'admin':
        abort(403)
    usuario = Usuario.query.get_or_404(id)
    try:
        db.session.delete(usuario)
        db.session.commit()
        flash("🗑️ Usuario eliminado correctamente", "info")
    except Exception as e:
        db.session.rollback()
        flash(f"❌ Error al eliminar usuario: {str(e)}", "danger")
    return redirect(url_for('usuarios_bp.listar_usuarios'))
