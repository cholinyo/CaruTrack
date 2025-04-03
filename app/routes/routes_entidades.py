from flask import Blueprint

entidades_bp = Blueprint('entidades_bp', __name__)

@entidades_bp.route('/entidades')
def listar_entidades():
    return "Lista de entidades"