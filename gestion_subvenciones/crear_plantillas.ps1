# Crear el directorio si no existe
$templatesPath = "gestion_subvenciones\app\templates"
if (-Not (Test-Path $templatesPath)) {
    New-Item -Path $templatesPath -ItemType Directory -Force
}

# Crear historial_solicitud.html
$historialContent = @"
{% extends 'base.html' %}
{% block title %}Historial - Solicitud{% endblock %}
{% block content %}
<h2>Historial de cambios para la solicitud de {{ solicitud.entidad }}</h2>
<ul class="list-group mt-3">
    {% for item in historial %}
        <li class="list-group-item">
            <strong>{{ item.fecha.strftime('%d/%m/%Y %H:%M') }}</strong> - 
            {{ item.usuario }}: {{ item.descripcion }}
        </li>
    {% else %}
        <li class="list-group-item text-muted">No hay registros en el historial.</li>
    {% endfor %}
</ul>
<a href="{{ url_for('main.listar_solicitudes') }}" class="btn btn-secondary mt-3">Volver</a>
{% endblock %}
"@
$historialPath = Join-Path $templatesPath "historial_solicitud.html"
$historialContent | Out-File -FilePath $historialPath -Encoding utf8

# Crear eliminar_solicitud.html
$eliminarContent = @"
{% extends 'base.html' %}
{% block title %}Eliminar Solicitud{% endblock %}
{% block content %}
<h2>¿Estás seguro de que quieres eliminar esta solicitud?</h2>
<p><strong>Entidad:</strong> {{ solicitud.entidad }}</p>
<p><strong>Concepto:</strong> {{ solicitud.concepto }}</p>
<form method="POST">
    <button type="submit" class="btn btn-danger">Sí, eliminar</button>
    <a href="{{ url_for('main.listar_solicitudes') }}" class="btn btn-secondary">Cancelar</a>
</form>
{% endblock %}
"@
$eliminarPath = Join-Path $templatesPath "eliminar_solicitud.html"
$eliminarContent | Out-File -FilePath $eliminarPath -Encoding utf8

Write-Host "Archivos de plantilla creados correctamente en $templatesPath"
