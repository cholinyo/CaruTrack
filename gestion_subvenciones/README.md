# CaruTrack

Aplicación web para la gestión y seguimiento de subvenciones solicitadas por el Ayuntamiento de Onda.

## 🚀 Tecnologías utilizadas

- Python 3
- Flask
- SQLAlchemy
- Flask-Migrate
- Flask-Login
- Flask-Bcrypt
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

5. Crea el primer usuario:

```bash
python crear_usuario.py
```

6. Ejecuta la aplicación:

```bash
flask run
```

Abre en el navegador: [http://localhost:5000](http://localhost:5000)

---

## 📁 Estructura del proyecto

```
app/
├── __init__.py
├── models.py
├── routes.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── nueva.html
│   ├── editar.html
│   ├── eliminar.html
│   ├── solicitudes.html
│   ├── nueva_solicitud.html
│   ├── editar_solicitud.html
│   ├── historial_solicitud.html
│   └── denegadas.html
├── static/
config.py
run.py
crear_usuario.py
```

---

## 🔐 Sistema de usuarios y roles

- Login y logout con Flask-Login.
- Gestión de contraseñas con Flask-Bcrypt.
- Usuarios con rol `gestor` pueden crear, editar o eliminar registros.
- Las solicitudes se bloquean automáticamente si su estado pasa a "Concedida" o "Denegada".

---

## 🔧 Funcionalidades

### 🟢 Subvenciones

- Listado de subvenciones concedidas.
- Registro de nuevas subvenciones.
- Edición y eliminación de subvenciones (solo por gestores).
- Filtro por entidad, año o estado.

### 🟡 Solicitudes de subvención

- Registro y edición de solicitudes.
- Estados: "No solicitada", "En preparación", "Presentada", "Resolución parcial", "Concedida", "Denegada".
- Al cambiar el estado a:
  - **Concedida** → se crea automáticamente una subvención y se bloquea la solicitud.
  - **Denegada** → se crea una entrada en el módulo de subvenciones denegadas.

### 🔴 Subvenciones denegadas

- Listado de subvenciones denegadas con motivo y resolución.

### 📜 Historial de cambios

- Registro automático de los cambios realizados sobre cada solicitud.
- Visualización del historial desde la propia solicitud.

---

## 📝 Licencia

MIT