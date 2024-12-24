## para recuperar los venv:

ir al directorio

#crear el entorno virtual
uv venv
#activar el venv
source .venv/bin/activate
#sincronizar con uv
uv sync


probar los servicios en local
probar dockerizados

#desactivar el venv
deactivate


### Estado 23/12 10:09
He corrido en local los 3 primeros servicios. to-feature-store me da problemas está intentando acceder a un atributo llamado materialization_job_schedule en un objeto de tipo FeatureGroup, pero este atributo no existe

### Estado 23/12 13:30
Corriendo en local todos los servicios.



# Notas

## Configuración del Entorno de Desarrollo

### Pre-commit y Ruff

Este proyecto utiliza pre-commit hooks para asegurar la calidad del código antes de cada commit. Los principales componentes son:
- **Ruff**: Linter y formateador de Python
- **pre-commit**: Gestor de hooks de git

### Instalación

1. Instalar las herramientas necesarias:
   ```bash
   uv pip install pre-commit ruff
   ```

2. Configurar pre-commit en el repositorio:
   ```bash
   pre-commit install
   ```

3. Verificar la instalación:
   ```bash
   pre-commit run --all-files
   ```

### Archivo de Configuración

El proyecto incluye la siguiente configuración en `.pre-commit-config.yaml`:

repos:
-   repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.2
    hooks:
    -   id: ruff

### Uso

- Los checks se ejecutarán automáticamente en cada commit
- Para ejecutar manualmente:
  ```bash
  pre-commit run --all-files  # todos los archivos
  pre-commit run             # solo archivos modificados
  ```

### Solución de Problemas

Si los hooks no se ejecutan:
1. Verificar que pre-commit está instalado: `pre-commit --version`
2. Reinstalar los hooks: `pre-commit install`
3. Limpiar la caché: `pre-commit clean`


### uv para crear el directorio de virtualenv
uv init nombre_del_entorno

# para añadir librerías
uv add nombre_de_la_librería
uv add quixstreams pydantic-settings requests loguru


### Añador el venv al interpreter path en cursor
cmd+shift+p
Python: Select Interpreter
Enter interpreter path:
   Ahí metemos el path de .venv/bin/python
