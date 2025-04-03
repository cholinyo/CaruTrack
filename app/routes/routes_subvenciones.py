from flask import Blueprint

subvenciones_bp = Blueprint('subvenciones_bp', __name__)

@subvenciones_bp.route('/subvenciones')
def listar_subvenciones():
    return "Lista de subvenciones"