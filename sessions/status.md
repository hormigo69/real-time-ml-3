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

