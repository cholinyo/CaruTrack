# Reestructuración del proyecto CaruTrack
Write-Host "Reorganizando estructura del proyecto CaruTrack..."

# Crear carpetas
New-Item -ItemType Directory -Force -Path ".\gestion_subvenciones\app\templates" | Out-Null
New-Item -ItemType Directory -Force -Path ".\gestion_subvenciones\app\static" | Out-Null
New-Item -ItemType Directory -Force -Path ".\gestion_subvenciones\migrations" | Out-Null
New-Item -ItemType Directory -Force -Path ".\gestion_subvenciones\tests" | Out-Null

# Mover archivos si existen
$filesToMove = @("app.py", "models.py", "routes.py", "forms.py")
foreach ($file in $filesToMove) {
    $source = ".\gestion_subvenciones\$file"
    $destination = ".\gestion_subvenciones\app\$file"
    if (Test-Path $source) {
        Move-Item $source $destination -Force
        Write-Host "Movido $file a app/"
    }
}

# Crear __init__.py si no existe
$initFile = ".\gestion_subvenciones\app\__init__.py"
if (!(Test-Path $initFile)) {
    Set-Content -Path $initFile -Value "# Inicializador del paquete Flask"
    Write-Host "Creado __init__.py"
}

# Crear run.py como punto de entrada
$runFile = ".\gestion_subvenciones\run.py"
if (!(Test-Path $runFile)) {
    $runContent = @"
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
"@
    Set-Content -Path $runFile -Value $runContent -Encoding UTF8
    Write-Host "Creado run.py"
}

Write-Host ""
Write-Host "Estructura reorganizada con éxito."

