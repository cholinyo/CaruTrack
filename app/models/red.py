from app.models.db import db
from datetime import date

class Red(db.Model):
    __tablename__ = 'redes'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    descripcion = db.Column(db.Text, nullable=True)
    ambito = db.Column(db.Enum('Mundial', 'Europea', 'Nacional', 'Autonómica', 'Local', 'Otros', name='ambito_enum_red'), nullable=False)
    fecha_adhesion = db.Column(db.Date, nullable=False, default=date.today)
    contacto_email = db.Column(db.String(120), nullable=True)
    contacto_telefono = db.Column(db.String(20), nullable=True)
    observaciones = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Red {self.nombre}>'