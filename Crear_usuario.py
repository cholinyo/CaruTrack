# filepath: c:\Users\vcaruncho\Downloads\CaruTrack\Crear_usuario.py
from app import create_app, db
from app.models.usuario import Usuario

app = create_app()

with app.app_context():
    # Crea un usuario
    nuevo_usuario = Usuario(
        nombre="admin",
        contraseña="admin",  # Esto se encriptará automáticamente
        rol="admin"
    )
    db.session.add(nuevo_usuario)
    db.session.commit()

    print("Usuario creado con éxito.")