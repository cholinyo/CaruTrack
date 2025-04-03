from flask import Blueprint

redes_bp = Blueprint('redes_bp', __name__)

@redes_bp.route('/redes')
def listar_redes():
    return "Lista de redes"