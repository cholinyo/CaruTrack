from run import app
from app import db
from flask_migrate import Migrate

with app.app_context():
    print("✅ La app Flask se ha cargado correctamente.")
    
    # Verifica que se puede acceder al engine de SQLAlchemy
    try:
        conn = db.engine.connect()
        print("✅ Conexión a la base de datos OK:", db.engine.url)
        conn.close()
    except Exception as e:
        print("❌ Error de conexión a la base de datos:", e)

    # Verifica que Migrate está inicializado
    try:
        migrate = Migrate(app, db)
        print("✅ Flask-Migrate también está correctamente configurado.")
    except Exception as e:
        print("❌ Error al inicializar Flask-Migrate:", e)
