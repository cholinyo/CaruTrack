from flask import Blueprint
from flask_login import login_required

usuarios_bp = Blueprint('usuarios_bp', __name__)

@usuarios_bp.route('/usuarios')
@login_required
def listar_usuarios():
    return "Lista de usuarios"