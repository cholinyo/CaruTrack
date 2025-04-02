from flask import Blueprint

entidades_bp = Blueprint('entidades', __name__)

@entidades_bp.route('/entidades', methods=['GET'])
def get_entidades():
    return "List of entidades"
