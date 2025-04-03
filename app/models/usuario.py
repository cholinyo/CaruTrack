from app.models.db import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    contraseña_hash = db.Column(db.String(128), nullable=False)
    rol = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Usuario {self.nombre}>'

    # Propiedad para establecer la contraseña encriptada
    @property
    def contraseña(self):
        raise AttributeError('La contraseña no se puede leer directamente.')

    @contraseña.setter
    def contraseña(self, contraseña):
        self.contraseña_hash = generate_password_hash(contraseña)

    # Método para verificar la contraseña
    def verificar_contraseña(self, contraseña):
        return check_password_hash(self.contraseña_hash, contraseña)

# filepath: app/models/__init__.py
from .db import db
from .usuario import Usuario  # Importar el modelo Usuario