from .entidad import Entidad
from .usuario import Usuario
from .subvencion import Subvencion
from .solicitud import SolicitudSubvencion
from .historial import HistorialSolicitud
from .subvencion_denegada import SubvencionDenegada

# Aquí también puedes importar 'db' si lo defines en un módulo separado, como en app/extensions.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()