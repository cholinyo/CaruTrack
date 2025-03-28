from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from .models import db, Subvencion, Usuario, SolicitudSubvencion, SubvencionDenegada, HistorialSolicitud
from datetime import datetime
from functools import wraps

main = Blueprint('main', __name__)
bcrypt = Bcrypt()

# Decorador para roles
def rol_requerido(*roles):
    def decorador(f):
        @wraps(f)
        def decorado(*args, **kwargs):
            if current_user.rol not in roles:
                abort(403)
            return f(*args, **kwargs)
        return decorado
    return decorador

# LOGIN
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
        error = "Usuario o contraseña incorrectos"
    return render_template('login.html', error=error)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

# SUBVENCIONES
@main.route('/')
@login_required
def index():
    query = Subvencion.query
    entidad = request.args.get('entidad', '').strip()
    estado = request.args.get('estado', '').strip()
    año = request.args.get('año', '').strip()

    if entidad:
        query = query.filter(Subvencion.entidad.ilike(f"%{entidad}%"))
    if estado:
        query = query.filter(Subvencion.estado == estado)
    if año.isdigit():
        query = query.filter(db.extract('year', Subvencion.fecha_solicitud) == int(año))

    subvenciones = query.all()
    estados_distintos = db.session.query(Subvencion.estado).distinct().order_by(Subvencion.estado).all()
    estados = [e.estado for e in estados_distintos if e.estado]

    return render_template('index.html', subvenciones=subvenciones, entidad=entidad, estado=estado, año=año, estados=estados)

