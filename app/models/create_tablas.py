# filepath: c:\Users\vcaruncho\Downloads\CaruTrack\create_tables.py
from app import create_app, db

app = create_app()

with app.app_context():
    db.create_all()  # Esto crea todas las tablas definidas en los modelos
    print("Tablas creadas correctamente.")