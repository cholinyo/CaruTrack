from flask import Blueprint

usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route('/usuarios', methods=['GET'])
def get_usuarios():
    return "List of usuarios"
