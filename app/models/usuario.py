# Importamos la base de datos compartida del proyecto
from app.models.db import db

# UserMixin proporciona funcionalidades necesarias para usar este modelo con Flask-Login
from flask_login import UserMixin

# Herramientas de Flask para generar y verificar contraseñas seguras
from werkzeug.security import generate_password_hash, check_password_hash


# Definimos la clase Usuario, que representa una tabla en la base de datos
# Hereda de db.Model para integrarse con SQLAlchemy y de UserMixin para Flask-Login
class Usuario(UserMixin, db.Model):
    # Nombre de la tabla en la base de datos
    __tablename__ = 'usuarios'

    # Columnas de la tabla:
    id = db.Column(db.Integer, primary_key=True)  # Identificador único
    username = db.Column(db.String(80), unique=True, nullable=False)  # Nombre de usuario
    password_hash = db.Column(db.String(128), nullable=False)  # Contraseña encriptada
    rol = db.Column(db.String(20), nullable=False, default='consulta')  # Rol del usuario
    email = db.Column(db.String(120), unique=True, nullable=True)  # Correo para recuperar contraseña

    # Método para establecer la contraseña encriptada
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Método para verificar si una contraseña es correcta
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Método requerido por Flask-Login para identificar el usuario
    def get_id(self):
        return str(self.id)

    # Representación en texto del objeto (útil para depurar)
    def __repr__(self):
        return f"<Usuario {self.username}>"
