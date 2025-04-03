from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from app.models.usuario import Usuario
from app.models.db import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nombre = request.form['nombre']
        contraseña = request.form['contraseña']
        usuario = Usuario.query.filter_by(nombre=nombre).first()

        if usuario and usuario.verificar_contraseña(contraseña):
            login_user(usuario)
            flash('Inicio de sesión exitoso.', 'success')
            return redirect(url_for('solicitudes_bp.listar_solicitudes'))
        else:
            flash('Nombre de usuario o contraseña incorrectos.', 'danger')

    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión.', 'success')
    return redirect(url_for('auth.login'))