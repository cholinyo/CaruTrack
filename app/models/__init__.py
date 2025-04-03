from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Importar modelos después de inicializar db
from .usuario import Usuario
from .entidad import Entidad
from .solicitud import Solicitud
#from .subvencion import Subvencion
from .red import Red