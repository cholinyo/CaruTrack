from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Importar modelos después de inicializar db
from .usuario import Usuario
from .entidad import Entidad
# Ensure the module exists or adjust the import path
try:
	from .solicitud_subvencion import Solicitud	
except ImportError:
	print("Module 'SolicitudSubvencion' not found. Please verify its existence and path.")
