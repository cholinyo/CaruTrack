from flask import Blueprint, render_template, request, redirect, url_for
from .models import db, Subvencion
from datetime import datetime

main = Blueprint('main', __name__)

# Ruta principal: listado de subvenciones
@main.route('/')
def index():
    subvenciones = Subvencion.query.all()
    return render_template('index.html', subvenciones=subvenciones)

@main.route('/nueva', methods=['GET', 'POST'])
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

# Editar subvención existente
@main.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_subvencion(id):
    subv = Subvencion.query.get_or_404(id)
    if request.method == 'POST':
        subv.num_expediente = request.form['num_expediente']
        subv.entidad = request.form['entidad']
        subv.concepto = request.form['concepto']
        subv.fecha_solicitud = request.form['fecha_solicitud']
        subv.estado = request.form['estado']
        subv.fondos_propios = 'fondos_propios' in request.form
        subv.importe_solicitado = request.form['importe_solicitado'] or 0
        subv.importe_concedido = request.form['importe_concedido'] or 0
        subv.importe_pagado = request.form['importe_pagado'] or 0

        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('editar.html', subv=subv)

# Eliminar subvención
@main.route('/eliminar/<int:id>', methods=['GET', 'POST'])
def eliminar_subvencion(id):
    subv = Subvencion.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(subv)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('eliminar.html', subv=subv)
