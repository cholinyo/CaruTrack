# routes/__init__.py
from flask import Blueprint

# Definir el Blueprint principal
main_bp = Blueprint('main', __name__)

# Importar las rutas asociadas al Blueprint
from . import main
