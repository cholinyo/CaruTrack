from app import create_app, db, bcrypt
from app.models import Usuario
from flask import Flask

app = create_app()

with app.app_context():
    username = input("Nombre de usuario: ")
    password = input("Contraseña: ")

    existing_user = Usuario.query.filter_by(username=username).first()
    if existing_user:
        print("❌ El usuario ya existe.")
    else:
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = Usuario(username=username, password_hash=password_hash)
        db.session.add(new_user)
        db.session.commit()
        print(f"✅ Usuario '{username}' creado correctamente.")
