from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from .models import db, Subvencion, Usuario
from datetime import datetime

main = Blueprint('main', __name__)
bcrypt = Bcrypt()

# RUTA: Listado de subvenciones (requiere login)
@main.route('/')
@login_required
def index():
    subvenciones = Subvencion.query.all()
    return render_template('index.html', subvenciones=subvenciones)

# RUTA: Crear nueva subvención (requiere login)
@main.route('/nueva', methods=['GET', 'POST'])
@login_required
def nueva_subvencion():
    if request.method == 'POST':
        try:
            nueva = Subvencion(
                expediente_opensea=request.form.get('expediente_opensea', ''),
                expediente_subvencion=request.form.get('expediente_subvencion', ''),
                entidad=request.form.get('entidad', ''),
                concepto=request.form.get('concepto', ''),
                tipo_fondo=request.form.get('tipo_fondo', ''),
                fecha_solicitud=datetime.strptime(request.form.get('fecha_solicitud', ''), "%Y-%m-%d").date()
                    if request.form.get('fecha_solicitud') else None,
                estado=request.form.get('estado', ''),
                fondos_propios=request.form.get('fondos_propios', ''),
                importe_solicitado=float(request.form.get('importe_solicitado') or 0),
                importe_concedido=float(request.form.get('importe_concedido') or 0),
                importe_pagado=float(request.form.get('importe_pagado') or 0),
                observaciones=request.form.get('observaciones', '')
            )
            db.session.add(nueva)
            db.session.commit()
            return redirect(url_for('main.index'))
        except Exception as e:
            return f"Error al guardar: {e}", 400

    return render_template('nueva.html')

# RUTA: Editar subvención (requiere login)
@main.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_subvencion(id):
    subv = Subvencion.query.get_or_404(id)
    if request.method == 'POST':
        subv.expediente_opensea = request.form.get('expediente_opensea', '')
        subv.expediente_subvencion = request.form.get('expediente_subvencion', '')
        subv.entidad = request.form.get('entidad', '')
        subv.concepto = request.form.get('concepto', '')
        subv.tipo_fondo = request.form.get('tipo_fondo', '')
        subv.fecha_solicitud = datetime.strptime(request.form.get('fecha_solicitud', ''), "%Y-%m-%d").date() \
            if request.form.get('fecha_solicitud') else None
        subv.estado = request.form.get('estado', '')
        subv.fondos_propios = request.form.get('fondos_propios', '')
        subv.importe_solicitado = float(request.form.get('importe_solicitado') or 0)
        subv.importe_concedido = float(request.form.get('importe_concedido') or 0)
        subv.importe_pagado = float(request.form.get('importe_pagado') or 0)
        subv.observaciones = request.form.get('observaciones', '')

        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('editar.html', subv=subv)

# RUTA: Eliminar subvención (requiere login)
@main.route('/eliminar/<int:id>', methods=['GET', 'POST'])
@login_required
def eliminar_subvencion(id):
    subv = Subvencion.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(subv)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('eliminar.html', subv=subv)

# RUTA: Login
@main.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        usuario = Usuario.query.filter_by(username=username).first()
        if usuario and bcrypt.check_password_hash(usuario.password_hash, password):
            login_user(usuario)
            return redirect(url_for('main.index'))
        else:
            error = "Usuario o contraseña incorrectos"
    return render_template('login.html', error=error)

# RUTA: Logout
@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))
