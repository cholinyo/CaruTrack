Write-Host "Reorganizando CaruTrack..."

# Variables
$base = ".\gestion_subvenciones"
$appDir = "$base\app"

# Crear carpetas
New-Item -ItemType Directory -Force -Path "$appDir\templates" | Out-Null
New-Item -ItemType Directory -Force -Path "$appDir\static" | Out-Null

# Archivos a mover
$filesToMove = @("app.py", "models.py", "routes.py", "forms.py")
foreach ($file in $filesToMove) {
    $src = "$base\$file"
    $dst = "$appDir\$file"
    if (Test-Path $src) {
        Move-Item $src $dst -Force
        Write-Host "Movido $file a app/"
    }
}

# Crear __init__.py con contenido base Flask
$initContent = @"
from flask import Flask
from .models import db
from .routes import main  # Asegúrate de que defines un blueprint 'main' en routes.py

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')  # Asegúrate de tener un archivo config.py con la clase Config
    db.init_app(app)
    app.register_blueprint(main)
    return app
"@
Set-Content -Path "$appDir\__init__.py" -Value $initContent -Encoding UTF8
Write-Host "Creado __init__.py"

# Crear run.py en la raíz del proyecto
$runContent = @"
from gestion_subvenciones.app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
"@
Set-Content -Path ".\run.py" -Value $runContent -Encoding UTF8
Write-Host "Creado run.py"

# Eliminar archivos innecesarios
$toDelete = @("$base\app.py", ".\reestructurar.ps1", ".\reestructurar_limpio.ps1")
foreach ($item in $toDelete) {
    if (Test-Path $item) {
        Remove-Item $item -Force
        Write-Host "Eliminado $item"
    }
}

Write-Host "`nEstructura reorganizada con éxito."