@main.route('/nueva', methods=['GET', 'POST'])
@login_required
@rol_requerido('gestor')
def nueva_subvencion():
    if request.method == 'POST':
        try:
            nueva = Subvencion(
                expediente_opensea=request.form.get('expediente_opensea', ''),
                expediente_subvencion=request.form.get('expediente_subvencion', ''),
                entidad=request.form.get('entidad', ''),
                concepto=request.form.get('concepto', ''),
                tipo_fondo=request.form.get('tipo_fondo', ''),
                fecha_solicitud=datetime.strptime(request.form.get('fecha_solicitud', ''), "%Y-%m-%d").date() if request.form.get('fecha_solicitud') else None,
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

@main.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@rol_requerido('gestor')
def editar_subvencion(id):
    subv = Subvencion.query.get_or_404(id)
    if request.method == 'POST':
        subv.expediente_opensea = request.form.get('expediente_opensea', '')
        subv.expediente_subvencion = request.form.get('expediente_subvencion', '')
        subv.entidad = request.form.get('entidad', '')
        subv.concepto = request.form.get('concepto', '')
        subv.tipo_fondo = request.form.get('tipo_fondo', '')
        subv.fecha_solicitud = datetime.strptime(request.form.get('fecha_solicitud', ''), "%Y-%m-%d").date() if request.form.get('fecha_solicitud') else None
        subv.estado = request.form.get('estado', '')
        subv.fondos_propios = request.form.get('fondos_propios', '')
        subv.importe_solicitado = float(request.form.get('importe_solicitado') or 0)
        subv.importe_concedido = float(request.form.get('importe_concedido') or 0)
        subv.importe_pagado = float(request.form.get('importe_pagado') or 0)
        subv.observaciones = request.form.get('observaciones', '')
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('editar.html', subv=subv)

@main.route('/eliminar/<int:id>', methods=['GET', 'POST'])
@login_required
@rol_requerido('gestor')
def eliminar_subvencion(id):
    subv = Subvencion.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(subv)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('eliminar.html', subv=subv)

# SOLICITUDES
@main.route('/solicitudes')
@login_required
def listar_solicitudes():
    solicitudes = SolicitudSubvencion.query.order_by(SolicitudSubvencion.fecha_solicitud.desc().nullslast()).all()
    return render_template('solicitudes.html', solicitudes=solicitudes)

@main.route('/solicitudes/nueva', methods=['GET', 'POST'])
@login_required
@rol_requerido('gestor')
def nueva_solicitud():
    if request.method == 'POST':
        nueva = SolicitudSubvencion(
            entidad=request.form['entidad'],
            concepto=request.form['concepto'],
            tipo_fondo=request.form['tipo_fondo'],
            fecha_solicitud=datetime.strptime(request.form['fecha_solicitud'], '%Y-%m-%d') if request.form['fecha_solicitud'] else None,
            estado=request.form['estado'],
            observaciones=request.form['observaciones'],
            importe_estimado=float(request.form['importe_estimado']) if request.form['importe_estimado'] else None,
            documentacion_adjunta='documentacion_adjunta' in request.form
        )
        db.session.add(nueva)
        db.session.commit()
        return redirect(url_for('main.listar_solicitudes'))

    estados = ['No solicitada', 'En preparación', 'Presentada', 'Resolución parcial', 'Concedida', 'Denegada']
    return render_template('nueva_solicitud.html', estados=estados)

@main.route('/solicitudes/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@rol_requerido('gestor')
def editar_solicitud(id):
    solicitud = SolicitudSubvencion.query.get_or_404(id)
    if solicitud.bloqueada:
        return render_template('editar_solicitud.html', solicitud=solicitud, estados=[], bloqueada=True)

    estados = ['No solicitada', 'En preparación', 'Presentada', 'Resolución parcial', 'Concedida', 'Denegada']
    campos_originales = solicitud.__dict__.copy()

    if request.method == 'POST':
        solicitud.entidad = request.form.get('entidad')
        solicitud.concepto = request.form.get('concepto')
        solicitud.tipo_fondo = request.form.get('tipo_fondo')
        fecha_str = request.form.get('fecha_solicitud')
        solicitud.fecha_solicitud = datetime.strptime(fecha_str, '%Y-%m-%d') if fecha_str else None
        nuevo_estado = request.form.get('estado', solicitud.estado)
        solicitud.estado = nuevo_estado
        solicitud.observaciones = request.form.get('observaciones')
        solicitud.importe_estimado = float(request.form.get('importe_estimado') or 0)
        solicitud.documentacion_adjunta = 'documentacion_adjunta' in request.form

        cambios = []
        for campo in ['entidad', 'concepto', 'tipo_fondo', 'fecha_solicitud', 'estado', 'observaciones', 'importe_estimado', 'documentacion_adjunta']:
            valor_antiguo = campos_originales.get(campo)
            valor_nuevo = getattr(solicitud, campo)
            if valor_antiguo != valor_nuevo:
                cambios.append(f"{campo} cambió de '{valor_antiguo}' a '{valor_nuevo}'")

        # Transiciones
        if nuevo_estado == 'Concedida' and solicitud.estado != 'Concedida':
            nueva = Subvencion(
                entidad=solicitud.entidad,
                concepto=solicitud.concepto,
                tipo_fondo=solicitud.tipo_fondo,
                fecha_solicitud=solicitud.fecha_solicitud,
                estado='Concedida',
                observaciones=solicitud.observaciones,
                importe_solicitado=solicitud.importe_estimado,
                importe_concedido=solicitud.importe_estimado,
                fondos_propios='Sí',
                expediente_opensea='',
                expediente_subvencion='',
                importe_pagado=0
            )
            db.session.add(nueva)
            solicitud.bloqueada = True
            cambios.append("La solicitud pasó a Concedida y se creó una Subvención.")
            flash("✅ Solicitud concedida y bloqueada. Subvención creada.")

        elif nuevo_estado == 'Denegada' and solicitud.estado != 'Denegada':
            denegada = SubvencionDenegada(
                entidad=solicitud.entidad,
                concepto=solicitud.concepto,
                tipo_fondo=solicitud.tipo_fondo,
                fecha_solicitud=solicitud.fecha_solicitud,
                estado='Denegada',
                observaciones=solicitud.observaciones,
                importe_estimado=solicitud.importe_estimado,
                documentacion_adjunta=solicitud.documentacion_adjunta,
                motivo_denegacion=request.form.get('motivo_denegacion'),
                resolucion=request.form.get('resolucion')
            )
            db.session.add(denegada)
            solicitud.bloqueada = True
            cambios.append("La solicitud fue denegada. Entrada creada en subvenciones denegadas.")
            flash("⚠️ Solicitud denegada y bloqueada. Entrada registrada.")

        if cambios:
            descripcion = "; ".join(cambios)
            log = HistorialSolicitud(
                solicitud_id=solicitud.id,
                usuario=current_user.username,
                descripcion=descripcion
            )
            db.session.add(log)

        db.session.commit()
        return redirect(url_for('main.listar_solicitudes'))

    return render_template('editar_solicitud.html', solicitud=solicitud, estados=estados, bloqueada=False)

@main.route('/denegadas')
@login_required
def listar_denegadas():
    denegadas = SubvencionDenegada.query.order_by(SubvencionDenegada.fecha_solicitud.desc().nullslast()).all()
    return render_template('denegadas.html', denegadas=denegadas)

@main.route('/solicitudes/<int:id>/historial')
@login_required
def ver_historial(id):
    solicitud = SolicitudSubvencion.query.get_or_404(id)
    historial = HistorialSolicitud.query.filter_by(solicitud_id=id).order_by(HistorialSolicitud.fecha.desc()).all()
    return render_template('historial_solicitud.html', solicitud=solicitud, historial=historial)

@main.route('/solicitudes/eliminar/<int:id>', methods=['GET', 'POST'])
@login_required
@rol_requerido('gestor')
def eliminar_solicitud(id):
    solicitud = SolicitudSubvencion.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(solicitud)
        db.session.commit()
        flash('✅ Solicitud eliminada correctamente.')
        return redirect(url_for('main.listar_solicitudes'))
    return render_template('eliminar_solicitud.html', solicitud=solicitud)
