from app.models.db import db

class Entidad(db.Model):
    __tablename__ = 'entidades'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    descripcion = db.Column(db.Text, nullable=True)
    ambito = db.Column(db.Enum('Mundial', 'Europeo', 'Nacional', 'Autonómico', 'Local', 'Otros', name='ambito_enum'), nullable=False)
    informacion = db.Column(db.Text, nullable=True)

    # Campos para los contactos
    contacto1_telefono = db.Column(db.String(20), nullable=True)
    contacto1_email = db.Column(db.String(120), nullable=True)
    contacto1_cargo = db.Column(db.String(100), nullable=True)

    contacto2_telefono = db.Column(db.String(20), nullable=True)
    contacto2_email = db.Column(db.String(120), nullable=True)
    contacto2_cargo = db.Column(db.String(100), nullable=True)

    contacto3_telefono = db.Column(db.String(20), nullable=True)
    contacto3_email = db.Column(db.String(120), nullable=True)
    contacto3_cargo = db.Column(db.String(100), nullable=True)

    contacto4_telefono = db.Column(db.String(20), nullable=True)
    contacto4_email = db.Column(db.String(120), nullable=True)
    contacto4_cargo = db.Column(db.String(100), nullable=True)

    contacto5_telefono = db.Column(db.String(20), nullable=True)
    contacto5_email = db.Column(db.String(120), nullable=True)
    contacto5_cargo = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f'<Entidad {self.nombre}>'