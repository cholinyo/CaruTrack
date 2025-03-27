# CaruTrack

Aplicación web para la gestión y seguimiento de subvenciones solicitadas por el Ayuntamiento de Onda.

## 🚀 Tecnologías utilizadas
- Python 3
- Flask
- SQLAlchemy
- Flask-Migrate
- SQLite (por defecto)

## 📦 Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/cholinyo/CaruTrack.git
cd CaruTrack/gestion_subvenciones
```

2. Crea un entorno virtual e instálalo:

```bash
python -m venv venv
.\venv\Scripts\activate   # En Windows
source venv/bin/activate  # En Linux/macOS

pip install -r requirements.txt
```

3. Configura el entorno:

Crea un archivo `.env` y añade:

```env
SECRET_KEY=clave-secreta
DATABASE_URL=sqlite:///subvenciones.db
```

4. Inicializa la base de datos:

```bash
flask db init
flask db migrate -m "Migración inicial"
flask db upgrade
```

5. Ejecuta la aplicación:

```bash
flask run
```

Abre en el navegador: [http://localhost:5000](http://localhost:5000)

## 📁 Estructura del proyecto

```
app/
├── __init__.py
├── models.py
├── routes.py
├── templates/
│   ├── index.html
│   ├── nueva.html
│   ├── editar.html
│   └── eliminar.html
├── static/
config.py
run.py
```

## 🔧 Funcionalidades
- Listado de subvenciones
- Registro de nueva subvención
- Edición de subvención existente
- Eliminación de subvención

## 📝 Licencia
MIT